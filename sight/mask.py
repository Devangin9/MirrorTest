'''
Created on 20-Jul-2013

@author: Devangini
'''
import cv2
import numpy as np

img = cv2.imread('E:\\python workspace\\CharlieCode\\lena.png')
cv2.imshow("image " , img)
# mask = cv2.imread('E:\\python workspace\\CharlieCode\\border.png')
print np.shape(img)
(w, h, channel) = np.shape(img)
# mask = cv2.imread('border.png',0)
mask = np.zeros((w, h), np.uint8, 1)
print np.shape(mask)
mask[10: 100, 10:100] = 1
res = cv2.bitwise_and(img,img,mask = mask)

cv2.imshow("image ", res)

cv2.waitKey(0)