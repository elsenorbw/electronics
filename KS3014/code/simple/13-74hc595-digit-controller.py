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


# specific to this pattern functions

bitmasks = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]


def push_byte(the_byte: int):
    low(latch_register_clock_pin)
    for this_bit in range(8):
        low(shift_register_clock_pin)
        if the_byte & 0x01 == 0x01:
            high(data_pin)
        else:
            low(data_pin)
        high(shift_register_clock_pin)
    high(latch_register_clock_pin)


def display(digit: int):
    # set the latch register low
    low(latch_register_clock_pin)

    # output all the individual bits..
    the_digit_bitmask = bitmasks[digit]
    for this_bit in range(8):
        # tell the chip to get ready for new data
        low(shift_register_clock_pin)
        time.sleep(0.01)

        # see if the bottom bit is set..
        if the_digit_bitmask & 0x01 == 0x01:
            high(data_pin)
        else:
            low(data_pin)

        time.sleep(0.01)

        # pop that into the latch chip
        high(shift_register_clock_pin)
        time.sleep(0.01)

        print(
            f"digit={digit}, original_bitmask={bitmasks[digit]:#02x}({bitmasks[digit]:>08b}), remaining_mask={the_digit_bitmask:>08b}"
        )

        # and discard that bit
        the_digit_bitmask >>= 1

    # set the latch register high - this should change the output on the lines to the new values
    high(latch_register_clock_pin)


# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

# initial pin configuration
set_output(data_pin)
set_output(shift_register_clock_pin, start_low=False)
set_output(latch_register_clock_pin, start_low=False)

push_byte(0)  # the chip remembers until powered down..

# the docs are calling the latch register rck for some reason..

try:
    while True:
        for the_digit in range(10):
            for i in range(4):
                print(f"Display loop {i}")
                push_byte(0)
                display(the_digit)
                time.sleep(0.75)

except Exception as e:
    print(f"Caught an exception ({e}), cleaning up..")
except KeyboardInterrupt as k:
    print(f"Stopping at user request - {k}")
except:
    print("Something very weird happened - stopping anyhow")


# and cleanup
push_byte(0)
GPIO.cleanup()
