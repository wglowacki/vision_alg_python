# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 15:00:07 2018

@author: Wojtas
"""

import cv2
import matplotlib.pyplot as plt

def DiffOfGaussians(gray_image, n, sigma, k, g_mask=3):
    dog = []
    gaussian_blur = cv2.GaussianBlur(gray_image, (g_mask,g_mask),sigma);

    for i in range(1,n+1):
        sigma *= k;
        current_blur = cv2.GaussianBlur(gaussian_blur,(g_mask,g_mask), sigma);
        dog.append(cv2.absdiff(gaussian_blur,current_blur));
        gaussian_blur = current_blur;
    return dog

def LocalMaximum(img, mask=5, threshold=0.6):
    x = [];
    y = [];
    rows, cols = img.shape;
    max_of_I = threshold * img.max();
    half = mask//2;
    for row in range(half,rows-half+1):
        for col in range(half,cols-half+1):
            current_pt = img[row,col];
            img[row,col] = 0;
            ROI = img[row-half:row+half+1,col-half:col+half+1];
            if(ROI.max() > max_of_I):
                x.append(col);
                y.append(row);
            img[row,col] = current_pt;
    return x, y

def LocalMaximumOfDOG(dog, mask = 5, threshold = 0.6):
    x = [];
    y = [];
    scale = []
    rows, cols = dog[0].shape;
    half = mask//2;
    for i in range(1,len(dog)-1):
        print(i)
        for row in range(half,rows-half+1):
            for col in range(half,cols-half+1):
                current_pt = dog[i][row,col];
                dog[i][row,col] = 0;
                ROI = dog[i][row-half:row+half+1,col-half:col+half+1];
                ROI_back = dog[i-1][row-half:row+half+1,col-half:col+half+1];
                ROI_next = dog[i+1][row-half:row+half+1,col-half:col+half+1];
                if current_pt > ROI.max() and current_pt > ROI_back.max() and current_pt > ROI_next.max() and current_pt > threshold:
                    x.append(col)
                    y.append(row)                    
                    scale.append(i)
                dog[i][row,col] = current_pt;
    return [x, y, scale];
        
fountain = cv2.imread("./pliki_harris/fontanna1.jpg")
fountain_pow = cv2.imread("./pliki_harris/fontanna_pow.jpg")

gray_fount = cv2.cvtColor(fountain, cv2.COLOR_BGR2GRAY)
gray_fount_pow = cv2.cvtColor(fountain_pow, cv2.COLOR_BGR2GRAY)
gray_fount_blurs = DiffOfGaussians(gray_fount, n=5, sigma=1.6, k=1.26)
gray_fount_pow_blurs = DiffOfGaussians(gray_fount_pow, n=15, sigma=1.6, k=1.26)
fount_maxs = LocalMaximumOfDOG(gray_fount_blurs, mask = 3, threshold = 2)
fount_pow_maxs = LocalMaximumOfDOG(gray_fount_pow_blurs, mask = 3, threshold = 2)

x2 = [];
y2 = [];
max_elements = 9;
for i in range(0,len(fount_pow_maxs[2])):
    if(fount_pow_maxs[2][i]==max_elements):
        x2.append(fount_pow_maxs[0][i]);
        y2.append(fount_pow_maxs[1][i]);

plt.figure(1), plt.hold(True), plt.imshow(gray_fount_pow_blurs[max_elements]), plt.plot(y2,x2,'r.'), plt.show()

