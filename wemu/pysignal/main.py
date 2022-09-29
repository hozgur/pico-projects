from machine import Pin, Timer
import time
led = Pin(17, Pin.OUT)
out = Pin(16, Pin.OUT)

timer = Timer()

def blink(timer):
    led.toggle()
    out.on()
    time.sleep_us(10)
    out.off()
    time.sleep_us(30)
    out.on()
    time.sleep_us(5)
    out.off()
    time.sleep_us(100)
    out.on()
    time.sleep_us(7)
    out.off()
    

timer.init(freq=50, mode=Timer.PERIODIC, callback=blink)