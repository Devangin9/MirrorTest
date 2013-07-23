'''
Created on 28-Apr-2013

@author: Devangini

http://www.neuroforge.co.uk/index.php/77-tutorials/79-stereo-vision-tutorial

http://stackoverflow.com/questions/6241607/distance-to-the-object-using-stereo-camera

'''

import cv2.cv as cv
import numpy as np
import cv2

            
columns = 9
rows = 6
nimages = 5
num_pts = columns * rows


dims = (columns, rows)
width = 480
height = 320



ply_header = '''ply
format ascii 1.0
element vertex %(vert_num)d
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
'''

def write_ply(fn, verts, colors):
    verts = verts.reshape(-1, 3)
    colors = colors.reshape(-1, 3)
    verts = np.hstack([verts, colors])
    with open(fn, 'w') as f:
        f.write(ply_header % dict(vert_num=len(verts)))
        np.savetxt(f, verts, '%f %f %f %d %d %d')
            
class StereoVision:
    
   
    
    
    def startCameras(self):
        
        self.video1 = cv.CaptureFromCAM(0)
        cv.SetCaptureProperty(self.video1, cv.CV_CAP_PROP_FRAME_WIDTH, width)
        cv.SetCaptureProperty(self.video1, cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        
        self.video2 = cv.CaptureFromCAM(1)
        cv.SetCaptureProperty(self.video2, cv.CV_CAP_PROP_FRAME_WIDTH, width)
        cv.SetCaptureProperty(self.video2, cv.CV_CAP_PROP_FRAME_HEIGHT, height)
    
    def collectCheckboardPoints(self):
        
        self.pointsArray1 = np.zeros((nimages, num_pts, 2)) 
        self.pointsArray2 = np.zeros((nimages, num_pts, 2)) 

        cv.NamedWindow("camera")
        cv.NamedWindow("camera2")
        
      
        i = 0
        while True :
            frame = cv.QueryFrame(self.video1)
        #     print type(frame)
        #     [rows1, cols] = cv.GetSize(frame)
            image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, frame.nChannels)        
            cv.Copy(frame, image)
            cv.ShowImage("camera", frame)
            grayScaleFullImage = cv.CreateImage((image.width, image.height), 8, 1)
            cv.CvtColor(image, grayScaleFullImage, cv.CV_BGR2GRAY)
            
            frame2 = cv.QueryFrame(self.video2)
            image2 = cv.CreateImage(cv.GetSize(frame2), cv.IPL_DEPTH_8U, frame2.nChannels)        
            cv.Copy(frame2, image2)
            cv.ShowImage("camera2", frame2)
            grayScaleFullImage2 = cv.CreateImage((image2.width, image2.height), 8, 1)
            cv.CvtColor(image2, grayScaleFullImage2, cv.CV_BGR2GRAY)
             
             
            found, points = cv.FindChessboardCorners(grayScaleFullImage, dims, cv.CV_CALIB_CB_ADAPTIVE_THRESH)
            if found != 0:
                print "found chess board " + str(np.shape(points))
                cv.DrawChessboardCorners(image, dims, points, found)
                cv.ShowImage("win2", image)
                cv.WaitKey(2)
        #     else:
        #         print "no chess"
            found2, points2 = cv.FindChessboardCorners(grayScaleFullImage2, dims, cv.CV_CALIB_CB_ADAPTIVE_THRESH)
            if found2 != 0:
                print "found chess board2"
                cv.DrawChessboardCorners(image2, dims, points2, found2)
                cv.ShowImage("win3", image2)
                cv.WaitKey(2)
        
            if found and found2:
                
                print "entered here!!!!!"
               
                self.pointsArray1[i, :] = points
                self.pointsArray2[i, :] = points2
                i = i + 1
                
            if i == nimages:
                self.size = cv.GetSize(image)
                break
            
            if cv.WaitKey(10) == 27:
                break 
        
        cv.DestroyWindow("Camera 1")
        cv.DestroyWindow("Camera 2")
        
