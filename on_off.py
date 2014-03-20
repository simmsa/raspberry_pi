import time
import sys

import RPi.GPIO as io

io.setmode(io.BOARD)

sequence_length = sys.argv[1]

signal_in = 18

led = 22

io.setup(signal_in, io.IN)
io.setup(led, io.OUT)

sequence = []

while True:
	try:
		signal = io.input(signal_in)
		print signal
		sequence.append(signal)
		if 0 in sequence:
			io.output(led, 1)
		else:
			io.output(led, 0)
		if len(sequence) > sequence_length:
			sequence.pop(0)
		time.sleep(1)
	except KeyboardInterrupt:
		io.cleanup()
		sys.exit()