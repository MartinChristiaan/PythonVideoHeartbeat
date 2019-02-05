
from framecapture import Stationary
from facetracker import FaceTracker
import numpy as np
import scipy.io as sio
from scipy import signal
from evaluator import calculateSNR
import matplotlib.pyplot as plt
capture =Stationary()
tracker = FaceTracker()
R = 0
G = 1
B = 2

frames = []
rad = 10
for i in range(1201):
    frame,_ = capture.get_frame()
    face = tracker.crop_to_face(frame)
    if i == 0:
        pass
    if i == 1:
        h,w = face.shape[:2]
        h = int(h/rad)
        w = int(w/rad)
        rPPG = np.zeros((1200,h,w,3))
    if i > 0:
        for y in range(h):
            for x in range(w):
                for col in [R,G,B]:
                    rPPG[i-1,x,y,col] = 1/(rad*rad) * np.sum(face[y*rad:y*rad+rad,x*rad:x*rad + rad,col]) 
print("Loaded frames")
import time

nwind= 7
fs = 20
fftlength = 300
f = np.linspace(fs/2,fftlength/2 + 1) * 60
       
fft_roi = range(int(fftlength/2+1)) # We only care about this part of the fft because it is symmetric anyway
bpf_div= 60 * fs / 2
b_BPF40220,a_BPF40220 = signal.butter(10, ([40/bpf_div, 220/bpf_div]),  'bandpass') 
skin_vec = [1,0.66667,0.5]
snr = np.zeros((nwind,h,w))
bpm = np.zeros((nwind,h,w))
for wind in range(nwind):
    for y in range(h):
        tstart = time.time()
        for x in range(w):
            col_c = np.zeros((3,fftlength))
            for col in [R,G,B]:
                start = wind*150
                col_stride = rPPG[start:start+fftlength,y,x,col]# select last samples
                y_ACDC = signal.detrend(col_stride/np.mean(col_stride))
                col_c[col] = y_ACDC * skin_vec[col]
            X_chrom = col_c[R]-col_c[G]
            Y_chrom = col_c[R] + col_c[G] - 2* col_c[B]
            Xf = signal.filtfilt(b_BPF40220,a_BPF40220,X_chrom) # Applies band pass filter
            Yf = signal.filtfilt(b_BPF40220,a_BPF40220,Y_chrom)
            Nx = np.std(Xf)
            Ny = np.std(Yf)
            alpha_CHROM = Nx/Ny
            x_stride_method = Xf- alpha_CHROM*Yf
            STFT = np.fft.fft(x_stride_method,fftlength)[fft_roi]
            normalized_amplitude = np.abs(STFT)/np.max(np.abs(STFT))
            bpm_id = np.argmax(normalized_amplitude)
            snr[wind,y,x] = calculateSNR(normalized_amplitude,bpm_id)
            
            #bpm[wind,y,x] = f[bpm_id]

        dt = time.time() - tstart 
        # print("progress : " + str(y * w) + " out of "+  str(h*w))
        # print("progress : " + str(y) + " out of "+  str(h))
        # print("dt : " + str(dt) + " remaining "+  str((h-y-1)*dt))
meansnr = snr.mean(axis=0).T
np.savetxt("snrtest.csv", meansnr, delimiter=",")



plt.figure()
plt.imshow(snr.mean(axis=0).T)
plt.colorbar()
#plt.imshow(bpm.mean(axis=0))
plt.show()