#         del(self.video1)
#         del(self.video2)
        
        
            
            
            
    def stereoCalibrate(self):
        print " rows " + str(rows)
        print "columns " + str(columns)
        print "points " + str(num_pts)
        #         nimages = 8
        #         num_pts = 5
        
        #       (CV_MAT_DEPTH(_imagePoints1->type) == CV_32F || CV_MAT_DEPTH(_imagePoints1->type) == CV_64F) 
        #         && ((_imagePoints1->rows == pointsTotal && _imagePoints1->cols*cn == 2) || 
        #               (_imagePoints1->rows == 1 && _imagePoints1->cols == pointsTotal && cn == 2)) 
        
        #       CV_32FC1 == CV_32F, CV_32FC2 == CV_32FC(2) == CV_MAKETYPE(CV_32F, 2), and CV_MAKETYPE(depth, n) == ((x&7)<<3) + (n-1). 
        #       This means that the constant type is formed from the depth, taking the lowest 3 bits, and the number of channels minus 1,
        #       taking the next log2(CV_CN_MAX) bits.
        opts = cv.CreateMat(nimages * num_pts, 3, cv.CV_32FC1)
        ipts1 = cv.CreateMat(nimages * num_pts, 2, cv.CV_32F)
        ipts2 = cv.CreateMat(nimages * num_pts, 2, cv.CV_32F)
        #         ipts1 = cv.CreateMat(nimages * num_pts, 2, cv.CV_32F)
        #         ipts2 = cv.CreateMat(nimages * num_pts, 2, cv.CV_32F)
        npts = cv.CreateMat(nimages, 1, cv.CV_32SC1)
        for i in range(0, nimages):
            npts[i, 0] = num_pts
          
        # Create first Intrinsic Camera Matrix and Distortion Matrix
        intrinsics1 = cv.CreateMat(3, 3, cv.CV_64FC1)
        distortion1 = cv.CreateMat(4, 1, cv.CV_64FC1)
          
        cv.SetZero(intrinsics1)
        cv.SetZero(distortion1)
        intrinsics1[0, 0] = 1.0
        intrinsics1[1, 1] = 1.0
          
        # Create second Intrinsic Camera Matrix and Distortion Matrix
        intrinsics2 = cv.CreateMat(3, 3, cv.CV_64FC1)
        distortion2 = cv.CreateMat(4, 1, cv.CV_64FC1)
          
        cv.SetZero(intrinsics2)
        cv.SetZero(distortion2)
        # focal lengths have 1/1 ratio
        intrinsics2[0, 0] = 1.0
        intrinsics2[1, 1] = 1.0
        
        # CV_64F CV_32FC1 
        R = cv.CreateMat(3, 3, cv.CV_64F)
        T = cv.CreateMat(3, 1, cv.CV_64F)
        E = cv.CreateMat(3, 3, cv.CV_64F)
        F = cv.CreateMat(3, 3, cv.CV_64F)
        
        
        #         print type(points)
        #         imagePoints1 = np.asarray(points, np.uint8 , 3) 
        #         imagePoints2 = np.asarray(points2, np.uint8, 3)
        #         print "HERE " + str(type(imagePoints2))
        #         imagePoints11 = imagePoints1.T
        #         imagePoints22 = imagePoints2.T
        #         imagePoints111 = cv.fromarray(imagePoints11)
        #         imagePoints222 = cv.fromarray(imagePoints22)
        
        print np.shape(opts)
