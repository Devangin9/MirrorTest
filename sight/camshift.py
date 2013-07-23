# /usr/bin/env python

'''
Camshift tracker
================

This is a demo that shows mean-shift based tracking
You select a color objects such as your face and it tracks it.
This reads from video camera (0 by default, or the camera number the user enters)

http://www.robinhewitt.com/research/track/camshift.html

Usage:
------
    camshift.py [<video source>]

    To initialize tracking, select the object with mouse

Keys:
-----
    ESC   - exit
    b     - toggle back-projected probability visualization
'''

import numpy as np
import cv2
import video
import cv2.cv as cv
from sight.MotionDetector3 import MotionDetector
from config.CameraConstants import _CameraConstants
import math
import time

CameraConstants = _CameraConstants()
width = CameraConstants.cameraWidth()
height = CameraConstants.cameraHeight()

class Camshift(object):
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH , width);
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT , height);    
        
        ret, self.frame = self.cam.read()
        cv2.namedWindow('camshift')
        cv2.setMouseCallback('camshift', self.onmouse)

        self.selection = None
        self.drag_start = None
        self.tracking_state = 0
        self.show_backproj = False
        self.returnToDetection = False
        self.MotionDetector = MotionDetector()
        cvmat = cv.fromarray(self.frame)
        self.MotionDetector.initialize(cvmat)
        
#     def __init__(self, video_src):
#         self.cam = video.create_capture(video_src)
#         ret, self.frame = self.cam.read()
#         cv2.namedWindow('camshift')
#         cv2.setMouseCallback('camshift', self.onmouse)
# 
#         self.selection = None
#         self.drag_start = None
#         self.tracking_state = 0
#         self.show_backproj = False

    def onmouse(self, event, x, y, flags, param):
        x, y = np.int16([x, y])  # BUG
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
            self.tracking_state = 0
        if self.drag_start:
            if flags & cv2.EVENT_FLAG_LBUTTON:
                h, w = self.frame.shape[:2]
                xo, yo = self.drag_start
                x0, y0 = np.maximum(0, np.minimum([xo, yo], [x, y]))
                x1, y1 = np.minimum([w, h], np.maximum([xo, yo], [x, y]))
                self.selection = None
                if x1 - x0 > 0 and y1 - y0 > 0:
                    self.selection = (x0, y0, x1, y1)
            else:
                self.drag_start = None
                if self.selection is not None:
                    self.tracking_state = 1
                    
    def defineRegionOfInterest(self, image, pt1, pt2):
        x0 = pt1[0]
        y0 = pt1[1]
        x1 = pt2[0]
        y1 = pt2[1]
        self.selection = (x0, y0, x1, y1)
        
        image_mat = cv.GetMat(image)
        image_array = np.asarray(image_mat, np.uint8, 3)
        self.processObjectOfInterest(image_array)
        
        
        if self.returnToDetection:
            return

    def show_hist(self):
        bin_count = self.hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count * bin_w, 3), np.uint8)
        for i in xrange(bin_count):
            h = int(self.hist[i])
            cv2.rectangle(img, (i * bin_w + 2, 255), ((i + 1) * bin_w - 2, 255 - h), (int(180.0 * i / bin_count), 255, 255), -1)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)
        
    def trackScene(self):
        while True:
            ret, self.frame = self.cam.read()
            
            if self.tracking_state == 1:
                self.findObjectOfInterest(self.frame)
                if self.returnToDetection:
                    return
                
            cv2.imshow('camshift', self.vis)

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            if ch == ord('b'):
                self.show_backproj = not self.show_backproj
        cv2.destroyAllWindows()

    def run(self):
        while True:
            ret, self.frame = self.cam.read()
            
            if self.selection:
                self.processObjectOfInterest(self.frame)
            if self.tracking_state == 1:
                self.findObjectOfInterest(self.frame)
                
            cv2.imshow('camshift', self.vis)
            
            time.sleep(5)

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            if ch == ord('b'):
                self.show_backproj = not self.show_backproj
        cv2.destroyAllWindows()
    
    def processObjectOfInterest(self, image):
        
        self.vis = image.copy()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))
        
        print "going 1"
        x0, y0, x1, y1 = self.selection
        self.track_window = (x0, y0, x1 - x0, y1 - y0)
        hsv_roi = hsv[y0:y1, x0:x1]
        mask_roi = mask[y0:y1, x0:x1]
        hist = cv2.calcHist([hsv_roi], [0], mask_roi, [16], [0, 180])
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX);
        self.hist = hist.reshape(-1)
        self.show_hist()

        vis_roi = self.vis[y0:y1, x0:x1]
        cv2.bitwise_not(vis_roi, vis_roi)
        self.vis[mask == 0] = 0
        
        self.selection = None
        self.tracking_state = 1
        
        
