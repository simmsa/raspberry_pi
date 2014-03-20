import time
import sys

import RPi.GPIO as io

io.setmode(io.BOARD)

signal_out = 16
signal_in = 18

io.setup(signal_out, io.OUT)
io.setup(signal_in, io.IN)

io.output(signal_out, 1)

while True:
	try:
		print io.input(signal_in)

		time.sleep(1)
	except KeyboardInterrupt:
		io.cleanup()
		sys.exit()