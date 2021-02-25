# Dan McGinn

from flask import Flask,render_template,url_for,request,redirect, make_response, Response, request # micro web framework 
from camera import VideoCamera # Camera Module
import RPi.GPIO as GPIO # GPIO library to control GPIO pins of Raspberry Pi
# from smbus2 import SMBus # i2c capabilities to control atmega328p
import time, threading, os, socket, random, json
from time import time
from random import random
import board, adafruit_hcsr04 # Libraries for Ultrasonic Sensor

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

app = Flask(__name__)

ip_address = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0] # Get IP Address
s.close()

host_port = 8000 # Set host port

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D6) # Setup Untrasonic Sensor

# Initialize Variables for I2C Communication 
# addr = 0x8 # bus address
# bus = SMBus(1) # indicates /dev/ic2-1
# numb = 1

@app.route('/')
def index():
    return render_template('RoverController.html')

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

@app.route("/test", methods=["POST"])
def test():
    slider1 = request.form["slider1"]  # Get slider Value
    p.ChangeDutyCycle(float(slider1)) # Change duty cycle
    sleep(1)
    p.ChangeDutyCycle(0)
    return render_template_string(TPL)

# Send sensor values to webserver
@app.route('/data', methods=["GET", "POST"])
def data():
    # Data1 = random() * 100 # Random Number for testing
    while True:
        try:
            distance = sonar.distance
        except RuntimeError:
            distance = 'Error'
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    data = [time() * 1000, distance, temp]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

if __name__ == '__main__':

    app.run(host=ip_address, port=host_port, debug=False)
    