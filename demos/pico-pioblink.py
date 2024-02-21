from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep

@asm_pio(set_init=PIO.OUT_LOW)
def led_blink():
    label("mainloop")
    set(pins, 0)    [31]    # Turns off LED
    set(x, 0)       [31]    # Sets X flag for conditional jump
    jmp("delay")    [31]    # Jumps to delay routine
    label("return_0")
    set(pins, 1)    [31]
    jmp("delay")    [31]
    label("return_1")
    jmp("mainloop") [31]
    label("delay")
    set(y, 31)
    label("sub_delay_loop")
    jmp(y_dec, "sub_delay_loop") [31]   # Jumps to "sub_delay_loop" while y is not zero
    jmp(not_x, "return_0")  # If x = 0 then return to "return_0"
    jmp("return_1")           # Otherwise, return to "return_1"

sm1 = StateMachine(1, led_blink, freq=2000, set_base=Pin(3))
sm1.active(1)