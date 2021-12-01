import os
import io
import cv2
from base_camera import BaseCamera
import picamera
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
            with picamera.array.PiRGBArray(camera) as stream:
                while True:
                    camera.capture(stream, format='bgr')
                    # At this point the image is available as stream.array
                    image = stream.array