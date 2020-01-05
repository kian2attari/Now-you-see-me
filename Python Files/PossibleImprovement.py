# -*- coding: utf-8 -*-
"""
Created on Sun Oct 20 04:41:14 2019

@author: Kian
"""

import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
from imageai.Detection import VideoObjectDetection
import cv2
import time







camera = cv2.VideoCapture(0)

def forFrame(frame_number, output_array, output_count, returned_frame):
    print(returned_frame)
    cv2.imshow('gray', returned_frame)
    time.sleep(0.4)
    
    
if __name__ == '__main__':
    execution_path = os.getcwd()
    detector = VideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path , "yolo.h5"))
    detector.loadModel(detection_speed="faster")

    custom_objects = detector.CustomObjects(car=True, person=True, bus=True, chair=True, truck=True, refrigerator=True, oven=True, bicycle=True, skateboard=True, train=True, bench=True, motorcycle=True, bed=True, suitcase=True) 
    
    detections = detector.detectCustomObjectsFromVideo(camera_input=camera, custom_objects=custom_objects, save_detected_video = False, return_detected_frame=True, per_frame_function=forFrame, minimum_percentage_probability=30, frames_per_second=20,)