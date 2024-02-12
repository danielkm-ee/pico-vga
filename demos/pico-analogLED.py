from machine import ADC, Pin, PWM
import time

adc = ADC(Pin(26))
pwm = PWM(Pin(15))

pwm.freq(1000)

while True:
    duty = adc.read_u16()
    pwm.duty_u16(duty)
