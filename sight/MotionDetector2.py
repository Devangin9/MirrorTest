'''
Created on 27-Apr-2013

@author: Devangini

https://github.com/dereks/motion_tracking/blob/master/track.py

Python Motion Tracker

Reads an incoming video stream and tracks motion in real time.
Detected motion events are logged to a text file.  Also has face detection.

'''
#!/usr/bin/env python

# See also: http://sundararajana.blogspot.com/2007/05/motion-detection-using-opencv.html

import cv2.cv as cv
import cv2
import time

from scipy import *
from scipy.cluster import vq
import numpy
import sys, os, random, hashlib

# import config.CameraConstants
from config.CameraConstants import _CameraConstants

#
# BBoxes must be in the format:
# ( (topleft_x), (topleft_y) ), ( (bottomright_x), (bottomright_y) ) )
top = 0
bottom = 1
left = 0
right = 1

width = _CameraConstants().cameraWidth()
height = _CameraConstants().cameraHeight()


            




class MotionDetector:
    
    
    
    def __init__(self):
        
       
        fps = 60  # 15
        is_color = True

        self.capture = cv.CaptureFromCAM(0)
        # cv.SetCaptureProperty( self.capture, cv.CV_CAP_PROP_FRAME_WIDTH, 640 );
        # cv.SetCaptureProperty( self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 480 );
        
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_WIDTH, width);
        cv.SetCaptureProperty(self.capture, cv.CV_CAP_PROP_FRAME_HEIGHT, height);        
        
        frame = cv.QueryFrame(self.capture)
        frame_size = cv.GetSize(frame)
        
        self.writer = None        
        
        frame = cv.QueryFrame(self.capture)
        cv.NamedWindow("Target", 1)        
        
        

    def run(self):
        # Initialize
        # log_file_name = "tracker_output.log"
        # log_file = file( log_file_name, 'a' )
        
        print "hello"
        
        frame = cv.QueryFrame(self.capture)
        frame_size = cv.GetSize(frame)
        
        # Capture the first frame from webcam for image properties
        display_image = cv.QueryFrame(self.capture)
        
        # Greyscale image, thresholded to create the motion mask:
        grey_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, 1)
        
        
        # The RunningAvg() function requires a 32-bit or 64-bit image...
        running_average_image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_32F, 3)
        
        # ...but the AbsDiff() function requires matching image depths:
        running_average_in_display_color_depth = cv.CloneImage(display_image)
        
        # RAM used by FindContours():
        mem_storage = cv.CreateMemStorage(0)

        
        # The difference between the running average and the current frame:
        difference = cv.CloneImage(display_image)
        
        target_count = 1
        last_target_count = 1
        last_target_change_t = 0.0
        k_or_guess = 1
        codebook = []
        frame_count = 0
        last_frame_entity_list = []
        
        t0 = time.time()
        
        # For toggling display:
        image_list = [ "camera", "difference", "threshold", "display", "faces" ]
        image_index = 3  # Index into image_list
    
    
        # Prep for text drawing:
        text_font = cv.InitFont(cv.CV_FONT_HERSHEY_COMPLEX, .5, .5, 0.0, 1, cv.CV_AA)
        text_coord = (5, 15)
        text_color = cv.CV_RGB(255, 255, 255)

        
        
        # Set this to the max number of targets to look for (passed to k-means):
        max_targets = 5
        
        while True:
            
            # Capture frame from webcam
            camera_image = cv.QueryFrame(self.capture)
            
            frame_count += 1
            frame_t0 = time.time()
            
            # Create an image with interactive feedback:
            display_image = cv.CloneImage(camera_image)
            
            # Create a working "color image" to modify / blur
            color_image = cv.CloneImage(display_image)

            # Smooth to get rid of false positives
            cv.Smooth(color_image, color_image, cv.CV_GAUSSIAN, 19, 0)
            
            # Use the Running Average as the static background            
            # a = 0.020 leaves artifacts lingering way too long.
            # a = 0.320 works well at 320x240, 15fps.  (1/a is roughly num frames.)
            cv.RunningAvg(color_image, running_average_image, 0.320, None)
            
            # Convert the scale of the moving average.
            cv.ConvertScale(running_average_image, running_average_in_display_color_depth, 1.0, 0.0)
            
            # Subtract the current frame from the moving average.
            cv.AbsDiff(color_image, running_average_in_display_color_depth, difference)
           
            cv.ShowImage("difference ", difference)
            
            # Convert the image to greyscale.
            cv.CvtColor(difference, grey_image, cv.CV_RGB2GRAY)
            
           

            # Threshold the image to a black and white motion mask:
            cv.Threshold(grey_image, grey_image, 2, 255, cv.CV_THRESH_BINARY)
            # Smooth and threshold again to eliminate "sparkles"
            cv.Smooth(grey_image, grey_image, cv.CV_GAUSSIAN, 19, 0)
            cv.Threshold(grey_image, grey_image, 240, 255, cv.CV_THRESH_BINARY)
            
            grey_image_as_array = numpy.asarray(cv.GetMat(grey_image))
            non_black_coords_array = numpy.where(grey_image_as_array > 3)
            # Convert from numpy.where()'s two separate lists to one list of (x, y) tuples:
            non_black_coords_array = zip(non_black_coords_array[1], non_black_coords_array[0])
            
            
