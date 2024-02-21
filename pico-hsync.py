"""
Horizontal SYNC
Author: Daniel Monahan
Running the statemachine at 25MHz approximates the 25.175MHz pixel frequency.

We can then count cycles to determine the amountof pixels drawn, which should add up to 800p.
We simply pull the hsync pin down for 96p (~3.84us)
then wait for the remaining 704p (~28.16us)
"""
from machine import Pin
from rp2 import PIO, StateMachine, asm_pio

@asm_pio(set_init=PIO.OUT_HIGH)
def hsync():
    label("main")
    set(pins, 0)    [31]    # sets hpulse pin low, begin hsync
    nop()           [31]
    nop()           [31]
    set(pins, 1)    [15]    # sets hpulse pin high, hsync ends, backporch starts
    set(x, 9)      [31]    # backporch ends
    label("visible")        #  begin visible area
    nop()           [31]
    nop()           [30]
    jmp(x_dec, "visible")
    nop()           [15]    # visible area ends, wait for frontporch
    jmp("main")             # go to "main"

hsync_sm = StateMachine(0, hsync, freq=25000, set_base=Pin(3)) # FIXME: running the state machine at 10**-3 of desired frequency
# running hsync program on SM0, syncpulse pin is set to 3
hsync_sm.active(1)

