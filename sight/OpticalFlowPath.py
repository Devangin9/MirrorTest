'''
Created on 21-Jul-2013

@author: Devangini
'''
import cv2
import cv2.cv as cv
import math
from scipy.weave.accelerate_tools import Vector
import numpy as np

class OpticalFlowPath:
    
    def __init__(self):
        self.startIndex = 3
        self.endIndex = 10
        
        self.thresholdValue = 5
        self.rho = 1
        self.theta = 180
        self.minLineLength = 2
        self.maxLineGap = 10
        
#         self.thresholdValue = 30
#         self.rho = 1
#         self.theta = 180
#         self.minLineLength = 1
#         self.maxLineGap = 10
        self.image1 = None
      
      
    def changeThreshold(self, thresholdValue):
        self.thresholdValue = thresholdValue
        print "input " + str(thresholdValue)
        self.findLines()
        
    def changeRho(self, rho):
        self.rho = rho
        self.findLines()
    
    def changeTheta(self, theta):
        self.theta = theta
        print "input " + str(theta)
        self.findLines()
    
    def changeMinLineLength(self, minLineLength):
        self.minLineLength = minLineLength
        self.findLines()
    
    def changeMaxLineGap(self, maxLineGap):
        self.maxLineGap = maxLineGap
        self.findLines()
        
    def findLines(self):
        print "params" , self.rho, self.theta, self.thresholdValue, self.minLineLength  , self.maxLineGap
        (w, h, c) = np.shape(self.image1)
        newImage = np.zeros((w, h, 3), np.uint8)
        
        # convert to grey scale
        grayImage = cv2.cvtColor(self.image1, cv.CV_BGR2GRAY)
    
        lines = cv2.HoughLinesP(grayImage, rho=self.rho, theta=np.pi / self.theta, threshold=self.thresholdValue, minLineLength=self.minLineLength  , maxLineGap=self.maxLineGap)
        
#         lines = cv2.HoughLinesP(grayImage, rho=1, theta=np.pi/90, threshold=40, minLineLength=20  , maxLineGap=30)
        
        print lines
        
        if lines != None:
            print np.shape(lines[0])
            
            for x1, y1, x2, y2 in lines[0]:
                cv2.line(newImage, (x1, y1), (x2, y2), (0, 255, 255), 1)
            
        cv2.imshow("lines", newImage)
        
    def findPath(self, image):
        
        self.image1 = image
        
#         cv2.imshow("image 1", self.image1)
#         
#         # Creating trackbar for kernel size
#         cv2.createTrackbar('threshold', 'image 1', 1, 100, self.changeThreshold)
#         cv2.createTrackbar('rho', 'image 1', 1, 100, self.changeRho)
#         cv2.createTrackbar('theta', 'image 1', 1, 180, self.changeTheta)
#         cv2.createTrackbar('minlength', 'image 1', 1, 100, self.changeMinLineLength)
#         cv2.createTrackbar('maxlength', 'image 1', 1, 100, self.changeMaxLineGap)
        
        
        self.findLines()
        
        
    def constructPath(self):  
        index = self.startIndex
        # read first image
        self.image1 = cv2.imread("E:\\python workspace\\CharlieCode\\images\\optical%d.png" % (index))
        
        
        cv2.imshow("image 1", self.image1)
        
        # Creating trackbar for kernel size
        cv2.createTrackbar('threshold', 'image 1', 1, 100, self.changeThreshold)
        cv2.createTrackbar('rho', 'image 1', 1, 100, self.changeRho)
        cv2.createTrackbar('theta', 'image 1', 1, 180, self.changeTheta)
        cv2.createTrackbar('minlength', 'image 1', 1, 100, self.changeMinLineLength)
        cv2.createTrackbar('maxlength', 'image 1', 1, 100, self.changeMaxLineGap)
        self.findLines()
        
        
        
        index = index + 1
        
        
        self.image1 = cv2.imread("E:\\python workspace\\CharlieCode\\images\\optical%d.png" % (index))
        index = index + 1
        self.findLines()
            
            
        cv2.waitKey(0)

if __name__ == '__main__':
    opticalPath = OpticalFlowPath()
    opticalPath.constructPath()
