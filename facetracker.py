import numpy as np
import cv2
import scipy.io as sio
import math

cascPath = "haarcascade_frontalface_default.xml"
face_cascade = cv2.CascadeClassifier(cascPath)

def crop_frame(frame,rect):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    return frame[y:y+h,x:x+w]


class FaceTracker():
    def __init__(self):
        self.tracker =cv2.TrackerKCF_create()#TrackerKCF_create()
        self.found_face = False
    def crop_to_face(self,frame): 
        gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        success=False
        if not self.found_face:
            faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
            if len(faces)>0:
                face=faces[0]
                face=(face[0],face[1],face[2],face[3])
                self.tracker.init(frame,face)
                self.found_face= True
                success = True
        else:
            (success, face) = self.tracker.update(frame) 
        if success:       
            x,y,dx,dy = face
            face = [int(x),max(int(y),0),int(dx),int(dy)]
            frame_cropped = crop_frame(frame,face)
            return frame_cropped
        return frame
        
         

