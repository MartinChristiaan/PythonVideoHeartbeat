import cv2
import os
import time
def write_text(img,text,location):
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    cv2.putText(img,text,location,font,fontScale,fontColor,lineType)


def draw_rect(frame,rect):
    rects = [rect]
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

