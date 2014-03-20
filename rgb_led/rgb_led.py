import time
import sys

import RPi.GPIO as io

# RGB LED Testing

# Setup Active States
LED_ON = 1
LED_OFF = 0
RGB_ON = 1
RGB_OFF = 0

# LED Configuration
# Setting GPIO ports

LED_1 = 7 # 4
LED_2 = 11 # 17
LED_3 = 12 # 18
LED_4 = 13 # 21, 27
LED_5 = 15 # 22

argv_color = sys.argv[1]
argv_speed = float(sys.argv[2])
argv_lower_limit = int(sys.argv[3])

LED = [LED_1, LED_2, LED_3, LED_4, LED_5]

RGB_RED = 16 # 23
RGB_GREEN = 18 # 24
RGB_BLUE = 22 # 25

# RGB = [RGB_RED, RGB_GREEN, RGB_BLUE]
RGB = {"red": RGB_RED, "green": RGB_GREEN, "blue": RGB_BLUE}

def led_setup():
	io.setmode(io.BOARD)

	for val in LED:
		io.setup(val, io.OUT)
	for val in RGB:
		io.setup(RGB[val], io.OUT)

def led_activate(led):
	io.output(led, LED_ON)

def led_deactivate(led):
	io.output(led, LED_OFF)

def led_clear():
	for val in LED:
		led_deactivate(val)
	for val in RGB:
		led_deactivate(RGB[val])

def rgb_activate(values):
	start = 0
	for val in values:
		if val > 0:
			led_activate(RGB[start])
		else:
			led_deactivate(RGB[start])
		start += 1

red = [1, 0, 0]
green = [0, 1, 0]
blue = [0, 0, 1]
white = [1, 1, 1]
yellow = [1, 1, 0]
cyan = [0, 1, 1]
purple = [1, 0, 1]

colors = {"red": red, "green": green, "blue": blue, "white": white, "yellow": yellow, "cyan": cyan, "purple": purple}

def rgb_cycle(times):
	for x in xrange(times):
		for color in colors:
			rgb_activate(color)
			time.sleep(0.1)

def led_pulse(led, speed, lower_limit):
	p = io.PWM(led, 50)

	p.start(0)

	try:
		while True:
			for i in range(lower_limit, 100):
				p.ChangeDutyCycle(i)
				time.sleep(speed)
			for i in range(100, lower_limit, -1):
				p.ChangeDutyCycle(i)
				time.sleep(speed)
	except KeyboardInterrupt:
		pass

	p.stop()

def rgb_pulse(rgb_led, color, speed, lower_limit):
	r = io.PWM(rgb_led["red"], 50)
	g = io.PWM(rgb_led["green"], 50)
	b = io.PWM(rgb_led["blue"], 50)

	r.start(0)
	g.start(0)
	b.start(0)

	if color not in colors:
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

def main():
	led_setup()
	led_clear()
	rgb_pulse(RGB, colors[argv_color], argv_speed, argv_lower_limit)
	led_clear()
	io.cleanup()

main()