'''
Created on 01-Apr-2013

@author: Devangini

This program is demonstration for face and object detection using haar-like features.
The program finds faces in a camera image or video stream and displays a red box around them.

Original C implementation by:  ?
Python implementation by: Roman Stanchak, James Bowman
'''
#!/usr/bin/python



import sys
import cv2
import cv2.cv as cv
from optparse import OptionParser
import numpy as np
import colorsys
from expressionreco import EyeBallExtractor
from expressionreco import EyebrowExtractor 
from sight.camshift import Camshift
from sight.MotionDetector3 import MotionDetector
from config.CameraConstants import _CameraConstants
from sight.test_surf import SurfMatcher


# Parameters for haar detection
# From the API:
# The default parameters (scale_factor=2, min_neighbors=3, flags=0) are tuned
# for accurate yet slow object detection. For a faster operation on real video
# images the settings are:
# scale_factor=1.2, min_neighbors=2, flags=CV_HAAR_DO_CANNY_PRUNING,
# min_size=<minimum possible face size

min_size = (20, 20)  # (50, 50)
image_scale = 2
haar_scale = 1.2
min_neighbors = 2
haar_flags = cv.CV_HAAR_DO_CANNY_PRUNING
HCDIR = "E:\\Softwares\\opencv\\data\\haarcascades\\" 
DATADIR2 = "E:\\Softwares\\opencv\\data\\extracascades\\" 
LBPDIR = "E:\\Softwares\\opencv\\data\\lbpcascades\\"
DATADIR = "E:\\python workspace\\Charlie\\data\\"
isOpticalFlow = False

CameraConstants = _CameraConstants()
width = CameraConstants.cameraWidth()
height = CameraConstants.cameraHeight()



# def set_scale(val):
#     global hist_scale
#     hist_scale = val
# cv2.createTrackbar('scale', 'hist', hist_scale, 32, set_scale)
# 
# def hs_histogram(src):
#     # Convert to HSV
#     hsv = cv.CreateImage(cv.GetSize(src), 8, 3)
#     cv.CvtColor(src, hsv, cv.CV_BGR2HSV)
# 
#     # Extract the H and S planes
#     h_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
#     s_plane = cv.CreateMat(src.rows, src.cols, cv.CV_8UC1)
#     cv.Split(hsv, h_plane, s_plane, None, None)
#     planes = [h_plane, s_plane]
# 
#     h_bins = 180
#     s_max  = 255
#     s_bins = s_max
#     hist_size = [h_bins, s_bins]
#     # hue varies from 0 (~0 deg red) to 180 (~360 deg red again */
#     h_ranges = [0, 180]
#     # saturation varies from 0 (black-gray-white) to
#     # 255 (pure spectrum color)
#     
#     s_ranges = [0, s_max]
#     ranges = [h_ranges, s_ranges]
#     scale = 10
#     hist = cv.CreateHist([h_bins, s_bins], cv.CV_HIST_ARRAY, ranges, 1)
#     cv.CalcHist([cv.GetImage(i) for i in planes], hist)
#     cv.NormalizeHist(hist, 1)
#     (_, max_value, _,max_idx ) = cv.GetMinMaxHistValue(hist)
#     
#     print "max value  " + str(max_value)
#     print "max value coords " + str(max_idx)
#     print "range " + str(colorsys.rgb_to_hsv(1, 1, 1))
#     print "color "  + str(colorsys.hls_to_rgb(14/180,1,  114/255))
#     print "size " + str(hist_size)
# 
#     hist_img = cv.CreateImage((h_bins*scale, s_bins*scale), 8, 3)
# 
#     for h in range(h_bins):
#         for s in range(s_bins):
#             bin_val = cv.QueryHistValue_2D(hist, h, s)
#             intensity = cv.Round(bin_val * 255 / max_value)
#             cv.Rectangle(hist_img,
#                          (h*scale, s*scale),
#                          ((h+1)*scale - 1, (s+1)*scale - 1),
#                          cv.RGB(intensity, intensity, intensity), 
#                          cv.CV_FILLED)
#     return hist_img


