import time

import RPi.GPIO as io

io.setmode(io.BOARD)

signal_out = 16
signal_in = 18

io.setup(signal_out, io.OUT)
io.setup(signal_in, io.IN)

while True:
	io.output(signal_out, 1)

	print io.input(signal_in)

	time.sleep(1)