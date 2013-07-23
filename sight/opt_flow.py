# /usr/bin/env python

import numpy as np
import cv2
import video
from config.CameraConstants import _CameraConstants
import cv2.cv as cv
from sight import OpticalFlowPath


CameraConstants = _CameraConstants()
width = CameraConstants.cameraWidth()
height = CameraConstants.cameraHeight()

help_message = '''
USAGE: opt_flow.py [<video_source>]

Keys:
 1 - toggle HSV flow visualization
 2 - toggle glitch

'''

CameraConstants = _CameraConstants()
width = CameraConstants.cameraWidth()
height = CameraConstants.cameraHeight()

class OpticalFlow:
    
    def __init__(self):
        self.lines = None
        self.avgX = 0
        self.avgY = 0
        self.prevgray = None
        self.imageIndex = 0
        self.opticalPath = OpticalFlowPath.OpticalFlowPath()
        self.prevLines = None
        self.xdim = 0
        self.ydim = 0
        self.w = 0
        self.h = 0
        
    def draw_flow(self, img, flow, step=8):
        print type(img)
        h, w = img.shape[:2]
        
        if self.h == 0 :
            self.h = w
            self.w = h
            
        y, x = np.mgrid[step / 2:h:step, step / 2:w:step].reshape(2, -1)
        fx, fy = flow[y, x].T
        
#         print fx, fy
        print "shape :: " + str(np.shape(x)) + " " + str(int((w - step / 2 + 1) / step)) + " " + str(int((h - step / 2 + 1) / step))
        self.xdim = int((w - step / 2 + 1) / step) + 1
        self.ydim = (int((h - step / 2 + 1) / step)) + 1
        
        
        
        # find the mean of fx
        self.avgX = np.median(fx)
        self.avgY = np.median(fy)
        
        print "avgX " + str(self.avgX) + " avg Y " + str(self.avgY)
        
#         lowValY = 1
#         array_np = np.asarray(fx)
#         low_values_indices = array_np < lowValY  # Where values are low
#         array_np[low_values_indices] = 0  # All low values set to 0
#          
#         fx = array_np
#         
#         lowValY = 1
#         array_np = np.asarray(fy)
#         low_values_indices = array_np < lowValY  # Where values are low
#         array_np[low_values_indices] = 0  # All low values set to 0
#          
#         fy = array_np
        
        
        lines = np.vstack([x, y, x + fx, y + fy]).T.reshape(-1, 2, 2)
        lines = np.int32(lines + 0.5)
        print "lien type " + str(type(lines))
        self.lines = lines
        
        print "00 entry " + str(lines[100])
        
#         lines.clip(0)
        vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        cv2.polylines(vis, lines, 0, (0, 255, 0))
#         for (x1, y1), (x2, y2) in lines:
#             cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
        return vis
    
    def draw_hsv(self, flow):
        h, w = flow.shape[:2]
        fx, fy = flow[:, :, 0], flow[:, :, 1]
        ang = np.arctan2(fy, fx) + np.pi
        v = np.sqrt(fx * fx + fy * fy)
        hsv = np.zeros((h, w, 3), np.uint8)
        hsv[..., 0] = ang * (180 / np.pi / 2)
        hsv[..., 1] = 255
        hsv[..., 2] = np.minimum(v * 4, 255)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return bgr
    
    def warp_flow(self, img, flow):
        h, w = flow.shape[:2]
        flow = -flow
        flow[:, :, 0] += np.arange(w)
        flow[:, :, 1] += np.arange(h)[:, np.newaxis]
        res = cv2.remap(img, flow, None, cv2.INTER_LINEAR)
        return res
    
    def getOpticalFlow(self, prevgray, gray):
        flow = cv2.calcOpticalFlowFarneback(prevgray, gray , 0.5, 3, 5, 3, 2, 0.4, cv2.OPTFLOW_USE_INITIAL_FLOW)
        
#         cv2.imshow('flow', self.warp_flow(gray, flow))
        
        
        cv2.imshow('flow', self.draw_flow(gray, flow))
        
    def distance(self, distX, distY):
        return np.sqrt(distX * distX + distY * distY)  
    
    def euclideanDistance(self, pt1X, pt1Y, pt2X, pt2Y):
        distX = (pt1X - pt2X)
        distY = (pt1Y - pt2Y)
        return self.distance(distX, distY)
        
    def getAverageOpticalFlow(self, image, binary_mask):

        avgLength = self.distance(self.avgX, self.avgY)    
        print "avg length " + str(avgLength)   
        step = 5
        
        (w, h, channels) = np.shape(image)
        motionCanvas = np.zeros((w, h, channels), np.uint8)
        
