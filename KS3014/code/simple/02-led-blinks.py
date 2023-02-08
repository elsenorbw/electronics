import RPi.GPIO as GPIO
import time


# the positive side of the LED circuit is on GPIO pin 18 (I hope)
led_pin = 18

# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

# set the pin as an output pin
GPIO.setup(led_pin, GPIO.OUT)

# and turn it off
GPIO.output(led_pin, GPIO.LOW)

# 30 seconds..
for _ in range(30):
    # on for half a second
    GPIO.output(led_pin, GPIO.HIGH)
    time.sleep(0.5)

    # and off for half a second
    GPIO.output(led_pin, GPIO.LOW)
    time.sleep(0.5)

# and cleanup
GPIO.cleanup()
