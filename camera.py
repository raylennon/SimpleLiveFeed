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
    '''
    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75)
            camera.set(cv2.CAP_PROP_EXPOSURE, 100)
            _, img = camera.read()

            # encode as a jpeg image and return it
            yield cv2.imencode('.jpg', img)[1].tobytes()
    '''
    @staticmethod
    def frames():
        # Initialize the camera
        camera = PiCamera()
        
        # Set the camera resolution
        camera.resolution = (640, 480)
        
        # Set the number of frames per second
        camera.framerate = 32
        
        # Generates a 3D RGB array and stores it in rawCapture
        raw_capture = PiRGBArray(camera, size=(640, 480))
        
        # Wait a certain number of seconds to allow the camera time to warmup
        time.sleep(0.5)
        
        # Capture frames continuously from the camera
        for frame in camera.capture_continuous(raw_capture, format="bgr", use_video_port=True):
            
            # Grab the raw NumPy array representing the image
            image = frame.array
            
            # Display the frame using OpenCV
            yield image.tobytes()

            # Clear the stream in preparation for the next frame
            raw_capture.truncate(0)
