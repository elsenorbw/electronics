import RPi.GPIO as GPIO
import time


# the various pins in order
the_pins = [18, 23, 24, 25, 12, 16, 20, 21]

# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

# set the pin as an output pin
for this_pin in the_pins:
    GPIO.setup(this_pin, GPIO.OUT)

    # and turn it off
    GPIO.output(this_pin, GPIO.LOW)


def set_pin_states(the_pins, state):
    for this_pin in the_pins:
        GPIO.output(this_pin, state)
        time.sleep(0.05)


def light_up(the_pins, target_pin):
    for this_idx, this_pin in enumerate(the_pins):
        if this_idx == target_pin:
            the_val = GPIO.HIGH
        else:
            the_val = GPIO.LOW
        GPIO.output(this_pin, the_val)


def knightrider(the_pins):
    for target_idx in range(len(the_pins)):
        light_up(the_pins, target_idx)
        time.sleep(0.05)
    for target_idx in reversed(range(len(the_pins) - 1)):
        light_up(the_pins, target_idx)
        time.sleep(0.05)


# 5 goes..
for _ in range(5):
    set_pin_states(the_pins, GPIO.HIGH)
    set_pin_states(the_pins, GPIO.LOW)

# and knightrider...
for _ in range(20):
    knightrider(the_pins)


# and cleanup
GPIO.cleanup()
