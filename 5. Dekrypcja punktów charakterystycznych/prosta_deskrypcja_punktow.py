import cv2
import matplotlib.pyplot as plt
import math
import pm
import numpy as np

def Harris(gray_img, sobel_mask=2, gaussian_mask=2, k=0.05):

    sobel_x = cv2.Sobel(gray_img, cv2.CV_32F, 1,0, ksize=sobel_mask);
    sobel_y = cv2.Sobel(gray_img, cv2.CV_32F, 0,1, ksize=sobel_mask);
    sobel_x2 = sobel_x**2;
    sobel_x2 = cv2.GaussianBlur(sobel_x2, (gaussian_mask,gaussian_mask),0);
    sobel_y2 = sobel_y**2;
    sobel_y2 = cv2.GaussianBlur(sobel_y2, (gaussian_mask,gaussian_mask),0);
    sobel_xy = sobel_x * sobel_y;
    sobel_xy = cv2.GaussianBlur(sobel_xy, (gaussian_mask,gaussian_mask),0);
    
    det_m = sobel_x2*sobel_y2 - sobel_xy*sobel_xy;
    trace_m = sobel_x2 + sobel_y2;
    
    re_img = det_m - k*trace_m*trace_m;
    return re_img;
    
def LocalMaximum(img, mask=5, thresh=0.5):
    result = [];
    half = mask//2;
    thresh = thresh * np.max(img)
    for i in range(half, img.shape[0]-half+1):
        for j in range(half, img.shape[1]-half+1):
            roi = img[i-half:i+half+1,j-half:j+half+1];
            if (np.max(roi) == img[i, j]):
                if (img[i][j] > thresh):
                    result.append([i,j])
    return result

def CharPointsDescription(H, points, roi_size=15):
    rows, cols = H.shape;
    half = roi_size//2
    cp = list(filter(lambda p: p[0]>=half and p[0]<rows-half-1 and p[1]>=half and p[1]<cols-half-1, points))
    roi= [];
    for i in cp:
        new_roi = H[i[0]-half:i[0]+half+1, i[1]-half:i[1]+half+1]
        new_roi = new_roi.flatten();
        roi.append(new_roi);
    wy = list(zip(roi,cp))
    return wy

def CompDesc(desc1, desc2, N=20):
    dif = [];
    for e1 in range (0,len(desc1)):
        for e2 in range(0, len(desc2)):
            dif.append([ np.sum(cv2.absdiff(desc1[e1][0],desc2[e2][0])) , [ desc1[e1][1] , desc2[e2][1] ] ])
    dif.sort(key=lambda x: x[0])
    return dif[0:N]
#    list_n = [];
#    result = [];
#    for i in desc1:
#        min_dist = math.inf;
#        minimum = 0;
#        for j in desc2:
#            dist = sum(cv2.absdiff(i[0],j[0]));
#            if dist < min_dist:
#                min_dist = dist;
#                minimum = j[1];            
#                list_n.append((i[1], minimum, min_dist));
#    list_n.sort(key=lambda tup: tup[2], reverse=True)
#    list_n = list_n[0:N-1]
#    for i in list_n:
#        result.append((i[0],i[1]))
#    return result

b1 = cv2.imread('harris_files/budynek1.jpg')
b2 = cv2.imread('harris_files/budynek2.jpg')
f1 = cv2.imread('harris_files/fontanna1.jpg')
f2 = cv2.imread('harris_files/fontanna2.jpg')
#
f1g = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
f2g = cv2.cvtColor(f2, cv2.COLOR_BGR2GRAY)
points_1 = LocalMaximum(Harris(f1g,7,7, 0.05), mask=5, thresh=0.2)
points_2 = LocalMaximum(Harris(f2g,7,7, 0.05), mask=5, thresh=0.2)
filt_font1 = CharPointsDescription(f1g, points_1, 20)
filt_font2 = CharPointsDescription(f2g, points_2, 20)
best_fit_found = CompDesc(filt_font1, filt_font2, 20)
points=[]
for i in range(0,20):
    points.append(best_fit_found[i][1])

plt.figure();
plt.gray();
pm.plot_matches(f1g, f2g, points)

b1g = cv2.cvtColor(b1, cv2.COLOR_BGR2GRAY)
b2g = cv2.cvtColor(b2, cv2.COLOR_BGR2GRAY)
pb1 = LocalMaximum(Harris(b1g,7,7, 0.05), mask=5, thresh=0.1)
pb2 = LocalMaximum(Harris(b2g,7,7 , 0.05), mask=5, thresh=0.1)
#
ffb1 = CharPointsDescription(b1g, pb1, 15)
ffb2 = CharPointsDescription(b2g, pb2, 15)
best_fit_build = CompDesc(ffb1, ffb2, 20)
pointsb=[]
for i in range(0,20):
    pointsb.append(best_fit_build[i][1])
plt.figure(); plt.gray();
pm.plot_matches(b1g, b2g, pointsb)


e1 = cv2.imread('eiffel1.jpg')
e2 = cv2.imread('eiffel2.jpg')
e1g = cv2.cvtColor(e1, cv2.COLOR_BGR2GRAY)
e2g = cv2.cvtColor(e2, cv2.COLOR_BGR2GRAY)
pe1 = LocalMaximum(Harris(e2g,3,3, 0.05), mask=5, thresh=0.1)
pe2 = LocalMaximum(Harris(e2g,3,3, 0.05), mask=5, thresh=0.1)

ffe1 = CharPointsDescription(e1g, pe1, 15)
ffe2 = CharPointsDescription(e2g, pe2, 15)
best_fit_eif = CompDesc(ffe1, ffe2, 20)
pointse=[]
for i in range(0,20):
    pointse.append(best_fit_eif[i][1])
pm.plot_matches(e2g, e2g, pointse)
#plt.figure(1)
#plt.subplot(1,2,1), plt.imshow(budynek1), plt.hold(True), plt.plot(c_b1,r_b1,'r.'), plt.title('Budynek 1'), plt.show();
#plt.subplot(1,2,2), plt.imshow(budynek2), plt.hold(True), plt.plot(c_b2,r_b2,'r.'), plt.title('Budynek 2'), plt.show();
#plt.figure(2)
#plt.subplot(1,2,1), plt.imshow(fontanna1), plt.hold(True), plt.plot(c_f1,r_f1,'r.'), plt.title('Fontanna 1'), plt.show();
#plt.subplot(1,2,2), plt.imshow(fontanna2), plt.hold(True), plt.plot(c_f2,r_f2,'r.'), plt.title('Fontanna 2'), plt.show();