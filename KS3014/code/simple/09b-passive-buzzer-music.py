import RPi.GPIO as GPIO
import time


# Happy birthday
Do = 262
Re = 294
Mi = 330
Fa = 349
Sol = 392
La = 440
Si = 494
Do_h = 523
Re_h = 587
Mi_h = 659
Fa_h = 698
Sol_h = 784
La_h = 880
Si_h = 988

song_1 = [
    Sol,
    Sol,
    La,
    Sol,
    Do_h,
    Si,
    Sol,
    Sol,
    La,
    Sol,
    Re_h,
    Do_h,
    Sol,
    Sol,
    Sol_h,
    Mi_h,
    Do_h,
    Si,
    La,
    Fa_h,
    Fa_h,
    Mi_h,
    Do_h,
    Re_h,
    Do_h,
]


beat_1 = [
    0.5,
    0.5,
    1,
    1,
    1,
    1 + 1,
    0.5,
    0.5,
    1,
    1,
    1,
    1 + 1,
    0.5,
    0.5,
    1,
    1,
    1,
    1,
    1,
    0.5,
    0.5,
    1,
    1,
    1,
    1 + 1,
]


# the positive side of the LED circuit is on GPIO pin 18 (I hope)
buzzer_pin = 18

# use the GPIO numbering system
GPIO.setmode(GPIO.BCM)

# set the pin as an output pin
GPIO.setup(buzzer_pin, GPIO.OUT)

# and create a pulse width modulation
buzzer_pwm = GPIO.PWM(buzzer_pin, 440)
buzzer_pwm.start(50)


def play_song(notes, timing, the_pwm):
    for i in range(len(notes)):
        # play this note..
        the_pwm.ChangeFrequency(notes[i])
        time.sleep(timing[i] * 0.5)


# play the song once..
for _ in range(1):
    play_song(song_1, beat_1, buzzer_pwm)
    time.sleep(0.3)


# and cleanup
GPIO.cleanup()
