import RPi.GPIO as GPIO
import time

# pin definitions for this sketch

data_pin = 17
shift_register_clock_pin = 22  # sck
latch_register_clock_pin = 27  # rck


# standard functions that are useful every time


def is_iterable(obj):
    try:
        _ = iter(obj)
    except:
        return False
    return True


def set_output(pin_list, start_low=True):
    if not is_iterable(pin_list):
        pin_list = [pin_list]

    for this_pin in pin_list:
        GPIO.setup(this_pin, GPIO.OUT)
        if start_low:
            GPIO.output(this_pin, GPIO.LOW)
        else:
            GPIO.output(this_pin, GPIO.HIGH)


def high(the_pin):
    if is_iterable(the_pin):
        for this_pin in the_pin:
            GPIO.output(this_pin, GPIO.HIGH)
    else:
        GPIO.output(the_pin, GPIO.HIGH)


def low(the_pin):
    if is_iterable(the_pin):
        for this_pin in the_pin:
            GPIO.output(this_pin, GPIO.LOW)
    else:
        GPIO.output(the_pin, GPIO.LOW)


def pulse(the_pin):
    """Execute a high-low pulse"""
    high(the_pin)
    low(the_pin)


# specific to this pattern functions

bitmasks = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]


def display(digit: int):
    # output all the individual bits..
    the_digit_bitmask = bitmasks[digit]

    for this_bit in range(8):
        # see if the bottom bit is set..
        if the_digit_bitmask & 0x01 == 0x01:
            high(data_pin)
        else:
            low(data_pin)

        pulse(shift_register_clock_pin)

        # and discard that bit
        the_digit_bitmask >>= 1

    # and pulse the latch register
    pulse(latch_register_clock_pin)


# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

# initial pin configuration
set_output(data_pin)
set_output(shift_register_clock_pin, start_low=True)
set_output(latch_register_clock_pin, start_low=True)


# the docs are calling the latch register rck for some reason..

try:
    while True:
        for the_digit in range(10):
            for i in range(2):
                print(f"Display loop {i} for digit {the_digit}")
                display(the_digit)
                time.sleep(0.5)

except Exception as e:
    print(f"Caught an exception ({e}), cleaning up..")
except KeyboardInterrupt as k:
    print(f"Stopping at user request - {k}")
except:
    print("Something very weird happened - stopping anyhow")


# and cleanup
GPIO.cleanup()
