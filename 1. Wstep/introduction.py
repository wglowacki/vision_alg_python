# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle 
import numpy as np
import os, os.path
##TASK 1.
'''
image = cv2.imread('./mandril.jpg')
cv2.imshow('name', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("opencv_mandirl.png", image)

print(image.shape)  # rozmiary /wiersze, kolumny, glebia/
print(image.size)   # liczba bajtow
print(image.dtype)  # typ danych
'''
##TASK 2.
'''
I = plt.imread('mandril.jpg')
plt.figure(1)
plt.imshow(I)
plt.title('MyMandril')
plt.axis('off')
plt.show()

#plt.imasve('matplot_mandril.png', I)

x = [100, 150, 200, 250]
y = [50, 100, 150, 200]
plt.plot(x, y, 'r.', markersize=10) 

fig,ax = plt.subplots(1)
rect = Rectangle((50,50), 50, 100,fill=False, ec='r');
ax.add_patch(rect)
plt.show()
'''

##TASK 3.
'''
I = cv2.imread('./mandril.jpg')
IG = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
IHSV = cv2.cvtColor(I, cv2.COLOR_BGR2HSV)

IH = IHSV[:,:,0];
IS = IHSV[:,:,1];
IV = IHSV[:,:,2];

cv2.imshow('I', I)
cv2.imshow('IG', IG)
cv2.imshow('IH', IH)
cv2.imshow('IS', IS)
cv2.imshow('IV', IV)

I = plt.imread('mandril.jpg')
def rgb2gray(I):
    return 0.299*I[:,:,0] + 0.587*I[:,:,1] + 0.114*I[:,:,2]
I_HSV = plt.colors.rgb_to_hsv(I)
plt.figure(1)
plt.gray()
plt.imshow(I[:,:,0])
'''
##TASK 4.
'''
I = plt.imread('mandril.jpg')
height, width = I.shape[:2] #pobieranie 1 i 2 elementu: wysokości i szerokosci
scale = 1.75
Ix2 = cv2.resize(I,(int(scale*height),int(scale*width)))
cv2.imshow("BigMandril",Ix2)

I_2 = scipy.misc.imreasize(I, 0.5)
'''

##TASK 5.
'''
lena = cv2.imread('lena.png')
mand = cv2.imread('mandril.jpg')
gray_mand = cv2.cvtColor(mand, cv2.COLOR_BGR2GRAY)
gray_lena = cv2.cvtColor(lena, cv2.COLOR_BGR2GRAY)

len_and_mand = gray_mand + gray_lena
cv2.imshow('+', len_and_mand)

len_minus_mand = gray_lena - gray_mand
len_mult_mand = gray_lena * gray_mand
linear = 0.2 * len_and_mand
cv2.imshow('+', len_and_mand)
cv2.imshow('-', len_minus_mand)
cv2.imshow('*', np.uint8(len_mult_mand))
cv2.imshow("linear",np.uint8(linear))

abs_diff = cv2.absdiff(gray_lena, gray_mand)
cv2.imshow('abs_diff', abs_diff)
cv2.waitKey(0)
'''
##TASK 6.
'''
lena = cv2.imread('lena.png')
mand = cv2.imread('mandril.jpg')
gray_mand = cv2.cvtColor(mand, cv2.COLOR_BGR2GRAY)
gray_lena = cv2.cvtColor(lena, cv2.COLOR_BGR2GRAY)
a = gray_lena[115,15];

def hist(image):
    h=np.zeros((256, 1), np.int32) #jednokolumnowa tablica zer
    height, width = image.shape[:2]
    for y in range (height):
        for x in range (width):
            h[image[y,x]]+=1
    return h;
f_hist = hist(gray_lena)
#plt.plot(f_hist)

hist_lena = cv2.calcHist([gray_lena], [0], None, [256], [0,256])
#plt.plot(hist_lena)

plt.subplot(221), plt.imshow(lena, 'gray')
plt.subplot(222), plt.imshow(gray_lena, 'gray')
plt.subplot(223), plt.plot(f_hist)
plt.subplot(224), plt.plot(hist_lena)

eq_hist=cv2.equalizeHist(gray_lena)
plt.plot(eq_hist)


clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
# clipLimit - maksymalna wysokosc slupka histogramu - wartosci powyzej
# rozdzielana sa pomiedzy sasiadow
# tileGridSize - rozmiar pojedycznczego bloku obrazu (metoda lokalna, dziala
# 1na rozdzielnych blokach obrazu)
I_CLAHE = clahe.apply(gray_lena)
three_images = np.hstack((gray_lena,eq_hist, I_CLAHE)) #stacking images side-by-side
cv2.imshow('Compared images', three_images)
cv2.waitKey(0)
'''