class FaceTracker:
    
    
    def __init__(self):
        self.MotionDetector = None
        self.capture = None
        self.matcher = SurfMatcher()
        parser = OptionParser(usage="usage: %prog [options] [filename|camera_index]")
        parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default=HCDIR + "haarcascade_frontalface_alt_tree.xml")
          
        # parser.add_option("-c", "--cascade", action="store", dest="cascade", type="str", help="Haar cascade file, default %default", default = "../data/haarcascades/haarcascade_frontalface_alt.xml")
        (options, args) = parser.parse_args()
      
        self.cascade = cv.Load(options.cascade)
         # detect eyes
        self.cascade2 = cv.Load(DATADIR2 + "haarcascade eye.xml")
        # cascade2 = cv.Load(HCDIR + "..\\eyes\\eye.xml")
         
        # cascade3 = cv.Load(HCDIR + "haarcascade_mcs_mouth.xml")
        self.cascade3 = cv.Load(DATADIR2 + "Mouth.xml")
        
        self.cascade4 = cv.Load(HCDIR + "haarcascade_mcs_nose.xml")
        
    def detectMouth(self, img, mouthArea, pt1, centerY, cascade3):
        mouth = cv.HaarDetectObjects(mouthArea, cascade3, cv.CreateMemStorage(0),
                                                 haar_scale, min_neighbors, haar_flags, min_size)
        # in case of multiple find the maximum box
        minArea = 0
        pt3 = (0, 0)
        pt4 = (0, 0)
        if mouth:
            for ((x, y, w, h), n) in mouth:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                if(w * h > minArea):
                    minArea = w * h
                    pt3 = (x, y)
                    pt4 = (x + w, y + h)    
        cv.Rectangle(img, (pt1[0] + pt3[0], centerY + pt3[1]), (pt1[0] + pt4[0], centerY + pt4[1]), cv.RGB(0, 0, 255))
        
        
    def detectRightEye(self, img, rightEyeArea, centerX, centerY, pt1, cascade2):
        rightEye = cv.HaarDetectObjects(rightEyeArea, cascade2, cv.CreateMemStorage(0),
                                        haar_scale, min_neighbors, haar_flags, min_size)
        # in case of multiple find the maximum box
        minArea = 0
        pt3 = (0, 0)
        pt4 = (0, 0)
        if rightEye:
            for ((x, y, w, h), n) in rightEye:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                if(w * h > minArea):
                    minArea = w * h
                    pt3 = (x, y)
                    pt4 = (x + w, y + h)
    #                         pt3 = (int(x * image_scale), int(y * image_scale))
    #                         pt4 = (int((x + w) * image_scale), int((y + h) * image_scale))
    #                         print "point 3 " + str(pt3)
    #                         print "point 4 " + str(pt4)
    #                         
    #                         cv.Rectangle(img, (centerX + pt3[0], pt1[1] + pt3[1]),(centerX + pt4[0], pt1[1] + pt4[1]), cv.RGB(0, 255, 255))
    #                         cv.Rectangle(img, pt3, pt4, cv.RGB(0, 0, 255))
        if(minArea > 0):       
            cv.Rectangle(img, (centerX + pt3[0], pt1[1] + pt3[1]), (centerX + pt4[0], pt1[1] + pt4[1]), cv.RGB(0, 255, 255))
            pointX = centerX + pt3[0] + 10
            pointY = pt1[1] + pt3[1] + 10
            distanceX = pt4[0] - pt3[0] - 10
            distanceY = pt4[1] - pt3[1] - 10
            eyePart = cv.GetSubRect(img, (pointX, pointY, distanceX, distanceY))
