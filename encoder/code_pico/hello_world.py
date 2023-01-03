from picolcd1inch3 import LCD_1inch3

lcd = LCD_1inch3()
lcd.fill(0)
lcd.text('Hello World', 0, 0, 0xffff)
lcd.show()
