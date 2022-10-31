#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
import base64

# import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

import time
from apscheduler.schedulers.background import BackgroundScheduler
import numpy as np
import cv2

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def takepic():
    frame = Camera().get_frame()
    asb64 = base64.b64decode(frame)
    jpg_as_np = np.frombuffer(asb64, dtype=np.uint8)
    img = cv2.imdecode(jpg_as_np, flags=1)
    cv2.imwrite('imgs/+'+time.strftime("%Y%m%d-%H%M%S")+'.png', img)



if __name__ == '__main__':

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=takepic, trigger="interval", seconds=60)

    scheduler.start()

    app.run(host='0.0.0.0', threaded=True, port=80)