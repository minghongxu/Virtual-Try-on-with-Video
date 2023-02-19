import cv2
import numpy as np
import os

#path = './data/train/cloth'
#path_save = './data/train/cloth-mask'
path = './data/test/cloth'
path_save = './data/test/cloth-mask'

for i in os.listdir(path):
    file_name,extension= os.path.splitext(i)


    image1 =cv2.imread(os.path.join(path,i))

    img1 =cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)

    ret, thresh2 = cv2.threshold(img1, 240, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow('Binary Threshold Inverted', thresh2)


    cv2.imwrite(os.path.join(path_save,i),cv2.resize(thresh2,(192,256)))
