import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle 
import numpy as np
import os, os.path


def draw_flow(img, u, v, step, thresh, color):
    y, x = img.shape
    mm=(u*u+v*v)**0.5
    m=mm>thresh
    for j in range(0,y,step):
        for i in range(0,x,step):
            if m[j][i]:
                cv2.line(img, (i,j), (i+np.int32(u[j][i]), j+np.int32(v[j][i])), color)
    
#Wczytywanie sekwencji wideo, odejmowanie ramek, indeksacja

#loop through image_path_list to open each image
img = []
I_VIS = []
ground_truth = []
i_step = 4;
for i in range (1,1700, i_step):
    image = cv2.imread('./highway/input/in%06d.jpg' %i)
    I_VIS.append(image) #array of images
    img.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
