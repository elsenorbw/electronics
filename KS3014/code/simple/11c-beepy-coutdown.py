import RPi.GPIO as GPIO
import time
from threading import Timer


# define the various pins in use..
digit_1 = 22
digit_2 = 27
digit_3 = 17
digit_4 = 24

# and now the segment displays..
bottom_right = 12
top_left = 26
top_right = 13
bottom = 20
bottom_left = 16
decimal_point = 21
top = 19
middle = 25

segment_pins = [
    top,
    top_right,
    bottom_right,
    bottom,
    bottom_left,
    top_left,
    middle,
]

buzzer_pin = 18

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
    -1: [False, False, False, False, False, False, False],
}


digit_pins = [digit_1, digit_2, digit_3, digit_4]


def display_digit(the_digit):
    settings = zip(segment_pins, digits_layouts[the_digit])
    for pin, enabled in settings:
        if enabled:
            pin_state = GPIO.HIGH
        else:
            pin_state = GPIO.LOW
        GPIO.output(pin, pin_state)


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

set_output(segment_pins)
set_output(digit_pins)
set_output([buzzer_pin])


def chop_int(i):
    result = []

    while i >= 10:
        result.append(i % 10)
        i //= 10
    result.append(i)

    # padding
    while len(result) < 4:
        result.append(0)

    return list(reversed(result))


the_value = 1234


def display():
    if the_value >= 0:
        the_digits = chop_int(the_value)
    else:
        the_digits = [-1, -1, -1, -1]

    for target_digit, value_to_display in zip(digit_pins, the_digits[:4]):
        high(digit_pins)
        low(target_digit)

        # and light the thing up..
        display_digit(value_to_display)
        time.sleep(0.005)

    # and get ourselves called again..
    if the_value != -42:
        t = Timer(0.005, display)
        t.start()


def nobuzz():
    low(buzzer_pin)


def beep(beep_length):
    high(buzzer_pin)
    t = Timer(beep_length, nobuzz)
    t.start()


try:
    # start the display loop
    display()

    # now run our logic
    delay_between_numbers = 0.1
    delay_reduction = 0.9

    for target_idx in range(1500, 0, -1):
        # display this value on the segment display
        the_value = target_idx

        # is it time to change the buzzer state ?
        if target_idx % 50 == 0:
            delay_between_numbers *= delay_reduction
            delay_between_numbers = max(delay_between_numbers, 0.01)
            beep(0.5)

        time.sleep(delay_between_numbers)

    # and now beep solidly and flash the display
    for _ in range(10):
        high(buzzer_pin)
        the_value = 0
        time.sleep(0.25)
        low(buzzer_pin)
        the_value = -1
        time.sleep(0.25)

except:
    print(f"Caught an exception, cleaning up..")


# and cleanup
the_value = -42
time.sleep(0.5)
GPIO.cleanup()
