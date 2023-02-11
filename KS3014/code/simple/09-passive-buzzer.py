import RPi.GPIO as GPIO
import time


# the positive side of the LED circuit is on GPIO pin 18 (I hope)
buzzer_pin = 18

# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

# set the pin as an output pin
GPIO.setup(buzzer_pin, GPIO.OUT)

# and turn it off
GPIO.output(buzzer_pin, GPIO.LOW)


def noise(iterations: int, interval_ms: int, the_pin: int):
    interval_seconds = interval_ms / 1000.0
    print(f"Executing {iterations} loops with a delay of {interval_seconds}")
    for _ in range(iterations):
        GPIO.output(the_pin, GPIO.HIGH)
        time.sleep(interval_seconds)
        GPIO.output(the_pin, GPIO.LOW)
        time.sleep(interval_seconds)


for _ in range(50):
    noise(50, 1, buzzer_pin)
    time.sleep(0.3)


# and cleanup
GPIO.cleanup()
