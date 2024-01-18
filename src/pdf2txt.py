from pdfminer.pdfinterp import PDFPageInterpreter,PDFResourceManager
from pdfminer.converter import TextConverter,PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage

# import pdfplumber
from PyQt5 import QtWidgets
import os
import sys
import re
import time

def jzc_to_w6():
    pass

    # 使用pdfminer
def read_pdf(pdf_path):
    # 获取pdf文档
    fp = open(pdf_path, "rb")
    # 创建一个与文档相关的解释器
    parser = PDFParser(fp)

    # pdf文档的对象，与解释器连接起来
    doc = PDFDocument(parser=parser)
    parser.set_document(doc=doc)

    # 如果是加密pdf，则输入密码
    # doc._initialize_password()

    # 创建pdf资源管理器
    resource = PDFResourceManager()

    # 参数分析器
    laparam = LAParams()

    # 创建一个聚合器
    device = PDFPageAggregator(resource, laparams=laparam)

    # 创建pdf页面解释器
    interpreter = PDFPageInterpreter(resource, device)
    print("开始读取")
    txt_write_flag = False
    read_text = "" # 读取到的源文件
    write_txt = ""
    jzc_re_com1 = re.compile(r"PGclient\.writeReg\(\'WR_DISPLAY_REG[\s]*FF[\s]*([0-9a-fA-F]{2})[\s]*")  # jzc格式正则表达式1
    jzc_re_com2 = re.compile(r"WR_DISPLAY_REG[\s]*FF[\s]*([0-9a-fA-F]{2})[\s]*")  # jzc格式正则表达式2
    jzc_re_com3 = re.compile(r"([0-9a-fA-F]{2})")  # jzc 将0000转换成0x00,0x00

    jzc_flag = 0 # jzc标识符
    test_flag = 0 #
    # 获取页面的集合
    for page in PDFPage.get_pages(fp):
        # 使用页面解释器来读取
        interpreter.process_page(page)

        # 使用聚合器来获取内容
        layout = device.get_result()
        for out in layout:
            if hasattr(out, "get_text"):
                # print(out.get_text())
                txt = out.get_text()
                read_text += txt
                if re.findall(r"Sleep out[\s\S]*29.", txt):  # 将Sleep out ...(29)去掉
                    txt = re.sub(r"Sleep out[\s\S]*29.", "", txt)
                    # print(txt)
                if re.findall(r"III、[\s]*Initial[\s]*Code[\s]*\n", txt):    # txt的内容从W6平台格式后面开始
                    txt_write_flag = True
                    txt = ""
                elif str(txt).count("需要烧录的 Page："):     # txt的内容到：需要烧录的 Page：结束
                    txt_write_flag = False

                if txt_write_flag and (txt != " \n"):
                    if txt.count("000000"):
                        txt = txt
                    if re.search(jzc_re_com1, txt):
                        jzc_flag = 1
                        txt = txt.strip().replace("#", "//").replace("\n", "").replace(" ", "")
                        txt = re.sub(jzc_re_com1, r"REGS.WRITE(0,39\1", txt)
                        write_txt += txt
                    elif re.search(jzc_re_com2, txt):
                        jzc_flag = 1
                        txt = txt.strip().replace("#", "//").replace("\n", "$$").replace(" ", "")
                        txt = re.sub(jzc_re_com2, r"REGS.WRITE(0,39\1", txt)
                        write_txt += txt
                    else:
                        write_txt += txt.replace("#", "//")
                    # 写入txt文件

    w6_fileName = pdf_path.replace(".pdf", "_W6.txt")
    pdf2txt_fileName = pdf_path.replace(".pdf", "PDF直出.txt")
    re_compile_page = re.compile(r"\d+\s+/\s+\d+")  # 页码的正则表达式
    write_txt = re.sub(re_compile_page, "", write_txt)
    write_txt = re.sub(r"[\s]{2,}\n", "\n", write_txt)
    # write_txt = write_txt.replace(r"REGS.WRITE", "\nREGS.WRITE")
    # write_txt = write_txt.replace(r")REGS.WRITE", ")\nREGS.WRITE")  # REGS.WRITE(0,390808')REGS.WRITE(0,39FE00')
    if jzc_flag == 1:
        # write_txt = re.sub(r"\s", "", write_txt)
        write_txt = write_txt.replace(r"$$", "")  # REGS.WRITE(0,0x39,0x78,$$0x1D
        write_txt = jzc_re_com3.sub(r"0x\1,", write_txt)     # 0000替换成0x00,0x00格式
        write_txt = write_txt.replace(r",')", ")")  # 将"')"替换成 ")"
        write_txt = re.sub(r"0xDe,lay0x([0-9]{2}),([0-9]*)ms", r"//TIME.DELAY(\1\2)", write_txt)  # 将0xDe,lay0x10,0ms)替换成TIME.DELAY(100)
        write_txt = re.sub(r"0x([0-9]{2}),([0-9]*[HZhz]{2})", r"\1\2", write_txt)   # 将0x12,0Hz 变成120HZ
        write_txt = write_txt.replace("REGS.WRITE(", "\nREGS.WRITE(")   # 230530

    with open(w6_fileName, "w", encoding="utf-8") as fw:
        fw.write(write_txt)
        print(write_txt)
    # with open(pdf2txt_fileName, "w", encoding="utf-8") as fw1:
    #     fw1.write(read_text)
    #     print(write_txt)
    print("读取结束")
    return w6_fileName, "W6格式转换成功"

    # 使用pdfminer
    # 使用pdfplumber
