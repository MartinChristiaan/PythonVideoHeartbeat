from framecapture import WebcamCapture,MixedMotion,Stationary,Fitness
from simpleupdater import SimpleUpdater,HeartBeatGUI
from landmark_detect import LandmarkTrackerEyeSafe
#from landmark_detect2 import LandmarkTrackerFull
from skinclassifier import apply_skin_classifier
from rppgsensor import *
from TextWriter import refresh
from facetracker import FaceTracker
from plotter import Plotter
from exporter import export_data,export_to_matlab,export_data_named
from signalprocessor import ChrominanceExtracter
from evaluator import Evaluator



if __name__ == '__main__':
    
    capture = WebcamCapture()
    landmarkdetect = LandmarkTrackerEyeSafe()
    tracker = FaceTracker()
    sensor = SimplePPGSensor(capture)
    processor = ChrominanceExtracter(300,sensor,capture)
    gui = HeartBeatGUI()
    evalu = Evaluator(processor)
    plotr = Plotter(sensor,processor,evalu,gui.w)
    #updater = SimpleUpdater()
    def update_fun(key):
        frame,should_stop = capture.get_frame()
        
        face = tracker.crop_to_face(frame)
        #landmarkdetect.detect(face)
#         blackout_regions(face)
        face,npixels = apply_skin_classifier(face,13,5)
        
    #  face,npixels = apply_skin_classifier(face)
        # # roi = roifinder.get_roi(frame_rot,landmarkdetect)
        sensor.sense_ppg(face,npixels)

        processor.extract_pulse()
        evalu.evaluate(frame)
        plotr.update_data()
        refresh()

        return [frame,face],should_stop    

    gui.start_updating(update_fun)
    #updater.start_updating(update_fun)
    #export_data_named(evalu,name)
    #export_to_matlab(sensor)



    #plotr.stop()