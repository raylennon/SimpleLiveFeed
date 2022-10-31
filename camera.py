import os
import io
import cv2
from base_camera import BaseCamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
from datetime import datetime

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(-1, cv2.CAP_V4L)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')
        t1 = datetime(1000, 1, 1); dt=0
        while True:
            t2 = datetime.now()
            dt = (t2-t1).total_seconds()

            _, img = camera.read()

            if dt > 15:
                cv2.imwrite('imgs/+'+time.strftime("%Y%m%d-%H%M%S")+'.png', img)
                t1=t2
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()