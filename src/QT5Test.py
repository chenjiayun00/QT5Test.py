# from ui.PyQt5test import Ui_MainWindow  # 导入PyQt5test.py文件中的Ui_MainWindow类
from ui.MainForm import Ui_MainWindow   # 导入MainForm.py文件中的Ui_MainWindow类
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
import threading
import pdf2txt
import AodCreat

import time

lock = threading.Lock()
BASE_DIR = os.getcwd()


def get_txt(chType, fileName):
    """
    将对应的pdf文件转换成对应格式的txt文件
    :param path: pdf文件路径
    :param chType: 需要转换成的格式
    :return:
    """
    remesg = ""
    if chType == "W6":
        result_file, remesg = pdf2txt.read_pdf(fileName)
    elif chType == "6404":
        result_file, remesg = pdf2txt.w6_to_6404(fileName, chType)
    elif chType == "6601A-D-PHY":
        result_file, remesg = pdf2txt.w6_to_6601A_D(fileName, chType)
    # elif chType == "6601A-C-PHY":
    #     result_file, remesg = pdf2txt.w6_to_6601A_C(fileName, chType)

    return remesg, result_file


def creat_images(mkPath, w, h, mkType,*args):
    """
    :param mkPath: 图片保存路径
    :param w: 图片宽度
    :param h: 图片高度
    :param mkType: 类型
    :param args:
    :return:
    """
    remesg = ""
    if mkType == "GRAY":
        print("生成灰阶线程")
        result_file = AodCreat.CreatGray(mkPath, w, h)
    elif mkType == "AOD":
        print("生成AOD线程")
        result_file = AodCreat.creatAODGray(mkPath, w, h)
    elif mkType == "DEMURA":
        print("生成DEMURA线程")
        print(args)
        result_file = AodCreat.creat_demura_photos(mkPath, w, h, *args)


class Thread_run_imge(QThread):
    mySignal = pyqtSignal(str)
    # show_message_signal = pyqtSignal(str)

    def __init__(self, mkPath, w, h, mkType, demura_list):
        super(Thread_run_imge, self).__init__()
        self.mkPath = mkPath
        self.w = w
        self.h = h
        self.mkType = mkType
        self.demura_list = demura_list

    def run(self):
        self.mySignal.emit("开始生成 {} 图片=========".format(self.mkType))
        print("线程开始=====")
        creat_images(self.mkPath, self.w, self.h, self.mkType,self.demura_list)
        self.mySignal.emit("{} 图片生成完成=========".format(self.mkType))
        print("线程结束=====")


def read_txt(fileName):
    with open(fileName, "r", encoding="utf-8") as f:
        return f.read()


class Thread_run(QThread):
    mySignal = pyqtSignal(str)
    show_message_signal = pyqtSignal(str)
    set_text_edit_target_signal = pyqtSignal(str)

    def __init__(self, fileName, chType):
        super(Thread_run, self).__init__()
        self.fileName = fileName
        self.chType = chType

    def run(self):
        self.mySignal.emit("读取开始")
        remesg, result_file = get_txt(self.chType, self.fileName)
        self.mySignal.emit("读取结束")
        self.mySignal.emit(remesg)
        self.show_message_signal.emit(remesg)
        readdate = read_txt(result_file)
        self.set_text_edit_target_signal.emit(readdate)


