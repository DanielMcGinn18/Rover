import RPi.GPIO as GPIO
from time import sleep
from flask import Flask,render_template,url_for,request,redirect, make_response, Response, request # micro web framework 
import socket
import json
from time import time

import smbus

motors = 0

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
	if request.method == "POST":
		if request.form.get("Fwd"):
			print('Fwd')
			data = [0, 1, 50, 1, 1, 50]
			bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
		elif request.form.get("Stop"):
			print('Stop')
			data = [0, 1, 0, 1, 1, 0]
			bus.write_i2c_block_data(i2c_address, i2c_cmd, data)
		return render_template('motorcontrol.html')


#background process happening without any refreshing
@app.route('/background_process')
def background_process():
	print('Yes')
	default_name = '0'
	data = request.form.get('test', default_name)
	print(data)
	return ("nothing")

if __name__ == '__main__':

	app.run(host=ip_address, port=8000, debug=False)
