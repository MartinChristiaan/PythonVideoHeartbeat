
import argparse
import time
import dlib
import cv2
import keyboard
import numpy as np
def rect_to_bb(rect):
	# take a bounding predicted by dlib and convert it
	# to the format (x, y, w, h) as we would normally do
	# with OpenCV
	x = rect.left()
	y = rect.top()
	w = rect.right() - x
	h = rect.bottom() - y
 
	# return a tuple of (x, y, w, h)
	return (x, y, w, h)

def shape_to_np(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((68, 2), dtype=dtype)
 
	# loop over the 68 facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, 68):
		coords[i] = (shape.part(i).x, shape.part(i).y)
 
	# return the list of (x, y)-coordinates
	return coords

class LandmarkDetecter():
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("predictor.dat")
        
    def detect(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = self.detector(gray, 0)
        for rect in rects:
            # compute the bounding box of the face and draw it on the
            # frame
            (bX, bY, bW, bH) = rect_to_bb(rect)
            cv2.rectangle(frame, (bX, bY), (bX + bW, bY + bH),
                (0, 255, 0), 1)
    
            # determine the facial landmarks for the face region, then
            # convert the facial landmark (x, y)-coordinates to a NumPy
            # array
            shape = self.predictor(gray, rect)
            shape = shape_to_np(shape)
    
            # loop over the (x, y)-coordinates for the facial landmarks
            # and draw each of them
            for (i, (x, y)) in enumerate(shape):
                cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
               # cv2.putText(frame, str(i + 1), (x - 10, y - 10),
               #     cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

def mean_pos(points):
    x_mean = np.mean(points[:,0,0])
    y_mean = np.mean(points[:,0,1])
    return x_mean,y_mean

import math
def dist(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    dx2 = (x1-x2)*(x1-x2)
    dy2 = (y1-y2)*(y1-y2)
    return math.sqrt(dx2+dy2)

class LandmarkTracker():
    def __init__(self):
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("predictor.dat")
        self.started_tracking = False
        self.shape = []
        self.prev_gray = []
        self.lk_params = dict( winSize  = (15,15),maxLevel = 2,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.cnt = 0
    def mark_landmarks(self,frame):
        eyel = self.points[:5]
        eyer = self.points[6:11]
        mouth = self.points[11:] 
        for i in range(eyel.shape[0]):
            col =  (0, 0, 255)   
            cv2.circle(frame, (eyel[i,0,0], eyel[i,0,1]), 1, col, -1)
        for i in range(eyer.shape[0]):
            col =  (0, 255,0)
            cv2.circle(frame, (eyer[i,0,0], eyer[i,0,1]), 1, col, -1)
        for i in range(mouth.shape[0]):
            col =  (255, 0, 0)         
            cv2.circle(frame, (mouth[i,0,0], mouth[i,0,1]), 1, col, -1)
        peyel = mean_pos(eyel)
        peyer = mean_pos(eyer)
        pmouth = mean_pos(mouth)
        
        cv2.line(frame,peyel,peyer,(255,0,0),1)            
        cv2.line(frame,peyel,pmouth,(255,0,0),1)            
        cv2.line(frame,peyer,pmouth,(255,0,0),1)

  
              # b = dist(peyel,peyer)/2
            # c = dist(peyer,pmouth)
            # a = math.sqrt(c*c - b*b)
            # x,y = peyer
            # pmin = int(x),int(y-a/3)
            # pmax = int(x),int(y-a/1.25)
            # cv2.line(frame,pmin,pmax,(255,0,0),1)
    def detect(self, frame,key):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.cnt % 100000 == 0: 
            print("Update")
            rects = self.detector(gray, 0)
            for rect in rects:
        
                shape = self.predictor(gray, rect)
                shape = shape_to_np(shape)
                
                shape = shape[37:]
                self.points = np.zeros((len(shape),1,2),dtype = np.float32)
                for i,(x,y) in enumerate(shape):
                    self.points[i,0,0] = x
                    self.points[i,0,1] = y
                    
         

        else:
            self.points, st, err = cv2.calcOpticalFlowPyrLK(self.prev_gray, gray, self.points, None, **self.lk_params)
 
        self.mark_landmarks(frame)
        self.prev_gray = gray
        self.cnt +=1