class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    # 建立的是Main Window项目，故此处导入的是QMainWindow
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initTab_1_UI()
        self.fileName = self.lineEdit_path.text()

        self.chType = self.combox_type.currentText()

        self.initTab_3_UI()
    # def btn_click(self):    # 定义槽函数btn_click(),也可以理解为重载类Ui_MainWindow中的函数btn_click()
    #     fileName,fileType = QFileDialog.getOpenFileName(self, "选取文件", os.getcwd(), "pdf Files(*.pdf);; All Files(*)")
    #     self.textEdit.setText(fileName)

    # ============PDF转txt界面==============
    def initTab_1_UI(self):
        # 单个条目
        self.combox_type.addItem("W6")
        # 多个条目
        self.combox_type.addItems(["6404", "6601A-D-PHY"])

    def btn_search_path_click(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", os.path.join(os.path.dirname(os.getcwd()), "file"), "pdf Files(*.pdf);; All Files(*)")
        self.lineEdit_path.setText(fileName)

    def btn_comfor_click(self):  # 点击确定按钮
        fileName = self.lineEdit_path.text()
        chType = self.combox_type.currentText()
        if os.path.isfile(fileName) is False:
            QMessageBox.information(self, "提示", "请先选择文件")
            return False
        if chType is False:
            QMessageBox.information(self, "提示", "请先转换类型")
            return False
        self.btn_comfort.setEnabled(False)  # 设置按钮不可点击
        self.thread_run = Thread_run(fileName, chType)  # 实例化线程
        self.thread_run.mySignal.connect(self.update_text_edit)     # 信号连接槽函数
        self.thread_run.set_text_edit_target_signal.connect(self.update_text_edit_target)   # 信号连接槽函数
        self.thread_run.show_message_signal.connect(self.show_message_box)   # 信号连接槽函数

        self.thread_run.start()  # 开启线程

        # python内置的threading模块
        # thread_get_txt = threading.Thread(target=get_txt)
        # thread_get_txt.start()

    def update_text_edit(self, text):  # 槽函数，带有一个str参数,用来接收自定义信号传递的值
        self.textEdit.append(text)   # 往控件textEdit中追加一行

    def update_text_edit_target(self, text):  # 槽函数，带有一个str参数,用来接收自定义信号传递的值
        self.textEdit_Target.setText(text)   # 往控件textEdit中追加一行

    def show_message_box(self, message):
        self.btn_comfort.setEnabled(True)
        QMessageBox.information(self, "提示", message, QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
    # ============PDF转txt界面==============

    # ============图片生成界面==============
    def initTab_3_UI(self):
        # 设置图片默认宽和高
        self.lineEdit_Width.setText("100")
        self.lineEdit_Height.setText("200")
        self.lineEdit_Demura.setText("16,32,64,128,192,224")
        self.pushButton_CreatPic.clicked.connect(self.pushButton_CreatPic_clcik)
        # 设置需要生成的画面
        # self.checkBox_Gray.setCheckState(self, True)
        # self.checkBox_Aod.setCheckState(self, True)
        # self.checkBox_Demura.setCheckState(self, True)


    def update_text_edit_log(self, text):  # 槽函数，带有一个str参数,用来接收自定义信号传递的值
        self.textEdit_Log.append(text)   # 往控件textEdit_Log中追加一行

    def pushButton_CreatPic_clcik(self):
        AodCreat.img_w = int(self.lineEdit_Width.text())    # 图片宽度
        AodCreat.img_h = int(self.lineEdit_Height.text())    # 图片高度
        Demura_gray_list = self.lineEdit_Demura.text().split(",")   # 将字符串"16,32,64,128,192,224" 转换成列表 ['16', '32', '64', '128', '192', '224']
        Demura_gray_list = [int(i) for i in Demura_gray_list]  # 将列表['16', '32', '64', '128', '192', '224']转换成[16, 32, 64, 128, 192, 224]

        # 定义要创建的目录,路径不能有中文
        FILENAME_GRAY = "TEMS\\{}X{}_GRAY".format(str(AodCreat.img_w), str(AodCreat.img_h))
        FILENAME_AOD = "TEMS\\{}X{}_AOD".format(str(AodCreat.img_w), str(AodCreat.img_h))
        FILENAME_Demura = "TEMS\\{}X{}_DEMURA".format(str(AodCreat.img_w), str(AodCreat.img_h))

        # 将两个目录拼接 BASE_DIR + r"\" + FILENAME_GRAY
        mkPath_GRAY = os.path.join(BASE_DIR, FILENAME_GRAY)
        mkPath_AOD = os.path.join(BASE_DIR, FILENAME_AOD)
        mkPath_Demura = os.path.join(BASE_DIR, FILENAME_Demura)

        AodCreat.mkdir(mkPath_GRAY)
        AodCreat.mkdir(mkPath_AOD)
        AodCreat.mkdir(mkPath_Demura)

        print("生成的灰阶图路径为：", mkPath_GRAY)
        print("生成的AOD灰阶图路径为：", mkPath_AOD)
        print("生成的Demura灰阶图路径为：", mkPath_Demura)
        print("图片宽度为：{}; lineEdit_Width = {}".format(self.lineEdit_Width.text(), self.lineEdit_Height.text()))
        print("图片高度为：{}; ".format(self.lineEdit_Demura.text()))

        if self.checkBox_Gray.isChecked():
            mkType = "GRAY"
            self.textEdit_Log.setText("正在生成0-255灰阶图片...")
            print("正在生成0-255灰阶图片...{}x{}".format(AodCreat.img_w,AodCreat.img_h))

            self.thread_run_imge = Thread_run_imge(mkPath_GRAY, AodCreat.img_w,AodCreat.img_h,mkType,Demura_gray_list)  # 实例化线程

            self.thread_run_imge.mySignal.connect(self.update_text_edit_log)  # 信号连接槽函数
            # self.thread_run_imge.show_message_signal.connect(self.show_message_box)  # 信号连接槽函数

            self.thread_run_imge.start()  # 开启线程
        if self.checkBox_Aod.isChecked():
            mkType = "AOD"
            self.textEdit_Log.setText("正在生成AOD灰阶图片...")
            print("正在生成AOD灰阶图片...")
            self.thread_run_imge2 = Thread_run_imge(mkPath_AOD, AodCreat.img_w, AodCreat.img_h, mkType,
                                                   Demura_gray_list)  # 实例化线程

            self.thread_run_imge2.mySignal.connect(self.update_text_edit_log)  # 信号连接槽函数
            # self.thread_run_imge2.show_message_signal.connect(self.show_message_box)  # 信号连接槽函数
            self.thread_run_imge2.start()  # 开启线程


        if self.checkBox_Demura.isChecked():
            mkType = "DEMURA"
            self.textEdit_Log.setText("正在生成Demura灰阶图片...")
            print("正在生成Demura灰阶图片...")
            self.thread_run_imge3 = Thread_run_imge(mkPath_Demura, AodCreat.img_w, AodCreat.img_h, mkType,
                                                   Demura_gray_list)  # 实例化线程

            self.thread_run_imge3.mySignal.connect(self.update_text_edit_log)  # 信号连接槽函数
            # self.thread_run_imge3.show_message_signal.connect(self.show_message_box)  # 信号连接槽函数
            self.thread_run_imge3.start()  # 开启线程


        # self.textEdit_Log.setText("图片生成完成")
        QMessageBox.information(self, "提示", "点击", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

    # ============图片生成界面==============
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())



