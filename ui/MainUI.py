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


DATADIR = "E:\\python workspace\\CharlieCode\\data\\"
HCDIR = "E:\\Softwares\\opencv\\data\\haarcascades\\" 
DATADIR2 = "E:\\Softwares\\opencv\\data\\extracascades\\"


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
        self.a = Image.fromarray(self.gray_im)
        self.b = ImageTk.PhotoImage(image=self.a)
        self.canvas.create_image(0, 0, image=self.b, anchor=tk.NW)
        self.topWindow.update()
        
#         call facetracker
#         (readsuccessful, f) = self.cam2.read()
#         imageArray = f
#         imageFrame = cv.CreateImageHeader((imageArray.shape[1], imageArray.shape[0]), cv.IPL_DEPTH_8U, 3)
#         cv.SetData(imageFrame, imageArray.tostring(),
#            imageArray.dtype.itemsize * 3 * imageArray.shape[1])
#         self.tracker.detect_and_draw(imageFrame, self.cascade, self.cascade2, self.cascade3)
        
        self.topWindow.after(1, self.update_video)
        
        
    
    
    def trial(self):
        self.topWindow = tk.Tk()
        cameraIndex = 0
        cameraIndex2 = 2
        self.startVideo(cameraIndex, cameraIndex2)
#         self.callFaceTracker(cameraIndex2)
        
    def startVideo(self, cameraIndex, cameraIndex2):
        
        masterPane = tk.Frame(self.topWindow)
        masterPane.pack()
        videoframe = tk.LabelFrame(masterPane, text='Captured video')
        videoframe.grid(column=0, row=0, columnspan=1, rowspan=1, padx=5, pady=5, ipadx=5, ipady=5)

        
        self.cam = cv2.VideoCapture(cameraIndex)  # 2)
        
        CameraConstants = _CameraConstants()
        self.cam.set(cv.CV_CAP_PROP_FRAME_WIDTH, CameraConstants.cameraWidth())
        self.cam.set(cv.CV_CAP_PROP_FRAME_HEIGHT, CameraConstants.cameraHeight())
#         cv.SetCaptureProperty(self.cam, cv.CV_CAP_PROP_FRAME_WIDTH, width)
#         cv.SetCaptureProperty(self.cam, cv.CV_CAP_PROP_FRAME_HEIGHT, height) 
        
        self.canvas = tk.Canvas(videoframe, width=(CameraConstants.cameraWidth()), height=(CameraConstants.cameraHeight()))
        self.canvas.grid(column=0, row=0)

#         self.cam2 = cv2.VideoCapture(cameraIndex2) 
        
        self.topWindow.after(0, self.update_video)
        labelName = tk.Label(masterPane, text="Hello, world!")
        labelName.grid(column=0, row=3)
        
        

        path = 'E:\python workspace\CharlieCode\emoticon_smile.png'
#         image = Image.open(path)
        img = ImageTk.PhotoImage(Image.open(path))
        # panel = tk.Label(root, image = img)
        # panel.pack(side = "bottom", fill = "both", expand = "yes")
        smileButton = tk.Button(masterPane, text="Smile")
        smileButton.grid(row=1, column=1)
        sadButton = tk.Button(masterPane, text="Frown")
        sadButton.grid(row=4, column=1)
        surpriseButton = tk.Button(masterPane, text="Surprise")
        surpriseButton.grid(row=2, column=1)
        neutralButton = tk.Button(masterPane, text="Neutral")
        neutralButton.grid(row=3, column=1)
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

    def callFaceTracker(self, cameraIndex2):   
        arguments = (str(cameraIndex2))
        sys.argv = ["FaceTracker.py"] + list(arguments)
        # sys.argv = ["testing mainf"] + list(m_args)
        
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
                   
    
        if len(args) != 1:
            parser.print_help()
            sys.exit(1)
    
        # input_name = args[0]
#         if input_name.isdigit():
#             capture = cv.CreateCameraCapture(int(input_name))
#         else:
#             capture = None
    
        # cv.NamedWindow("result", 1)
        frame_copy = self.cam2.read()  # self.cam.read()
        
        
        imageArray = frame_copy[1]
        imageFrame = cv.CreateImageHeader((imageArray.shape[1], imageArray.shape[0]), cv.IPL_DEPTH_8U, 3)
        cv.SetData(imageFrame, imageArray.tostring(),
           imageArray.dtype.itemsize * 3 * imageArray.shape[1])
        # imageArray = np.zeros(())
        
        self.tracker = FaceTracker.FaceTracker()
        # print frame_copy.shape
        self.tracker.detect_and_draw(imageFrame, self.cascade, self.cascade2, self.cascade3)
#     cv2.cv.iplimage
#         if capture:
#             frame_copy = None
#             while True:
#                 frame = cv.QueryFrame(capture)
#                 if not frame:
#                     cv.WaitKey(0)
#                     break
#                 if not frame_copy:
#                     frame_copy = cv.CreateImage((frame.width,frame.height),
#                                                 cv.IPL_DEPTH_8U, frame.nChannels)
#                 if frame.origin == cv.IPL_ORIGIN_TL:
#                     cv.Copy(frame, frame_copy)
#                 else:
#                     cv.Flip(frame, frame_copy, 0)
#      
#                 FaceTracker.detect_and_draw(frame_copy, cascade, cascade2, cascade3)
#      
#                 if cv.WaitKey(10) >= 0:
#                     break
#         else:
#             image = cv.LoadImage(input_name, 1)
#             FaceTracker.detect_and_draw(image, cascade)
#             cv.WaitKey(0)
            
            
        
        # cv.DestroyWindow("result")

    def smileCharlie(self):
        print "charlie smiling!!!"
            
        
        
if __name__ == '__main__':
    call = VideoCall()
    call.trial()
#     call.callFaceTracker()
    
