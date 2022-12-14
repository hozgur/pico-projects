import machine, display, time, math, network, utime

tft.clear()
for j in range(100):
    for i in range(0,241):
        color=0xFFFFFF-tft.hsb2rgb(i+j, 1, 1)
        tft.line(i,0,i,135,color)

#text="ST7789 with micropython!"
#tft.text(0,0,text,0x000000)
#tft.set_fg(0x000000)
#tft.ellipse(120,67,120,67)
#tft.line(0,0,240,135)
