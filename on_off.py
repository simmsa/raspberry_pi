import time
import sys

import RPi.GPIO as io

io.setmode(io.BOARD)

signal_in = 18


# def on_off(signal_in, sequence_length):
#     io.setup(signal_in, io.IN)
#     sequence = []
#     while True:
#         try:
#             signal = io.input(signal_in)
#             sequence.append(signal)
#             if 0 not in sequence:
#                 yield True, "Switch is on."
#             else:
#                 yield False, "Switch is off."
#             if len(sequence) > sequence_length:
#                 sequence.pop(0)
#             time.sleep(0.01)
#         except KeyboardInterrupt:
#             io.cleanup()
#             sys.exit()

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


if __name__ == "__main__":
    while True:
        try:
            print check_on_off(signal_in, 5)
            time.sleep(0.01)
        except KeyboardInterrupt:
            io.cleanup()
            sys.exit(1)

