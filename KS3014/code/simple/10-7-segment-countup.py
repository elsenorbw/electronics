import RPi.GPIO as GPIO
import time


# the positive side of the LED circuit is on GPIO pin 18 (I hope)
# order is : top, top-right, bottom-right, bottom, bottom-left, top-left, middle, decimal-point
bottom_right = 16
top_left = 19
top_right = 6
bottom = 20
bottom_left = 21
decimal_point = 12
top = 13
middle = 26

segment_pins = [
    top,
    top_right,
    bottom_right,
    bottom,
    bottom_left,
    top_left,
    middle,
]

digits_layouts = {
    0: [True, True, True, True, True, True, False],
    1: [False, True, True, False, False, False, False],
    2: [True, True, False, True, True, False, True],
    3: [True, True, True, True, False, False, True],
    4: [False, True, True, False, False, True, True],
    5: [True, False, True, True, False, True, True],
    6: [True, False, True, True, True, True, True],
    7: [True, True, True, False, False, False, False],
    8: [True, True, True, True, True, True, True],
    9: [True, True, True, True, False, True, True],
}

# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

# set all the pins to output and off..
for this_pin in segment_pins:
    # set the pin as an output pin
    GPIO.setup(this_pin, GPIO.OUT)
    GPIO.output(this_pin, GPIO.LOW)

GPIO.setup(decimal_point, GPIO.OUT)
GPIO.setup(decimal_point, GPIO.LOW)


def display_digit(the_digit):
    settings = zip(segment_pins, digits_layouts[the_digit])
    for pin, enabled in settings:
        if enabled:
            pin_state = GPIO.HIGH
        else:
            pin_state = GPIO.LOW
        GPIO.output(pin, pin_state)


def dp_on():
    GPIO.output(decimal_point, GPIO.HIGH)


def dp_off():
    GPIO.output(decimal_point, GPIO.LOW)


# Infinite countups..
try:
    while True:
        for digit in range(10):
            # setup the pins..
            display_digit(digit)
            dp_off()
            time.sleep(0.5)
            dp_on()
            time.sleep(0.5)

except:
    print(f"Caught an exception, exiting")

# and cleanup
GPIO.cleanup()
