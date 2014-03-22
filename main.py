import os
import glob
import time
import sys
import thread

import RPi.GPIO as io

import tweet

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

switch_in = 12

io.setup(switch_in, io.IN)

def check_on_off(signal_in, sequence_length):
	signal = io.input(signal_in)
	sequence.append(signal)
	if len(sequence) > sequence_length:
		sequence.pop(0)

	if 0 not in sequence:
		return True
	else:
		return False


########################## LED Setup and Pulse Functions


RGB_RED = 16 # 23
RGB_GREEN = 18 # 24
RGB_BLUE = 22 # 25

RGB = {"red": RGB_RED, "green": RGB_GREEN, "blue": RGB_BLUE}

red = [1, 0, 0]
green = [0, 1, 0]
blue = [0, 0, 1]
white = [1, 1, 1]
yellow = [1, 1, 0]
cyan = [0, 1, 1]
purple = [1, 0, 1]

colors = {"red": red, "green": green, "blue": blue, "white": white, "yellow": yellow, "cyan": cyan, "purple": purple}

def rgb_setup():
	for val in RGB:
		io.setup(RGB[val], io.OUT)

def rgb_pulse(rgb_led, color, speed, lower_limit):
	r = io.PWM(rgb_led["red"], 50)
	g = io.PWM(rgb_led["green"], 50)
	b = io.PWM(rgb_led["blue"], 50)

	r.start(0)
	g.start(0)
	b.start(0)

	if color not in colors.values():
		raise ValueError("Please enter a valid color")

	try:
		while True:
			for i in range(lower_limit, 100):
				r.ChangeDutyCycle(i * color[0])
				g.ChangeDutyCycle(i * color[1])
				b.ChangeDutyCycle(i * color[2])
				time.sleep(speed)
			for i in range(100, lower_limit, -1):
				r.ChangeDutyCycle(i * color[0])
				g.ChangeDutyCycle(i * color[1])
				b.ChangeDutyCycle(i * color[2])
				time.sleep(speed)


	except KeyboardInterrupt:
		pass

	r.stop()
	g.stop()
	b.stop()


######################## Main Loop

previous_temp = None

rgb_setup()

r = io.PWM(RGB["red"], 50)
g = io.PWM(RGB["green"], 50)
b = io.PWM(RGB["blue"], 50)

r.start(0)
g.start(0)
b.start(0)

current_color = "white"

switch_status = True

sequence = []

temp_status = "normal"

last_tweet_check = time.time()

tweet_check_count = 0

while True:
	try:
		# if check_on_off(switch_in, 5):
		# 	print "Checking Temp..."
		# 	temp_reading = read_temp()
		# 	if temp_reading:
		# 		print temp_reading
		# 		previous_temp = temp_reading
		# 	elif previous_temp:
		# 		print previous_temp
		# 	else:
		# 		print "No temp readings yet."
		# else:
		# 	print "Switch Off"

		# time.sleep(0.001)

		r.ChangeDutyCycle(0)
		g.ChangeDutyCycle(0)
		b.ChangeDutyCycle(0)

		sequence = []

		for i in range(250):
			signal = io.input(switch_in)
			sequence.append(signal)
			time.sleep(0.01)

		if 0 in sequence:
			switch_status = False
		else:
			switch_status = True

		temp_reading = read_temp()
		if temp_reading:
			print temp_reading

			if temp_reading >= 90:
				current_color = "red"
				if temp_status != "really hot":
					tweet.tweet("Holy cow it is really hot in here!")
					temp_status = "really hot"
			elif temp_reading >= 75:
				current_color = "yellow"
				if temp_status != "hot":
					tweet.tweet("Man I'm starting to sweat in here!")
					temp_status = "hot"
			elif temp_reading >= 45:
				current_color = "green"
				if temp_status != "normal":
					tweet.tweet("Looks like everything is back to normal.")
					temp_status = "normal"
			elif temp_reading >= 32:
				current_color = "cyan"
				if temp_status != "cold":
					tweet.tweet("Brr.. its getting colder in here!")
					temp_status = "cold"
			else:
				current_color = "blue"
				if temp_status != "really cold":
					tweet.tweet("Come on turn up the heat, I'm freezin my ass off in here!")
					temp_status = "really_cold"

			previous_temp = temp_reading
		else:
			print previous_temp

		if time.time() - last_tweet_check > 60:
			tweet.temp_request(temp_reading)
			print "The tweet check count is:", tweet_check_count
			last_tweet_check = time.time()
			tweet_check_count += 1

		for i in range(100):
			color = colors[current_color]
			if switch_status:
				r.ChangeDutyCycle(i * color[0])
				g.ChangeDutyCycle(i * color[1])
				b.ChangeDutyCycle(i * color[2])
			time.sleep(0.02)

		for i in range (100, 1, -1):
			color = colors[current_color]
			if switch_status:
				r.ChangeDutyCycle(i * color[0])
				g.ChangeDutyCycle(i * color[1])
				b.ChangeDutyCycle(i * color[2])
			time.sleep(0.02)

	except KeyboardInterrupt:
		io.cleanup()
		sys.exit(1)

		r.stop()
		g.stop()
		b.stop()

