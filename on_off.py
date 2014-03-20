import time
import sys

import RPi.GPIO as io

io.setmode(io.BOARD)


signal_in = 18

led = 22

io.setup(signal_in, io.IN)
io.setup(led, io.OUT)

while True:
	try:
		print io.input(signal_in)
		if io.input(signal_in):
			io.output(led, 1)
		else:
			io.output(led, 0)
		time.sleep(1)
	except KeyboardInterrupt:
		io.cleanup()
		sys.exit()