import math
import numpy as np
class HotspotPPGSensor():
    def get_rawppg(self,frame,peyer,peyel,pmouth):
        # Forhead
        forehead_rect = peyer


        # Che
class SimplePPGSensor():
    def __init__(self):
        self.rppg = []
    def sense_ppg(self,frame,num_pixels):
        r_avg = np.sum(frame[:,:,0])/num_pixels
        g_avg = np.sum(frame[:,:,1])/num_pixels
        b_avg = np.sum(frame[:,:,2])/num_pixels
        ppg = [r_avg,g_avg,b_avg]
        for i,col in enumerate(ppg):
            if math.isnan(col):
                ppg[i] = 0
        self.rppg.append(i)
        

        