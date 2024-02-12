"""
This program the two programmable PIO ports to perform a handshake operation
Setup:
5 GPIO pins as a register, pins 9-13
'data ready' out-pin19 in-pin16
'data taken' out-pin18 in-pin17

PIO 1::
Acts as our main PIO on the pico
defined by paral_prog().
displays it's output 5 GPIO pins, 9-13,
with a sideset pin, pin 19 ('data ready' out)
waits for high on pin17 ('data taken' in)

PIO2::
Acts as a seudo-auxillary uController
defined by wait_pin_high().
waits for high on pin 17 ('data ready' in)
sets high on sideset pin18 ('data taken' out)
waits for data ready low, and
sets data taken low
"""
from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep

##pio1:: Outputs a nibble+ (5bits) through 5 GPIO pins
# and sets the data ready high
@asm_pio(sideset_init=PIO.OUT_LOW, out_init=(rp2.PIO.OUT_HIGH,) * 5, out_shiftdir=PIO.SHIFT_RIGHT,
         autopull=True, pull_thresh=16 )
def paral_prog():
    pull()                     #pull data from the transmit SR
    out(pins, 5)    .side(1)   #output data to 5 pins and set 'data ready' line high
    wait(1, pin, 0)           #wait for the 'data taken' line to go high
    nop()           .side(0)   #set the 'data ready' line low

#this sets the other PIO to act as a surrogate TIM computer to
#generate a 'data taken' signal when a 'data ready' signal is received
@rp2.asm_pio(sideset_init=PIO.OUT_LOW)
def wait_pin_high():
    wrap_target()

    wait(1, pin, 0)            #wait for the 'data ready' line to go high
    nop()           .side(1)   #set the 'data taken' line high
    wait(0, pin, 0)            #wait for the 'data ready' line to go low
    nop()           .side(0)   #set the 'data taken' line low

    wrap()

pin17 = Pin(17, Pin.IN, Pin.PULL_UP)    #define 'data taken' pin for first PIO
pin16 = Pin(16, Pin.IN, Pin.PULL_UP)    #define 'data ready' in for second PIO

paral_sm = StateMachine(0, paral_prog, freq=2000, sideset_base=Pin(19), out_base=Pin(9), in_base=Pin(16))
#parallel data out pins 9-13, 'data ready' out pin 19, 'data taken' in pin 16
paral_sm.active(1)      #activates paral_sm program in first PIO

sm4 = StateMachine(4, wait_pin_high, sideset_base=Pin(18), in_base=Pin(17))
#'data ready' in pin 17, 'data taken' out pin 18
sm4.active(1)        #activates wait_pin_high on second PIO

#routine to generate data to output
while True:
    for i in range(32):
        paral_sm.put(i)
        print(i)
        sleep(0.2)
