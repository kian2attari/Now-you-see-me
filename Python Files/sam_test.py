
import cv2
import numpy as np

def __init__(self, index=0):
    self.cap = cv2.VideoCapture(index)
    self.openni = index in (cv2.CAP_OPENNI, cv2.CAP_OPENNI2)
    self.fps = 0
        
VideoCapture capture(cap)
for(;;)
{
    Mat depthMap;
    capture >> depthMap;
    if( waitKey( 30 ) >= 0 )
        break;
}