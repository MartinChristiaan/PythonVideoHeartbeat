import cv2
import abc
import os
class FrameCapture():
    def get_frame(self):
        return _,_
class WebcamCapture(FrameCapture):
   
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3, 1280)
        self.camera.set(4, 720)

    def get_frame(self):
        _,frame = self.camera.read()
        return frame,False

class MixedMotion(FrameCapture):    
    def __init__(self):
        self.frame = 0
        self.video_folder = "C:\\Users\\marti\\Downloads\\Data\\mixed_motion\\bmp\\"

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

class Fitness(FrameCapture):    
    def __init__(self):
        self.frame = 0
        self.vi_cap = cv2.VideoCapture("C:\\Users\\marti\\Downloads\\Data\\trail2.mp4")
        
    #settings.use_resampling = True
    def get_frame(self):
        _,frame = self.vi_cap.read()
 #       rows,cols = frame.shape[:2]
        #M = cv2.getRotationMatrix2D((cols/2,rows/2),270,1)
        #frame = cv2.warpAffine(frame,M,(cols,rows))
#        frame = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)
        return frame,False

