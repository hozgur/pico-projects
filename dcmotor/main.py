
from machine import Pin, PWM, ADC
import time
import rp2
from micropython import const

pwm.freq(1000)
pwm_duty = 20000
pwm.duty_u16(pwm_duty)

target_rpm = 1200

start_time = time.ticks_ms() # get millisecond counter
start_encoder = encoder.get_pulse_count()

duty_offset = 22000
cur_offset = duty_offset

eprev = 0 # for PID derivative calculation
eintegral = 0 # for PID integral calculation

while True:    
    deltaT = time.ticks_diff(time.ticks_ms(), start_time) # compute time difference
    deltaE = start_encoder - encoder.get_pulse_count()
    start_time = time.ticks_ms() # get millisecond counter
    start_encoder = encoder.get_pulse_count()
    
    pps = 1000 * deltaE / deltaT # pulse per second
    rpm = 60 * pps / ppr
    
    e = (target_rpm - rpm)
    
    
    # PID
    kp = 5
    kd = 0
    ki = 0.0001
    dedt = (e - eprev)/deltaT/1e-3
    eintegral = eintegral + e * deltaT/1e-3
    
    #control signal
    u = kp * e + kd * dedt + ki * eintegral
    
    eprev = e
    iu = int(u)
    
    pwm_duty = iu + cur_offset
    if pwm_duty > 65535:
        pwm_duty = 65535
    if pwm_duty < 0:
        pwm_duty = 0
    pwm.duty_u16(pwm_duty)
    adc_val = (pot.read_u16()-1700) >> 8
    if adc_val < 0:
        adc_val = 0
    target_rpm = 8 * adc_val
    if adc_val == 0:
        cur_offset = 0
    else:
        cur_offset = duty_offset
    print(target_rpm,pwm_duty)
    
    