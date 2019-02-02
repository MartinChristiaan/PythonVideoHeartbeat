from framecapture import WebcamCapture,MixedMotion
from simpleupdater import SimpleUpdater
from landmark_detect import LandmarkDetecter,LandmarkTracker
from skinclassifier import apply_skin_classifier
capture =WebcamCapture()
landmarkdetect = LandmarkTracker()

def update_fun(key):
    frame,_ = capture.get_frame()
    #frame,npixels = apply_skin_classifier(frame)
    landmarkdetect.detect(frame,key)
    return frame,False    

SimpleUpdater(update_fun)