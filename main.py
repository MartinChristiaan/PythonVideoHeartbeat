from framecapture import WebcamCapture,MixedMotion,Translation,Stationary,Fitness
from simpleupdater import SimpleUpdater,HeartBeatGUI
from landmark_detect import LandmarkDetecter,LandmarkTracker,LandmarkTrackerEyeSafe
from skinclassifier import apply_skin_classifier
from rppgsensor import SimplePPGSensor
from TextWriter import refresh
from facetracker import FaceTracker
from plotter import Plotter

from signalprocessor import ChrominanceExtracter
from evaluator import Evaluator

if __name__ == '__main__':
    capture =MixedMotion()
    landmarkdetect = LandmarkTrackerEyeSafe()
    tracker = FaceTracker()
    sensor = SimplePPGSensor(capture)
    processor = ChrominanceExtracter(300,sensor,capture)
    #gui = HeartBeatGUI()
    evalu = Evaluator(processor)
    updater = SimpleUpdater()
    #plotr = Plotter(sensor,processor,evalu)
    

    def update_fun(key):
        frame,_ = capture.get_frame()
        #frame,npixels = apply_skin_classifier(frame)
        landmarkdetect.detect(frame)
        #face = tracker.crop_to_face(frame)
        #face,npixels = apply_skin_classifier(face)
        
        #sensor.sense_ppg(face,npixels)

        #processor.extract_pulse()
        #evalu.evaluate(frame)
        #plotr.update_data()
        refresh()

        return [frame],False    


    #gui.start_updating(update_fun)

    updater.start_updating(update_fun)
    #plotr.stop()