'''
Created on 10-Apr-2013

@author: Devangini
'''

import cv2.cv as cv
import cv2
import numpy as np
import math


# from camera.EyeBallExtractor2 import imageArray
isShowImages = True

def extractEyeBall(imgMatrix):
    # img = cv2.imread("E:\\python workspace\\Charlie\\eye1.jpg")

    print type(imgMatrix)
    imageArray = np.asarray(imgMatrix)

    # (rows, cols, channels) =  img.shape
    
    rows = imgMatrix.rows
    cols = imgMatrix.cols
    
#     print rows
#     print cols
    
    cv2.imshow("input", imageArray)
    
    originalImage = imgMatrix 
     
    # split them into channels
    b8u = cv.CreateMat(rows, cols, cv.CV_8UC1)  # cv.CloneMat(img)  
    g8u = cv.CreateMat(rows, cols, cv.CV_8UC1)  # cv.CloneMat(img)  
    r8u = cv.CreateMat(rows, cols, cv.CV_8UC1)  # cv.CloneMat(img)    
    cv.Split(originalImage, b8u, g8u, r8u, None);
    
    # invert colors
    for i in range(rows):
        for j in range(cols):
            r8u[i, j] = 255 - r8u[i, j];
            g8u[i, j] = 255 - g8u[i, j];
            b8u[i, j] = 255 - b8u[i, j];
            
    cv.Merge(b8u, g8u, r8u, None, originalImage)      
    if isShowImages:  
        cv.ShowImage("subtraction ", originalImage)

    # convert it to grey scale
    grayScaleImage = cv.CreateMat(rows, cols, cv.CV_8UC1)
    cv.CvtColor(originalImage, grayScaleImage, cv.CV_BGR2GRAY); 
    cv.ShowImage("grey ", grayScaleImage)
    
    greyArray = np.asarray(grayScaleImage, np.uint8, 1)
    # binaryImage = cv.CreateMat(rows, cols, cv.CV_8UC1)
    # #make it binary by making it threshold at 220
    ret, binaryImage = cv2.threshold(greyArray, 220, 255, cv2.THRESH_BINARY)
    
    print type(binaryImage)
    
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        # cv2.erode(binaryImage, element, binaryImage)
        # cv.Dilate(binaryImage, binaryImage)
    
    
    # cv.Erode(binaryImage, binaryImage)
    # cv.Dilate(binaryImage, binaryImage)
    
    # show the image
    cv2.imshow("binary image ", binaryImage)    
    
    
    params = cv2.SimpleBlobDetector_Params()
    #             params.minDistBetweenBlobs = 1.0  # minimum 10 pixels between blobs
    #             params.filterByArea = True        # filter my blobs by area of blob
    #             params.minArea = 5.0             # min 20 pixels squared
    #             params.maxArea = 500.0            # max 500 pixels squared
    params.minDistBetweenBlobs = 50.0
    params.filterByInertia = False
    params.filterByConvexity = False
    params.filterByColor = False
    params.filterByCircularity = False
    params.filterByArea = True
    params.minArea = 2.0
    params.maxArea = 500.0
        
    myBlobDetector = cv2.SimpleBlobDetector(params)
    keypoints = myBlobDetector.detect(binaryImage)
    print "blobs " + str(keypoints)
    
    # extract the x y coordinates of the keypoints: 
    
    for i in range(0, len(keypoints) - 1):
        print keypoints[i].pt
        pt1 = (int(keypoints[i].pt[0]), int(keypoints[i].pt[1]))
        pt2 = (int(keypoints[i + 1].pt[0]), int(keypoints[i + 1].pt[1]))
        cv2.line(imageArray, pt1, pt2, (255, 0, 0))
    #                 float X=keypoints[i].pt.x; 
    #                 float Y=keypoints[i].pt.y;
    
    cv2.imshow("eye ", imageArray)

 
