import os
import io
import cv2
from base_camera import BaseCamera
import picamera
import numpy as np

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
        #camera = cv2.VideoCapture(Camera.video_source)
        camera = picamera.PiCamera()
        #if not camera.isOpened():
        #    raise RuntimeError('Could not start camera.')
        stream = io.BytesIO()
        while True:
            # read current frame
            #camera.set(cv2.CAP_PROP_EXPOSURE,-4)
            #_, img = camera.read()
            camera.capture(stream, format='jpeg')
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            img = cv2.imdecode(data, 1)[:, :, ::-1]
            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()