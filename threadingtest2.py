from framecapture import WebcamCapture,MixedMotion,Translation,Stationary,Fitness
from simpleupdater import SimpleUpdater,HeartBeatGUI
from rppgsensor import SimplePPGSensor
from TextWriter import refresh
from facetracker import FaceTracker
from plotter import Plotter
from multiprocessing import Process, Manager, Queue
import sched, time, threading
from signalprocessor import ChrominanceExtracter
from evaluator import Evaluator


def track_face(q,qback):
    tracker = FaceTracker()
    while True:
        if not q.empty():
             frame = q.get()
             face = tracker.crop_to_face(frame)
             qback.put(face)
        else:
             time.sleep(0.1)

if __name__ == '__main__':
    capture =Stationary()
    updater = SimpleUpdater()
    
   

    q = Queue()
    qback = Queue()
    p = Process(target=track_face, args=(q,qback))
    p.start()


    def update_fun(key):
        frame,_ = capture.get_frame()
        q.put(frame)

        while qback.empty():
            time.sleep(0.001)
        face = qback.get()
        refresh()
        # print("On Time")
        return [face],False

          #print("FOUND FRAME!")

        #face,npixels = apply_skin_classifier(face)
        
        #sensor.sense_ppg(face,npixels)

        #processor.extract_pulse()
        #evalu.evaluate(frame)
        #plotr.update_data()
        
         


    #gui.start_updating(update_fun)

    updater.start_updating(update_fun)
    #plotr.stop()
    p.join()