#  Raspberry Pi Master for Arduino Slave
#  Connects to Arduino via I2C

from smbus import SMBus

addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

numb = 1

print ("Enter PWM value for Motor (0-255)")
while numb == 1:

	input1 = int(input(">>>>   "))
	input1 = int(input1/2)

	if 0 <= number <= 255:
		bus.write_byte(addr, input1) # switch it on
	else:
		numb = 0