#         motionCanvas2 = np.ones((w, h, channels), np.uint8)
        
#         cv2.polylines(motionCanvas, self.lines, 0, (0, 255, 0))

        for (x1, y1), (x2, y2) in self.lines:
            length = self.euclideanDistance(x1, y1, x2, y2)
#             print "length " + str(length)
            if length > 0.8:  # avgLength * 40:
                cv2.line(motionCanvas, (x1, y1), (x2, y2), (255, 255, 255))
#             cv2.circle(motionCanvas, (x1, y1), 1, (0, 255, 0), -1)

#         cv2.line(motionCanvas, (0, 0), (100, 100), (0, 255, 0), 5)
        
        cv2.imshow("motion", motionCanvas)
        
        
        
        print type(binary_mask)
#         (w, h) = cv.GetSize(binary_mask)
#         zerosArray = np.zeros((h, w), np.uint8, 3)

        if binary_mask != None:
         
            maskMat = cv.GetMat(binary_mask)
    #          
    #         (w, h) = cv.GetSize(binary_mask)
    #         maskMat2 = cv.CreateMat(w, h, cv.CV_8UC3)
    #         cv.CvtColor(maskMat, maskMat2, cv.CV_GRAY2BGR)
            maskArray = np.asarray(maskMat, np.uint8, 3)
    #         
            motionCanvas2 = np.copy(motionCanvas)
            
            print "size of input image " + str(np.shape(maskArray)) + " " + str(np.shape(motionCanvas2))
    #         
    #         print type(motionCanvas) , np.shape(motionCanvas)
    #         print type(maskArray) , np.shape(maskArray)
            motionCanvas2 = cv2.bitwise_and(motionCanvas2, motionCanvas2, mask=maskArray)
    #         motionCanvas2 = cv2.add(motionCanvas, zerosArray, motionCanvas2, maskArray)
            
            cv2.imshow("motion 2 ", motionCanvas2)
            
            self.opticalPath.findPath(motionCanvas2)
#             cv2.imwrite("E:\\python workspace\\CharlieCode\\images\\optical%d.png" % (self.imageIndex), motionCanvas2)
#             self.imageIndex = self.imageIndex + 1
        
        
        
    def getOpticalPath(self):
        if self.prevLines == None:
            print "assigning previous lines "
            self.prevLines = self.lines
            return
        else:
            print "comparing optical flows"
            newLines = self.lines.copy()
            # have two optical flows
            # now merge them
            # iterate lines
            
            print "shapes " + str(np.shape(self.lines)) + " " + str(np.shape(self.prevLines)) 
            
            count = 0
            minLength = 1
            neighbourhoodSize = 3
            
            motionVectors = np.zeros((self.w, self.h, 3), np.uint8)
#             cv2.line(motionVectors, (100, 100), (0, 0), (0, 255, 255))

            for i in range(0, self.xdim):
                for j in range(0, self.ydim):
            
#             for line in self.prevLines:
                    line = self.prevLines[i * self.ydim + j]
                    # take two points and calculate distance between them
                    # calculate distance between them
                    pt1 = line[0]
                    pt2 = line[1]
                    distance12 = self.euclideanDistance(float(pt1[0]), float(pt1[1]), float(pt2[0]), float(pt2[1]))
    
#                     print " -> min distance = " + str(distance12) + " : " + str(pt1) + " , " + str(pt2)
                        
                    
                    if distance12 > minLength:
#                         cv2.line(motionVectors, (pt1[0], pt1[1]), (pt2[0], pt2[1]), (0, 0, 255))
                        
                        count = count + 1
#                         print "distance " + str(distance12)
                        # see if there is a corresponding line is lines
                        # check the neighbourhood
                        minboundX = max(0, i - neighbourhoodSize)
                        maxboundX = min(self.ydim, i + neighbourhoodSize)
                        minboundY = max(0, j - neighbourhoodSize)
                        maxboundY = min(self.xdim, j + neighbourhoodSize)
                         
                        # find minimum distance 
                         
                        minDistance = 1000
                        minIndex = -1
                         
                        for k in range(minboundX, maxboundX):
                            for l in range(minboundY, maxboundY):
                                index = k * self.ydim + l
                                 
                                line2 = self.lines[index]
                                pt3 = line2[0]
                                pt4 = line2[1]
                                distance34 = self.euclideanDistance(float(pt3[0]), float(pt3[1]), float(pt4[0]), float(pt4[1]))        
                                
