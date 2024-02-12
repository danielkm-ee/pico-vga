from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(15))
pwm.freq(1000)

button = Pin(16, Pin.IN, Pin.PULL_DOWN)

while True:
    if button.value():
        for duty in range(65025):
            pwm.duty_u16(duty)
            sleep(0.0001)
        for duty in range(65025, 0, -1):
            pwm.duty_u16(duty)
            sleep(0.0001)


