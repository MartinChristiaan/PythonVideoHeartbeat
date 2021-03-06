import cv2
import abc
import os
import time
from TextWriter import write_text
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
    def __init__(self,frame):
        self.fs = 20
        self.video_folder = "C:\\Users\\marti\\Downloads\\Data\\mixed_motion\\bmp\\"
        self.frame = frame
        self.next_path = self.video_folder + str(self.frame) + ".bmp"

    def get_frame(self):
        self.frame+=1
        curpath = self.next_path
        self.next_path = self.video_folder + str(self.frame) + ".bmp"
        exists = os.path.isfile(self.next_path)
        if exists:
            frame = cv2.imread(curpath)
            write_text(frame,"Frame : " + str(self.frame))
            return frame,False       
        else:
            frame = cv2.imread(curpath)
            write_text(frame,"Frame : " + str(self.frame))
            return frame,True

class Stationary(FrameCapture):    
    def __init__(self,frame):
        self.fs = 20
        self.video_folder = "C:\\Users\\marti\\Downloads\\Data\\stationary\\bmp\\"
        self.frame = frame
        self.next_path = self.video_folder + str(self.frame) + ".bmp"

    def get_frame(self):
        self.frame+=1
        curpath = self.next_path
        self.next_path = self.video_folder + str(self.frame) + ".bmp"
        exists = os.path.isfile(self.next_path)
        if exists:
            frame = cv2.imread(curpath)
            write_text(frame,"Frame : " + str(self.frame))
            return frame,False       
        else:
            frame = cv2.imread(curpath)
            write_text(frame,"Frame : " + str(self.frame))
            return frame,True



class Fitness(FrameCapture):    
    def __init__(self):
        self.frame = 0
        
        self.vi_cap = cv2.VideoCapture("C:\\Users\\marti\\Downloads\\Data\\me\\Talking.mp4")
        _,self.nextframe = self.vi_cap.read()
        self.fs =  self.vi_cap.get(cv2.CAP_PROP_FPS)
        print("FPS : " + str(self.fs) )
    #settings.use_resampling = True
    def get_frame(self):
        frame = self.nextframe
        _,self.nextframe = self.vi_cap.read()
        try:
            if self.nextframe.size ==None:
                return frame,True
        except Exception:
            return frame,True
        return frame,False
        
 #       rows,cols = frame.shape[:2]
        #M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
        #frame = cv2.warpAffine(frame,M,(cols,rows))
#        frame = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        
