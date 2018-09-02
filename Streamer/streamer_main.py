#!/usr/bin/python
# -*- coding: ascii -*-
import sys
import time
import signal
from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
from camera import VideoCamera
import cv2

app = Flask(__name__)

# context = zmq.Context()
# socket = context.socket(zmq.REP)
# socket.bind("tcp://*:5558")

@app.route('/')
def index():
    return render_template('robot2.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/Move_forward')
def move_forward():
    forward_message = "Moving Forward..."
    print forward_message
    return forward_message

@app.route("/forward", methods=['GET' , 'POST'])
def move_forward2():
    #Moving forward code
    forward_message = "Moving Forward..."
    return render_template('robot2.html', message=forward_message);

@app.route('/square/', methods=['POST'])
def square():
	num = float(request.form.get('number', 0))
	square = num ** 2
	data = {'square': square}
	data = jsonify(data)
	return data

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
