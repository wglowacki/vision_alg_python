import cv2
import numpy as np
import matplotlib.pyplot as plt

wzor = cv2.imread('./obrazy_Mellin/wzor.pgm')
domek = cv2.imread('./obrazy_Mellin/domek_r0.pgm')

wzor = cv2.cvtColor(cv2.imread('./obrazy_Mellin/wzor.pgm'), cv2.COLOR_BGR2GRAY)
domek = cv2.cvtColor(cv2.imread('./obrazy_Mellin/domek_r0.pgm'), cv2.COLOR_BGR2GRAY)

wzor_ = np.zeros(domek.shape)

l = np.int((domek.shape[0]-wzor.shape[0])/2)
r = np.int((domek.shape[1]+wzor.shape[1])/2)
wzor_[l:r,l:r] = wzor

## obrazki gotowe do przetwarzania
wzor_p = np.fft.fftshift(wzor_)
domek_p = np.fft.fftshift(domek)

wzor_fft = np.fft.fft2(wzor_p)
domek_fft = np.fft.fft2(domek_p)

conj_wzor = np.conj(wzor_fft)

ccor = np.fft.ifft2((conj_wzor * domek_fft)/abs(conj_wzor * domek_fft))

ccor_shift = np.fft.ifftshift(ccor)

y,x = np.unravel_index( np.argmax(abs(ccor_shift)), abs(ccor_shift).shape)
 
dx = x - wzor_.shape[0]//2
dy = y - wzor_.shape[1]//2

macierz_translacji = np.float32([[1,0,dx],[0,1,dy]])
obraz_przesuniety = cv2.warpAffine(wzor_, macierz_translacji, (wzor_.shape[1], wzor_.shape[0]))

plt.figure(1)
plt.imshow(domek)
plt.plot(x,y,'ro')
plt.gray()

plt.figure(2)
plt.imshow(obraz_przesuniety)
plt.plot(x,y,'ro')
plt.gray()