###TASK 7.

lena = cv2.imread('lena.png')
mand = cv2.imread('mandril.jpg')
gray_mand = cv2.cvtColor(mand, cv2.COLOR_BGR2GRAY)
gray_lena = cv2.cvtColor(lena, cv2.COLOR_BGR2GRAY)
a = gray_lena[115,15];
blur = cv2.GaussianBlur(gray_lena,(5,5),0)
gaussian = np.hstack((gray_lena,blur )) #stacking images side-by-side
median_fil3 = cv2.medianBlur(gray_lena, 3)
median_fil5 = cv2.medianBlur(gray_lena, 5)
median = np.hstack((gray_lena,median_fil3, median_fil5 )) #stacking images side-by-side
sobel_x = cv2.Sobel(gray_lena,cv2.CV_64F,1,0, ksize=3)
sobel_y = cv2.Sobel(gray_lena,cv2.CV_64F,0,1, ksize=3)
sobels = np.hstack((sobel_x, sobel_y))
laplacian = cv2.Laplacian(gray_lena, cv2.CV_64F)
gaussian = np.hstack((gray_lena,blur )) #stacking images side-by-side

bila = cv2.bilateralFilter(gray_lena, 15, 80, 70 )
cv2.imshow('Bilateral filter', bila)
cv2.imshow('Gaussian blur', gaussian)
cv2.imshow('Median blur', median)
cv2.imshow('Sobels x and y', sobels)
cv2.imshow('Laplacian', laplacian)
cv2.waitKey(0)

###TASK 8.
#Wczytywanie sekwencji wideo, odejmowanie ramek, indeksacja
'''
image_dir = "img_seq/"
image_path_list = []
image_extensions = [".jpg"]
image_extensions = [item.lower() for item in image_extensions]
#create a list all files in directory and
#append files with a vaild extention to image_path_list
for file in os.listdir(image_dir):
    extension = os.path.splitext(file)[1]
    if extension.lower() not in image_extensions:
        continue
    image_path_list.append(os.path.join(image_dir, file))
 
#loop through image_path_list to open each image
image_array = []
I_VIS = []
for image_path in image_path_list:
    image = cv2.imread(image_path)
    
    # display the image on screen with imshow()
    # after checking that it loaded
    if image is not None:
       # cv2.imshow(image_path, image)
        I_VIS.append(image)
        image_array.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)) #array of gray images
    elif image is None:
        print ("Error loading: " + image_path)
        #end this loop iteration and move on to next image
        continue
   # key = cv2.waitKey(10)
cv2.destroyAllWindows()

#Odejmowanie ramek i binaryzacja
kernel1 = np.ones((3,3), np.uint8)
kernel2 = np.ones((3,3), np.uint8)
for i in range(1,len(image_array)):
    diff_image = cv2.absdiff(image_array[i], image_array[i-1])
    binary_diff = cv2.threshold(diff_image,22,140,cv2.THRESH_BINARY)
# D - obraz
# 10 - prog
# 255 - co ma byc przypisane na wyjscie jako wartosc maksymalna
# cv2.THRESH_BINARY - typ binaryzacji (tu najprostsza - za obiekty piksele powyzej progu)
    binary_diff = binary_diff[1]
    img_erosion = cv2.erode(binary_diff, kernel1, iterations=1)
    img_dilation = cv2.dilate(img_erosion, kernel2, iterations=1)
    median_blur = cv2.medianBlur(img_dilation, 3)
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

cv2.waitKey(0)
cv2.destroyAllWindows()
'''