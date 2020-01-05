import cv2
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
from imageai.Detection import ObjectDetection
                                                         


class Camera(object):
    
    detector = ObjectDetection()
    custom_objects = detector.CustomObjects(car=True, person=True, bus=True,
                                            chair=True, truck=True, 
                                            refrigerator=True, oven=True, 
                                            bicycle=True, skateboard=True, 
                                            train=True, bench=True, 
                                            motorcycle=True, bed=True, 
                                            suitcase=True) 


    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)
        self.openni = index in (cv2.CAP_OPENNI, cv2.CAP_OPENNI2)
        self.fps = 0
        execution_path = os.getcwd()
        self.detector.setModelTypeAsYOLOv3()
        self.detector.setModelPath(os.path.join(execution_path , "yolo.h5"))
        self.detector.loadModel(detection_speed="fastest")
        print ("Model Loaded")


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()

    def release(self):
        if not self.cap: return
        self.cap.release()
        self.cap = None

    def capture(self, callback, gray=False):
        if not self.cap:
            sys.exit('The capture is not ready')

        while True:

            t = cv2.getTickCount()
            
            
            if self.openni:
                if not self.cap.grab():
                    sys.exit('Grabs the next frame failed')
                ret, depth = self.cap.retrieve(cv2.CAP_OPENNI_DEPTH_MAP)
                
                # ret, frame = self.cap.retrieve(cv2.CAP_OPENNI_GRAY_IMAGE
                
                ret, frame = self.cap.retrieve(cv2.CAP_OPENNI_DEPTH_MAP
                    if gray else cv2.CAP_OPENNI_BGR_IMAGE)
                    
                detections = self.detector.detectCustomObjectsFromImage(
                        custom_objects=self.custom_objects, input_type="array",
                        input_image=frame, output_type="array",
                        minimum_percentage_probability=20)[0]
                
                if callback:
                    callback(detections, depth, self.fps)
            else:
                ret, frame = self.cap.read()
                
                detections = self.detector.detectCustomObjectsFromImage(
                        custom_objects=self.custom_objects, input_type="array",
                        input_image=frame, output_type="array",
                        minimum_percentage_probability=20)[0]
                
                if not ret:
                    sys.exit('Reads the next frame failed')
                if gray:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if callback:
                    callback(detections, self.fps)

            t = cv2.getTickCount() - t
            self.fps = cv2.getTickFrequency() / t
            
            # esc, q
            ch = cv2.waitKey(10) & 0xFF
            if ch == 27 or ch == ord('q'):
                break



    def fps(self):
        return self.fps

    def get(self, prop_id):
        return self.cap.get(prop_id)

    def set(self, prop_id, value):
        self.cap.set(prop_id, value)


if __name__ == '__main__':
    callback = lambda gray, fps: cv2.imshow('gray', gray)
    
    with Camera(0) as cam:
        print("Camera: %dx%d, %d" % (
            cam.get(cv2.CAP_PROP_FRAME_WIDTH),
            cam.get(cv2.CAP_PROP_FRAME_HEIGHT),
            cam.get(cv2.CAP_PROP_FPS)))
        cam.capture(callback)

    cv2.destroyAllWindows()
