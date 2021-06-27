import smbus

bus = smbus.SMBus(1)

# I2C address of Arduino Slave
i2c_address = 0x07
i2c_cmd = 0x01

numb = 1

print ("Enter in the format 'motor, direction, speed'")
print ("motor: 0 for B 1 for A")
print("direction: 0 clockwise, 1 counter-clockwise")
print ("speed: 0 is off, and 255 is full speed")

while numb == 1:

	input1 = input(">>>>   ")
	innputArray = input1.split(",")
	for i in range(0, len(innputArray)):
		innputArray[i] = int(innputArray[i])
	innputArray[2] = int(innputArray[2]/2)
	if len(innputArray) >= 5:
		innputArray[5] = int(innputArray[5]/2)
	if (0 <= innputArray[0] <= 1) and (0 <= innputArray[1] <= 1) and (0 <= innputArray[2] <= 255):
		bus.write_i2c_block_data(i2c_address, i2c_cmd, innputArray)
	else:
		numb = 0