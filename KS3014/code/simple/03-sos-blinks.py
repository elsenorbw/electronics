import RPi.GPIO as GPIO
import time

# the positive side of the LED circuit is on GPIO pin 18 (I hope)
led_pin = 18


def dot(the_pin=led_pin):
    GPIO.output(the_pin, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(the_pin, GPIO.LOW)
    time.sleep(0.1)


def dash(the_pin=led_pin):
    GPIO.output(the_pin, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(the_pin, GPIO.LOW)
    time.sleep(0.1)


morse_code_alphabet = {
    "A": [dot, dash],
    "B": [dash, dot, dot, dot],
    "C": [dash, dot, dash, dot],
    "D": [dash, dot, dot],
    "E": [dot],
    "F": [dot, dot, dash, dot],
    "G": [dash, dash, dot],
    "H": [dot, dot, dot, dot],
    "I": [dot, dot],
    "J": [dot, dash, dash, dash],
    "K": [dash, dot, dash],
    "L": [dot, dash, dot, dot],
    "M": [dash, dash],
    "N": [dash, dot],
    "O": [dash, dash, dash],
    "P": [dot, dash, dash, dot],
    "Q": [dash, dash, dot, dash],
    "R": [dot, dash, dot],
    "S": [dot, dot, dot],
    "T": [dash],
    "U": [dot, dot, dash],
    "V": [dot, dot, dot, dash],
    "W": [dot, dash, dash],
    "X": [dash, dot, dot, dash],
    "Y": [dash, dot, dash, dash],
    "Z": [dash, dash, dot, dot],
}


def send_message(the_message: str):
    gap_between_letters = 1
    space_gap = 3
    for this_character in the_message:
        if " " == this_character:
            time.sleep(space_gap)
        else:
            the_signals = morse_code_alphabet[this_character]
            for this_signal in the_signals:
                this_signal(led_pin)
        time.sleep(gap_between_letters)


# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

# set the pin as an output pin
GPIO.setup(led_pin, GPIO.OUT)

# and turn it off
GPIO.output(led_pin, GPIO.LOW)

# 10 messages
for _ in range(10):
    send_message("SOS")

# and cleanup
GPIO.cleanup()
