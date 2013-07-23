'''
Created on 13-Jul-2013

@author: Devangini
'''

import cv2
import numpy as np

vis = cv2.imread("E://python workspace//CharlieCode//faceimage.png")

track_box = ((128.5, 163.0), (202.69900512695312, 276.8576354980469), 154.49142456054688)

center = (int(track_box[0][0]), int(track_box[0][1]))

rotateAngle = 180 + track_box[2]


cv2.circle(vis, center, 2, (255, 0, 0))

rotationMatrix = cv2.getRotationMatrix2D(center, rotateAngle , 1)
shape = np.shape(vis)
print shape[0 : 2]
faceArray = np.zeros( shape[0:2], np.uint8, 3)
faceArray2 = np.zeros((track_box[1][0], track_box[1][1]), np.uint8, 3)
faceArray = cv2.warpAffine(vis, rotationMatrix, np.shape(faceArray), flags=cv2.INTER_LINEAR)
faceArray2 = cv2.getRectSubPix(faceArray, np.shape(faceArray2), track_box[0])
#             cv.GetRectSubPix(originalArray2, faceMatrix, track_box[0])

cv2.imshow("face image", vis)

cv2.imshow("face image 2", faceArray)

cv2.imshow("face image 3", faceArray2)



cv2.waitKey(0)