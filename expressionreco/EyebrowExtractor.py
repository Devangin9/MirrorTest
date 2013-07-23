'''
Created on 11-Apr-2013

@author: Devangini
'''

import cv2.cv as cv
import cv2
import numpy as np


hsv_map = np.zeros((180, 256, 3), np.uint8)
h, s = np.indices(hsv_map.shape[:2])
hsv_map[:,:,0] = h
hsv_map[:,:,1] = s
hsv_map[:,:,2] = 255
hsv_map = cv2.cvtColor(hsv_map, cv2.COLOR_HSV2BGR)

hist_scale = 10

def extractEyeBrows(originalImage, pt1, centerX, centerY, eyeBallParams):
    
    (eyeBallCenterX, eyeBallCenterY, eyeBallRadius) = eyeBallParams
                # find good features
#                 eig_image = cv.CreateMat(gray_im.rows, gray_im.cols, cv.CV_32FC1)
#                 temp_image = cv.CreateMat(gray_im.rows, gray_im.cols, cv.CV_32FC1)
#                 for (x,y) in cv.GoodFeaturesToTrack(gray_im, eig_image, temp_image, 10, 0.04, 1.0, useHarris = True):
#                     print "good feature at", x,y
#                     cv.Rectangle(img, (int(x), int(y)),(int(x) + 20, int(y) + 20), cv.RGB(255, 255, 255))
                        
                
                    
    #find color of the skin
    #prepare histogram
    

    eyebrow_Area = cv.GetSubRect(originalImage, (int(pt1[0] * 1.1), int(pt1[1] * 1.2), centerX - pt1[0], int((centerY - pt1[1])*0.6)))
    eyebrow_Area2 = cv.CloneMat(eyebrow_Area)
    cv.Smooth( eyebrow_Area2, eyebrow_Area2, cv.CV_GAUSSIAN, 9 ,1 )

    hsv_image = cv.CreateMat(eyebrow_Area.height, eyebrow_Area.width, cv.CV_8UC3)
    imageArray = np.asarray(eyebrow_Area2, dtype=np.uint8)
    
    
    
    hsv_image  = cv2.cvtColor(imageArray, cv2.COLOR_BGR2HSV)
   
    
#                 histogram2 = hs_histogram(leftEyeArea)
#                 print(histogram2)
#                 imageArray2 = np.asarray(histogram2, dtype=np.uint8)
#                 cv2.imshow("histo " , histogram2)
    
#                 
    #dark = imageArray[...,2] < 32
    #set not frequent to dark
    #imageArray[dark] = 0
    #histogram = cv.CreateHist(2, cv.CV_HIST_ARRAY)
    histogram = cv2.calcHist( [hsv_image], [0, 1], None, [180, 256], [0, 180, 0, 256] )
      
    h1 = np.clip(histogram*0.005*hist_scale, 0, 1)
    vis = hsv_map*h1[:,:,np.newaxis] / 255.0
    #print type(vis)
    #cv2.imshow('hist', vis)
    
    
         
    #backproj = None
    #cv.CalcBackProject(hsv_image, backproj, histogram)
    ranges = [0, 180, 0, 256]
    
    backproj = cv2.calcBackProject([hsv_image], [0, 1], histogram, ranges, 10)
   
     
    cv2.imshow("back proj ", backproj)
                