
import time
from picolcd1inch3 import LCD_1inch3
from rgb import RGB
lcd = LCD_1inch3(0.5)
lcd.fill(0)
for z in range(30):
    for y in range(30):
        for x in range(30):
            lcd.fill_rect(x*8, y*8, 8, 8, RGB(x,y,z))

    lcd.show()
    time.sleep(0.1)

