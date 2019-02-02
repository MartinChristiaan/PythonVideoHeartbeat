import cv2
import abc
import os
class FrameCapture():
    def get_frame(self):
        return _,_
class WebcamCapture(FrameCapture):
   
    def __init__(self):
        self.camera = cv2.VideoCapture(1)
        self.camera.set(3, 1920)
        self.camera.set(4, 1080)

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