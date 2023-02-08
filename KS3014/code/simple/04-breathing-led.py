import RPi.GPIO as GPIO
import time


def brighten(the_pulsewidthmodulation):
    for this_brightness in range(0, 101, 1):
        the_pulsewidthmodulation.ChangeDutyCycle(this_brightness)
        time.sleep(0.01)


def darken(the_pulsewidthmodulation):
    for this_brightness in range(100, -1, -1):
        the_pulsewidthmodulation.ChangeDutyCycle(this_brightness)
        time.sleep(0.01)


# the positive side of the LED circuit is on GPIO pin 18 (I hope)
led_pin = 18

# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

# set the pin as an output pin
GPIO.setup(led_pin, GPIO.OUT)

# and turn it off
GPIO.output(led_pin, GPIO.LOW)

# create a pulse width modulation
pulse_width_modulation_gpio18 = GPIO.PWM(18, 100)
pulse_width_modulation_gpio18.start(0)

# 5 fades..
for _ in range(5):
    brighten(pulse_width_modulation_gpio18)
    darken(pulse_width_modulation_gpio18)

# and cleanup
GPIO.cleanup()
