from framecapture import WebcamCapture,MixedMotion,Translation,Fitness
from simpleupdater import SimpleUpdater,HeartBeatGUI
from landmark_detect import LandmarkDetecter,LandmarkTracker
from skinclassifier import apply_skin_classifier
from rppgsensor import SimplePPGSensor
from TextWriter import refresh
from facetracker import FaceTracker
from plotter import Plotter
from signalprocessor import ChrominanceExtracter
from evaluator import Evaluator
capture =Translation()
#landmarkdetect = LandmarkTracker()
tracker = FaceTracker()
sensor = SimplePPGSensor()
processor = ChrominanceExtracter(300,sensor,capture)
gui = HeartBeatGUI()
evalu = Evaluator(processor)

plotr = Plotter(gui.w,sensor,processor,evalu)
def update_fun(key):
    frame,_ = capture.get_frame()
    #frame,npixels = apply_skin_classifier(frame)
    #landmarkdetect.detect(frame,key)
    face = tracker.crop_to_face(frame)
    face,npixels = apply_skin_classifier(face)
    sensor.sense_ppg(face,npixels)
    processor.extract_pulse()
    evalu.evaluate()
    #plotr.update_plots()  
    refresh()

    return face,False    

gui.start_updating(update_fun)

#SimpleUpdater(update_fun)
