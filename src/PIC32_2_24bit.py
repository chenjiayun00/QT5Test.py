import os

import matplotlib.image as mpimg
from PIL import Image

path = r"./32bit"
def image_convert(path):
    newpath = path + "to24bit"
    files = os.listdir(path)
    # print(files)
    for img_name in files:
        # print(k)
        img_path = path + r"/" +img_name
        img = Image.open(img_path)
        save_img = img.convert('RGB')  # 32位深转24位深
        save_img.save(newpath + r"/" + img_name)


    # img_path='1.bmp'

    # img = Image.open(img_path)
    # # save_img = img.convert('RGBA')    #24位深转32位深
    # save_img = img.convert('RGB')    # 32位深转24位深
    # save_img.save('1to32.bmp')

if __name__ =="__main__":
    image_convert(path)