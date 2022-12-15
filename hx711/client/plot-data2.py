import pygame

import numpy as np
useMockData = False

WIDTH = 1024
HEIGHT = 768

timescale = 4

if useMockData:
    import SerialMock
    ser = SerialMock()
else:
    import serial
    # initialize serial port
    ser = serial.Serial()
    ser.port = 'COM10' #Arduino serial port
    ser.baudrate = 115200
    ser.timeout = 10 #specify timeout when using readline()
    ser.open()
    if ser.is_open==True:
        print("\nAll right, serial port now open. Configuration:\n")
        print(ser, "\n") #print serial parameters

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Serial Plotter")

# Define colors
black = (0, 0, 0)
red = (255, 0, 0)

data = np.zeros((WIDTH//timescale,2))
data[:,0] = np.arange(WIDTH//timescale) * timescale


def readData():
    # Read data from the serial port
    line = ser.readline()
    # Decode the data
    data = int(line) /500 + HEIGHT//2
    if(data > HEIGHT):        
        print("overflow+ ", bin(int(line)))
        data = HEIGHT        
    if(data < -100):
        print("overflow- ", bin(int(line)))
        data = 0

    return data

cache = []
# Main loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    data[:,1] = np.roll(data[:,1],-1)
    for i in range(timescale):
        cache.append(readData())
    data[-1,1] = sum(cache)/timescale
    cache = []    
    # Draw the data
    screen.fill(black)
    #draw grid
    for i in range(0, WIDTH, 100):
        pygame.draw.line(screen, (50,50,50), (i, 0), (i, HEIGHT))
    for i in range(0, HEIGHT, 100):
        pygame.draw.line(screen, (50,50,50), (0, i), (WIDTH, i))
    #draw data
    pygame.draw.lines(screen, red, False, data, 1)
    pygame.display.flip()
    
