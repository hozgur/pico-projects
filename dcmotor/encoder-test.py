from machine import Pin, PWM
import time
import rp2
led = Pin(25,Pin.OUT)
led.on()



@rp2.asm_pio()
def pulse_counter():
    label("loop")
    # We wait for a rising edge
    wait(0, pin, 0)
    wait(1, pin, 0)
    jmp(x_dec, "loop")  # If x is zero, then we'll wrap back to beginning
    

class PulseCounter:
    # pin should be a machine.Pin instance
    def __init__(self, sm_id, pin):
        self.sm = rp2.StateMachine(0, pulse_counter,freq=1000000, in_base=pin)
        # Initialize x to zero
        self.sm.put(0)
        self.sm.exec("pull()")
        self.sm.exec("mov(x, osr)")
        # Start the StateMachine's running.
        self.sm.active(1)

    def get_pulse_count(self):
        self.sm.exec("mov(isr, x)")
        self.sm.exec("push()")
        # Since the PIO can only decrement, convert it back into +ve
        return self.sm.get() # & 0x7fffffff
    

encoder = PulseCounter(0,Pin(17,Pin.IN,Pin.PULL_UP))

print(encoder.get_pulse_count())