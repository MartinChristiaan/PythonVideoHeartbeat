import math
import numpy as np
class HotspotPPGSensor():
    def get_rawppg(self,frame,peyer,peyel,pmouth):
        # Forhead
        forehead_rect = peyer


        # Che
class PPGSensor():
    def __init__(self):
        self.rppgl = []
        self.rppg = np.array([])
        
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
        self.rppg = np.transpose(np.array(self.rppgl))
        

        