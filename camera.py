import os
import io
import cv2
from base_camera import BaseCamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time

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

        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.framerate = 32
        rawCapture = PiRGBArray(camera, size=(640, 480))

        time.sleep(0.1)

        with PiCamera() as camera:
            time.sleep(2)
            stream = PiRGBArray(camera, size=(640, 480))
            for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):
                    # Truncate the stream to the current position (in case
                    # prior iterations output a longer image)
                    stream.truncate()
                    stream.seek(0)
                    yield frame.array.tobytes()
