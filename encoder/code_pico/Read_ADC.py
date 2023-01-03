import machine
import time

analog_value = machine.ADC(26)

while True:
    reading = analog_value.read_u16()
    print("ADC: ", reading)
    time.sleep(0.5)
    
