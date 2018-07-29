# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
import numpy as np

I = cv2.imread('./I.jpg')
J = cv2.imread('./J.jpg')
IG = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
JG = cv2.cvtColor(J, cv2.COLOR_BGR2GRAY)
im_diff = cv2.absdiff(IG,JG)

#fragmenty obrazu 3x3
w2 = 1
dx = 1
dy = dx
(rows, cols) = IG.shape
 
def of(IG, JG, u0, v0, w2=1, dy=1, dx=1):
    u = np.zeros((rows,cols), dtype=np.float64)
    v = np.zeros((rows,cols), dtype=np.float64)
    for j in range(dx+w2, rows-w2-dx):
        for i in range(dy+w2, cols-w2-dy):
            IO = np.float32(I[j-w2:j+w2+1,i-w2:i+w2+1]);
            dd = np.ones((2*dx+1, 2*dy+1),dtype=np.float64)
            dd = dd*np.inf
            for m in range(-dx,dx+1):
                for n in range(-dy,dy+1):
                    un = np.int(u0[j,i])
                    vn = np.int(v0[j,i])
                    JO = np.float32(J[j+m-w2+un:j+m+w2+1+un, i+n-w2+vn:i+n+w2+1+vn]);
                    dd[m+dx][n+dy] = np.sum((np.square(IO-JO)))
            ind = np.unravel_index(np.argmin(dd, axis=None), dd.shape)
            u[j+np.int(u0[j,i]),i+np.int(v0[j,i])] = ind[0]
            v[j+np.int(u0[j,i]),i+np.int(v0[j,i])] = ind[1]
    return u, v

def pyramid(im, max_scale):
    images=[im];
    for k in range(1, max_scale):
        images.append(cv2.resize(images[k-1], (0,0), fx=0.5, fy=0.5))#, interpolation=cv2.INTER_NEAREST))
    return images

IP = pyramid(IG, 3)
JP = pyramid(JG, 3)
u0 = np.zeros(IP[-1].shape, np.float32)
v0 = np.zeros(JP[-1].shape, np.float32)

u_f,v_f = of(IG,JG, u0,v0,w2=1,dx=1,dy=1)
for i in range (1,3):
    u_f = cv2.resize(u_f,(0,0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST);
    v_f = cv2.resize(v_f,(0,0), fx=2, fy=2, interpolation=cv2.INTER_NEAREST);
    u_f,v_f = of(IP[3-i],JP[3-i], u_f,v_f,w2=1,dx=1,dy=1)\

#u0 = np.zeros((rows,cols), dtype=np.float64)
#v0 = np.zeros((rows,cols), dtype=np.float64)
#u,v = of(I, J, u0, v0, w2=1, dy=1, dx=1)  
plt.figure(1)
plt.gray()
plt.imshow(im_diff)
plt.hold(True)
plt.quiver(u_f,v_f,scale = 0.5, scale_units='dots')
plt.hold(False)
plt.show();