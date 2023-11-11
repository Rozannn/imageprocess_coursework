import random
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import cv2
import heapq
from PIL import Image
import PIL.ImageOps


# 求卷积运算
def convolution(img_old, kernel):
    img_new = np.zeros(img_old.shape, dtype=int)
    for i in range(1, img_new.shape[0] - 1):  # 第一列和最后一列不用处理
        for j in range(1, img_new.shape[1] - 1):
            tmp = 0  # 初始化为0,用来求和
            for k in range(-1, 2):
                for l in range(-1, 2):
                    tmp += img_old[i + k][j + l] * kernel[k + 1][l + 1]
            img_new[i][j] = abs(tmp)
    return img_new


def method_choose(method,img):
    global horizontal_img
    global vertical_img
    if method == 0:
        # Roberts算子
        # 公式 g(i,j)=abs(f(i+1,j+1)-f(i,j)+abs(f(i+1,j)-f(i,j+1))
        Roberts_img = np.zeros(img.shape, dtype=int)
        for i in range(1, img.shape[0] - 1):  # 第一列和最后一列不用处理
            for j in range(1, img.shape[1] - 1):
                Roberts_img[i][j] = abs(int(img[i + 1][j + 1]) - int(img[i][j])) + abs(
                    int(img[i + 1][j]) - int(img[i][j + 1]))

        white_Roberts_img = np.full(Roberts_img.shape, 255, dtype=np.uint8)  # 像素反转
        final_img = white_Roberts_img - Roberts_img

    if method == 1:
        # 水平锐化
        kernel_horizontal = np.array([[1, 2, 1],
                                      [0, 0, 0],
                                      [-1, -2, -1]])
        horizontal_img = convolution(img, kernel_horizontal)

        white_horizontal_img = np.full(horizontal_img.shape, 255, dtype=np.uint8)
        final_img = white_horizontal_img - horizontal_img

    if method == 2:
        # 垂直锐化
        kernel_vertical = np.array([[1, 0, -1],
                                    [2, 0, -2],
                                    [1, 0, -1]])
        vertical_img = convolution(img, kernel_vertical)

        white_vertical_img = np.full(vertical_img.shape, 255, dtype=np.uint8)
        final_img = white_vertical_img - vertical_img

    if method == 3:
        # Sobel算子
        # 利用垂直锐化和水平锐化的结果
        sobel_img = np.sqrt(vertical_img * vertical_img + horizontal_img * horizontal_img)
        sobel_img = np.minimum(sobel_img, 255)  # 调整灰度大小，最大为255
        # print(np.max(img_Sobel))

        white_Sobel_img = np.full(vertical_img.shape, 255, dtype=np.uint8)
        final_img = white_Sobel_img - sobel_img

    if method == 4:
        # Laplacian锐化
        kernel_Laplacian = np.array([[0, -1, 0],
                                     [-1, 4, -1],
                                     [0, -1, 0]])
        Laplacian_img = convolution(img, kernel_Laplacian)
        Laplacian_img = abs(Laplacian_img)

        white_Laplacian_img = np.full(Laplacian_img.shape, 255, dtype=np.uint8)
        final_img = white_Laplacian_img - Laplacian_img

    return final_img

