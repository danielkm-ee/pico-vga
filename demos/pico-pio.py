from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep

@asm_pio(sideset_init=PIO.OUT_LOW,out_init=(rp2.PIO.OUT_HIGH,) * 5, out_shiftdir=PIO.SHIFT_RIGHT,
         autopull=True, pull_thresh=16 )
def paral_prog():
    pull()          #.side(0)
    out(pins, 5)    .side(1)
    nop()           .side(0) [1]

paral_sm = StateMachine(0, paral_prog, freq=2000, sideset_base=Pin(14), out_base=Pin(9))
#parallel data out pins 9-13, Data ready out pin 14
paral_sm.active(1)

arr = [0,2,4,8,16,32]
while True:
    for i in range(32):
        paral_sm.put(i)
        print(i)
        sleep(0.25)
    for i in arr:
        paral_sm.put(i)
        print(i)
        sleep(0.25)
    

