import cv2
import math
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import time
import os

BASE_DIR = os.getcwd()
img_w = 1080
img_h = 2400
gray_list = [16, 32, 64, 128, 192, 224]  # demura灰阶图片
# 定义要创建的目录,路径不能有中文
FILENAME_GRAY = "TEMS\\{}X{}_GRAY".format(str(img_w), str(img_h))
FILENAME_AOD = "TEMS\\{}X{}_AOD".format(str(img_w), str(img_h))
FILENAME_Demura = "TEMS\\{}X{}_DEMURA".format(str(img_w), str(img_h))

# 将两个目录拼接 BASE_DIR + r"\" + FILENAME_GRAY
mkPath_GRAY = os.path.join(BASE_DIR, FILENAME_GRAY)
mkPath_AOD = os.path.join(BASE_DIR, FILENAME_AOD)
mkPath_Demura = os.path.join(BASE_DIR, FILENAME_Demura)
def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path + ' 目录已存在')
        return False


def creatAODGray(mkPath,w,h):
    '''
    生成AOD灰阶画面
    '''
    image = Image.new('RGB', (w, h), (0, 0, 0))
    # image.save(str.format("D:\A1\{}.bmp",0))
    image.save(mkPath + str.format("\\{}.bmp", 0))

    time.sleep(5)
    r = round(((w * h) * 0.15/math.pi) ** 0.5)
    print("AOD的半径R= :", r)
    print("正在生成AOD灰阶画面...")
    for num in range(0, 256):
        img_path = mkPath + str.format("\\{}.bmp", 0)

        img = cv2.imread(img_path) # 读取图片

        cv2.circle(img, (round(w/2), round(h/2)), r, (num, num, num), -1)
        # cv2.circle(img, center, radius, color[, thickness[, lineType[, shift]]])
        # cv2.circle(输入的图片data,圆心位置,圆的半径,圆的颜色,圆形轮廓的粗细（如果为正）负数(-1)表示要绘制实心圆,圆边界的类型,中心坐标和半径值中的小数位数)
        #                          600*1326 780
        # cv2.imshow('img',img)
        # cv2.waitKey()
        cv2.imwrite(mkPath + str.format("\\AOD_{}.bmp", num), img)

    os.remove(img_path)
def draw_GrayPhotos_test(mkPath1, w, h, r, g, b, name):

    """
    :param img_w: 宽
    :param img_h: 高
    :param R:
    :param G:
    :param B:
    :param B:
    :param name: 图片名称
    :return:
   """
    print(mkPath1)
    print(name)
    # 生成背景图片
    print(w,h,r,g,b)
    # image = Image.new('RGB', (w, h), (r, g, b))
    # 保存原始版本
    print("保存原始版本")

    # image.save(str.format("{}/{}.bmp", mkPath1, name))


def draw_GrayPhotos(mkPath1, w, h, r, g, b, name):

    """
    :param img_w: 宽
    :param img_h: 高
    :param R:
    :param G:
    :param B:
    :param B:
    :param name: 图片名称
    :return:
   """
    # 生成背景图片
    image = PIL.Image.new('RGB', (w, h), (r, g, b))
    # 保存原始版本
    image.save(str.format("{}/{}.bmp", mkPath1, name))


def CreatGray(mkPath, img_ww, img_hh):
    # 生成0-255灰阶图
    print("正在生成灰阶画面...")
    for num in range(0, 256):
        name = str(num) + "Gray"
        r, g, b = num, num, num

        draw_GrayPhotos(mkPath, img_ww, img_hh, r, g, b, name)
    # 生成红绿蓝画面
    print("正在生成R、G、B画面...")
    draw_GrayPhotos(mkPath, img_ww, img_hh, 255, 0, 0, "R")
    draw_GrayPhotos(mkPath, img_ww, img_hh, 0, 255, 0, "G")
    draw_GrayPhotos(mkPath, img_ww, img_hh, 0, 0, 255, "B")
    print("生成R、G、B画面完成")

def creat_demura_photos(mkPath,w,h,gray_list):

    print("正在生成Demura画面...")
    for num in gray_list:
        name_r = "R" + str(num)
        name_g = "G" + str(num)
        name_b = "B" + str(num)
        name_w = "w" + str(num)

        draw_GrayPhotos(mkPath, w, h, num, 0, 0, name_r)
        draw_GrayPhotos(mkPath, w, h, 0, num, 0, name_g)
        draw_GrayPhotos(mkPath, w, h, 0, 0, num, name_b)

        draw_GrayPhotos(mkPath, w, h, num, num, num, name_w)


if __name__ == '__main__':
    BASE_DIR = os.getcwd()
    img_w = int(input("请输入img_w:"))
    img_h = int(input("请输入img_h:"))

    gray_list = [16, 32, 64, 128, 192, 224]  # demura灰阶图片
    # 定义要创建的目录,路径不能有中文
    FILENAME_GRAY = "TEMS\\{}X{}_GRAY".format(str(img_w), str(img_h))
    FILENAME_AOD = "TEMS\\{}X{}_AOD".format(str(img_w), str(img_h))
    FILENAME_Demura = "TEMS\\{}X{}_DEMURA".format(str(img_w), str(img_h))

    # 将两个目录拼接 BASE_DIR + r"\" + FILENAME_GRAY
    mkPath_GRAY = os.path.join(BASE_DIR, FILENAME_GRAY)
    mkPath_AOD = os.path.join(BASE_DIR, FILENAME_AOD)
    mkPath_Demura = os.path.join(BASE_DIR, FILENAME_Demura)

    # 创建目录
    mkdir(mkPath_GRAY)
    mkdir(mkPath_AOD)
    mkdir(mkPath_Demura)

    creatAODGray(mkPath_AOD,img_w,img_h)
    CreatGray(mkPath_GRAY,img_w,img_h)
    # creat_demura_photos(mkPath_Demura,gray_list)
    print("全部画面生成完成！")
