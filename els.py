import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog as filedialog




def max_filtering(Window, Image):
    fill = np.full((Image.shape[0]+(Window//2)*2, Image.shape[1]+(Window//2)*2), -1)
    fill[(Window//2):fill.shape[0]-(Window//2), (Window//2):fill.shape[1]-(Window//2)] = Image.copy()
    temp = np.full((Image.shape[0]+(Window//2)*2, Image.shape[1]+(Window//2)*2), -1)
    for y in range(0,fill.shape[0]):
        for x in range(0,fill.shape[1]):
            if fill[y,x]!=-1:
                mask = fill[y-(Window//2):y+(Window//2)+1,x-(Window//2):x+(Window//2)+1]
                max = np.amax(mask)
                temp[y,x] = max
    output = temp[(Window//2):fill.shape[0]-(Window//2), (Window//2):fill.shape[1]-(Window//2)].copy()
    return output


def min_filtering(Window, Image):
    fill = np.full((Image.shape[0]+(Window//2)*2, Image.shape[1]+(Window//2)*2), 300)
    fill[(Window//2):fill.shape[0]-(Window//2), (Window//2):fill.shape[1]-(Window//2)] = Image.copy()
    temp = np.full((Image.shape[0]+(Window//2)*2, Image.shape[1]+(Window//2)*2), 300)
    for y in range(0,fill.shape[0]):
        for x in range(0,fill.shape[1]):
            if fill[y,x]!=300:
                mask = fill[y-(Window//2):y+(Window//2)+1,x-(Window//2):x+(Window//2)+1]
                min = np.amin(mask)
                temp[y,x] = min
    output = temp[(Window//2):fill.shape[0]-(Window//2), (Window//2):fill.shape[1]-(Window//2)].copy()
    return output


#B is the filtered image and I is the original image
def background_subtraction(Image, Back):
    O = Image - Back
    norm_img = cv2.normalize(O, None, 0,255, norm_type=cv2.NORM_MINMAX)
    return norm_img

def min_max_filtering(Mode, Window, Image):
    if Mode == 0:
        #max_filtering
        max = max_filtering(Window, Image)
        #min_filtering
        output = min_filtering(Window, max)
        #subtraction
        normalised_img = background_subtraction(Image, output)
    elif Mode == 1:
        #min_filtering
        min = min_filtering(Window, Image)
        #max_filtering
        output = max_filtering(Window, min)
        #subtraction
        normalised_img = background_subtraction(Image, output)
    return normalised_img
