from framecapture import WebcamCapture,MixedMotion,Stationary,Fitness
from simpleupdater import SimpleUpdater,HeartBeatGUI
from landmark_detect import LandmarkTrackerEyeSafe
#from landmark_detect2 import LandmarkTrackerFull
from skinclassifier import apply_skin_classifier
from rppgsensor import *
from TextWriter import refresh
from facetracker import FaceTracker
from plotter import Plotter
from exporter import export_data,export_to_matlab
from signalprocessor import ChrominanceExtracter
from evaluator import Evaluator

if __name__ == '__main__':
    capture = Fitness()
    #landmarkdetect = LandmarkTrackerEyeSafe()
    tracker = FaceTracker()
    #roifinder = LandMarkRoiFinder()
#    sensor = SimpleForeheadSensor(capture)
    #sensor = RegionSensor(capture)
    sensor = SimplePPGSensor(capture)
    processor = ChrominanceExtracter(300,sensor,capture)
    #gui = HeartBeatGUI()
    evalu = Evaluator(processor)
    updater = SimpleUpdater()

    #plotr = Plotter(sensor,processor,evalu,gui.w)

    def update_fun(key):
        frame,should_stop = capture.get_frame()
        #frame,npixels = apply_skin_classifier(frame)
        #landmarkdetect.detect(frame)

        face = tracker.crop_to_face(frame)
      
        face,npixels = apply_skin_classifier(face)
        # roi = roifinder.get_roi(frame_rot,landmarkdetect)
        # face,npixels = apply_skin_classifier(roi)
        sensor.sense_ppg(face,npixels)

        processor.extract_pulse()
        evalu.evaluate(frame)
      # plotr.update_data()
        refresh()

        return [frame,face],should_stop    

    #gui.start_updating(update_fun)
    updater.start_updating(update_fun)
    export_data(evalu)
    #export_to_matlab(sensor)



    #plotr.stop()