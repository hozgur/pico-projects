import pygame
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
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Serial Plotter")


# Define colors
black = (0, 0, 0)
red = (255, 0, 0)

data = [0 for _ in range(640)]

x = 0
# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    # Read data from the serial port
    line = ser.readline()
    data_as_list = line.split(b',')
    #i = int(data_as_list[0])
    data[x] = int(data_as_list[1])/1000 + 100

    # Draw the data
    screen.fill(black)
    for i in range(640):
        pygame.draw.line(screen, red, (i, 480), (i, 480 - data[i]), 1)

    pygame.display.flip()
    x = (x + 1) % 640
