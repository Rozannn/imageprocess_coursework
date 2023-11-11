import random
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import heapq


def sp_noise(image, prob):
    """
    添加椒盐噪声
    prob:噪声比例
    每遍历到一个像素点，就用随机函数获取一个随机值，
    如果这个值满足某个条件，则向当前点像素点添加胡椒噪声或者食盐噪声
    """
    # 待输出的图片
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    # 遍历图像，获取叠加噪声后的图像
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                # 添加胡椒噪声
                output[i][j] = 0
            elif rdn > thres:
                # 添加食盐噪声
                output[i][j] = 255
            else:
                # 不添加噪声
                output[i][j] = image[i][j]
    return output


def Gaussian_noise(image, mean=0, var=0.001):
    """
        添加高斯噪声
        mean : 均值
        var : 方差
        先将图片的像素点归一化，则像素值在0到1之间
        然后生成高斯噪声：均值是0，方差是  ，
        则这个噪声的特点是：噪声值集中在0附近，而且以0为对称轴对称，有正也有负，
        将噪声叠加到图片上，此时图片的像素值可能大于0或者小于1，
        所以需要使用clip函数将像素值裁剪到0和1之间。
    """
    # 将图片的像素值归一化，存入矩阵中
    image = np.array(image / 255, dtype=float)
    # 生成正态分布的噪声，其中mean表示均值，var表示方差
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    # 将噪声叠加到图片上
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    # 将图像的归一化像素值控制在low_clip和1.0之间，防止噪声越界
    out = np.clip(out, low_clip, 1.0)
    # 将图像的像素值恢复到0到255之间
    out = np.uint8(out * 255)
    return out


def neighborhood_smooth(img, k=4):
    """
    局部平滑法
    k:默认为4邻域
    """
    h, w = img.shape[:2]
    smooth_img = np.zeros((h - 2, w - 2), dtype=np.uint8)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            smooth_img[i - 1, j - 1] = (int(img[i - 1, j]) + int(img[i + 1, j])
                                        + int(img[i, j - 1]) + int(img[i, j + 1])) / k
    return smooth_img


def Transfinite_pixel_smoothing_method(img, T=50):
    """
    超限像素平滑法
    img:椒盐噪声/高斯噪声图片
    T:默认50
    """
    # 首先调用局部平滑法进行处理
    neighborhood_img = neighborhood_smooth(img, k=4)
    h, w = neighborhood_img.shape[:2]
    for i in range(h):
        for j in range(w):
            if np.abs(neighborhood_img[i, j] - img[i, j]) <= T:
                neighborhood_img[i, j] = img[i, j]
    return neighborhood_img


# # 读入图像
# src = cv.imread("image.png", 0)  # 以灰度图像读入
# img = src.copy()

# # 生成噪声图片
# img_sp = sp_noise(img, prob=0.2)  # 添加椒盐噪声，噪声比例为0.02
# img_gaussian = Gaussian_noise(img, mean=0, var=0.01)  # 添加高斯噪声，均值为0，方差为0.01

# # 超限像素平滑法处理两种噪声图片
# result_img_sp = Transfinite_pixel_smoothing_method(img_sp, T=60)
# result_img_gauss = Transfinite_pixel_smoothing_method(img_gaussian, T=60)



