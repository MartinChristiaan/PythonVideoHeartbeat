from framecapture import WebcamCapture,MixedMotion,Translation,Fitness
from simpleupdater import SimpleUpdater
from landmark_detect import LandmarkDetecter,LandmarkTracker
from skinclassifier import apply_skin_classifier
from TextWriter import refresh
capture =Fitness()
landmarkdetect = LandmarkTracker()

def update_fun(key):
    frame,_ = capture.get_frame()
    #frame,npixels = apply_skin_classifier(frame)
    landmarkdetect.detect(frame,key)
    refresh()
    return frame,False    

SimpleUpdater(update_fun)
