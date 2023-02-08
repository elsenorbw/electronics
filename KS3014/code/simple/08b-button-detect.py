import RPi.GPIO as GPIO
import time


# the various pins in order
the_pins = [18, 23, 24, 25, 12, 16, 20, 21]
buzzer_pin = 13
button_pin = 19


# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

GPIO.setup(buzzer_pin, GPIO.OUT)
GPIO.output(buzzer_pin, GPIO.LOW)

GPIO.setup(button_pin, GPIO.IN, GPIO.PUD_UP)


def button_pressed(button_pin):
    the_val = GPIO.input(button_pin)
    return the_val == 0


def output_situation(the_pins, buzzer_pin, situation_level):
    if situation_level > 6:
        GPIO.output(buzzer_pin, GPIO.HIGH)
    else:
        GPIO.output(buzzer_pin, GPIO.LOW)

    # now light up the relevant lights..
    for idx, the_pin in enumerate(the_pins, start=1):
        if idx <= situation_level:
            the_val = GPIO.HIGH
        else:
            the_val = GPIO.LOW
        GPIO.output(the_pin, the_val)


def buzz():
    GPIO.output(buzzer_pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(buzzer_pin, GPIO.LOW)


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


# loop until we want to break free..
situation = 0
while situation < 10:
    # is the button pressed ?
    if button_pressed(button_pin):
        situation += 1
    else:
        situation -= 1
    # bounds..
    situation = max(0, situation)
    situation = min(10, situation)
    #  apply the current situation to the output devices..
    output_situation(the_pins, buzzer_pin, situation)

    # and wait a moment..
    time.sleep(0.5)


for _ in range(5):
    set_pin_states(the_pins, GPIO.HIGH)
    buzz()
    set_pin_states(the_pins, GPIO.LOW)

# and knightrider...
for _ in range(20):
    knightrider(the_pins)


# and cleanup
GPIO.cleanup()
