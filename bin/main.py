from pdfminer.pdfinterp import PDFPageInterpreter,PDFResourceManager
from pdfminer.converter import TextConverter,PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdevice import PDFDevice
from pdfminer.pdfpage import PDFPage



from PyQt5 import QtWidgets
import os
import sys

BASE_PATH = os.path.dirname(os.getcwd())
pdf_name = r"file\G2667FP108FF-006_电讯检&Gam_V01(VM4_RD)_20220314.pdf"
txt_name = r"file\G2678FA101FF-006_电讯检_V04(VM4_NT)_20211028.pdf"

pdf_path = os.path.join(BASE_PATH,pdf_name)
txt_path = os.path.join(BASE_PATH,txt_name)

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


def read_pdf():
    txt_write_flag = False
    write_txt = ""
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
                if str(txt).count("W6平台格式"):
                    txt_write_flag = True
                elif str(txt).count("需要烧录的 Page："):
                    txt_write_flag = False

                if txt_write_flag and (txt != " \n"):
                    write_txt += txt
                    # 写入txt文件

    with open(pdf_path.replace(".pdf", ".txt"), "w", encoding="utf-8") as fw:
        fw.write(write_txt)

read_pdf()

if __name__ =="__maine":
