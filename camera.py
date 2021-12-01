import os
import io
import cv2
from base_camera import BaseCamera
import picamera
import picamera.array
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
        with picamera.PiCamera() as camera:
            camera.start_preview()
            time.sleep(2)
            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, format='jpeg'):
                # YOURS:  for frame in camera.capture_continuous(stream, format="bgr",  use_video_port=True):
                    # Truncate the stream to the current position (in case
                    # prior iterations output a longer image)
                    stream.truncate()
                    stream.seek(0)
                    yield stream.array.tobytes()
