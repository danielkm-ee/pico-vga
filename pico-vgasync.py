"""
Horizontal SYNC
Running the statemachine at 25MHz approximates the 25.175MHz pixel frequency.
We can then count cycles to determine the amount of pixels drawn, which should add up to 800px.
We simply pull the hsync pin down for 96px (~3.84us)
then set high for the remaining 704px (~28.16us)

Vertical SYNC
1 line = 800px, we divide the pixel frequency by 800 to get the line frequency (31250)
We then count cycles to determine the number of lines drawn.
"""
from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

### set up PIO programs::
@asm_pio(set_init=PIO.OUT_HIGH)
def hsync():
    # counts pixels
    wait(1, pin, 0)
    wrap_target()
    set(pins, 0)    [31]        # sets hpulse pin low, begin hpulse (96px)
    nop()           [31]
    nop()           [31]
    set(pins, 1)    [15]        # sets hpulse pin high, hsync ends, backporch starts (48px)
    set(x, 9)      [31]         # backporch ends
    label("visiblePix")         # begin visible area (640px)
    nop()           [31]
    nop()           [30]
    jmp(x_dec, "visiblePix")    # jumps to "visiblePix" if x register is nonzero
    nop()           [15]        # visible area ends, wait for frontporch (16px)
    wrap()                      # go to 'wrap_target()'

@asm_pio(set_init=PIO.OUT_HIGH)
def vsync():
    # counts lines
    wait(1, pin, 0)
    wrap_target()
    set(pins, 0)    [1]         # sets vpulse pin low, begin vsync (2 lines)
    set(pins, 1)    [31]        # sets vpulse pin high, vsync ends, backporch starts (33 lines)
    set(y, 14)                  # backporch ends
    label("visibleLines")       # begin visible area (480 lines)
    nop()           [30]
    jmp(y_dec, "visibleLines")
    nop()           [9]         # visible area ends, wait for frontporch (10 lines)
    wrap()

@asm_pio(set_init=PIO.OUT_LOW)
def redVideo():
    wait(1, pin, 0)
    wrap_target()
    nop()           [31]
    nop()           [31]
    nop()           [31]
    nop()           [15]        # blanking period ends
    set(x, 9)       [31]        # backporch ends
    label("visiblePix")         # begin visible area (640px) 
    set(pins, 1)           [20]
    set(pins, 0)           [20]
    set(pins, 0)           [20]
    jmp(x_dec, "visiblePix") 
    set(pins, 0)           [15] # begin blanking period (160px)
    wrap()

@asm_pio(set_init=PIO.OUT_LOW)
def greenVideo():
    wait(1, pin, 0)
    wrap_target()
    nop()           [31]
    nop()           [31]
    nop()           [31]
    nop()           [15]        # blanking period ends
    set(x, 9)       [31]        # backporch ends
    label("visiblePix")         # begin visible area (640px)
    set(pins, 0)           [20]
    set(pins, 1)           [20]
    set(pins, 0)           [20]
    jmp(x_dec, "visiblePix")
    set(pins, 0)           [15] # begin blanking period (160px)
    wrap()

@asm_pio(set_init=PIO.OUT_LOW)
def blueVideo():
    wait(1, pin, 0)
    wrap_target()
    nop()           [31]
    nop()           [31]
    nop()           [31]
    nop()           [15] 
    set(x, 9)       [31]        # blanking period ends
    label("visiblePix")         # begin visible area (640px)
    set(pins, 0)           [20]
    set(pins, 0)           [20]
    set(pins, 1)           [20]
    jmp(x_dec, "visiblePix")
    set(pins, 0)           [15] # begin blanking period (160px)
    wrap()

### configure and run PIO StateMachines::
activateButton = Pin(0, Pin.IN, Pin.PULL_DOWN)

## Initilize and configure sync pulse StateMachines
hsync_sm = StateMachine(0, hsync, freq=25000000, set_base=Pin(7), in_base=Pin(0))
# running hsync program on SM0, syncpulse pin is set to 7
vsync_sm = StateMachine(1, vsync, freq=31250, set_base=Pin(8), in_base=Pin(0))
# running vsync program on SM1, syncpulse pin is set to 8


## Initilize and configure video signal StateMachines
red_sm = StateMachine(2, redVideo, freq=25000000, set_base=Pin(15), in_base=Pin(0))
# running redVideo program on SM2, red is set to pin 15
green_sm = StateMachine(4, greenVideo, freq=25000000, set_base=Pin(13), in_base=Pin(0))
# running greenVideo program on SM4, green is set to pin 13
blue_sm = StateMachine(5, blueVideo, freq=25000000, set_base=Pin(14), in_base=Pin(0))
# running blueVideo program on SM5, red is set to pin 14

## Activate sync pulse StateMachines
hsync_sm.active(1)
vsync_sm.active(1)

demo = 1 # 0
# Activate color demo
red_sm.active(demo)
green_sm.active(demo)
blue_sm.active(demo)