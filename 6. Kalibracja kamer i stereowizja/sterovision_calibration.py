import cv2
import numpy as np
#  kryternia przetwania obliczen (blad+liczba iteracji)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# przygotowanie punktow 2D w postaci: (0,0,0), (1,0,0), (2,0,0) ....,(6,7,0)
objp = np.zeros((6 * 7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
# tablice do przechowywania punktow obiektow (3D) i punktow na obrazie (2D)
objpoints = [] # punkty 3d w przestrzeni (rzeczywsite)
imgpoints_R = [] # punkty 2d w plaszczyznie obrazu.
imgpoints_L = [];

for fname in range (1,13):
    # wczytanie obrazu
    img_L = cv2.imread('images_left/left%02d.jpg' %fname)
    img_R = cv2.imread('images_right/right%02d.jpg' %fname)
    # konwersja do odcieni szarosci
    gray_L = cv2.cvtColor(img_L, cv2.COLOR_BGR2GRAY)
    gray_R = cv2.cvtColor(img_R, cv2.COLOR_BGR2GRAY)
    # wyszukiwanie naroznikow na planszy
    ret_L, corners_L = cv2.findChessboardCorners(gray_L, (7,6), None)
    ret_R, corners_R = cv2.findChessboardCorners(gray_R, (7,6), None)
    # jesli znaleniono na obrazie punkty
    if ret_L == True and ret_R == True:
        #dolaczenie wspolrzednych 3D
        objpoints.append(objp)
        # poprawa lokalizacji punktow (podpiskelowo)
        corners2_L = cv2.cornerSubPix(gray_L,corners_L, (11,11), (-1,-1), criteria)
        corners2_R = cv2.cornerSubPix(gray_R,corners_R, (11,11), (-1,-1), criteria)
        # dolaczenie poprawionych punktow
        imgpoints_L.append(corners2_L)
        imgpoints_R.append(corners2_R)
        # wizualizacja wykrytych naroznikow
        cv2.drawChessboardCorners(img_L, (7,6), corners2_L, ret_L)
        cv2.drawChessboardCorners(img_R, (7,6), corners2_R, ret_R)
        cv2.imshow("Corners right camera",img_R);
        cv2.imshow("Corners left camera",img_L);
        cv2.waitKey(0)
            
[retl, mtxl, distl, rvecsl, tvecsl] = cv2.calibrateCamera(objpoints, imgpoints_L, gray_L.shape[::-1], None, None)
[retr, mtxr, distr, rvecsr, tvecrs] = cv2.calibrateCamera(objpoints, imgpoints_R, gray_R.shape[::-1], None, None)
hl, wl = img_L.shape[:2]
hr, wr = img_R.shape[:2]
alfa = 1; #all pixels are correct
newcameramtxl, roil = cv2.getOptimalNewCameraMatrix(mtxl, distl, (wl,hl), alfa, (wl,hl))
newcameramtxr, roir = cv2.getOptimalNewCameraMatrix(mtxr, distr, (wr,hr), alfa, (wr,hr))
#dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
mapxl, mapyl = cv2.initUndistortRectifyMap(mtxl, distr, None, newcameramtxl,(wr,hr), 5)
mapxr, mapyr = cv2.initUndistortRectifyMap(mtxl, distr, None, newcameramtxl,(wl,hl), 5)
dstl = cv2.remap(img_L, mapxl, mapyl, cv2.INTER_LINEAR)
dstr = cv2.remap(img_R, mapxr, mapyr, cv2.INTER_LINEAR)
xl, yl, wl, hl = roil
xr, yr, wr, hr = roir
dstl = dstl[yl:yr+hl, xl:xl+wl]
dstr = dstr[yr:yr+hl, xr:xr+wr]
cv2.imshow('left calibrated', dstl);
cv2.waitKey(0)
cv2.imwrite('calibresultl.png', dstl);
cv2.imshow('right calibrated', dstr);
cv2.waitKey(0)
cv2.imwrite('calibresultr.png', dstr);

retval, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objpoints,imgpoints_L,imgpoints_R,mtxl,distl, mtxr,distr,gray_L.shape[::-1])
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, gray_L.shape[::-1], R, T)
map1_L, map2_L = cv2.initUndistortRectifyMap(cameraMatrix1, distCoeffs1, R1, P1, gray_L.shape[::-1], cv2.CV_16SC2)
map1_R, map2_R = cv2.initUndistortRectifyMap(cameraMatrix2, distCoeffs2, R2, P2, gray_R.shape[::-1], cv2.CV_16SC2)
dst_L = cv2.remap(img_L, map1_L, map2_L, cv2.INTER_LINEAR)
dst_R = cv2.remap(img_R, map1_R, map2_R, cv2.INTER_LINEAR)

N, XX, YY = dst_L.shape[::-1] # pobranie rozmiarow obrazka (kolorowego)
visRectify = np.zeros((YY,XX*2,N),np.uint8) # utworzenie nowego obrazka o szerokosci x2
visRectify[:,0:640:,:] = dst_L      # przypisanie obrazka lewego
visRectify[:,640:1280:,:] = dst_R   # przypisanie obrazka prawego
# Wyrysowanie poziomych linii
for y in range (0,480,10):
    cv2.line(visRectify, (0,y), (1280,y), (255,0,0))
    cv2.imshow('visRectify',visRectify)  #wizualizacja
cv2.waitKey(0)