#             return EyeBallExtractor.extractEyeBall(eyePart)
            
            # return (pt3, pt4)
    
    def detectLeftEye(self, originalImage, cascade2, pt1, centerX, centerY):
        
        
        leftEyeArea = cv.GetSubRect(originalImage, (pt1[0], pt1[1], centerX - pt1[0], centerY - pt1[1]))
        
        
        leftEye = cv.HaarDetectObjects(leftEyeArea, cascade2, cv.CreateMemStorage(0),
                                      haar_scale, min_neighbors, haar_flags, min_size)
        # in case of multiple find the maximum box
        minArea = 0
        pt3 = (0, 0)
        pt4 = (0, 0)
        if leftEye:
            for ((x, y, w, h), n) in leftEye:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                if(w * h > minArea):
                    minArea = w * h
                    pt3 = (x, y)
                    pt4 = (x + w, y + h)
                    
                    
        if(minArea > 0):
            cv.Rectangle(originalImage, (pt1[0] + pt3[0], pt1[1] + pt3[1]), (pt1[0] + pt4[0], pt1[1] + pt4[1]), cv.RGB(255, 255, 0)) 
            pointX = pt1[0] + pt3[0] + 10
            pointY = pt1[1] + pt3[1] + 10
            distanceX = pt4[0] - pt3[0] - 10
            distanceY = pt4[1] - pt3[1] - 10
            eyePart = cv.GetSubRect(originalImage, (pointX, pointY, distanceX, distanceY))
            # eyePartArray = np.asarray(eyePart, np.uint8, 3)
            # eyePart = cv.GetSubRect(originalImage, (pt1[0] + pt3[0], pt1[1] + pt3[1], pt4[0] - pt3[0],  pt4[1] - pt3[1]))
#             eyeBallParams = EyeBallExtractor.extractEyeBall(eyePart)
                            
            # EyebrowExtractor.extractEyeBrows(originalImage, pt1, centerX, centerY, eyeBallParams)\
    
    def detectNose(self, originalImage, cascade2, centerX, centerY):
        
        widthX = 150
        widthY = 150
        noseArea = cv.GetSubRect(originalImage, (centerX - widthX / 2 , centerY - widthY / 2, widthX, widthY))
        
        
        nose = cv.HaarDetectObjects(noseArea, cascade2, cv.CreateMemStorage(0),
                                      haar_scale, min_neighbors, haar_flags, min_size)
        # in case of multiple find the maximum box
        minArea = 0
        pt3 = (0, 0)
        pt4 = (0, 0)
        if nose:
            for ((x, y, w, h), n) in nose:
                # the input to cv.HaarDetectObjects was resized, so scale the
                # bounding box of each face and convert it to two CvPoints
                if(w * h > minArea):
                    minArea = w * h
                    pt3 = (x, y)
                    pt4 = (x + w, y + h)      
                    
        if(minArea > 0):
            cv.Rectangle(originalImage, (centerX - widthX / 2 + pt3[0], centerY - widthY / 2 + pt3[1]), (centerX - widthX / 2 + pt4[0], centerY - widthY / 2 + pt4[1]), cv.RGB(255, 0, 255)) 
            
    
    
    def detect_and_draw(self, originalImage):
        # allocate temporary images
        
        print type(originalImage)
        grayScaleFullImage = cv.CreateImage((originalImage.width, originalImage.height), 8, 1)
        smallScaleFullImage = cv.CreateImage((cv.Round(originalImage.width / image_scale),
                       cv.Round (originalImage.height / image_scale)), 8, 1)
    
        # convert color input image to grayscale
        cv.CvtColor(originalImage, grayScaleFullImage, cv.CV_BGR2GRAY)
    
        # scale input image for faster processing
        cv.Resize(grayScaleFullImage, smallScaleFullImage, cv.CV_INTER_LINEAR)
    
        cv.EqualizeHist(smallScaleFullImage, smallScaleFullImage)
    
        if(self.cascade):
            t = cv.GetTickCount()
            # detect faces
            faces = cv.HaarDetectObjects(smallScaleFullImage, self.cascade, cv.CreateMemStorage(0),
                                         haar_scale, min_neighbors, haar_flags, min_size)
            t = cv.GetTickCount() - t
            print "detection time = %gms" % (t / (cv.GetTickFrequency() * 1000.))
            if faces:
                print "detected face"
                for ((x, y, w, h), n) in faces:
                    # the input to cv.HaarDetectObjects was resized, so scale the
                    # bounding box of each face and convert it to two CvPoints
                    pt1 = (int(x * image_scale), int(y * image_scale))
                    pt11 = (int(x * image_scale) + 10, int(y * image_scale) + 10)
                    pt2 = (int((x + w) * image_scale), int((y + h) * image_scale))
                    # face 
                    cv.Rectangle(originalImage, pt1, pt2, cv.RGB(255, 0, 0), 3, 8, 0)
                    
                    if isOpticalFlow:
                        originalArray2 = cv.CloneImage(originalImage)
                        faceArea = cv.GetSubRect(originalArray2, (pt1[0], pt1[1], pt2[0] - pt1[0], pt2[1] - pt1[1]))
                        faceArea2 = cv.CloneMat(faceArea)
                        cv.ShowImage("face area", faceArea2)
                        self.MotionDetector.iterativeMotionDetector(faceArea2)
                                        
     
                    # get the center of the rectangle
                    centerX = (pt1[0] + pt2[0]) / 2     
                    centerY = (pt1[1] + pt2[1]) / 2 + int(0.1 * w * image_scale)
                      
                    # around nose region
                    cv.Rectangle(originalImage, (centerX, centerY), (centerX + 10, centerY + 10), cv.RGB(255, 0, 255))   
                    
                         
                    # detect left eye
                    # cv.SetZero(sub)  55
                    self.detectLeftEye(originalImage, self.cascade2, pt1, centerX, centerY)
                    
                    # detect right eye
                    rightEyeArea = cv.GetSubRect(originalImage, (centerX, pt1[1], pt2[0] - centerX  , centerY - pt1[1]))
                    # cv.SetZero(rightEyeArea)    
                    self.detectRightEye(originalImage, rightEyeArea, centerX, centerY, pt1, self.cascade2)
                    