#             cv.SegmentMotion(non_black_coords_array, None, storage, timestamp, seg_thresh)
            
            # print "min_size is: " + str(min_size)
            # Listen for ESC or ENTER key
            c = cv.WaitKey(7) % 0x100
            if c == 27 or c == 10:
                break
            
            # Toggle which image to show
#             if chr(c) == 'd':
#                 image_index = ( image_index + 1 ) % len( image_list )
#             
#             image_name = image_list[ image_index ]
#             
#             # Display frame to user
#             if image_name == "camera":
#                 image = camera_image
#                 cv.PutText( image, "Camera (Normal)", text_coord, text_font, text_color )
#             elif image_name == "difference":
#                 image = difference
#                 cv.PutText( image, "Difference Image", text_coord, text_font, text_color )
#             elif image_name == "display":
#                 image = display_image
#                 cv.PutText( image, "Targets (w/AABBs and contours)", text_coord, text_font, text_color )
#             elif image_name == "threshold":
#                 # Convert the image to color.
#                 cv.CvtColor( grey_image, display_image, cv.CV_GRAY2RGB )
#                 image = display_image  # Re-use display image here
#                 cv.PutText( image, "Motion Mask", text_coord, text_font, text_color )
#             elif image_name == "faces":
#                 # Do face detection
#                 detect_faces( camera_image, haar_cascade, mem_storage )                
#                 image = camera_image  # Re-use camera image here
#                 cv.PutText( image, "Face Detection", text_coord, text_font, text_color )
#             cv.ShowImage( "Target", image )
                
                
            image1 = display_image
        
            cv.ShowImage("Target 1", image1)
            
            
#             if self.writer: 
#                 cv.WriteFrame( self.writer, image );
            
            # log_file.flush()
            
            # If only using a camera, then there is no time.sleep() needed, 
            # because the camera clips us to 15 fps.  But if reading from a file,
            # we need this to keep the time-based target clipping correct:
            frame_t1 = time.time()
            

            # If reading from a file, put in a forced delay:
            if not self.writer:
                delta_t = frame_t1 - frame_t0
                if delta_t < (1.0 / 15.0): time.sleep((1.0 / 15.0) - delta_t)
                
                
        t1 = time.time()
        time_delta = t1 - t0
        processed_fps = float(frame_count) / time_delta
        print "Got %d frames. %.1f s. %f fps." % (frame_count, time_delta, processed_fps)
        
if __name__ == "__main__":
    t = MotionDetector()
#    import cProfile
#    cProfile.run( 't.run()' )
    t.run()