# def read_pdf_by_pdfplumber(pdf_path):
#
#     t_start = time.time()
#     print("开始读取")
#     txt_write_flag = False
#     read_text = "" # 读取到的源文件
#     write_txt = ""
#     jzc_re_com1 = re.compile(r"(PGclient\.writeReg\(\'WR_DISPLAY_REG[\s]*FF[\s]*)([0-9a-fA-F]{2})[\s]*")  # jzc格式正则表达式1
#     jzc_re_com2 = re.compile(r"WR_DISPLAY_REG[\s]*FF[\s]*([0-9a-fA-F]{2})[\s]*")  # jzc格式正则表达式2
#     jzc_re_com3 = re.compile(r"([0-9a-fA-F]{2})")  # jzc 将0000转换成0x00,0x00
#     re_compile_page = re.compile(r"\d+\s*/\s*\d+")  # 页码的正则表达式
#
#     jzc_flag = 0 # jzc标识符
#     test_flag = 0 #
#
#     # 打开pdf文档
#     fp = pdfplumber.open(pdf_path)
#     page_num = len(fp.pages)
#     # with-open-as 进行 PDF -> TXT
#     with pdfplumber.open(pdf_path) as pdf:
#
#         for i in range(page_num):
#             page = pdf.pages[i]
#             t_start1 = time.time()
#             text = page.extract_text()
#
#             t_end = time.time()
#             print("读取一页耗时：", t_end - t_start1)
#             text = re.sub(re_compile_page, "\n", text)  # 页码改为换行符
#             if text != None:
#                 read_text += text
#                 # print(text)
#                 print("第{%d}页读写完成"%(i))
#
#     t_end = time.time()
#     print("读取耗时：",t_end - t_start)
#     text_arr = read_text.split("\n")
#     write_txt = ""
#     W6_text = ""
#     start_flag = 0
#     for txt in text_arr:
#         if re.findall(r"III、[\s]*Initial[\s]*Code", txt):  # 开始截取
#             start_flag += 1
#             if start_flag == 2:
#                 txt_write_flag = True
#                 txt = ""
#         if re.findall(r"Sleep out", txt):  # 将Sleep out ...(29)去掉
#             txt_write_flag = False
#             break
#
#         if txt_write_flag == True:
#             write_txt += txt
#     if re.search(jzc_re_com1, write_txt):   #
#         write_txt = re.sub(jzc_re_com1, "\n" + r"\1\2", write_txt)    # 原格式
#
#         W6_text = write_txt.strip().replace("#", "//").replace("\n", "").replace(" ", "") # W6格式
#         W6_text = re.sub(jzc_re_com1, r"REGS.WRITE(0,39\2", W6_text)
#         W6_text = W6_text.replace(r"$$", "")  # REGS.WRITE(0,0x39,0x78,$$0x1D
#         W6_text = jzc_re_com3.sub(r"0x\1,", W6_text)  # 0000替换成0x00,0x00格式
#         W6_text = W6_text.replace(r",')", ")")  # 将"')"替换成 ")"
#         W6_text = re.sub(r"0xDe,lay0x([0-9]{2}),([0-9]*)ms", r"//TIME.DELAY(\1\2)",W6_text)  # 将0xDe,lay0x10,0ms)替换成TIME.DELAY(100)
#         W6_text = re.sub(r"0x([0-9]{2}),([0-9]*[HZhz]{2})", r"\1\2", W6_text)  # 将0x12,0Hz 变成120HZ
#         W6_text = W6_text.replace("REGS.WRITE(", "\nREGS.WRITE(")  # 230530
#
#     pdf2txt_fileName = pdf_path.replace(".pdf", "PDF直出.txt")
#     with open(pdf2txt_fileName, "w", encoding="utf-8") as fw1:
#         fw1.write(write_txt)
#         print(write_txt)
#     w6_fileName = pdf_path.replace(".pdf", "_W6.txt")
#     with open(w6_fileName, "w", encoding="utf-8") as fw:
#         fw.write(W6_text)
#     t_end = time.time()
#     print("读写耗时：", t_end - t_start)
#     print("读取结束")
#
#     return w6_fileName, "PDF文档读取成功"

