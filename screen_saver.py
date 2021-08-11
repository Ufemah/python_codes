import pygame

pygame.init()

size = width, height = 1280, 720
speed = [1, 1]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball = pygame.image.load("src/screen_saver/intro_ball.gif")
ballrect = ball.get_rect()

screen.fill(black)

screen.blit(ball, ballrect)
pygame.display.update()

while True:

    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    ballrect = ballrect.move(speed)
    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    screen.blit(ball, ballrect)
    pygame.display.update()
    pygame.time.delay(2)
