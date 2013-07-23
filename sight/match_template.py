'''
Created on 10-Jul-2013

@author: Devangini

https://gist.github.com/moshekaplan/5080519
'''
import cv2
from cv2 import cv
from config.CameraConstants import _CameraConstants

method = cv.CV_TM_SQDIFF_NORMED

CameraConstants = _CameraConstants()
width = CameraConstants.cameraWidth()
height = CameraConstants.cameraHeight()

class MatchTemplate:
    
    def __init__(self):
        self.template_name = None
        self.cam = cv2.VideoCapture(0)
        
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH , width)
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT , height)

    def defineTargetImage(self, image):
        self.template_name = image
    
    def matchTemplate(self, haystack):



# template_name = "mozicon128.png"
# image_name = "test2.jpeg"

        # Load
        needle = cv2.imread(template_name)
        
        
        # Convert to gray:
#         needle_g = cv2.cvtColor(needle, cv2.CV_32FC1) 
        needle_g = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY) 
        
#         haystack_g = cv2.cvtColor(haystack, cv2.CV_32FC1) 
        
        # Attempt match
        d = cv2.matchTemplate(needle_g, haystack, cv2.cv.CV_TM_SQDIFF_NORMED)
         
        # we want the minimum squared difference
        mn, _, mnLoc, _ = cv2.minMaxLoc(d)
        
        # Print it, for comparison
        print mn
        
        # Draw the rectangle
        MPx, MPy = mnLoc
        
        trows, tcols = needle_g.shape[:2]
        
        # Normed methods give better results, ie matchvalue = [1,3,5], others sometimes shows errors
        cv2.rectangle(haystack, (MPx, MPy), (MPx + tcols, MPy + trows), (0, 0, 255), 2)
        
        cv2.imshow('output', haystack)
        
#         cv2.waitKey(0)
#         import sys
#         sys.exit(0)
        
    def findInVideoSequence(self):
        while True:
            ret, self.frame = self.cam.read()
            
            if ret:
                image = self.frame.copy()
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                cv2.imshow("input ", image)
#                 cv2.imwrite("face4.png", image)
                self.matchTemplate(image) 
            

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
        cv2.destroyAllWindows()

if __name__ == '__main__':
    template_name = "E:\\python workspace\\CharlieCode\\face1.png"
    image_name = "E:\\python workspace\\CharlieCode\\face5.png"
    
    matcher = MatchTemplate()
    
    matcher.defineTargetImage(template_name)
    
#     haystack = cv2.imread(image_name)
#     matcher.matchTemplate(haystack)

    matcher.findInVideoSequence()
    
