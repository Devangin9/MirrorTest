'''
Created on 10-Apr-2013

@author: Devangini
'''

import cv2.cv as cv
import cv2
import numpy as np

img = cv2.imread("E:\\python workspace\\Charlie\\eye1.jpg")

print type(img)

(rows, cols, channels) =  img.shape



originalImage = cv.CreateMat(rows, cols, cv.CV_8UC3)
originalImage = cv.fromarray(img)
originalImage2 = cv.fromarray(img)
    
#cv.ConvertScale(img, invertedImage)
#onesMatrix = cv.CreateMat(img.rows, img.cols,cv.CV_8UC3 )
#cv.FloodFill(onesMatrix, (0, 0), 1)
#onesArray = np.ones((img.rows, img.cols), np.uint8)
#onesArray = np.copy(onesArray)
#print onesArray.flags.contiguous
 
 
#convert to hsv
#hsvImage = cv.CreateMat(rows, cols, cv.CV_8UC3)
#cv.CvtColor(originalImage, hsvImage, cv.CV_RGB2HSV);
 
#cv.ShowImage("hsv ", hsvImage)
 
#split them into channels
b8u = cv.CreateMat(rows, cols, cv.CV_8UC1)#cv.CloneMat(img)  
g8u = cv.CreateMat(rows, cols, cv.CV_8UC1)#cv.CloneMat(img)  
r8u = cv.CreateMat(rows, cols, cv.CV_8UC1)#cv.CloneMat(img)    
cv.Split(originalImage, b8u, g8u, r8u, None);
#cv.Split(originalImage, hsv_planes[0], hsv_planes[1], hsv_planes[2], None)
 
#cv.ShowImage("hue ", hueChannel)
#cv.ShowImage("saturation", saturationChannel)
 
#invert hue channel

 
#print(type(hueChannel))
 
for i in range(rows):
    for j in range(cols):
        #print valueChannel[i,j]
        #hsv_planes[2][i, j] = 180 - hsv_planes[2][i, j]
        r8u[i,j] = 255 - r8u[i,j];
        g8u[i,j] = 255 - g8u[i,j];
        b8u[i,j] = 255 - b8u[i,j];
        #cv.FloodFill(onesMatrix, (i, j), 255)
        #onesMatrix.  [i][j][0] = 255
#cv.Merge(hsv_planes, originalImage)
cv.Merge(b8u, g8u, r8u, None, originalImage)      
#convert into rgb again
#cv.CvtColor( hsvImage, originalImage, cv.CV_HSV2RGB);
        
#merge hsv together
 
 
#onesMatrix = cv.fromarray( onesArray)
 
#print img.channels()
#cv.Sub(onesMatrix, img, originalImage)
#cv.Invert(invertedImage, invertedImage)

cv.ShowImage("subtraction ", originalImage)

 
#convert it to grey scale
grayScaleImage = cv.CreateMat(rows, cols, cv.CV_8UC1)
cv.CvtColor(originalImage, grayScaleImage, cv.CV_BGR2GRAY);
# 
cv.ShowImage("grey ", grayScaleImage)
#  
binaryImage = cv.CreateMat(rows, cols, cv.CV_8UC1)
# #make it binary by making it threshold at 220
cv.Threshold(grayScaleImage, binaryImage, 200, 255, cv2.THRESH_BINARY )


#cv.Erode(binaryImage, binaryImage)
#cv.Dilate(binaryImage, binaryImage)

#show the image
cv.ShowImage("binary image ", binaryImage)
#
# storage = cv.CreateMemStorage()
# contours = cv.FindContours(binaryImage, storage, cv.CV_RETR_TREE,cv.CV_CHAIN_CODE)   
# print type(contours)


    
# for (x,y) in contours:
#     print (x,y)
    
# cv.DrawContours(originalImage2,contours,(0, 0, 255),(0,255,0),50)

#poly = cv.ApproxPoly(contours)


#imageArray = np.asarray(binaryImage, dtype=np.uint8, order = 1)


#contours, hier = cv2.findContours(imageArray,  cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


#boundingBox = cv2.boundingRect(contours)

#cv2.drawContours(imageArray, contours, 0, (0, 255, 0))



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
params.minArea = 20.0
params.maxArea = 500.0

myBlobDetector = cv2.SimpleBlobDetector(params)
keypoints = myBlobDetector.detect(originalImage2)
print "blobs " + str(keypoints)

# extract the x y coordinates of the keypoints: 

for i in range(0, len(keypoints) - 1):
    print keypoints[i].pt
    pt1 = (int(keypoints[i].pt[0]), int(keypoints[i].pt[1]))
    pt2 = (int(keypoints[i + 1].pt[0]), int(keypoints[i + 1].pt[1]))
    cv2.line(originalImage2, pt1, pt2, (255, 0, 0))
#                 float X=keypoints[i].pt.x; 
#                 float Y=keypoints[i].pt.y;

cv.ShowImage("eye ", originalImage2)



#apply hough transform
#storage = cv.CreateMat(binaryImage.cols, 1,  cv.CV_8UC1)

#circles = cv.HoughCircles(binaryImage, storage,cv.CV_HOUGH_GRADIENT, 2 , 2)


#for i in range(0,len(np.asarray(storage))):
    #cv.Circle(originalImage, ( int(np.asarray(storage)[i][0][0]), int(np.asarray(storage)[i][0][1]) ), int(np.asarray(storage)[i][0][2]), cv.CV_RGB(255, 0, 0), 2, 8, 0 )

#for i in range(0,len(np.asarray(storage))):
 #   cv.Circle(img, ( int(np.asarray(storage)[i][0][0]), int(np.asarray(storage)[i][0][1]) ), int(np.asarray(storage)[i][0][2]), cv.CV_RGB(255, 0, 0), 2, 8, 0 )
  
#cv.HoughCircles(grayScaleImage, storage, cv.CV_HOUGH_GRADIENT, 2, int(grayScaleImage.height/4), 200, 100 );

#     for i in range(len(circles)) :
#         print "cirlce " + str(circles[i])
#         p = cv.GetSeqElem( circles, i );
#         cv.Circle( img, cv.Point(cv.Round(p[0]),cv.Round(p[1])), 3, cv.CV_RGB(0,255,0), -1, 8, 0 );
#         cv.Circle( img, cv.Point(cvRound(p[0]),cvRound(p[1])), 
     
while True:
    if cv.WaitKey(10) == 27:
        break
