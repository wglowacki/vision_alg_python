
import pickle
import numpy as np
from sklearn import svm


f = open('hog.p', 'rb')
HOG_data = pickle.load(f)
f.close()

[row, col] = HOG_data.shape
train_pos = HOG_data[1:60,:]
val_pos = HOG_data[60:80,:]
test_pos = HOG_data[80:100,:]

train_neg = HOG_data[100:160,:]
val_neg = HOG_data[160:180,:]
test_neg = HOG_data[180:200,:]

train = np.concatenate((train_pos,train_neg))
test = np.concatenate((test_pos,test_neg))
val = np.concatenate((val_pos,val_neg))

clf = svm.SVC(kernel='linear', C = 1.0)
data = train[:,1:3780]
labels = train [:,0]

clf.fit(data,labels)

datat = test[:,1:3780]
labelst = test [:,0]
lp = clf.predict(datat)


tp = 0
tn = 0 
fp = 0 
fn = 0

for j in range ( 0 , lp.shape[0]):
    if(labelst[j] == lp[j]):
        if(labelst[j]>0):
            tp = tp+1
        else:
            tn = tn + 1
    else:
        if(labelst[j]>0):
            fp = fp+1
        else:
            fn = fn+1
print('test:')
print('tp, tn, fp, fn')
print(tp,tn,fp,fn)


datav = val[:,1:3780]
labelsv = val [:,0]
lp2 = clf.predict(datav)


tp = 0
tn = 0 
fp = 0 
fn = 0

for j in range ( 0 , lp2.shape[0]):
    if(labelsv[j] == lp[j]):
        if(labelsv[j]>0):
            tp = tp+1
        else:
            tn = tn + 1
    else:
        if(labelsv[j]>0):
            fp = fp+1
        else:
            fn = fn+1
print('\nvalid data')
print('tp, tn, fp, fn')
print(tp,tn,fp,fn)