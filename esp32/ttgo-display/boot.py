# This file is executed on every boot (including wake-boot from deepsleep)
import sys
sys.path[1] = '/flash/lib'

import machine, display, time, math, network, utime

tft = display.TFT()
tft.init(tft.ST7789,bgr=False,rot=tft.LANDSCAPE, miso=17,backl_pin=4,backl_on=1, mosi=19, clk=18, cs=5, dc=16)
tft.setwin(40,52,320,240)
tft.set_bg(0xFFFFFF)