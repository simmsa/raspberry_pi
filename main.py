import time
import sys

import RPi.GPIO as io

from on_off import check_on_off
from temp_sensor import read_temp

switch_in = 10

sequence = []

while True:
	try:
		if check_on_off(switch_in, 5):
			print read_temp()

		time.sleep(0.001)
	except KeyboardInterrupt:
		io.cleanup()
		sys.exit(1)

