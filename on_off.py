import time
import sys

import RPi.GPIO as io

io.setmode(io.BOARD)

signal_in = 18

io.setup(signal_in, io.IN)

while True:
	try:
		print io.input(signal_in)

		time.sleep(1)
	except KeyboardInterrupt:
		io.cleanup()
		sys.exit()