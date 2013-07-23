'''
Created on 08-Jul-2013

@author: Devangini
'''
import numpy as np
import cv2.cv as cv
# vector<Point3f > modelPoints;
# modelPoints.push_back(Point3f(-36.9522f,39.3518f,47.1217f));    //l eye
# modelPoints.push_back(Point3f(35.446f,38.4345f,47.6468f));              //r eye
# modelPoints.push_back(Point3f(-0.0697709f,18.6015f,87.9695f)); //nose
# modelPoints.push_back(Point3f(-27.6439f,-29.6388f,73.8551f));   //l mouth
# modelPoints.push_back(Point3f(28.7793f,-29.2935f,72.7329f));    //r mouth
# modelPoints.push_back(Point3f(-87.2155f,15.5829f,-45.1352f));   //l ear
# modelPoints.push_back(Point3f(85.8383f,14.9023f,-46.3169f));    //r ear
 
a = (1, 2)
point2 = [-36.9522,39.3518,47.1217]
arrayPoints = np.array(point2)

np.append(arrayPoints, point2 , 0)

mat = cv.fromarray(arrayPoints)
# op = Mat(modelPoints);
# op = op / 35; //just a little normalization...
# rvec = Mat(rv);
# double _d[9] = {1,0,0,
#           0,-1,0,
#          0,0,-1}; //rotation: looking at -z axis
# Rodrigues(Mat(3,3,CV_64FC1,_d),rvec);
# tv[0]=0;tv[1]=0;tv[2]=1;
# tvec = Mat(tv);
# double _cm[9] = { 20, 0, 160,
#            0, 20, 120,
#              0,  0,   1 };  //"calibration matrix": center point at center of picture with 20 focal length.
# camMatrix = Mat(3,3,CV_64FC1,_cm);