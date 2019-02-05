from framecapture import FrameCapture
import cv2
import numpy as np
import time
from TextWriter import write_text
import sys
from PyQt5 import QtGui  
from PyQt5 import QtCore  
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from util.qt_util import *
from util.pyqtgraph_util import *

class Updater():

    def __init__ (self):
        self.should_stop = False
        self.pressed_key = -1
        self.dt  =1
        self.wanted_frame=0

    def update(self):
        tstart = time.time()      
        frames,should_stop = self.update_fun(self.pressed_key)# self.frame_capture.get_frame()
        mystr = " time :  {:.2f}".format(self.dt*1000) + " (ms)" + " Fps :	{:.2f}".format(1/self.dt)
        sys.stdout.write("\r"+mystr)
        sys.stdout.flush()
        try:
            
            write_text(frames[self.wanted_frame],"fps : " + '{0:.2f}'.format(1/self.dt))
        except Exception:
            pass
            
        cv2.imshow("images",frames[self.wanted_frame])

        self.should_stop = should_stop
        
        self.pressed_key=cv2.waitKey(1) & 0XFF
        if self.pressed_key== 27 :
            print("Escape")
            self.should_stop = True
        if self.pressed_key == 119:
            self.wanted_frame+=1
            if self.wanted_frame == len(frames):
                self.wanted_frame = 0
        self.dt = time.time()-tstart


class SimpleUpdater(Updater):
    def start_updating(self,update_fun):
        self.update_fun = update_fun
        while not self.should_stop:
            self.update()
        cv2.destroyAllWindows()
class HeartBeatGUI(Updater):
    def __init__ (self):
        super(HeartBeatGUI,self).__init__()
        self.app,self.w = create_basic_app()

    def start_updating(self,update_fun):
        self.update_fun = update_fun
        timer = QtCore.QTimer()
        timer.start(10)
        timer.timeout.connect(self.update)
        execute_app(self.app,self.w)   

