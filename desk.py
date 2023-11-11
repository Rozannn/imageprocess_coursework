from turtle import *
import tkinter as tk
from PIL import Image, ImageTk
from image_process import *
font=("华文行楷", 17, "normal")  # 正文格式
title=("华文行楷", 30, "normal")  # 标题格式
color = 'LightSteelBlue'
class Init():
    def __init__(self):

        self.master = tk.Tk()
        self.master.title("智能信息处理课程设计")
        self.master.geometry("1000x600+500+100")
        self.master.config(width=600, height=400)
        self.face = tk.Frame(self.master)
        self.face.pack()
        text = '\n\n\n智能信息处理课程设计\n\n'
        text1 = '\n\n\n团队成员：文静蕾，苏雪，宁瑞泓，张庭瑞\n\n'

        tk.Label(self.face, text=text, font=title,height=3).pack()
        tk.Label(self.face, text=text1,height=2).pack()
        tk.Label(self.face, text=text1,height=2).pack()
        tk.Button(self.face, text="进入", font=font, command=self.next, bg=color).pack()

    def next(self):
        self.face.destroy()
        self.image_pro=Application()
        self.image_pro.mainloop()
desk=Init()
desk.master.mainloop()
