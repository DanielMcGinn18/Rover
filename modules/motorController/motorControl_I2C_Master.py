import RPi.GPIO as GPIO
from time import sleep
from flask import Flask,render_template,url_for,request,redirect, make_response, Response, request # micro web framework 
import socket
import json
from time import time

import smbus

speed = 20

bus = smbus.SMBus(1)

# I2C address of Arduino Slave
i2c_address = 0x07
i2c_cmd = 0x01

app = Flask(__name__)

ip_address = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0] # Get IP Address
s.close()

#rendering the HTML page which has the button
@app.route('/')
def index():
	return render_template('motorcontrol.html')


@app.route("/", methods=['GET', 'POST'])
def submit(): 
	global speed
	if request.method == "POST":
		if request.form.get("Fwd"):
			print('Forward')
			data = [0, 1, int(speed), 1, 1, int(speed)]
			bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
		elif request.form.get("Left"):
			print('Left')
			data = [0, 0, int(speed), 1, 1, int(speed)]
			bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
		elif request.form.get("Right"):
			print('Right')
			data = [0, 1, int(speed), 1, 0, int(speed)]
			bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
		elif request.form.get("Bwd"):
			print('Backward')
			data = [0, 0, int(speed), 1, 0, int(speed)]
			bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
		elif request.form.get("Stop"):
			print('Stop')
			data = [0, 1, 0, 1, 1, 0]
			bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
		elif request.form.get("Speed"):
			speed = request.form.get("Speed")
			print(request.form.get("Speed"))
		return render_template('motorcontrol.html')

@app.route('/data', methods=["GET", "POST"])
def data():
	global speed
	string = speed
	data = [time() * 1000, string]
	response = make_response(json.dumps(data))
	response.content_type = 'application/json'
	return response

if __name__ == '__main__':

	app.run(host=ip_address, port=8000, debug=False)
