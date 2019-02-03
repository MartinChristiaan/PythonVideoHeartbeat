from framecapture import WebcamCapture,MixedMotion,Translation,Fitness
from simpleupdater import SimpleUpdater
from landmark_detect import LandmarkDetecter,LandmarkTracker
from skinclassifier import apply_skin_classifier
from rppgsensor import SimplePPGSensor
from TextWriter import refresh
from facetracker import FaceTracker

capture =MixedMotion()
#landmarkdetect = LandmarkTracker()
tracker = FaceTracker()
sensor = SimplePPGSensor()
def update_fun(key):
    frame,_ = capture.get_frame()
    #frame,npixels = apply_skin_classifier(frame)
    #landmarkdetect.detect(frame,key)
    face = tracker.crop_to_face(frame)
    face,npixels = apply_skin_classifier(face)
    sensor.sense_ppg(face,npixels)
        
    refresh()
    return face,False    



SimpleUpdater(update_fun)
