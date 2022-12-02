def RGB(r,g,b):
    '''Convert 3 5-bit values to a 16-bit RGB565 value
       rgb values must be in range of 0-31. 
    '''
    g = (g * 63 //31 ) & 0x3F
    return ((g & 7) << 13) + (b << 8) + (r << 3)  + ( g >> 3)
 

if __name__ == "__main__":
    print("{0:b}".format(RGB(31,31,31)))
    print("{0:b}".format(RGB(31,00,00)))
    print("{0:b}".format(RGB(00,31,00)))
    print("{0:b}".format(RGB(00,00,31)))
    