def w6_to_lua(w6_file_name, lua_type):
    # w6_str_a = "REGS.WRITE(0,0x05,"
    # w6_str_b = "REGS.WRITE(0,0x15,"
    # w6_str_c = "REGS.WRITE(0,0x39,"
    re_w6_ocm = re.compile(r"REGS\.WRITE\(0,0[\w]{3},")  # w6格式正则表达式
    re_jzc_ocm = re.compile(r"PGclient.writeReg\([\s]*\'WR_DISPLAY_REG[\s]*FF[\s]*")  #JZC格式正则表达式
    print(lua_type)
    if lua_type == "6404":
        lua_str = "dcs_w("
        lua_delay = "delay"
    elif lua_type == "6601A-D-PHY":
        lua_str = "DMIPI.REG_W("
        lua_delay = "TIME.DELAY"
    # elif lua_type == "6601A-C-PHY":
    #     lua_str = "CMIPI.REG_W("
    #     lua_delay = "TIME.DELAY"
    lua_file_name = w6_file_name.replace("W6.txt", lua_type + ".txt")

    write_data = ""
    last_line = ""
    with open(w6_file_name, "r", encoding="utf-8") as f_r:
        for data in f_r:
            data = data.replace("//", "--").replace("#", "--").replace("')", "")
            data = re.sub(re_w6_ocm, lua_str, data)
            data = re.sub(re_jzc_ocm, "\r\n"+lua_str, data)
            data = data.strip()
            if data.startswith("--") or data.startswith("TIME.DELAY"):
                if last_line.__contains__("--") or last_line.__contains__("TIME.DELAY") or last_line == "":
                    data = "\n" + data
                else:
                    data = ")\n" + data
                write_data += data
                last_line = data
            else:
                re_com_ = r"0[\w]{3}[\s]*--"  # 匹配类似于 0xbb --
                if re.search(re_com_, data):
                    aa = re.search(re_com_, data).group()  # 匹配类似于 0xbb --
                    bb = list(aa)  # 字符串不能直接插入，需要先转成列表
                    bb.insert(4, ")")
                    bb = "".join(bb)
                    data = re.sub(re_com_, bb, data)  # 将类似于 0xbb --变成0xbb)--
                # data = data.strip()
                if data.startswith(lua_str) or data == "":
                    if last_line.__contains__("--") or last_line.__contains__("TIME.DELAY") or last_line == "":
                        data = "\n" + data
                    else:
                        data = ")\n" + data

                write_data += data
                last_line = data
    write_data = write_data.replace("\n)\n", "\n\n").replace("TIME.DELAY", lua_delay).replace("))", ")").strip()
    if write_data.endswith(")"):
        pass
    else:
        write_data = write_data + ")"
    with open(lua_file_name, "w", encoding="utf-8") as fw:
        fw.write(write_data)
    print(write_data)
    return lua_file_name, lua_type + "格式转换完成"

def w6_to_6404(fileName, lua_type):
    if str(fileName).endswith(".pdf"):
        w6_fileName, mesg = read_pdf(fileName)
        # w6_fileName, mesg = read_pdf_by_pdfplumber(fileName)
        lua_file_name, mesg = w6_to_lua(w6_fileName, lua_type)
    elif str(fileName).upper().endswith(".TXT"):
        w6_fileName = fileName
        lua_file_name, mesg = w6_to_lua(w6_fileName, lua_type)
    else:
        pass
    return lua_file_name, mesg

def w6_to_6601A_C(fileName, lua_type):
    if str(fileName).endswith(".pdf"):
        w6_fileName, mesg = read_pdf(fileName)
        # w6_fileName, mesg = read_pdf_by_pdfplumber(fileName)
        lua_file_name, mesg = w6_to_lua(w6_fileName, lua_type)
    elif str(fileName).upper().endswith(".TXT"):
        w6_fileName = fileName
        lua_file_name, mesg = w6_to_lua(w6_fileName, lua_type)
    else:
        pass
    return lua_file_name, mesg


def w6_to_6601A_D(fileName, lua_type):
    if str(fileName).endswith(".pdf"):
        w6_fileName, mesg = read_pdf(fileName)
        # w6_fileName, mesg = read_pdf_by_pdfplumber(fileName)
        lua_file_name, mesg = w6_to_lua(w6_fileName, lua_type)
    elif str(fileName).upper().endswith(".TXT"):
        w6_fileName = fileName
        lua_file_name, mesg = w6_to_lua(w6_fileName, lua_type)
    else:
        pass
    return lua_file_name, mesg


if __name__ =="__main__":
    BASE_PATH = os.path.dirname(os.getcwd())
    # pdf_name = r"file\G2667FP108FF-006_电讯检&Gam_V01(VM4_RD)_20220314.pdf"
    pdf_name = r"C:\Users\10176\Desktop\G3678FP102FF-00C_电讯检_V04_20230920.pdf"
    # txt_name = r"file\G2678FA101FF-006_电讯检_V04(VM4_NT)_20211028.pdf"
    pdf_path = os.path.join(BASE_PATH, pdf_name)
    # txt_path = os.path.join(BASE_PATH, txt_name)
    w6_fileName = r"C:\Users\10176\Desktop\G3678FP102FF-00C_电讯检_V04_20230920"
    w6_fileName = os.path.join(BASE_PATH, w6_fileName)

    # read_pdf(pdf_path)
    # w6_to_6404(w6_fileName, "6404")
    # read_pdf(pdf_name)
    read_pdf_by_pdfplumber(pdf_name)
    # fileName = r"C:\Users\10176\Desktop\D30全代码.txt"
    # lua_type = "6601A-D-PHY"
    # w6_to_6601A_D(fileName, lua_type)