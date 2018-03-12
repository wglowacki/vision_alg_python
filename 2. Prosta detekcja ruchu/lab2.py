#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle 
import numpy as np
import os, os.path

###TASK 8.
#Wczytywanie sekwencji wideo, odejmowanie ramek, indeksacja

#loop through image_path_list to open each image
image_array = []
I_VIS = []
for i in range (300,450):
    image = cv2.imread('img_seq/in%06d.jpg' %i)
    I_VIS.append(image)
    image_array.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)) #array of gray images
#Odejmowanie ramek i binaryzacja
kernel1 = np.ones((2,2), np.uint8)
kernel2 = np.ones((2,2), np.uint8)
for i in range(1,len(image_array)):
    diff_image = cv2.absdiff(image_array[i], image_array[i-1])
    binary_diff = cv2.threshold(diff_image,10,80,cv2.THRESH_BINARY)
# D - obraz
# 10 - prog
# 255 - co ma byc przypisane na wyjscie jako wartosc maksymalna
# cv2.THRESH_BINARY - typ binaryzacji (tu najprostsza - za obiekty piksele powyzej progu)
    binary_diff = binary_diff[1]
    img_erosion = cv2.erode(binary_diff, kernel2, iterations=1)
    img_dilation = cv2.dilate(img_erosion, kernel2, iterations=1)
    median_blur = cv2.medianBlur(img_dilation, 5)
    cv2.imshow('binary diff', median_blur)
    cv2.waitKey(10)
    
    retval, labels, stats, centroids = cv2.connectedComponentsWithStats(median_blur)
    cv2.imshow("Labels",np.uint8(labels/stats.shape[0]*255))
    if (stats.shape[0] > 1): # czy sa jakies obiekty
        pi, p = max(enumerate(stats[1:,4]), key=(lambda x: x[1]))
        pi = pi + 1
        # wyrysownie bbox
        cv2.rectangle(I_VIS[i],(stats[pi,0],stats[pi,1]),(stats[pi,0]+stats[pi,2],stats[pi,1]+stats[pi,3]),(255,0,0),2)
        # wypisanie informacji
        cv2.putText(I_VIS[i],"%f" % stats[pi,4],(stats[pi,0],stats[pi,1]),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0))
        cv2.putText(I_VIS[i],"%d" %pi,(np.int(centroids[pi,0]),np.int(centroids[pi,1])),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0))
        cv2.imshow('obraz', I_VIS[i])
        
cv2.waitKey(0)
cv2.destroyAllWindows()