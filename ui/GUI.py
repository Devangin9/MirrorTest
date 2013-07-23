'''
Created on 09-May-2013

@author: Devangini
'''
import sys
from optparse import OptionParser
import expressionreco.FaceTracker
import cv2
import cv2.cv as cv
from expressionreco import FaceTracker
import Tkinter as tk 
from PIL import Image, ImageTk
from ttk import Style
from Tkconstants import BOTH
from config.CameraConstants import _CameraConstants
import numpy as np
from Tkinter import StringVar
from sight.camshift import Camshift


DATADIR = "E:\\python workspace\\CharlieCode\\data\\"
HCDIR = "E:\\Softwares\\opencv\\data\\haarcascades\\" 
DATADIR2 = "E:\\Softwares\\opencv\\data\\extracascades\\"

CameraConstants = _CameraConstants()


class VideoCall:
    
    def openCallWindow(self, topWindow):
        print "open call window"
        self.topWindow = topWindow
        self.frame = tk.Frame(topWindow)
        self.topWindow.title("Charlie : UI")
        
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        self.frame.grid()
        cameraIndex = 0
        cameraIndex2 = 2
#         RecordAndPlay.recordAndPlay()
        self.startVideo(cameraIndex, cameraIndex2)
        self.callFaceTracker(cameraIndex2)
        
       
        
    
    def update_video(self):
        (self.readsuccessful, self.f) = self.cam.read()
        
        self.gray_im = cv2.cvtColor(self.f, cv2.COLOR_RGB2BGRA)
        # self.gray_im = cv2.cvtColor(self.f, cv2.COLOR_RGB2GRAY)
        
#         print "needed type " + str(type(self.gray_im))
        self.a = Image.fromarray(self.gray_im)
        self.b = ImageTk.PhotoImage(image=self.a)

        self.canvas.create_image(0, 0, image=self.b, anchor=tk.NW)
        
        self.canvas.update()

        if self.state == 0:
            self.callFaceTracker(self.f)
        elif self.state == 1:
            faceArray = self.camshift.findObjectOfInterest(self.f)
            a = Image.fromarray(faceArray)
            b = ImageTk.PhotoImage(image=a)
            self.canvas2.create_image(0, 0, image=b, anchor=tk.NW)
            self.canvas2.update()
        
        self.topWindow.after(1, self.update_video)
        
        
    
    
    def trial(self):
        self.topWindow = tk.Tk()
        cameraIndex = 0
        cameraIndex2 = 2
        self.tracker = FaceTracker.FaceTracker()
        self.startVideo(cameraIndex, cameraIndex2)
        
#         self.callFaceTracker(cameraIndex2)
        
    def startVideo(self, cameraIndex, cameraIndex2):
        
        self.masterPane = tk.Frame(self.topWindow)
        self.masterPane.pack()
        
        self.cam = cv2.VideoCapture(cameraIndex)  # 2)
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, CameraConstants.cameraWidth())
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, CameraConstants.cameraHeight())
        
        videoframe = tk.LabelFrame(self.masterPane, text='Captured video')
        videoframe.grid(column=0, row=0, columnspan=1, rowspan=1, padx=5, pady=5, ipadx=5, ipady=5)

        self.canvas = tk.Canvas(videoframe, width=(CameraConstants.cameraWidth()), height=(CameraConstants.cameraHeight()))
        self.canvas.grid(column=0, row=0)
        
        
        self.state = 0
        self.textVar = StringVar() 
        labelName = tk.Label(self.masterPane, textvariable=self.textVar)  # tk.Label(masterPane, text="Phase : None")
        self.textVar.set("state: Starting...")
        labelName.grid(column=1, row=0)
        
        
        videoframe2 = tk.LabelFrame(self.masterPane, text='Processed video 1')
        videoframe2.grid(column=0, row=1, columnspan=1, rowspan=1, padx=5, pady=5, ipadx=5, ipady=5)

        self.canvas2 = tk.Canvas(videoframe2, width=(CameraConstants.cameraWidth()), height=(CameraConstants.cameraHeight()))
        self.canvas2.grid(column=0, row=0)
        
#         videoframe3 = tk.LabelFrame(self.masterPane, text='Processed video 2')
#         videoframe3.grid(column=1, row=1, columnspan=1, rowspan=1, padx=5, pady=5, ipadx=5, ipady=5)
# 
#         self.canvas3 = tk.Canvas(videoframe2, width=(CameraConstants.cameraWidth()), height=(CameraConstants.cameraHeight()))
#         self.canvas3.grid(column=0, row=0)
            
            
            
        self.topWindow.after(0, self.update_video)
        

#         path = 'E:\python workspace\CharlieCode\emoticon_smile.png'
# #         image = Image.open(path)
#         img = ImageTk.PhotoImage(Image.open(path))
#         # panel = tk.Label(root, image = img)
#         # panel.pack(side = "bottom", fill = "both", expand = "yes")
#         smileButton = tk.Button(self.masterPane, text="Smile")
#         smileButton.grid(row=1, column=1)
#         sadButton = tk.Button(self.masterPane, text="Frown")
#         sadButton.grid(row=4, column=1)
#         surpriseButton = tk.Button(self.masterPane, text="Surprise")
#         surpriseButton.grid(row=2, column=1)
#         neutralButton = tk.Button(self.masterPane, text="Neutral")
#         neutralButton.grid(row=3, column=1)
#         photo = ImageTk.PhotoImage(image)
#         smileButton = tk.Button(self.topWindow, image=photo, \
#                                      command=self.smileCharlie)
#         
#         smileButton.grid(row=0, column=4)
#         label = tk.Label(self.topWindow, image=photo)
#         label.image = photo # keep a reference!
#         label.grid(row = 4, column = 1)
        # label.pack()
        
        self.topWindow.mainloop()
        del self.cam

    def callFaceTracker(self, imageFrame):   
        
        imageMat = cv.fromarray(imageFrame)
        image = cv.GetImage(imageMat)
        (isFaceDetected, detectedFaceImage, wholeImage, pt1, pt2) = self.tracker.detect_and_draw(image)
        
        if isFaceDetected:
            
            array = np.asarray(detectedFaceImage, np.uint8, 3)
            arrayCopy = array.copy()
            cv2.imshow("face image ", arrayCopy)
#             print "got type " + str(type(arrayCopy))
            a = Image.fromarray(arrayCopy)
            b = ImageTk.PhotoImage(image=a)
            
            self.canvas2.create_image(0, 0, image=b, anchor=tk.NW)
            self.canvas2.update()
            
            print "here....."
            
            self.goToNextState(True)
            
            originalImage2 = cv.CloneImage(wholeImage)
            self.camshift = Camshift()
            self.camshift.defineRegionOfInterest(originalImage2, pt1, pt2)
    

    def goToNextState(self, isNext):
        if isNext:
            if self.state == 0:
                self.state = 1
                self.textVar.set("state : tracking faces")
        else:
            if self.state == 1:
                self.state = 0
                self.textVar.set("state : detecting faces...")

    def smileCharlie(self):
        print "charlie smiling!!!"
            
        
        
if __name__ == '__main__':
    call = VideoCall()
    call.trial()
#     call.callFaceTracker()
    