#                     self.detectNose(originalImage, cascade4, centerX, centerY)
                    
                            
                    
                
                 
                     
                    
                    # now apply mask for values in range +/- 10% of index_1
                    # form a map for showing the eyebrows
                    # cloneImageArray = cv.CloneMat(imageArray)
                    # cloneImageArray = np.empty_like (imageArray)
                    # cloneImageArray[:] = imageArray
                    # cv2.imshow("left eye " ,cloneImageArray)
                
                    # res = cv2.bitwise_and(cloneImageArray,cloneImageArray,mask = backproj)
                    # cv2.imshow("res" ,res)
                
                
                    # detect left eyebrow
                    # by doing simple contour detection
    #                 print type(leftEyeArea)
    #                 gray_im = cv.CreateMat(leftEyeArea.height, leftEyeArea.width, cv.CV_8UC1)
    #                 #gray_im = cv.CreateImage((leftEyeArea.rows, leftEyeArea.cols), cv.IPL_DEPTH_8U, 1)
    #                 print type(gray_im)
    #                 cv.CvtColor(leftEyeArea, gray_im, cv.CV_RGB2GRAY)
    #                 imageArray = np.asarray(gray_im, dtype=np.uint8)
    #                 #floatMat.convertTo(ucharMat, CV_8UC1);
    # 
    #                 # scale values from 0..1 to 0..255
    #                 #floatMat.convertTo(ucharMatScaled, CV_8UC1, 255, 0); 
    #                 contours0, hier = cv2.findContours( backproj , cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # #               
    # 
    #                 cv_im = cv.CreateMat(img.width, img.height, cv.CV_8UC3)
    #                 cv.SetData(cv_im, img.tostring())
    #                     
    #                 #print type(cv_im)
    #                 
    #                 originalImageArray = np.asarray(cv_im, dtype=np.uint8)
    #                 
    #                 print " length " + str(len(contours0))   
    #                 #print type(contours0)
    #                 
    #                 lines = None
    #                 linesList = list()
    #                 for item in contours0:
    #                     #print "item " + str(item)
    #                        
    #                     #print type(item)
    #                     for i in range(1, len(item)):
    #                         #for j in range(len(item[i][0])):
    #                         #print str(item[i][0][0]) + " " + str(item[i][0][1])
    #                         #lines.append([[item[i][0][0], item[i][0][1]]])
    #                         if lines != None:
    #                             np.append(lines, item[i][0])
    #                         else:
    #                             lines = np.array(item[i][0])
    #                         linesList.append((item[i][0][0] , item[i][0][1]))
    #                         #cv2.circle(backproj, ( item[i][0][0] , item[i][0][1]), 10, (255,255,255), 10)
    #                         #cv.Circle(img, (pt1[0] + item[i][0][0] ,int(pt1[1] * 1.1)+ item[i][0][1]), 5, (255,0,255))
    #                             
    #                             
    #                
    #                 
    #                 #print type(originalImageArray)
    #                 print lines
    #                 #cv2.polylines(originalImageArray, lines, True, cv.RGB(255, 255, 0), 10)
    #                 print type(linesList)
    #                 #cv.PolyLine(cv_im, linesList, False, cv.RGB(255, 255, 0), 10)
    #                 #cv2.drawContours(backproj, contours0, , cv.RGB(55, 55, 55))
                
                    
                    
                    # canny_output = None
                    # canny_output = cv2.Canny(backproj, 700, 1000, canny_output, 7)
                    # cv2.imshow("canny ", canny_output)
                    
                    # cv.Canny(hsv_image, contours0, 10, 60);
                    # contours, hier = cv2.findContours( canny_output , cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #               
    
    
    
                   
                    
                    
                    
    
                
                    # cv2.drawContours(originalImageArray,lines,-1,(0,255,0),3)
                   
                    # detect mouth
                    mouthArea = cv.GetSubRect(originalImage, (pt1[0], centerY, pt2[0] - pt1[0], pt2[1] - centerY))
                    self.detectMouth(originalImage, mouthArea, pt1, centerY, self.cascade3)
                    
                    
                    
                    
                    # start tracking face
                    if not isOpticalFlow:
                        originalArray2 = cv.CloneImage(originalImage)
                        faceArea = cv.GetSubRect(originalArray2, (pt1[0], pt1[1], pt2[0] - pt1[0], pt2[1] - pt1[1]))
                        faceArea2 = cv.CloneMat(faceArea)
                        return (True, faceArea2, originalImage, pt1, pt2)
                        