#         print np.shape(points)
        print np.shape(self.pointsArray1)
        print type(self.pointsArray2)
        
        for k in range(0, nimages):
            for i in range(0, columns):
                for j in range(0, rows):
                    print (j * columns + i)
                    opts[k * num_pts + j * columns + i, 0] = j * 10
                    opts[k * num_pts + j * columns + i, 1] = i * 10
                    opts[k * num_pts + j * columns + i, 2] = 0
                    ipts1[k * num_pts + j * columns + i, 0] = self.pointsArray1[k, j * columns + i][0]
                    ipts1[k * num_pts + j * columns + i, 1] = self.pointsArray1[k, j * columns + i][1]
                    ipts2[k * num_pts + j * columns + i, 0] = self.pointsArray2[k, j * columns + i][0]
                    ipts2[k * num_pts + j * columns + i, 1] = self.pointsArray2[k, j * columns + i][1]
                
                
        
                
        #         print np.shape(imagePoints111)
        
        # cv.StereoCalibrate(objectPoints, imagePoints1, imagePoints2, pointCounts, cameraMatrix1, distCoeffs1, cameraMatrix2, distCoeffs2, imageSize, R, T, E=None, F=None, term_crit=(CV_TERMCRIT_ITER+CV_TERMCRIT_EPS, 30, 1e-6), flags=CV_CALIB_FIX_INTRINSIC) 
        cv.StereoCalibrate(opts, ipts1, ipts2 , npts, intrinsics1, distortion1, intrinsics2, distortion2, self.size, R, T, E, F, (cv.CV_TERMCRIT_ITER + cv.CV_TERMCRIT_EPS, 30, 1e-6), cv.CV_CALIB_FIX_INTRINSIC)
        
        size = self.size
        R1 = cv.CreateMat(3, 3, cv.CV_64F)
        R2 = cv.CreateMat(3, 3, cv.CV_64F)
        P1 = cv.CreateMat(3, 4, cv.CV_64F)
        P2 = cv.CreateMat(3, 4, cv.CV_64F)
        self.Q = cv.CreateMat(4, 4, cv.CV_64F)
        (roi1, roi2) = cv.StereoRectify(intrinsics1, intrinsics2, distortion1, distortion2, size, R , T, R1, R2, P1, P2, self.Q)
        
        [mat_w, mat_h] = self.size
          
        self.map1x = cv.CreateMat(mat_h, mat_w, cv.CV_32FC1)
        self.map2x = cv.CreateMat(mat_h, mat_w, cv.CV_32FC1)
        # Right maps
        self.map1y = cv.CreateMat(mat_h, mat_w, cv.CV_32FC1)
        self.map2y = cv.CreateMat(mat_h, mat_w, cv.CV_32FC1)
        # cv.InitUndistortMap(intrinsics, distortion, mapx, mapy)
        cv.InitUndistortRectifyMap(intrinsics1, distortion1, R1, P1, self.map1x, self.map1y)
        cv.InitUndistortRectifyMap(intrinsics2, distortion2, R2, P2, self.map2x, self.map2y)       
    
    # Left maps
    #         mat_h = height
    #         mat_w = width
    
    def getDepth(self, image, image2):
          
        grayScaleFullImage = cv.CreateImage((image.width, image.height), 8, 1)
        cv.CvtColor(image, grayScaleFullImage, cv.CV_BGR2GRAY)
        
        grayScaleFullImage2 = cv.CreateImage((image2.width, image2.height), 8, 1)
        cv.CvtColor(image2, grayScaleFullImage2, cv.CV_BGR2GRAY)
           
        [mat_w, mat_h] = self.size
        
        r = cv.CreateMat(mat_h, mat_w, cv.CV_8UC1)
        r2 = cv.CreateMat(mat_h, mat_w, cv.CV_8UC1)
        print type(r)
        print type(image)
        print type(self.map1x)
        print cv.GetSize(r)
        print cv.GetSize(self.map1x)
        cv.Remap(grayScaleFullImage, r, self.map1x, self.map1y)
        cv.Remap(grayScaleFullImage2, r2, self.map2x, self.map2y)
        
        cv.ShowImage("win3", r)
        cv.ShowImage("win4", r2)
        
        
        #stereo_match that comes in opencv
        
        # disparity range is tuned for 'aloe' image pair
        window_size = 3
        min_disp = 16
        num_disp = 112 - min_disp
        stereo = cv2.StereoSGBM(minDisparity=min_disp,
            numDisparities=num_disp,
            SADWindowSize=window_size,
            uniquenessRatio=10,
            speckleWindowSize=100,
            speckleRange=32,
            disp12MaxDiff=1,
            P1=8 * 3 * window_size ** 2,
            P2=32 * 3 * window_size ** 2,
            fullDP=False
        )
    
        print 'computing disparity...'
        disp = stereo.compute(np.asarray(r), np.asarray(r2)).astype(np.float32) / 16.0
    
        print 'generating 3d point cloud...'
        points = cv2.reprojectImageTo3D(disp, np.asarray(self.Q))
        
        
        colors = cv2.cvtColor(np.asarray(r), cv2.COLOR_GRAY2RGB)
        mask = disp > disp.min()
        out_points = points[mask]
        out_colors = colors[mask]
        # Resulting .ply file cam be easily viewed using MeshLab ( http://meshlab.sourceforge.net
        out_fn = 'out.ply'
        write_ply('out.ply', out_points, out_colors)
        print '%s saved' % 'out.ply'
    

        cv2.imshow('disparity', (disp - min_disp) / num_disp)
        
            
            
        
        
        # Once you're calibrated, you're ready to go. 
        # From here you can create a depth map. This will be covered in a Stereo Correspondence article. 
        # As a hint, you need both the left and right rectified images, which will be passed to your 
        # favourite Stereo Correspodance function to produce a disparity map. 
        # Effectively a depth map without a Kinect..... take that Microsoft.... also see our Kinect tutorials.. :-)
            
        
        


        
if __name__ == "__main__":
    t = StereoVision()
    t.startCameras()
    t.collectCheckboardPoints()
    t.stereoCalibrate()
    
    while True :
        frame = cv.QueryFrame(t.video1)
    #     print type(frame)
    #     [rows1, cols] = cv.GetSize(frame)
        image = cv.CreateImage(cv.GetSize(frame), cv.IPL_DEPTH_8U, frame.nChannels)        
        cv.Copy(frame, image)
        cv.ShowImage("camera", frame)
        
        
        frame2 = cv.QueryFrame(t.video2)
        image2 = cv.CreateImage(cv.GetSize(frame2), cv.IPL_DEPTH_8U, frame2.nChannels)        
        cv.Copy(frame2, image2)
        cv.ShowImage("camera2", frame2)
       

        t.getDepth(image, image2)
        
        if cv.WaitKey(10) == 27:
            break 
        
        
        
#    import cProfile
#    cProfile.run( 't.run()' )
    t.run()