#                                 print "point 3 " + str(pt3) + " point 4 " + str(pt4) + " : distance => " + str(distance34)
                                     
                                # find the distance between pt1 and pt2 of previous line
                                if distance34 > minLength:
                                    
#                                     cv2.line(motionVectors, (pt3[0], pt3[1]), (pt4[0], pt4[1]), (0, 255, 0))
                                 
                                    distance23 = self.euclideanDistance(float(pt2[0]), float(pt2[1]), float(pt3[0]), float(pt3[1]))
                                     
#                                     print "point 2 " + str(pt2) + " point 3 " + str(pt3) + " : distance => " + str(distance23)
                                     
                                    if distance23 < minDistance:
                                        minIndex = index
                                        minDistance = distance23
#                         
                        if minDistance < 3:
                            line3 = self.lines[minIndex]
                            pt3 = line3[0]
                            pt4 = line3[1]
#                             print "min index == " + str(minIndex) + " -> min distance = " + str(minDistance) + " : " + str(pt2) + " , " + str(pt3)
#                             if count == 1:
                            cv2.line(motionVectors, (pt3[0], pt3[1]), (pt4[0], pt4[1]), (0, 255, 0))
                            cv2.line(motionVectors, (pt2[0], pt2[1]), (pt3[0], pt3[1]), (255, 255, 255))
                            cv2.line(motionVectors, (pt1[0], pt1[1]), (pt2[0], pt2[1]), (0, 0, 255))
                            
                            
                    
#             print " > 0 lines = " + str(count) + " out of 1584"
            
            cv2.imshow("motion vectors ", motionVectors)
            
            
            self.prevLines = self.lines
                    
            
            
        
    def makeOpticalFlow(self, img, binary_mask):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         flow = cv2.calcOpticalFlowFarneback(prevgray, gray, 0.5, 3, 15, 3, 5, 1.2, 0)
#         flow = cv2.calcOpticalFlowFarneback(prevgray, gray , 0.5, 3, 5, 3, 2, 0.4, cv2.OPTFLOW_USE_INITIAL_FLOW)
        
# calcOpticalFlowSF(from, to, flow, layers, averaging_block_size, max_flow) -> None  or  calcOpticalFlowSF(from, 
# to, flow, layers, averaging_block_size, max_flow, sigma_dist, sigma_color, postprocess_window, sigma_dist_fix, 
# sigma_color_fix, occ_thr, upscale_averaging_radius, upscale_sigma_dist, upscale_sigma_color, speed_up_thr) -> 
#         calcOpticalFlowSF(frame1, frame2, flow, 3, 2, 4, 4.1, 25.5, 18, 55.0, 25.5, 0.35, 18, 55.0, 25.5, 10
#         flow = gray.clone()
#         cv2.calcOpticalFlowSF(prevgray, gray, flow, 3, 2, 4, 4.1, 25.5, 18, 55.0, 25.5, 0.35, 18, 55.0, 25.5, 10)
#         print "flow "+ str(flow)

        if self.prevgray == None:
            self.prevgray = gray
 
        self.getOpticalFlow(self.prevgray, gray)
        
        self.getAverageOpticalFlow(img, binary_mask)
        

        self.getOpticalPath()
        
        self.prevgray = gray
        
        cv2.imshow("camera", gray)
        
        
if __name__ == '__main__':
    import sys
    print help_message
    try: fn = sys.argv[1]
    except: fn = 0

    cam = cv2.VideoCapture(fn)
        
  
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
    cam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
    

    ret, prev = cam.read()
    prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    show_hsv = False
    show_glitch = False
    cur_glitch = prev.copy()
    
    opticalFlow = OpticalFlow()

    while True:
        ret, img = cam.read()
         
        opticalFlow.makeOpticalFlow(img, None)
 
        ch = 0xFF & cv2.waitKey(5)
        if ch == 27:
            break
        
#     print " distance " + str(opticalFlow.euclideanDistance(194, 171 , 84, 188))