#                         originalImage2 = cv.CloneImage(originalImage)
#                         camshift = Camshift()
#                         camshift.defineRegionOfInterest(originalImage2, pt1, pt2)

#                         originalArray2 = cv.CloneImage(originalImage)
#                         faceArea = cv.GetSubRect(originalArray2, (pt1[0], pt1[1], pt2[0] - pt1[0], pt2[1] - pt1[1]))
#                         faceArea2 = cv.CloneMat(faceArea)
#                         cv.ShowImage("face area", faceArea2)
#                         faceArray = np.asarray(faceArea2, np.uint8, 3)
#                         faceArray = cv2.cvtColor(faceArray, cv2.COLOR_BGR2GRAY)
#                         self.matcher.defineTargetImage(faceArray)
#                         self.matcher.findInVideoSequence()
                          
                    
                    
                              
                    
      
        cv.ShowImage("result", originalImage)
        
        return (False, originalImage, None, None, None)
        
    
        

if __name__ == '__main__':
  
    tracker = FaceTracker()
    
    if isOpticalFlow:
        tracker.MotionDetector = MotionDetector()
        tracker.MotionDetector.initialize()

  
    input_name = 0
#     if input_name.isdigit():
    tracker.capture = cv.CreateCameraCapture(int(input_name))
#     else:
#         tracker.capture = None
        
    cv.SetCaptureProperty(tracker.capture, cv.CV_CAP_PROP_FRAME_WIDTH, width);
    cv.SetCaptureProperty(tracker.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, height);
  
    cv.NamedWindow("result", 1)
     
    
    if tracker.capture:
        frame_copy = None
        while True:
            frame = cv.QueryFrame(tracker.capture)
            if not frame:
                cv.WaitKey(0)
                break 
            if not frame_copy:
                frame_copy = cv.CreateImage((frame.width, frame.height),
                                            cv.IPL_DEPTH_8U, frame.nChannels)
            if frame.origin == cv.IPL_ORIGIN_TL:
                cv.Copy(frame, frame_copy)
            else:
                cv.Flip(frame, frame_copy, 0)
                
            tracker.detect_and_draw(frame_copy)
  
            if cv.WaitKey(10) >= 0:
                break
    else:
        image = cv.LoadImage(input_name, 1)
        tracker.detect_and_draw(image)
        cv.WaitKey(0)
  
    cv.DestroyWindow("result")

