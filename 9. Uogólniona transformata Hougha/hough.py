import cv2
import numpy as np
import math
import matplotlib.pyplot as plt

    
I = cv2.imread('obrazy_hough/trybik.jpg')
I = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
ret, I_bin = cv2.threshold(I,127,255,cv2.THRESH_BINARY)
I_bin = ~I_bin

kernel = np.ones((3,3),np.uint8)
I_bin = cv2.morphologyEx(I_bin, cv2.MORPH_OPEN, kernel)
I_bin = cv2.morphologyEx(I_bin, cv2.MORPH_CLOSE, kernel)

bin, contours, hierarchy = cv2.findContours(I_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

sobelx = cv2.Sobel(I,cv2.CV_64F,1,0,ksize=5)    
sobely = cv2.Sobel(I,cv2.CV_64F,0,1,ksize=5)

gradient = np.sqrt(np.square(sobelx)+np.square(sobely)) 
gradient = np.divide(gradient, np.amax(gradient))

orientation = np.arctan2(sobely,sobelx)   

M = cv2.moments(contours[0], 1)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
#
#cv2.imshow('I',I_bin)    

Rtable =  [[] for i in range(360)]

for c in contours:
    for i in range(len(c)):
        x = c[i,0,0]
        y = c[i,0,1]
        length = np.sqrt(np.square(cx-x)+np.square(cy-y)) 
        angle = np.arctan2(cy-y,cx-x)
        orient = math.floor(orientation[x,y] *180 / np.pi)
        Rtable[orient].append((length, angle))
        
I_2 = cv2.imread('obrazy_hough/trybiki2.jpg')
I_2g = cv2.cvtColor(I_2, cv2.COLOR_BGR2GRAY)

sobelx_2 = cv2.Sobel(I_2g,cv2.CV_64F,1,0,ksize=5)    
sobely_2 = cv2.Sobel(I_2g,cv2.CV_64F,0,1,ksize=5)
        
gradient_2 = np.sqrt(np.square(sobelx_2)+np.square(sobely_2)) 
gradient_2 = np.divide(gradient_2, np.amax(gradient_2))

Hough = np.zeros((700,700))

for idx, row in enumerate(gradient_2):
    print(idx)
    for idy, item in enumerate(row):
        if(item>0.5):
            for idk, row_in in enumerate(Rtable):
                for idl, item_in in enumerate(row_in):
                    r = item_in[0]
                    fi = item_in[1]
                    x1 = math.floor(r*np.cos(fi) + idx)
                    y1 = math.floor(r*np.sin(fi) + idy)
                    Hough[x1,y1] = Hough[x1,y1] + 1 
 
mx = np.unravel_index(Hough.argmax(), Hough.shape)

plt.figure()
plt.imshow(I_2)                    
plt.plot([mx[1]], [mx[0]],'*', color='r')
                 
            
            
            
        
    
        
        
        
        
        