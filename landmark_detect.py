
import argparse
import time
import dlib
import cv2
import numpy as np
from TextWriter import write_text
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
        self.prev_points = []
        self.lk_params = dict( winSize  = (15,15),maxLevel = 2,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.cnt = 0
        self.blacklist = []
        self.eyel = np.array([])
        self.eyer = np.array([])
        self.mouth = np.array([])
        self.points = np.array([])        
        


    def mark_landmarks(self,frame):
        eyel = self.points[:5]
        eyer = self.points[6:11]
        mouth = self.points[11:] 
        for i in range(eyel.shape[0]):
            col =  (255, 255, 0) 
            if i in self.blacklist:
                col = (0,0,255)  
            cv2.circle(frame, (eyel[i,0,0], eyel[i,0,1]), 1, col, -1)
        for i in range(eyer.shape[0]):
            col =  (0, 255,0)
            if i+6 in self.blacklist:
                col = (0,0,255)
            cv2.circle(frame, (eyer[i,0,0], eyer[i,0,1]), 1, col, -1)
        for i in range(mouth.shape[0]):
            col =  (255, 0, 0)         
            if i+11 in self.blacklist:
                col = (0,0,255)
            cv2.circle(frame, (mouth[i,0,0], mouth[i,0,1]), 1, col, -1)


        eyel_ids = [id for id in range(5) if id not in self.blacklist]
        eyer_ids = [id for id in range(6,11) if id not in self.blacklist]
        mouth_bl = [id for id in range(11,self.points.shape[0]) if id not in self.blacklist]

        self.eyel = self.points[eyel_ids]
        self.eyer = self.points[eyer_ids]
        self.mouth = self.points[mouth_bl]

        write_text(frame,"Left Eye trackers : " + str(len(self.eyel)))
        write_text(frame,"Right Eye trackers : " + str(len(self.eyer)))
        write_text(frame,"Mouth trackers : " + str(len(self.mouth)))

        self.peyel = mean_pos(self.eyel)
        self.peyer = mean_pos(self.eyer)
        self.pmouth = mean_pos(self.mouth)
        try:
            cv2.line(frame,self.peyel,self.peyer,(255,0,0),1)            
            cv2.line(frame,self.peyel,self.pmouth,(255,0,0),1)            
            cv2.line(frame,self.peyer,self.pmouth,(255,0,0),1)
        except Exception:
            pass

    

    def detect(self, frame,key):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        if self.mouth.shape[0] < 15 or self.eyel.shape[0] < 5 or self.eyer.shape[0] < 5: 
            rects = self.detector(gray, 0)
            for rect in rects:
                shape = self.predictor(gray, rect)
                shape = shape_to_np(shape)
                self.blacklist = []
                shape = shape[37:]
                newpoints = np.zeros((len(shape),1,2),dtype = np.float32)
                for i,(x,y) in enumerate(shape):
                    newpoints[i,0,0] = x
                    newpoints[i,0,1] = y
                if self.points.shape[0] == 0: 
                    self.points = newpoints  
                else:
                    eyel = newpoints[:5]
                    eyer = newpoints[6:11]
                    mouth = newpoints[11:] 
                    if self.eyel.shape[0] < 5:
                        new_mean = mean_pos(eyel)
                        #if dist(new_mean,self.peyel) < 30:
                        self.points[:5] = eyel
                        self.blacklist = [id for id in self.blacklist if not id<5]

                    if self.eyer.shape[0] < 5:
                        new_mean = mean_pos(eyer)
                        #if dist(new_mean,self.peyer) < 30:
                        self.points[6:11] = eyer
                        self.blacklist = [id for id in self.blacklist if not id>5 and not id<11 ]
                    if self.mouth.shape[0] <15:
                        new_mean = mean_pos(mouth)
                        #if dist(new_mean,self.pmouth) < 30:
                        self.points[11:] = mouth
                        self.blacklist = [id for id in self.blacklist if not id>11]
                    self.prev_points = []
                    self.prev_gray = []
        else:
            self.points, _, _ = cv2.calcOpticalFlowPyrLK(self.prev_gray[-1], gray, self.points, None, **self.lk_params)
            pback, _, _ = cv2.calcOpticalFlowPyrLK(gray,self.prev_gray[-1], self.points, None, **self.lk_params)
            for i in range(1,len(self.prev_gray)-1):
                pback,_,_ = cv2.calcOpticalFlowPyrLK(self.prev_gray[-i],self.prev_gray[-(i+1)], pback, None, **self.lk_params)
            e = pback - self.prev_points[0]
            e = np.sqrt(e[:,0,0]*e[:,0,0] + e[:,0,1]*e[:,0,1])
            for i in range(e.shape[0]):
                if id not in self.blacklist and e[i] > 30:
                    self.blacklist.append(i)



        self.mark_landmarks(frame)
        self.prev_gray.append(gray)
        self.prev_points.append(self.points)
        if len(self.prev_gray) > 8:
            del self.prev_gray[0]
        if len(self.prev_points) > 8:
            del self.prev_points[0]
        self.cnt +=1


def get_bounding_box(points):
    minx = np.min(points[:,0,0])
    maxx = np.max(points[:,0,0])
    miny = np.min(points[:,0,1])
    maxy = np.max(points[:,0,1])

    return minx,miny,maxx-minx,maxy-miny
 
# class LandmarkTracker_Mosse():
#     def __init__(self):
#         self.detector = dlib.get_frontal_face_detector()
#         self.predictor = dlib.shape_predictor("predictor.dat")
#         self.started_tracking = False
#         self.shape = []
#         self.prev_gray = []
#         self.lk_params = dict( winSize  = (15,15),maxLevel = 2,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
#         self.cnt = 0
#         self.eyel_tracker = cv2.TrackerKCF_create()
#         self.eyer_tracker = cv2.TrackerKCF_create()
#         self.mouth_tracker = cv2.TrackerKCF_create()
        

#     def detect(self, frame,key):
#         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#         if self.cnt % 100000 == 0: 
#             print("Update")
#             rects = self.detector(gray, 0)
#             for rect in rects:

#                 shape = self.predictor(gray, rect)
#                 shape = shape_to_np(shape)
                
#                 shape = shape[37:]
#                 self.points = np.zeros((len(shape),1,2),dtype = np.float32)
#                 for i,(x,y) in enumerate(shape):
#                     self.points[i,0,0] = x
#                     self.points[i,0,1] = y
#                 eyel = self.points[:5]
#                 eyer = self.points[6:11]
#                 mouth = self.points[11:] 
#                 mouth_rect = get_bounding_box(eyel)
#                 self.mouth_tracker.init(frame,mouth_rect)



                
#         else:
#             (success, mouth_rect) = self.mouth_tracker.update(frame) 
#             if not success:
#                 print("Mouth Failure")
#     #    self.mark_landmarks(frame)
#         x, y, w, h = mouth_rect
#         x = int(x)
#         y = int(y)
#         w = int(w)
#         h = int(h)
#         cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

#         self.prev_gray = gray
#         self.cnt +=1