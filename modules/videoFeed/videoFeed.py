# Dan McGinn

from flask import Flask,render_template,url_for,request,redirect, make_response, Response, request # micro web framework 
from camera import VideoCamera # Camera Module
import RPi.GPIO as GPIO # GPIO library to control GPIO pins of Raspberry Pi
import time, threading, os, socket, random, json

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

app = Flask(__name__)

ip_address = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0] # Get IP Address
s.close()

host_port = 8000 # Set host port

@app.route('/')
def index():
    return render_template('videoFeed.html')

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':

    app.run(host=ip_address, port=host_port, debug=False)
    