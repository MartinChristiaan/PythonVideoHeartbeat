from framecapture import WebcamCapture,MixedMotion,Stationary,Fitness
#from landmark_detect2 import LandmarkTrackerFull
from facetracker import FaceTracker
import matplotlib.pyplot as plt
import cv2
import numpy as np
from scipy import signal
capture = WebcamCapture()
tracker = FaceTracker()
frame = plt.imread("t.jpg")

R = 0
G = 1
B = 2
face = tracker.crop_to_face(frame)
plt.figure()
plt.imshow(face)
skin_vec = [1,0.66667,0.5]
col_c = np.zeros_like(face)
for col in [R,G,B]:
    col_stride = face[:,:,col]# select last samples
    y_ACDC = signal.detrend(col_stride/np.mean(col_stride))
    col_c[:,:,col] = y_ACDC * skin_vec[col]
pass

X_chrom = col_c[:,:,R]-col_c[:,:,G]
Y_chrom = col_c[:,:,R] + col_c[:,:,G] - 2* col_c[:,:,B]
# Xf = signal.filtfilt(b_BPF40220,a_BPF40220,X_chrom) # Applies band pass filter
# Yf = signal.filtfilt(b_BPF40220,a_BPF40220,Y_chrom)
# Nx = np.std(Xf)
# Ny = np.std(Yf)
newface = np.zeros_like(face)
newface[:,:,R] =  X_chrom*10
newface[:,:,G] =  Y_chrom*10
plt.figure
plt.imshow(newface)
plt.show()
# grab the image channels, initialize the tuple of colors,
# the figure and the flattened feature vector
plt.figure()
plt.title("'Flattened' Color Histogram")
plt.xlabel("Bins")
plt.ylabel("Probability")
features = np.zeros((3,256))
total_pix = face.shape[0]*face.shape[1]
# loop over the image channels
color = ('b','g','r')
hist = np.zeros((3,256))
hist.shape
for i,col in enumerate(color):
    hist[i] = cv2.calcHist([face],[i],None,[256],[0,256])[:,0]
    plt.plot(hist[i],color = col)
    plt.xlim([0,256])

mask = np.zeros(face.shape[:2])
for x in range(face.shape[0]):
    for y in range(face.shape[1]):
        if hist[0,face[x,y,0]]<300 and hist[1,face[x,y,1]]<300  and hist[2,face[x,y,2]]<300:
            mask[x,y] = 255
        else:
            mask[x,y] = 0

plt.imshow(mask,cmap = "gray")

plt.show()





#landmarkdetect.detect(face)
#         blackout_regions(face)
# #face,npixels = apply_skin_classifier(face,13,5)
        
#     #  face,npixels = apply_skin_classifier(face)
#         # # roi = roifinder.get_roi(frame_rot,landmarkdetect)
#         sensor.sense_ppg(face,npixels)

#         processor.extract_pulse()
#         evalu.evaluate(frame)
#         plotr.update_data()
#         refresh()

#         return [frame,face],should_stop    

#     gui.start_updating(update_fun)
    #updater.start_updating(update_fun)
    #export_data_named(evalu,name)
    #export_to_matlab(sensor)



    #plotr.stop()