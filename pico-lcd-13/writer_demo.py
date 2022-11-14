# writer_demo.py Demo pogram for rendering arbitrary fonts to an SSD1306 OLED display.
# Illustrates a minimal example. Requires ssd1306_setup.py which contains
# wiring details.

# The MIT License (MIT)
#
# Copyright (c) 2018 Peter Hinch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


# https://learn.adafruit.com/monochrome-oled-breakouts/wiring-128x32-spi-oled-display
# https://www.proto-pic.co.uk/monochrome-128x32-oled-graphic-display.html

# V0.3 13th Aug 2018

from picolcd1inch3 import LCD_1inch3
from writer import CWriter
from rgb import RGB
# Font
import ArialRounded27

def test():
    lcd = LCD_1inch3()
    rhs = lcd.width -1
    lcd.line(rhs - 20, 0, rhs, 20, 1)
    square_side = 10
    lcd.fill_rect(rhs - square_side, 0, square_side, square_side, 1)

    wri = CWriter(lcd, ArialRounded27, fgcolor=RGB(31,31,31), bgcolor=0, verbose=False)
    CWriter.set_textpos(lcd, 0, 0)  # verbose = False to suppress console output
    wri.printstring('Hello World!\n')
    wri.printstring('IP:192.168.2.212\n')
    lcd.show()

if __name__ == "__main__":
    test()