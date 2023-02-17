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


def set_grid(x, y, bright):
    if bright:
        high(row_pins[x])
        low(col_pins[y])
    else:
        low(row_pins[x])
        high(col_pins[y])


def light_grid(x, y):
    set_grid(x, y, True)


def dark_grid(x, y):
    set_grid(x, y, False)


# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

set_output(row_pins)
set_output(col_pins)
high(col_pins)

try:
    old_x = -1
    old_y = -1
    start_x = 0
    start_y = 2

    # start at the beginning
    x = start_x
    y = start_y
    # and go down and right..
    x_increment = 1
    y_increment = 1

    while True:
        # calculate the next position..
        old_x = x
        old_y = y
        x += x_increment
        y += y_increment
        if x < 0 or x >= len(row_pins):
            # flip the script
            x_increment = 0 - x_increment
            # and apply it twice because we should have bounced..
            x += 2 * x_increment
        if y < 0 or y >= len(col_pins):
            y_increment = 0 - y_increment
            y += 2 * y_increment
        # and we're ready to draw
        light_grid(x, y)
        dark_grid(old_x, old_y)
        time.sleep(0.1)

except Exception as e:
    print(f"Caught an exception ({e}), cleaning up..")
except KeyboardInterrupt as k:
    print(f"Stopping at user request - {k}")
except:
    print("Something very weird happened - stopping anyhow")


# and cleanup
GPIO.cleanup()
