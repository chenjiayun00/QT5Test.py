from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import time
import sys

class ThreadUpdateUI(QDialog):
    def __init__(self):
        super(ThreadUpdateUI, self).__init__()
        self.setWindowTitle("线程测试")
        self.resize(600, 500)

        self.button = QPushButton()
        # self.lable.s
        # self.label.setGeometry(QRect(50, 40, 41, 21))
        # self.lable.text("已经执行")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wind = ThreadUpdateUI()
    wind.show()
    sys.exit(app.exec_())