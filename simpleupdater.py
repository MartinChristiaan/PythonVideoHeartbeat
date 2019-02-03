from framecapture import FrameCapture
import cv2
import numpy as np
import time
from TextWriter import write_text


class SimpleUpdater:
    def __init__ (self,update_fun):
        self.update_fun = update_fun
        self.should_stop = False
        self.pressed_key = -1
        self.dt  =1
        while self.should_stop == False:
            tstart = time.time()
            self.update()
            self.dt = time.time()-tstart
 
        cv2.destroyAllWindows()          

    def update(self):

        frame,should_stop = self.update_fun(self.pressed_key)# self.frame_capture.get_frame()
        try:
            write_text(frame,"fps : " + '{0:.2f}'.format(1/self.dt))
        except Exception:
            pass
        cv2.imshow("images", frame)
        self.should_stop = should_stop
        
        self.pressed_key=cv2.waitKey(1) & 0XFF
        if self.pressed_key== 27 :
            print("Escape")
            self.should_stop = True

    
