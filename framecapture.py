import cv2
import abc
import os
import time
class FrameCapture():
    def get_frame(self):
        return _,_
    def resample(self,rPPG):
        return rPPG
import numpy as np
class WebcamCapture(FrameCapture):
   
    def __init__(self):
        self.fs = 20
        self.camera = cv2.VideoCapture(1)
        self.camera.set(3, 1280)
        self.camera.set(4, 720)
        self.timestamps = []
        self.tprev = None

    def get_frame(self):
        _,frame = self.camera.read()
        if not self.tprev == None:
            self.timestamps.append(self.timestamps[-1] + (time.time() - self.tprev))
        else:
            self.timestamps.append(0)
        self.tprev = time.time()

        return frame,False
    def resample(self,rPPG):
        t = np.arange(0,self.timestamps[-1],1/self.fs)
            
        rPPG_resampled= np.zeros((3,t.shape[0]))
        for col in [0,1,2]:
            rPPG_resampled[col] = np.interp(t,self.timestamps,rPPG[col])
        return rPPG_resampled
        

class MixedMotion(FrameCapture):    
    def __init__(self):
        self.fs = 20
        self.video_folder = "C:\\Users\\marti\\Downloads\\Data\\mixed_motion\\bmp\\"
        self.frame = 0
    def get_frame(self):
        self.frame+=1
        frame_path = self.video_folder + str(self.frame) + ".bmp"
        exists = os.path.isfile(frame_path)
        if exists:
            return cv2.imread(frame_path),False
        else:
            print(frame_path + " Does not exist")
            return None,True

class Translation(FrameCapture):    
    def __init__(self):
        self.fs = 20
        self.frame = 0
        self.video_folder = "C:\\Users\\marti\\Downloads\\Data\\translation\\bmp\\"

    def get_frame(self):
        self.frame+=1
        frame_path = self.video_folder + str(self.frame) + ".bmp"
        exists = os.path.isfile(frame_path)
        if exists:
            return cv2.imread(frame_path),False
        else:
            print(frame_path + " Does not exist")
            return None,True

class Stationary(FrameCapture):    
    def __init__(self):
        self.fs = 20
        self.frame = 0
        self.video_folder = "C:\\Users\\marti\\Downloads\\Data\\stationary\\bmp\\"

    def get_frame(self):
        self.frame+=1
        frame_path = self.video_folder + str(self.frame) + ".bmp"
        exists = os.path.isfile(frame_path)
        if exists:
            return cv2.imread(frame_path),False
        else:
            print(frame_path + " Does not exist")
            return None,True

class Fitness(FrameCapture):    
    def __init__(self):
        self.frame = 0
        self.fs = 24
        self.vi_cap = cv2.VideoCapture("C:\\Users\\marti\\Downloads\\Data\\trail2.mp4")
        
    #settings.use_resampling = True
    def get_frame(self):
        _,frame = self.vi_cap.read()
 #       rows,cols = frame.shape[:2]
        #M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
        #frame = cv2.warpAffine(frame,M,(cols,rows))
#        frame = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        return frame,False