#         self.trackScene()
#         if self.returnToDetection:
#             return
        
        
    def findObjectOfInterest(self, image):
        self.vis = image.copy()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

#         if self.selection:
#             print "going 1"
#             x0, y0, x1, y1 = self.selection
#             self.track_window = (x0, y0, x1 - x0, y1 - y0)
#             hsv_roi = hsv[y0:y1, x0:x1]
#             mask_roi = mask[y0:y1, x0:x1]
#             hist = cv2.calcHist([hsv_roi], [0], mask_roi, [16], [0, 180])
#             cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX);
#             self.hist = hist.reshape(-1)
#             self.show_hist()
# 
#             vis_roi = vis[y0:y1, x0:x1]
#             cv2.bitwise_not(vis_roi, vis_roi)
#             vis[mask == 0] = 0

#         if self.tracking_state == 1:
#         print "going 2"
        self.selection = None
        prob = cv2.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
        prob &= mask
        term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
#         print "input tracking window " + str(self.track_window)
        if self.track_window[2] == 0 or self.track_window[3] == 0:
            # fall back to detection
            print "returning"
            self.returnToDetection = True
            return
        else:
            track_box, self.track_window = cv2.CamShift(prob, self.track_window, term_crit)
    
            if self.show_backproj:
                self.vis[:] = prob[..., np.newaxis]

            width = track_box[1][0]
            height = track_box[1][1]
            center = (int(track_box[0][0]), int(track_box[0][1]))
            angle = track_box[2]
#             cv2.rectangle(self.vis, point1, point2, (0, 255, 0), 2)            
#             cv2.ellipse(self.vis, track_box, (0, 0, 255), 2)
#             cv2.putText(self.vis, str(angle), (100, 100), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (255, 255, 0))
#             cv2.line(self.vis, center, extrema, (0, 0, 255), 3)
            
            print "track box " + str(track_box)
    
            originalArray2 = cv.CloneMat(cv.fromarray(self.vis))
            shape = np.shape(originalArray2)           
            if angle < 180:
                rotateAngle = angle + 360
            else:
                rotateAngle = 180 + angle
            
            rotationMatrix = cv2.getRotationMatrix2D(center, rotateAngle , 1)
            shape = np.shape(self.vis)
            print shape[0 : 2]
            faceArray = np.zeros( shape[0:2], np.uint8, 3)
            faceArray2 = np.zeros((track_box[1][0], track_box[1][1]), np.uint8, 3)
            faceArray = cv2.warpAffine(self.vis, rotationMatrix, np.shape(faceArray), flags=cv2.INTER_LINEAR)
            faceArray2 = cv2.getRectSubPix(faceArray, np.shape(faceArray2), track_box[0])

            cv2.imshow("face image", faceArray2)
            
            return faceArray2
#             self.MotionDetector.iterativeMotionDetector(cv.fromarray(faceArray2))
            

        

if __name__ == '__main__':
    import sys
    try: video_src = 0
    except: video_src = 0
    print __doc__
    Camshift().run()

