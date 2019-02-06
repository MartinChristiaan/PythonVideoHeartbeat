import math
import numpy as np
from framecapture import FrameCapture
from util.opencv_util import draw_rect, crop_frame
class LandMarkRoiFinder():
    def get_roi(self,frame,landmarktracker):
        peyer = landmarktracker.peyer
        peyel = landmarktracker.peyel
        pmouth = landmarktracker.pmouth
    
        x0 = peyel[0]
        x1 = peyer[0]
        y0 = pmouth[1]
        y1 = max(peyer[1],peyel[1])
        h = y1 - y0
        w = x1 - x0
        rect = int(x0-w*1.3),int(y0+2.2*h),int(w*3.5),int(-2.5*h)
        draw_rect(frame,rect)
        return crop_frame(frame,rect)

        # Che
class PPGSensor():
    def __init__(self,framecapture:FrameCapture):
        self.rppgl = []
        self.rppg = np.array([])
        self.cap = framecapture     
    def sense_ppg(self,frame,numpixels):
        pass   
     

class SimplePPGSensor(PPGSensor):
    def sense_ppg(self,frame,num_pixels):
        r_avg = np.sum(frame[:,:,0])/num_pixels
        g_avg = np.sum(frame[:,:,1])/num_pixels
        b_avg = np.sum(frame[:,:,2])/num_pixels
        ppg = [r_avg,g_avg,b_avg]
        for i,col in enumerate(ppg):
            if math.isnan(col):
                ppg[i] = 0
        self.rppgl.append(ppg)
        if len(self.rppgl)>300:
            del self.rppgl[0]
        rppg = np.transpose(np.array(self.rppgl))
        self.rppg = self.cap.resample(rppg)
        

        