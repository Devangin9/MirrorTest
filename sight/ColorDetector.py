'''
Created on 24-Jun-2013

@author: Devangini

http://en.wikipedia.org/wiki/Infant_vision

 There is a general debate among researchers with regards to the exact age that infants can detect
  different colors/chromatic stimuli due to important color factors such as brightness/luminance, saturation, and hue.
   Regardless of the exact timeline for when infants start to see particular colors,
    it is understood among researcher that infants' color sensitivity improves with age.

 It is generally accepted across all current research that infants prefer high contrast and bold colors at their earlier
   stages of infancy, rather than saturated colors.[24] One study found that newborn infants looked longer at checkered
    patterns of white and colored stimuli (including red, green, yellow) than they did at a uniform white color.
     However, infants failed to discriminate blue from white checkered patterns. Another study -
      recording the fixation time of infants to blue, green, yellow, red, and gray at two difference luminance levels -
       found that infants and adults deferred in their color preference.
        Newborns and one month did not show any preference among the colored stimuli.
         It was found that three month old infants preferred the longer wavelength (red and yellow)
          to the short-wavelength (blue and green) stimuli, while adults had the opposite.
           However, both adults and infants preferred colored stimuli over non-colored stimuli.
            According this study, it was suggest that infants had a general preference for colored stimuli 
            over non-colored stimuli at birth; however, infants were not able to distinguish between the different
             colored stimuli until after three months of age.
'''
import cv2.cv as cv
import numpy as np
import cv2

        
width = 480
height = 320

# HSV color space Threshold values for a RED laser pointer 
# hue
hmin = 0
hmax = 45  # hmax = 180
# saturation
smin = 50
smax = 100
# value
vmin = 250
vmax = 256

    
            
            
class ColorDetector:
    
    def startCamera(self):
        
        self.video1 = cv.CaptureFromCAM(0)
        cv.SetCaptureProperty(self.video1, cv.CV_CAP_PROP_FRAME_WIDTH, width)
        cv.SetCaptureProperty(self.video1, cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        
#          http://aravindc.com/2012/12/26/color-tracking-opencv-python-and-my-first-post/
    def findBrightObjects(self):
        
        cv.NamedWindow("camera")

        while True :
            frame = cv.QueryFrame(self.video1)
        #     print type(frame)
            [rows, cols] = cv.GetSize(frame)
            
#             image = cv.CreateMat(rows, cols, cv.CV_8UC3)
            image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, frame.nChannels)        
            cv.Copy(frame, image)
#             image = cv.GetMat(frame)
            cv.ShowImage("camera", image)
            
           
#             grayScaleFullImage = cv.CreateImage((image.width, image.height), 8, 1)
#             cv.CvtColor(image, grayScaleFullImage, cv.CV_BGR2GRAY)
            
#             convert to hsv
            hsvImage = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, frame.nChannels)  
            cv.CvtColor(image, hsvImage, cv.CV_BGR2HSV)
            cv.ShowImage("hsv", hsvImage)
           
#             hsvImage = cv2.cvtColor(imageArray, cv.CV_BGR2HSV)

#             h_plane = cv.CreateImage(cv.GetSize(image), 8, 1)
#             s_plane = cv.CreateImage(cv.GetSize(image), 8, 1)
#             v_plane = cv.CreateImage(cv.GetSize(image), 8, 1)
            
#           Split HSV into two of it's three channels. V channel is same as greyscale image so ignore.
#             cv.Split(hsvImage, h_plane, s_plane, v_plane, None)
#             http://robbierickman.blogspot.co.uk/2011/11/laserduckpy-coloured-object-tracking.html
            
            
#             planes = [h_plane, s_plane]
# 
#             h_bins = 30
#             s_bins = 32
#             hist_size = [h_bins, s_bins]
#             # hue varies from 0 (~0 deg red) to 180 (~360 deg red again */
#             h_ranges = [0, 180]
#             # saturation varies from 0 (black-gray-white) to
#             # 255 (pure spectrum color)
#             s_ranges = [0, 255]
#             ranges = [h_ranges, s_ranges]
#             scale = 10
#             hist = cv.CreateHist([h_bins, s_bins], cv.CV_HIST_ARRAY, ranges, 1)
#             cv.CalcHist([cv.GetImage(i) for i in planes], hist)
#             (_, max_value, _, _) = cv.GetMinMaxHistValue(hist)
#         
#             hist_img = cv.CreateImage((h_bins*scale, s_bins*scale), 8, 3)
#         
#             for h in range(h_bins):
#                 for s in range(s_bins):
#                     bin_val = cv.QueryHistValue_2D(hist, h, s)
#                     intensity = cv.Round(bin_val * 255 / max_value)
#                     cv.Rectangle(hist_img,
#                                  (h*scale, s*scale),
#                                  ((h+1)*scale - 1, (s+1)*scale - 1),
#                                  cv.RGB(intensity, intensity, intensity),
#                                  cv.CV_FILLED)
            
            # http://uvhar.googlecode.com/hg/test/laser_tracker.py
            # Threshold ranges of HSV components.
            
