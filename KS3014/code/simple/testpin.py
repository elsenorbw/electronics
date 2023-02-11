#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
import sys


valid_pins = [18, 23, 24, 25, 12, 16, 20, 21, 4, 17, 27, 22, 5, 6, 13, 19, 26]

# check a given pin is working correctly
if len(sys.argv) < 2:
    print(
        f"You need to provide a pin-id (or a comma separated list) (BCM) and optionally a number of seconds for each state (not {sys.argv})\nValid pins are {valid_pins}"
    )
    sys.exit(1)

# check the input pin is valid
pins = sys.argv[1]
individual_pins = pins.split(",")
the_pins = [int(s.strip()) for s in individual_pins]
valid_check = [x in valid_pins for x in the_pins]

if not all(valid_check):
    print(f"Invalid pin configuration {the_pins}, valid choices are {valid_pins}")
    sys.exit(2)

if len(sys.argv) > 2:
    state_seconds = int(sys.argv[2])
else:
    state_seconds = 5

print(
    f"Going to flip pin {the_pins} between high and low with each state lasting {state_seconds} seconds"
)

# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)


for the_pin in the_pins:
    # set the pin as an output pin
    GPIO.setup(the_pin, GPIO.OUT)

    # and turn it off
    GPIO.output(the_pin, GPIO.LOW)

try:
    idx = 0
    while True:
        the_pin = the_pins[idx]
        # on
        print(f"setting pin {the_pin} -> HIGH")
        GPIO.output(the_pin, GPIO.HIGH)
        time.sleep(state_seconds)

        # and off
        print(f"setting pin {the_pin} -> LOW")
        GPIO.output(the_pin, GPIO.LOW)
        time.sleep(state_seconds)

        # next
        idx += 1
        if idx >= len(the_pins):
            idx = 0

except:
    print(f"Caught an exception - exiting with cleanup")

# and cleanup
GPIO.cleanup()
