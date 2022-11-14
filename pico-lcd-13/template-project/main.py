from picolcd1inch3 import LCD_1inch3
from writer import CWriter
from rgb import RGB
# Font
import ArialRounded


lcd = LCD_1inch3()
wri = CWriter(lcd, ArialRounded, fgcolor=RGB(31,31,31), bgcolor=0, verbose=False)


CWriter.set_textpos(lcd, 0, 0)
wri.setcolor(RGB(31,20,0),None)
wri.printstring('Hello World!')
lcd.show()
