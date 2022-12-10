from machine import ADC, Pin
from time import sleep_ms
adc1 = ADC(Pin(26))     # create ADC object on ADC pin
adc2 = ADC(Pin(27))     # create ADC object on ADC pin

bufSize = 1500
buf =[0] * bufSize
i = 0
total = 0
while True:
    total -= buf[i]
    buf[i] = adc1.read_u16() - adc2.read_u16()
    total += buf[i]
    i=i+1
    val = total / bufSize
    if i == bufSize:
        i = 0
        print('Deger :%.2f' % val)
    #sleep_ms(1)