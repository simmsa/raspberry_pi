import time

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


LED = [LED_1, LED_2, LED_3, LED_4, LED_5]

RGB_RED = 16 # 23
RGB_GREEN = 18 # 24
RGB_BLUE = 22 # 25

RGB = [RGB_RED, RGB_GREEN, RGB_BLUE]

def led_setup():
	io.setmode(io.BOARD)

	for val in LED:
		io.setup(val, io.OUT)
	for val in RGB:
		io.setup(val, io.OUT)

def led_activate(led):
	io.output(led, LED_ON)

def led_deactivate(led):
	io.output(led, LED_OFF)

def led_clear():
	for val in LED:
		led_deactivate(val)
	for val in RGB:
		led_deactivate(val)

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
blue = [0, 1, 0]

colors = [red, green, blue]

def main():
	led_setup()
	led_clear()
	for color in colors:
		rgb_activate(color)
		time.sleep(3)
	led_clear()
	io.cleanup()

main()