#!/usr/bin/python
# -*- coding: ascii -*-
import sys
import time
import signal
from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2

app = Flask(__name__)

# context = zmq.Context()
# socket = context.socket(zmq.REP)
# socket.bind("tcp://*:5558")

@app.route('/')
def index():
    return render_template('index2.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)