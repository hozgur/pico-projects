from machine import Pin
from hx711_gpio import *
from utime import ticks_ms, ticks_diff, sleep, sleep_ms, sleep_us
from machine import Pin
from micropython import const

pin_OUT1 = Pin(15, Pin.IN, pull=Pin.PULL_DOWN)
pin_OUT2 = Pin(16, Pin.IN, pull=Pin.PULL_DOWN)
pin_SCK = Pin(25, Pin.OUT)

GAIN128 = const(1)
GAIN64  = const(3)
GAIN32  = const(2)

baseShift = 6
gainShift = [0,baseShift+2,baseShift,baseShift+1]

def read1(gain):
    for i in range(100):
        if pin_OUT1() == 0:
            break        
        #print("Waiting ",ticks_ms(),i, pin_OUT1())
        sleep_ms(1)
    else:
        print("Error on Read")
        return 0
    
    result = 0    
    for j in range(24):
        state = disable_irq()
        pin_SCK(True)
        sleep_us(2)
        pin_SCK(False)
        enable_irq(state)
        result = (result << 1) | pin_OUT1()
    for j in range(gain):
        state = disable_irq()
        pin_SCK(True)
        sleep_us(2)
        pin_SCK(False)
        enable_irq(state)
            
    return result >> gainShift[gain]


def read_all(gain):
    for i in range(100):
        if pin_OUT1() == 0 and pin_OUT2() == 0:
            break        
        #print("Waiting ",i, pin_OUT1(),pin_OUT2())
        sleep_ms(1)
    else:
        print("Error on Read")
        return 0
    
    result1 = 0
    result2 = 0
    for j in range(24 + gain):
        state = disable_irq()
        pin_SCK(True)
        pin_SCK(False)
        enable_irq(state)
        result1 = (result1 << 1) | pin_OUT1()
        result2 = (result2 << 1) | pin_OUT2()

    # shift back the extra bits
    result1 >>= gain
    result2 >>= gain
    return (result1, result2)

def run():    
    while True:
        sleep_ms(10)
        data = read1(GAIN32)
        print(data)
        
run()
