import cv2
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
from imageai.Detection import VideoObjectDetection
                                                         


class Camera(object):

    def __init__(self, index=0):
        self.cap = cv2.VideoCapture(index)
        self.openni = index in (cv2.CAP_OPENNI, cv2.CAP_OPENNI2)
        self.fps = 0


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
            
            # esc, q
            ch = cv2.waitKey(10) & 0xFF
            if ch == 27 or ch == ord('q'):
                break
            t = cv2.getTickCount()
            
            execution_path = os.getcwd()
            detector = VideoObjectDetection()
            detector.setModelTypeAsTinyYOLOv3()
            detector.setModelPath(os.path.join(execution_path , "yolo-tiny.h5"))
            detector.loadModel()
            video_path = detector.detectObjectsFromVideo(
                    camera_input=self.cap,
                    output_file_path=os.path.join(execution_path, "camera_detected_video"),
                    frames_per_second=10, log_progress=True, minimum_percentage_probability=30)
            print(video_path)
            
        
            if self.openni:
                if not self.cap.grab():
                    sys.exit('Grabs the next frame failed')
                ret, depth = self.cap.retrieve(cv2.CAP_OPENNI_DEPTH_MAP)
                
                # ret, frame = self.cap.retrieve(cv2.CAP_OPENNI_GRAY_IMAGE
                
q
                if callback:
                    callback(frame, depth, self.fps)
            else:
                ret, frame = self.cap.read()
                if not ret:
                    sys.exit('Reads the next frame failed')
                if gray:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if callback:
                    callback(frame, self.fps)

            t = cv2.getTickCount() - t
            self.fps = cv2.getTickFrequency() / t



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
