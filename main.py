# Dan McGinn

from flask import Flask,render_template,url_for,request,redirect, make_response, Response, request # micro web framework 
from camera import VideoCamera # Camera Module
import RPi.GPIO as GPIO # GPIO library to control GPIO pins of Raspberry Pi
import time, threading, os, socket, random, json
from time import time
from random import random
import board, adafruit_hcsr04 # Libraries for Ultrasonic Sensor

import smbus

speed = 20
direction = 'Stop'

bus = smbus.SMBus(1)

# I2C address of Arduino Slave
i2c_address = 0x07
i2c_cmd = 0x01

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT) 
fan = 0
GPIO.output(16, fan) # turn fan off

pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

app = Flask(__name__)

ip_address = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0] # Get IP Address
s.close()

host_port = 8000 # Set host port

def Forward(speed):
    global direction
    print('Forward')
    speed = int(speed)/2
    data = [0, 1, int(speed), 1, 1, int(speed)]
    bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
    direction = 'Forward'

def Left(speed):
    global direction
    speed = int(speed)/2
    print('Left')
    data = [0, 0, int(speed), 1, 1, int(speed)]
    bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
    direction = 'Left'

def Right(speed):
    global direction
    speed = int(speed)/2
    print('Right')
    data = [0, 1, int(speed), 1, 0, int(speed)]
    bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
    direction = 'Right'

def Backward(speed):
    global direction
    speed = int(speed)/2
    print('Backward')
    data = [0, 0, int(speed), 1, 0, int(speed)]
    bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
    direction = 'Backward'

def Stop():
    global direction
    print('Stop')
    data = [0, 1, 0, 1, 1, 0]
    bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
    direction = 'Stop'

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

@app.route("/", methods=['GET', 'POST'])
def submit(): 
    global fan, speed, direction
    if request.method == "POST":
        if request.form.get("fan"):
            if fan == 0:
                fan = 1
                GPIO.output(16, fan) # turn fan on
                print ("Fan On")
            else:
                fan = 0
                GPIO.output(16, fan) # turn fan off
                print ("Fan Off")
        if request.form.get("Fwd"):
            Forward(speed)
        elif request.form.get("Left"):
            Left(speed)
        elif request.form.get("Right"):
            Right(speed)
        elif request.form.get("Bwd"):
            Backward(speed)
        elif request.form.get("Stop"):
            Stop()
        elif request.form.get("Speed"):
            speed = request.form.get("Speed")
            print(request.form.get("Speed"))
            if direction == 'Forward':
                Forward(speed)
            elif direction == 'Left':
                Left(speed)
            elif direction == 'Right':
                Right(speed)
            elif direction == 'Backward':
                Backward(speed)
            else:
                Stop()
    return render_template('RoverController.html')

# Send sensor values to webserver
@app.route('/data', methods=["GET", "POST"])
def data():
    global speed, fan, direction
    directionData = direction
    speedData = speed
    if fan == 1:
        fanData = 'Cooling Fan: On'
    else:
        fanData = 'Cooling Fan: Off'
    temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    temp_US = ('CPU Temp: ' + str(round(((float(temp.split('=')[1].split("'")[0])*1.8)+30),2)) +
     u'\N{DEGREE SIGN}' + ' F') # Convert to Fahrenheit
    data = [time() * 1000, temp_US, speedData, fanData, directionData]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

if __name__ == '__main__':

    app.run(host=ip_address, port=host_port, debug=False)
    