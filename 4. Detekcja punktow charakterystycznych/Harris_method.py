# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 21:19:21 2018

@author: Wojtas
"""

import cv2
import matplotlib.pyplot as plt

def Harris(gray_img, sobel_mask=2, gaussian_mask=2, k=0.05):

    sobel_x = cv2.Sobel(gray_img, cv2.CV_32F, 1,0, ksize=sobel_mask);
    sobel_y = cv2.Sobel(gray_img, cv2.CV_32F, 0,1, ksize=sobel_mask);
    sobel_x2 = sobel_x * sobel_x;
    sobel_x2 = cv2.GaussianBlur(sobel_x2, (gaussian_mask,gaussian_mask),0);
    sobel_y2 = sobel_y * sobel_y;
    sobel_y2 = cv2.GaussianBlur(sobel_y2, (gaussian_mask,gaussian_mask),0);
    sobel_xy = sobel_x * sobel_y;
    sobel_xy = cv2.GaussianBlur(sobel_xy, (gaussian_mask,gaussian_mask),0);
    
    det_m = sobel_x2*sobel_y2 - (sobel_xy*sobel_xy);
    trace_m = sobel_x2 + sobel_y2;
    
    re_img = det_m - k*trace_m*trace_m;
    return re_img;
    
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

fountain1 = cv2.imread('pliki_harris/fontanna1.jpg')
fountain2 = cv2.imread('pliki_harris/fontanna2.jpg')
cv2.imshow('f', fountain1);
cv2.waitKey(0)
cv2.destroyAllWindows()
gray_fountain1 = cv2.cvtColor(fountain1, cv2.COLOR_BGR2GRAY)
gray_fountain2 = cv2.cvtColor(fountain2, cv2.COLOR_BGR2GRAY)
f1_x, f1_y = LocalMaximum(Harris(gray_fountain1,7,7, 0.05), mask=5, threshold=0.1)
f2_x, f2_y = LocalMaximum(Harris(gray_fountain2,7,7, 0.05), mask=5, threshold=0.1)
plt.figure(1)
plt.subplot(1,2,1), plt.imshow(fountain1), plt.hold(True), plt.plot(f1_x,f1_y,'*',color='r'), plt.title('Fountain 1'), plt.show();
plt.subplot(1,2,2), plt.imshow(fountain2), plt.hold(True), plt.plot(f2_x,f2_y,'*',color='r'), plt.title('Fountain 2'), plt.show();

#
#building1 = cv2.imread('pliki_harris/budynek1.jpg')
#building2 = cv2.imread('pliki_harris/budynek2.jpg')
#gray_building1 = cv2.cvtColor(building1, cv2.COLOR_BGR2GRAY)
#gray_building2 = cv2.cvtColor(building2, cv2.COLOR_BGR2GRAY)
#b1_x, b1_y = LocalMaximum(Harris(gray_building1,7,7, 0.05), mask=5, threshold=0.1)
#b2_x, b2_y = LocalMaximum(Harris(gray_building2,7,7, 0.05), mask=5, threshold=0.1)
#plt.figure(2)
#plt.subplot(1,2,1), plt.imshow(building1), plt.hold(True), plt.plot(b1_x,b1_y,'*',color='r'), plt.title('Building 1'), plt.show();
#plt.subplot(1,2,2), plt.imshow(building1), plt.hold(True), plt.plot(b2_y,b2_x,'*',color='r'), plt.title('Building 2'), plt.show();
