import time
from lsm6dsox import LSM6DSOX

from machine import Pin, I2C
lsm = LSM6DSOX(I2C(0, scl=Pin(13), sda=Pin(12)))

while (True):
    v = lsm.read_accel()
    # get distance from 0,0,0
    d = (v[0]**2 + v[1]**2 + (v[2]-1)**2)**0.5
    #print("x: %f, y: %f, z: %f, d: %.3f" % (v[0], v[1], v[2], d*100))
    print(int(d*4096))
    time.sleep_ms(10)