#             cv.InRangeS(h_plane, hmin, hmax, h_plane)
# #             cv.InRangeS(s_plane, smin, smax, s_plane)
# #             cv.InRangeS(v_plane, vmin, vmax, v_plane)
#             
#             finalImage = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
#     
#             # Perform an AND on HSV components to identify the laser!
#             cv.And(h_plane, s_plane, finalImage)
#             # This actually Worked OK for me without using Saturation.
#             # cv.cvAnd(laser_img, s_img,laser_img) 
#     
#             # Merge the HSV components back together.
#             cv.Merge(h_plane, s_plane, v_plane, None, hsvImage)
            
   
#             cv.ShowImage("hue", h_plane)
#             cv.ShowImage("saturation", s_plane)
#             cv.ShowImage("value", v_plane)
            
            thresholdImage = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
            cv.InRangeS(hsvImage, cv.Scalar(0, 100, 100), cv.Scalar(50, 255, 255), thresholdImage)
            
#             thresholdImage = cv2.threshold(hsvImage, [0, 100, 100], [50, 255, 255], cv2.THRESH_BINARY)
            cv.ShowImage("threshold image", thresholdImage)
            
            # remove noise from threshold image
            kernel = cv.CreateStructuringElementEx(9, 9, 5, 5, cv.CV_SHAPE_CROSS) 
             
            # Dilate- replaces pixel value with highest value pixel in kernel
            cv.Dilate(thresholdImage, thresholdImage, kernel, 2)
             
            # Erode- replaces pixel value with lowest value pixel in kernel
            cv.Erode(thresholdImage, thresholdImage, kernel, 2)

#             element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
#             cv.Dilate(thresholdImage, element, thresholdImage)
#             cv2.erode(thresholdImage, element, thresholdImage)
            
            cv.ShowImage("cleaned image ", thresholdImage)
            
            # contour detection
            imageArray = np.asarray(cv.GetMat(thresholdImage), np.uint8, 1)
            print type(imageArray)
            imageArray = imageArray.T
            
            
            
#             contours, hier = cv2.findContours(imageArray, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)   
#             print "TYPE " + str(type(contours)) + " " + str(len(contours))
#              
# #             for i in contours:
# #                 print i
#             maxArea = -1
#             contourIndex = -1
#             if contours: 
#                 for i in range(0, len(contours)):
#                     cnt = contours[i].astype('int')
#                     print type(cnt)
#                     area = cv2.contourArea(cnt)
#                     print area
#                     if area > maxArea:
#                         maxArea = area
#                         contourIndex = i
#                          
#             if contourIndex != -1:
#                 cv2.drawContours(imageArray, contours, contourIndex, (0, 0 , 255), 10)

            
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
            keypoints = myBlobDetector.detect(imageArray)
            print "blobs " + str(keypoints)
            
            # extract the x y coordinates of the keypoints: 

            for i in range(0, len(keypoints) - 1):
                print keypoints[i].pt
                pt1 = (int(keypoints[i].pt[0]), int(keypoints[i].pt[1]))
                pt2 = (int(keypoints[i + 1].pt[0]), int(keypoints[i + 1].pt[1]))
                cv2.line(imageArray, pt1, pt2, (255, 0, 0))
#                 float X=keypoints[i].pt.x; 
#                 float Y=keypoints[i].pt.y;
            
                     
            cv2.imshow("final detection ", imageArray)
#             
            
            if cv.WaitKey(10) == 27:
                break 
        
            
if __name__ == "__main__":
    t = ColorDetector()
    t.startCamera()
    t.findBrightObjects()
