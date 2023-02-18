import RPi.GPIO as GPIO
import time

# pin definitions for this sketch

pin_data = 17
pin_shift_clock = 22  # sck
pin_latch_clock = 27  # rck
pin_enable = 26  # wired to pin 13 of the latch chip
pin_clear = 19  # wired to pin 10 of the latch chip

# standard functions that are useful every time
LOW = 0
HIGH = 1

assert GPIO.HIGH == HIGH
assert GPIO.LOW == LOW


def setPin(pin, value):
    assert value in (LOW, HIGH)
    print(f"Setting pin {pin} to {value}")
    GPIO.output(pin, value)


show_segments = False
if show_segments:
    digit_bytes = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]
else:
    digit_bytes = [0x3F, 0x06, 0x5B, 0x4F, 0x66, 0x6D, 0x7D, 0x07, 0x7F, 0x6F]


def show_digit(number: int):
    setPin(pin_clear, LOW)
    setPin(pin_clear, HIGH)
    for i in range(8):
        setPin(pin_data, (digit_bytes[number] >> i) & 1)
        setPin(pin_shift_clock, HIGH)
        setPin(pin_shift_clock, LOW)
    setPin(pin_latch_clock, HIGH)
    setPin(pin_latch_clock, LOW)


# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

# initial pin configuration
GPIO.setup(pin_data, GPIO.OUT)
GPIO.setup(pin_shift_clock, GPIO.OUT)
GPIO.setup(pin_latch_clock, GPIO.OUT)
GPIO.setup(pin_enable, GPIO.OUT)  # leave at LOW for enabled
GPIO.setup(pin_clear, GPIO.OUT)  # should be HIGH for normal operation
setPin(pin_latch_clock, LOW)
setPin(pin_shift_clock, LOW)
setPin(pin_enable, LOW)
setPin(pin_clear, HIGH)


# the docs are calling the latch register rck for some reason..

num_repeats = 1
try:
    while True:
        for the_digit in range(len(digit_bytes)):
            for repeat_section in range(num_repeats):
                print(f"Display for digit {the_digit} ({digit_bytes[the_digit]:#02x})")
                show_digit(the_digit)
                time.sleep(0.5)

except Exception as e:
    print(f"Caught an exception ({e}), cleaning up..")
except KeyboardInterrupt as k:
    print(f"Stopping at user request - {k}")
except:
    print("Something very weird happened - stopping anyhow")


# and cleanup
setPin(pin_clear, LOW)
setPin(pin_clear, HIGH)
setPin(pin_latch_clock, HIGH)
setPin(pin_latch_clock, LOW)
GPIO.cleanup()
