import cv2
import numpy as np
import matplotlib.pyplot as plt
import math

def hanning2D(n):
    h = np.hanning(n)
    return np.sqrt(np.outer(h,h))

def highpassFilter(size):
    rows = np.cos(np.pi*np.matrix([-0.5 + x/(size[0]-1) for x in range(size[0])]))
    cols = np.cos(np.pi*np.matrix([-0.5 + x/(size[1]-1) for x in range(size[1])]))
    X = np.outer(rows,cols)
    return (1.0 - X) * (2.0 - X)

domek = cv2.cvtColor(cv2.imread('./obrazy_Mellin/domek_r30.pgm'), cv2.COLOR_BGR2GRAY)
wzor = cv2.cvtColor(cv2.imread('./obrazy_Mellin/domek_r0_64.pgm'), cv2.COLOR_BGR2GRAY)

# wzor w rozmiarze obrazka bez filtracji
wzor_NP = np.zeros(domek.shape, dtype=np.uint8) #  NP- non performance
# okno Hanninga dla wzoru
han = hanning2D(wzor.shape[0])

# centrowanie wzoru
wzor_ = np.zeros(domek.shape, dtype = np.uint8)
l = np.int((domek.shape[0]-wzor.shape[0])/2)
r = np.int((domek.shape[1]+wzor.shape[1])/2)
wzor_[l:r,l:r] = wzor * han
wzor_NP[l:r,l:r] = wzor 
# FFT na obrazkach
wzor_FFT = np.fft.fft2(wzor_)
domek_FFT = np.fft.fft2(domek)

# shift na obrazkach
wzor_SHIFT = np.fft.fftshift(wzor_FFT)
domek_SHIFT = np.fft.fftshift(domek_FFT)

# filtrowanie obrazków filterm górnoprzepustowym
wzor_F = wzor_SHIFT * highpassFilter(wzor_SHIFT.shape)
domek_F = domek_SHIFT * highpassFilter(domek_SHIFT.shape)

# parametry transformaty LogPolar
R = int(wzor_F.shape[0]//2)
M = 2*R/np.log(R)
# przygotowanie obrazków moduł liczb zespolonych
wzor_ABS = np.abs(wzor_F)
domek_ABS = np.abs(domek_F)
# transformata LogPolar
wzor_LP = cv2.logPolar(wzor_ABS, (wzor_F.shape[0]//2, wzor_F.shape[1]//2), M, cv2.INTER_LINEAR + cv2.WARP_FILL_OUTLIERS)
domek_LP = cv2.logPolar(domek_ABS, (domek_F.shape[0]//2, domek_F.shape[1]//2), M, cv2.INTER_LINEAR + cv2.WARP_FILL_OUTLIERS)

# ponowna transformata FFT
wzor_FFT2 = np.fft.fft2(wzor_LP)
domek_FFT2 = np.fft.fft2(domek_LP)

# korelacja ########################

ccor = np.conj(wzor_FFT2) * domek_FFT2
ccor = ccor/np.abs(ccor)
ccor = np.fft.ifftshift(ccor)
ccor = np.fft.ifft2(ccor)

wsp_kata, wsp_logr = np.unravel_index(np.argmax(abs(ccor)), ccor.shape)

# przeliczanie na skalowanie i stopnie
if wsp_logr > wzor_FFT2.shape[1]//2:
    wykl = wzor_FFT2.shape[1] - wsp_logr
else:
    wykl = - wsp_logr
A = (wsp_kata * 360.0)/wzor_FFT2.shape[1]
skala = np.exp(1/M) ** wykl
kat1 = 360 - A
kat2 = 360 - A - 180

# przeksztalcenie afiniczne
srodekTrans = [math.floor((domek.shape[0] + 1) / 2), math.floor((domek.shape[1] + 1 ) / 2)]
macierz_translacji1 = cv2.getRotationMatrix2D((srodekTrans[0], srodekTrans[1]), kat1, skala)
macierz_translacji2 = cv2.getRotationMatrix2D((srodekTrans[0], srodekTrans[1]), kat2, skala)

d1 = cv2.warpAffine(wzor_NP, macierz_translacji1, (wzor_NP.shape[1], wzor_NP.shape[0]))
d2 = cv2.warpAffine(wzor_NP, macierz_translacji2, (wzor_NP.shape[1], wzor_NP.shape[0]))

plt.figure(1)
plt.gray()
plt.imshow(wzor_NP)


d1fft = np.fft.fftshift(d1)
d2fft = np.fft.fftshift(d2)
d1fft = np.fft.fft2(d1fft)
d2fft = np.fft.fft2(d2fft)
d1fft = np.conj(d1fft)
d2fft = np.conj(d2fft)

korelacja1 = d1fft * domek_FFT
korelacja2 = d2fft * domek_FFT
korelacja1 = korelacja1/abs(korelacja1)
korelacja2 = korelacja2/abs(korelacja2)

korelacja1 = np.fft.ifftshift(korelacja1)
korelacja2 = np.fft.ifftshift(korelacja2)

korelacja1 = np.fft.ifft2(korelacja1)
korelacja2 = np.fft.ifft2(korelacja2)
korelacja1 = abs(korelacja1)
korelacja2 = abs(korelacja2)

y1, x1 = np.unravel_index( np.argmax(korelacja1), korelacja1.shape)
y2, x2 = np.unravel_index( np.argmax(korelacja2), korelacja2.shape)

if korelacja1[y1][x1] > korelacja2[y2][x2]:
    xk = x1
    yk = y1
    wzorzeck = d1
else:
    xk = x2
    yk = y2
    wzorzeck = d2
        
dx = xk - wzorzeck.shape[0]//2
dy = yk - wzorzeck.shape[1]//2
macierz_translacji = np.float32([[1,0,dx],[0,1,dy]]) 
obraz_przesuniety = cv2.warpAffine(wzorzeck, macierz_translacji, (wzorzeck.shape[1], wzorzeck.shape[0]))

plt.figure(1)
plt.imshow(obraz_przesuniety)
plt.figure(2)
plt.imshow(domek)
