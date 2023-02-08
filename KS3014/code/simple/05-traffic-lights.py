import RPi.GPIO as GPIO
import time


def show_red(red, amber, green):
    GPIO.output(red, GPIO.HIGH)
    GPIO.output(amber, GPIO.LOW)
    GPIO.output(green, GPIO.LOW)


def show_redamber(red, amber, green):
    GPIO.output(red, GPIO.HIGH)
    GPIO.output(amber, GPIO.HIGH)
    GPIO.output(green, GPIO.LOW)


def show_amber(red, amber, green):
    GPIO.output(red, GPIO.LOW)
    GPIO.output(amber, GPIO.HIGH)
    GPIO.output(green, GPIO.LOW)


def show_green(red, amber, green):
    GPIO.output(red, GPIO.LOW)
    GPIO.output(amber, GPIO.LOW)
    GPIO.output(green, GPIO.HIGH)


# the positive side of the LED circuit is on GPIO pin 18 (I hope)
red_pin = 18
amber_pin = 23
green_pin = 24

# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

# set the pin as an output pin
GPIO.setup(red_pin, GPIO.OUT)
GPIO.setup(amber_pin, GPIO.OUT)
GPIO.setup(green_pin, GPIO.OUT)

# and turn it off
GPIO.output(red_pin, GPIO.LOW)
GPIO.output(amber_pin, GPIO.LOW)
GPIO.output(green_pin, GPIO.LOW)


# quick test of the lights..
for _ in range(5):
    show_red(red_pin, amber_pin, green_pin)
    time.sleep(2)

    show_redamber(red_pin, amber_pin, green_pin)
    time.sleep(1)

    show_green(red_pin, amber_pin, green_pin)
    time.sleep(3)

    show_amber(red_pin, amber_pin, green_pin)
    time.sleep(1)

# and cleanup
GPIO.cleanup()
