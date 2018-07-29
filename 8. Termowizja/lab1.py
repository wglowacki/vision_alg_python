import cv2
import numpy as np

cap = cv2.VideoCapture('vid1_IR.avi')
kernel=np.ones([3,3], np.uint8)

while(cap.isOpened()):
    ret, frame = cap.read()
    G = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(G,50,255,cv2.THRESH_BINARY)
    opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
    dilation = cv2.dilate(thresh1,kernel,iterations = 1)
    cv2.imshow('Opening',opening)
    cv2.imshow('Erode',dilation)
    connectivity=4
    output = cv2.connectedComponentsWithStats(dilation, connectivity, cv2.CV_32S)
    for i in range(output[0]):
        if output[2][i][4]>2000 and output[2][i][3] > output[2][i][2]:
            cv2.rectangle(G,(output[2][i][0], output[2][i][1]),(output[2][i][0]+output[2][i][2], output[2][i][1]+output[2][i][3]),(160,190,12))
            #roi = gray[y1:y2, x1:x2]
            #cv2.imwrite('sample_%06d.png' % iPedestrian,ROI)
    cv2.imshow('Indeksacja',G)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 