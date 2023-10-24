from tkinter import *
from tkinter import messagebox

import PyQt5
import PyQt5
def func():
    print("我是陈同学")


# 创建窗口，实例化一个窗口对象
root = Tk()

# 窗口大小
root.geometry("900x600+374+182")

# 窗口标题
root.title("我的个性签名设计")

# 添加标签控件
lable = Label(root, text="签名:", font=("宋体", 25),fg="red")
"""
text参数用于指定显示的文本；
font参数用于指定字体大小和样式；
fg参数用于指定字体颜色
"""
# 标签定位
lable.grid()
"""
lable.grid()等价于lable.grid(row=0, column=1)
"""
# 添加输入框
entry = Entry(root, font=("宋体", 25), fg="red")
entry.grid(row=0, column=1)
"""
row=0,column=1表示我们将输入框控件，放在第1行第2列的位置；
python语言中，这个下标是从0开始的。
"""

# 添加点击按钮
button = Button(root, text="签名设计", font=("宋体", 25), fg="blue", command=func)
button.grid(row=1, column=1)

# 显示窗口
root.mainloop()
