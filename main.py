import os
import glob
import time
import sys
import thread

import RPi.GPIO as io


io.setmode(io.BOARD)

################## TEMP SENSING

os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")

base_dir = "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + "28*")[0]
device_file = device_folder + "/w1_slave"

def read_temp_raw():
	f = open(device_file, "r")
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	f = open(device_file, "r")
	lines = f.readlines()
	f.close()

	equals_pos = lines[1].find("t=")

	if equals_pos != 1:
		temp_string = lines[1][equals_pos + 2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32
		return temp_f
	else:
		return False

def continuous_read_temp(delay):
	while True:
		try:
			temp = read_temp()

			if temp:
				yield temp
				time.sleep(delay)
		except KeyboardInterrupt:
			pass

######################## Switch On/Off

switch_in = 10

sequence = []

def check_on_off(signal_in, sequence_length):
	io.setup(signal_in, io.IN)
	signal = io.input(signal_in)
	sequence.append(signal)
	if len(sequence) > sequence_length:
		sequence.pop(0)

	if 0 not in sequence:
		return True
	else:
		return False

######################## Main Loop

previous_temp = None

while True:
	try:
	# 	if check_on_off(switch_in, 5):
	# 		print "Checking Temp..."
	# 		temp_reading = read_temp()
	# 		if temp_reading:
	# 			print temp_reading
	# 			previous_temp = temp_reading
	# 		elif previous_temp:
	# 			print previous_temp
	# 		else:
	# 			print "No temp readings yet."
	# 	else:
	# 		print "Switch Off"

	# 	time.sleep(0.001)

		thread.start_new_thread(continuous_read_temp, (5))

	except KeyboardInterrupt:
		io.cleanup()
		sys.exit(1)

