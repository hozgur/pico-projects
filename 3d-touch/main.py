from picolcd1inch3 import LCD_1inch3
from writer import CWriter
from rgb import RGB
# Font
import ArialRounded27
from machine import Pin, PWM
import time

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9
#keys
keyA = Pin(15,Pin.IN,Pin.PULL_UP)
keyB = Pin(17,Pin.IN,Pin.PULL_UP)
keyX = Pin(19 ,Pin.IN,Pin.PULL_UP)
keyY= Pin(21 ,Pin.IN,Pin.PULL_UP)

up = Pin(2,Pin.IN,Pin.PULL_UP)
dowm = Pin(18,Pin.IN,Pin.PULL_UP)
left = Pin(16,Pin.IN,Pin.PULL_UP)
right = Pin(20,Pin.IN,Pin.PULL_UP)
ctrl = Pin(3,Pin.IN,Pin.PULL_UP)

MID = 1500000
MIN = 1000000
MAX = 2000000

# Initialize Servo
pwm = PWM(Pin(22))
pwm.freq(50)

# Initialize LCD
lcd = LCD_1inch3()
wri = CWriter(lcd, ArialRounded27, fgcolor=RGB(31,31,31), bgcolor=0, verbose=False)

CWriter.set_textpos(lcd, 0, 0)
wri.printstring('Position:')
lcd.show()

duty = 0
duty_step = 100000
while (True):
    if keyA.value() == 0:
        duty = 18 * duty_step
        
    if keyB.value() == 0:
        duty -= duty_step
        if duty < 0:
            duty = 0

    if keyX.value() == 0:
        duty = 11 * duty_step

    pwm.duty_ns(duty)

    CWriter.set_textpos(lcd, 0, 120)
    wri.printstring(str(duty/100000))
    lcd.show()
    if keyY.value() == 0:
        break