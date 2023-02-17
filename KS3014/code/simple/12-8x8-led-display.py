import RPi.GPIO as GPIO
import time


row_pins = [27, 4, 5, 17, 26, 6, 19, 13]
col_pins = [24, 16, 20, 18, 21, 23, 25, 12]


def is_iterable(obj):
    try:
        _ = iter(obj)
    except:
        return False
    return True


def set_output(pin_list):
    for this_pin in pin_list:
        GPIO.setup(this_pin, GPIO.OUT)
        GPIO.output(this_pin, GPIO.LOW)


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


# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

set_output(row_pins)
set_output(col_pins)

try:
    while True:
        # light em up..
        for this_row in row_pins:
            high(this_row)
            time.sleep(0.5)
        # and un-light em up..
        for this_row in row_pins:
            low(this_row)
            time.sleep(0.5)
except Exception as e:
    print(f"Caught an exception ({e}), cleaning up..")
except KeyboardInterrupt as k:
    print(f"Stopping at user request - {k}")
except:
    print("Something very weird happened - stopping anyhow")


# and cleanup
GPIO.cleanup()
