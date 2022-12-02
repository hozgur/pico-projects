from picolcd1inch3 import LCD_1inch3
from writer import CWriter
from rgb import RGB
# Font
import ArialRounded


lcd = LCD_1inch3()
wri = CWriter(lcd, ArialRounded, fgcolor=RGB(31,31,31), bgcolor=0, verbose=False)

for i in range(31):
    CWriter.set_textpos(lcd, i*2, 0)
    wri.setcolor(RGB(0,i,0))
    wri.printstring('Hello World!\n')
lcd.show()
