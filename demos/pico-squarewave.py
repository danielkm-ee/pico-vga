from machine import Pin
from rp2 import StateMachine, PIO, asm_pio
from time import sleep

@asm_pio(out_init=(rp2.PIO.OUT_HIGH,), autopull=True)
def square_wave():
    set(pins, 1)