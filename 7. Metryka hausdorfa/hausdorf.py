
import cv2
from math import sqrt, pow, inf
import numpy as np
import os
import matplotlib.pyplot as plt
import os.path

def findCor(contours):
    x_cor = contours[:,0,0]
    y_cor = contours[:,0,1]
    
    M = cv2.moments(contours)
    if(M['m00']!=0):
        x_c = int(M['m10']/M['m00'])
        y_c = int(M['m01']/M['m00'])
    else:
        x_c = 0;
        y_c = 0;    
    x_cor -= x_c
    y_cor -= y_c
    
    max_diff = 0
    for i in range(len(x_cor)):
        for j in range(len(x_cor)):
            diff = sqrt(pow(x_cor[i]-x_cor[j],2)+pow(y_cor[i]-y_cor[j],2))
            
            if diff > max_diff:
                max_diff = diff
                
    x_cor = np.divide(x_cor, max_diff)
    y_cor = np.divide(y_cor, max_diff)
    
    return x_cor, y_cor, x_c, y_c
    

def h_diff(x1,y1,x2,y2):
    h = 0
    
    for i in range(len(x1)):
        shortest = inf
        
        for j in range(len(x2)):
            diff = sqrt(pow(x1[i]-x2[j],2)+pow(y1[i]-y2[j],2))
            
            if diff < shortest:
                shortest = diff
        
        if shortest > h:
            h = shortest
            
    return h
       
def HausdorffDiff(x1,y1,x2,y2):
    return max(h_diff(x1,y1,x2,y2),h_diff(x2,y2,x1,y1))         

def ImageCords():
    imageCor = [];
    for imgFile in os.listdir('./hauss_imgs/imgs'):
        extension = os.path.splitext(imgFile)[1]
        if  extension != '.bmp':
            continue;
        I = cv2.imread('./hauss_imgs/imgs/'+imgFile)
        IG = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
        IGN = cv2.bitwise_not(IG)
        im2, contours, hierarchy = cv2.findContours(IGN,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
        x, y, x_c, y_c = findCor(contours[0])
        imageCor.append([imgFile.split('.')[0].split('_')[1],x,y])
    return imageCor

imageCor = ImageCords();

ImgOrg = cv2.imread('./hauss_imgs/Aegeansea.jpg')
IHSV = cv2.cvtColor(ImgOrg, cv2.COLOR_BGR2HSV)
# define range of blue color in HSV
lower = np.array([60,0,30])
upper = np.array([255,255,255])
mask = cv2.inRange(IHSV, lower, upper)
res = cv2.bitwise_and(IHSV,IHSV, mask= mask)
ret, thresh = cv2.threshold(res[:,:,2],50,255,0)
cv2.imshow('thresh image', thresh);
im2, contours, hierarchy = cv2.findContours(~thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
contours = list(filter(lambda el : el.shape[0]>15 and el.shape[0]<3000, contours))

#all_cord = []
#for i in range (0,len(contours)-1):
#    xBn, yBn, x_cBn, y_cBn = findCor(contours[i])
#    all_cord.append([xBn, yBn, x_cBn, y_cBn])

cv2.drawContours(ImgOrg,contours,-1,(255,255,0),3)
cv2.imshow("Contour1", ImgOrg)
cv2.waitKey(0)
cv2.destroyAllWindows();
for c in contours:
    xB, yB, x_c, y_c = findCor(c)

    similarities = []
    for imgCor in imageCor:
        
        h = HausdorffDiff(xB,yB,imgCor[1],imgCor[2])
        similarities.append([imgCor[0],h])

    similarities_arr = np.array(similarities)
    similarities_arr[np.argmin(similarities_arr[:,1])]
    cv2.putText(ImgOrg, str(np.argmin(similarities_arr[:,1])),(int(x_c),int(y_c)), cv2.FONT_HERSHEY_SIMPLEX, 1,(128,128,128))
    cv2.putText(ImgOrg, similarities_arr[np.argmin(similarities_arr[:,1])][0],(int(x_c),int(y_c)), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255))        
cv2.imshow("Contour", ImgOrg)
cv2.waitKey(0)
cv2.destroyAllWindows()
