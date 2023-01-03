import machine
import math
from micropython import const
import time
from picolcd1inch3 import LCD_1inch3
from writer import CWriter
from rgb import RGB
import ArialRounded27
from R_Encoder import R_Encoder

last_Enc_Counter = 0
Enc_Counter = 0
error = 0

Rotary_Enc = R_Encoder(15,14,7)
Rotary_Enc.Reset_Counter()

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
old_angle = 0
inc_angle=0

def RST_Inc_A(pin):
    global inc_angle
    angle = i2c.readfrom_mem(AS5600_id,0x0c,2)
    angle = ((angle[0] & 15) << 8) | angle[1]
    inc_angle = angle
    print(inc_angle)

#button_Show = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
button_Inc_A = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)
button_Inc_A.irq(trigger=machine.Pin.IRQ_FALLING, handler=RST_Inc_A)
button_Rst_Counter = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_UP)
#button_Enc_Val_Rst.irq(trigger=machine.Pin.IRQ_RISING, handler=rst_Counter)

#def rst_Counter(source):
 #   Rotary_Enc.Reset_Counter()
  #  print("resete girdi")


# SHOW STATUS POSSITION
lcd.rect(0,0,ROW_WIDTH,ROW_HEIGHT,RGB(31,31,31))
lcd.rect(ROW_WIDTH,0,ROW_WIDTH,ROW_HEIGHT,RGB(31,31,31))

# SHOW MAGNETIC ANGLE POSSITION
lcd.rect(0,ROW_HEIGHT,ROW_WIDTH*2,ROW_HEIGHT,RGB(31,31,31))

# SHOW ENC POSSITION
lcd.rect(0,ROW_HEIGHT*2,ROW_WIDTH*2,ROW_HEIGHT,RGB(31,31,31))

# SHOW ROTARY ANGLE POSSITION 
lcd.rect(0,ROW_HEIGHT*3,ROW_WIDTH*2,ROW_HEIGHT,RGB(31,31,31))


    
def showStatus():
    status = i2c.readfrom_mem(AS5600_id,REG_STATUS,1)
#    lcd.rect(0,0,ROW_WIDTH,ROW_HEIGHT,RGB(31,31,31))
#    lcd.rect(ROW_WIDTH,0,ROW_WIDTH,ROW_HEIGHT,RGB(31,31,31))
    
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
    lcd.fill_rect(1,1,ROW_WIDTH - 2, ROW_HEIGHT -2,RGB(0,31,0)) 
    
    #lcd.show()
       
def showAngle():
    global inc_angle
    angle = i2c.readfrom_mem(AS5600_id,0x0c,2)
    angle = ((angle[0] & 15) << 8) | angle[1]
    #print (angle, "magnetic")
    degree = angle * 360 / 4096
    inc_A = angle - inc_angle
    if (inc_A < 0):
        inc_A = 4096
        
        
        
        + inc_A
    
    inc_degree = inc_A * 360 / 4096
    #lcd.rect(0,ROW_HEIGHT,ROW_WIDTH*2,ROW_HEIGHT,RGB(31,31,31))
    lcd.fill_rect(1, ROW_HEIGHT+2, ROW_WIDTH*2-2, ROW_HEIGHT-5, RGB(0,0,0))
    CWriter.set_textpos(lcd, ROW_HEIGHT+3, 1)
    wri.printstring('{:0.1f}'.format(degree))
    
    lcd.fill_rect(1, ROW_HEIGHT*2+2, ROW_WIDTH*2-2, ROW_HEIGHT-5, RGB(0,0,0))
    CWriter.set_textpos(lcd, ROW_HEIGHT*2+3, 1)   
    wri.printstring('{:0.1f}'.format(inc_degree))
    #lcd.show()

if AS5600_id in devices:
    print('Found AS5600 (id =',hex(AS5600_id),')')
else:
    print('AS5600 Not Found! (id =',hex(AS5600_id),')')

#time.sleep(0.3)
#print("test")
#i2c.writeto(AS5600_id,bytearray([0x0b]))
#data = i2c.readfrom_mem(AS5600_id,11,1)

def showEncVal():
    lcd.fill_rect(1, ROW_HEIGHT*3+2, ROW_WIDTH*2-2, ROW_HEIGHT-5, RGB(0,0,0))    
    CWriter.set_textpos(lcd, ROW_HEIGHT*3+3, 1)   
    wri.printstring('{:0.1f}'.format(Rotary_Enc.Enc_Counter))
    """CWriter.set_textpos(lcd, ROW_HEIGHT*3+3, 1)
    enc_degree = Rotary_Enc.Enc_Counter * 360 / 5000
    wri.printstring('{:0.1f}'.format(enc_degree))"""
#    lcd.show()
      
while True:
    time.sleep(0.1)
    #if button_Show.value() == 0:
    showEncVal()
    #print("Button Pressed")
    showStatus()
    showAngle()
    lcd.show()
    if button_Rst_Counter.value() == 0:
        Rotary_Enc.Reset_Counter()
    #showStatus()
    #showAngle()
    
    
    #Qtr_Cntr = round(Rotary_Enc.Enc_Counter / 4)
    #if Qtr_Cntr != Last_Qtr_Cntr:
    #    print(Qtr_Cntr)
    #    last_Enc_Counter = Rotary_Enc.Enc_Counter
    #    Last_Qtr_Cntr = Qtr_Cntr
    