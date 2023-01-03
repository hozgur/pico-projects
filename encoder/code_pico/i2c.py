import machine
from micropython import const
import time
from picolcd1inch3 import LCD_1inch3
from writer import CWriter
from rgb import RGB
import ArialRounded27

REG_STATUS = const(0x0b)

MH = const(0x08)
ML = const(0x16)
MD = const (0x32)


def showStatus():
    status = i2c.readfrom_mem(AS5600_id,REG_STATUS,1)
    



lcd = LCD_1inch3()
wri = CWriter(lcd, ArialRounded27, fgcolor=RGB(31,31,31), bgcolor=0, verbose=False)
i2c = machine.I2C(0,scl=machine.Pin(17),sda=machine.Pin(16),freq=400000)
AS5600_id = const(0x36)  #Device ID
devices = i2c.scan()

if AS5600_id in devices:
    print('Found AS5600 (id =',hex(AS5600_id),')')
else:
    print('AS5600 Not Found! (id =',hex(AS5600_id),')')

time.sleep(0.3)
print("test")
#i2c.writeto(AS5600_id,bytearray([0x0b]))
data = i2c.readfrom_mem(AS5600_id,11,1)

CWriter.set_textpos(lcd, 0, 0)
wri.setcolor(RGB(0,31,0))
wri.printstring('Hello World!\n')
lcd.show()
print(bin(data[0]))