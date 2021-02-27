import RPi.GPIO as GPIO
from time import sleep
from flask import Flask, render_template, Response, request # micro web framework 
import socket

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT) 
fan = 0

app = Flask(__name__)

ip_address = '';
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
ip_address = s.getsockname()[0] # Get IP Address
s.close()

#rendering the HTML page which has the button
@app.route('/')
def json():
	return render_template('coolingfan.html')

#background process happening without any refreshing
@app.route('/background_process')
def background_process():
	global fan
	if fan == 0:
		fan = 1
		GPIO.output(16, fan) # switch it on
		print ("Fan On")
	else:
		fan = 0
		GPIO.output(16, fan) # switch it off
		print ("Fan Off")
	return ("nothing")

@app.route('/data', methods=["GET", "POST"])
def data():
	global fan
	data1 = 'Cooling Fan: ' + fan
	data = [fan]
	response = make_response(json.dumps(data))
	response.content_type = 'application/json'
	return response

if __name__ == '__main__':

	app.run(host=ip_address, port=8000, debug=False)
