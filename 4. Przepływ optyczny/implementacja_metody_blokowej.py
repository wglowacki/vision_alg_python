# -*- coding: utf-8 -*-

import cv2
import matplotlib.pyplot as plt
import numpy as np

I = cv2.imread('./I.jpg');
J = cv2.imread('./J.jpg');
IG = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY);
JG = cv2.cvtColor(J, cv2.COLOR_BGR2GRAY);

im_diff = cv2.absdiff(IG,JG);

#fragmenty obrazu 3x3
w2 = 1;
dx = dy = 1;
(rows, cols) = IG.shape;

u = np.zeros((rows,cols), dtype=np.float64)
v = np.zeros((rows,cols), dtype=np.float64)
        
for j in range(dx+w2, rows-w2-dx):
    for i in range(dy+w2, cols-w2-dy):
        roi_I = np.float32(I[j-w2:j+w2+1,i-w2:i+w2+1]);
        dd = np.ones((2*dx+1, 2*dy+1),dtype=np.float64)
        dd = dd*np.inf
        for m in range(-dx,dx+1):
            for n in range(-dy,dy+1):
                roi_J = np.float32(J[j+m-w2:j+m+w2+dx, i+n-w2:i+n+w2+dy]);
                dd[m+dx][n+dy] = np.sum((np.square(roi_I-roi_J)))
        ind = np.unravel_index(np.argmin(dd, axis=None), dd.shape)
        u[j,i] = ind[0]
        v[j,i] = ind[1]
        
plt.figure(1)
plt.gray()
plt.imshow(im_diff)
plt.hold(True)
plt.quiver(u,v,scale = 0.5, scale_units='dots')
plt.hold(False)
plt.show();