
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
pwm = PWM(Pin(12))
# Set the PWM frequency.
pwm.freq(1000)
pwm_duty = 20000
pwm.duty_u16(pwm_duty)

target_pps = 10

start_time = time.ticks_ms() # get millisecond counter
start_encoder = encoder.get_pulse_count()
eprev = 0
eintegral = 0

while True:
    #time.sleep(0.1)    
    deltaT = time.ticks_diff(time.ticks_ms(), start_time) # compute time difference
    deltaE = start_encoder - encoder.get_pulse_count()
    start_time = time.ticks_ms() # get millisecond counter
    start_encoder = encoder.get_pulse_count()
    
    pps = deltaE / deltaT
    e = (target_pps - pps)
    
    # PID
    kp = 500
    kd = 5
    ki = 0.01
    dedt = (e - eprev)/deltaT/1e-3
    eintegral = eintegral + e * deltaT/1e-3
    
    #control signal
    u = kp * e + kd * dedt + ki * eintegral
    
    eprev = e
    pwm_duty = int(u) + 22000
    if pwm_duty > 65535:
        pwm_duty = 65535
    if pwm_duty < 0:
        pwm_duty = 0
    pwm.duty_u16(pwm_duty)
        
    #print(u, pps, start_encoder)
    #print(start_encoder)