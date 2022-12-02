import machine
from micropython import const
import time
from picolcd1inch3 import LCD_1inch3
from writer import CWriter
from rgb import RGB
import ArialRounded27

REG_STATUS = const(0x0b)

MH = const(8)
ML = const(16)
MD = const (32)

ROW_WIDTH = 64
ROW_HEIGHT = const(32)

lcd = LCD_1inch3()
wri = CWriter(lcd, ArialRounded27, fgcolor=RGB(31,31,31), bgcolor=0, verbose=False)
i2c = machine.I2C(0,scl=machine.Pin(17),sda=machine.Pin(16),freq=400000)
AS5600_id = const(0x36)  #Device ID
devices = i2c.scan()


def showStatus():
    status = i2c.readfrom_mem(AS5600_id,REG_STATUS,1)
    lcd.rect(0,0,ROW_WIDTH,ROW_HEIGHT,RGB(31,31,31))
    lcd.rect(ROW_WIDTH,0,ROW_WIDTH,ROW_HEIGHT,RGB(31,31,31))
    print(bin(status[0]))
    if status[0] & MH:
        lcd.fill_rect(1,1,ROW_WIDTH - 2, ROW_HEIGHT -2,RGB(31,0,0))        
    if status[0] & ML:
        lcd.fill_rect(1,1,ROW_WIDTH - 2, ROW_HEIGHT -2,RGB(31,31,0))
    if status[0] & (ML | MH) == 0:
        lcd.fill_rect(1,1,ROW_WIDTH - 2, ROW_HEIGHT -2,RGB(0,31,0))
    if status[0] & MD:
        lcd.fill_rect(ROW_WIDTH + 1,1,ROW_WIDTH - 2, ROW_HEIGHT -2,RGB(0,31,0))
    else:
        lcd.fill_rect(ROW_WIDTH + 1,1,ROW_WIDTH - 2, ROW_HEIGHT -2,RGB(31,0,0))
        print("MD")
    lcd.show()
       
def showAngle():
    angle = i2c.readfrom_mem(AS5600_id,0x0c,2)
    angle = ((angle[0] & 7) << 8) | angle[1]
    #degree = angle * 360 / 4096
    lcd.rect(0,ROW_HEIGHT,ROW_WIDTH*2,ROW_HEIGHT,RGB(31,31,31))
    CWriter.set_textpos(lcd, ROW_HEIGHT, 1)
    wri.printstring('{:0.2f}'.format(angle))
    lcd.show()

if AS5600_id in devices:
    print('Found AS5600 (id =',hex(AS5600_id),')')
else:
    print('AS5600 Not Found! (id =',hex(AS5600_id),')')

time.sleep(0.3)
print("test")
#i2c.writeto(AS5600_id,bytearray([0x0b]))
data = i2c.readfrom_mem(AS5600_id,11,1)


while True:
    showStatus()
    showAngle()
    time.sleep(0.3)
