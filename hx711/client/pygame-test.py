import pygame

#Define colors
black = (0, 0, 0)
red = (255, 0, 0)

#Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1024, 768))
pygame.display.set_caption("Serial Plotter")

data = [(x, x) for x in range(1024)]

#main loop
while True:
    #Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    #Draw the data
    screen.fill(black)
    pygame.draw.lines(screen, red, False, data, 1)
    pygame.display.flip()