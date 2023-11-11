import cv2
import numpy as np
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog
from els import *
from ims import *
from ismt import *



class Application(tk.Toplevel):

    def __init__(self):
        super().__init__()
        self.I_smooth=Image.new('1',(256,256),1)
        self.title("图片处理")

        self.img_path = tk.StringVar()
        self.frame = tk.Frame(self)
        self.frame.pack(padx=10, pady=10)

        self.lbl_im = tk.Label(self.frame, text="图像")
        self.lbl_im.grid(row=1, column=0)
        self.lbl_file = tk.Label(self.frame, text="文件")
        self.lbl_file.grid(row=0, column=0)
        self.txt_file = tk.Entry(self.frame, width=50, textvariable=self.img_path)
        self.txt_file.grid(row=0, column=1, sticky=tk.W)

        self.btn_file = tk.Button(self.frame, text="选择", command=self.sel_img_file)
        self.btn_file.grid(row=0, column=1, sticky=tk.E)

        self.lbl_txt = tk.Label(self.frame,text='去阴影结果')
        self.lbl_txt.grid(row=1, column=1)

        self.lbl_txt = tk.Label(self.frame,text='锐化结果')
        self.lbl_txt.grid(row=1, column=2)

        self.lbl_txt = tk.Label(self.frame,text='平滑结果')
        self.lbl_txt.grid(row=1, column=3)

        self.exhibit1 = tk.Label(self.frame,bg='white')
        self.exhibit1.grid(row=2, column=0)

        self.exhibit = tk.Label(self.frame,bg='white')
        self.exhibit.grid(row=2, column=1)

        self.exhibit2 = tk.Label(self.frame,bg='white')
        self.exhibit2.grid(row=2, column=2)

        self.exhibit3 = tk.Label(self.frame,bg='white')
        self.exhibit3.grid(row=2, column=3)

        self.btn_elim = tk.Button(self.frame, text="去阴影(浅色背景)",width=50, command=self.elim_shadow1)
        self.btn_elim.grid(row=3, column=1, sticky=tk.W + tk.E)

        self.btn_elim1 = tk.Button(self.frame, text="去阴影(深色背景)",width=50, command=self.elim_shadow2)
        self.btn_elim1.grid(row=4, column=1, sticky=tk.W + tk.E)

        self.btn_elim2 = tk.Button(self.frame, text="图像锐化(Roberts)",width=50, command=self.image_sharp_roberts)
        self.btn_elim2.grid(row=3, column=2, sticky=tk.W + tk.E)
        
        self.btn_elim5 = tk.Button(self.frame, text="图像锐化(Laplacian)",width=50, command=self.image_sharp_laplacian)
        self.btn_elim5.grid(row=4, column=2, sticky=tk.W + tk.E)

        self.btn_elim4 = tk.Button(self.frame, text="图像高斯平滑",width=50, command=self.gauss_smth)
        self.btn_elim4.grid(row=3, column=3, sticky=tk.W + tk.E)

        self.btn_elim3 = tk.Button(self.frame, text="图像SP平滑",width=50, command=self.sp_smth)
        self.btn_elim3.grid(row=4, column=3, sticky=tk.W + tk.E)
    def sel_img_file(self):
        self.img_path.set(filedialog.askopenfilename(title="选择图片", initialdir="."))
        self.I = Image.open(self.img_path.get()).resize([400,400])
        img = ImageTk.PhotoImage(self.I)
        self.exhibit1.config(image=img)
        self.exhibit1.image=img

    def elim_shadow1(self ):
        if self.img_path:
            image = cv2.cvtColor(np.asarray(self.I), cv2.COLOR_RGB2BGR)
            b, g, r = cv2.split(image)
            b_output= min_max_filtering(Mode=0, Window=20, Image=b)
            g_output = min_max_filtering(Mode=0, Window=20, Image=g)
            r_output = min_max_filtering(Mode=0, Window=20, Image=r)
            result = cv2.merge([b_output, g_output , r_output ])
            result =  result.astype(np.uint8)
            image=Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
            self.I=image
            image=image.resize([400,400])
            img = ImageTk.PhotoImage(image)
            self.exhibit.config(image=img)
            self.exhibit.image=img
    def elim_shadow2(self ):
        if self.img_path:
            image = cv2.cvtColor(np.asarray(self.I), cv2.COLOR_RGB2BGR)
            b, g, r = cv2.split(image)
            b_output= min_max_filtering(Mode=1, Window=20, Image=b)
            g_output = min_max_filtering(Mode=1, Window=20, Image=g)
            r_output = min_max_filtering(Mode=1, Window=20, Image=r)
            result = cv2.merge([b_output, g_output , r_output ])
            result =  result.astype(np.uint8)
            image=Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
            self.I=image
            image=image.resize([400,400])
            img = ImageTk.PhotoImage(image)
            self.exhibit.config(image=img)
            self.exhibit.image=img
    def image_sharp_roberts(self):
        if self.img_path:
            img=np.asarray(self.I)
            img = img[:, :, 0]
            final_Roberts_img = method_choose(0,img)
            image=Image.fromarray(final_Roberts_img)
            self.I_sharp=image
            image=image.resize([400,400])
            img = ImageTk.PhotoImage(image)
            self.exhibit2.config(image=img)
            self.exhibit2.image=img
    def image_sharp_laplacian(self):
        if self.img_path:
            img=np.asarray(self.I)
            img = img[:, :, 0]
            final_sobel_img = method_choose(4,img)
            image=Image.fromarray(final_sobel_img)
            self.I_sharp=image
            image=image.resize([400,400])
            img = ImageTk.PhotoImage(image)
            self.exhibit2.config(image=img)
            self.exhibit2.image=img
    def gauss_smth(self):
        if self.img_path:
            img=np.asarray(self.I)
            img = img[:, :, 0]
            #image = Gaussian_noise(img, mean=0, var=0.01)  
            result = Transfinite_pixel_smoothing_method(img, T=60)
            result =  result.astype(np.uint8)
            image=Image.fromarray(result)
            self.I_smooth=image
            image=image.resize([400,400])
            img = ImageTk.PhotoImage(image)
            self.exhibit3.config(image=img)
            self.exhibit3.image=img
    def sp_smth(self):
        if self.img_path:
            img=np.asarray(self.I)
            img = img[:, :, 0]
#image = sp_noise(img, prob=0.2) 
            result = Transfinite_pixel_smoothing_method(img, T=60)
            result =  result.astype(np.uint8)
            image=Image.fromarray(result)
            self.I_smooth=image
            image=image.resize([400,400])
            img = ImageTk.PhotoImage(image)
            self.exhibit3.config(image=img)
            self.exhibit3.image=img

if __name__ == "__main__":
    app = Application()
    app.mainloop()
