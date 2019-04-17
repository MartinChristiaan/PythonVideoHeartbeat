import cv2
import numpy as np
lower = np.array([0, 48, 80], dtype = "uint8")
upper = np.array([20, 255, 255], dtype = "uint8")

def apply_skin_classifier(frame,elipse_size,blursize):
    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (elipse_size, elipse_size))
    skinMask = cv2.erode(skinMask, kernel, iterations = 2)
    skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
    skinMask = cv2.GaussianBlur(skinMask, (blursize, blursize), 0)
  
    num_skin_pixels = skinMask.clip(0,1).sum()
    skin = cv2.bitwise_and(frame, frame, mask = skinMask)
    return skin,num_skin_pixels