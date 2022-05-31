import re
import pygame, pymunk, math, sys


pygame.init()

screenY = 800
screenX = 800
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("Pymunk Visual")
space = pymunk.Space()  
space.gravity = (0, 10)
clock = pygame.time.Clock()

def create_apple(space, x, y):
    body = pymunk.Body(1, 100, body_type= pymunk.Body.DYNAMIC)  # mass, inertia, bodytype
    body.position = (x, y)
    shape = pymunk.Circle(body, 50)     # body, radius
    space.add(body, shape)      # adding the body and shape to the physics space
    return shape


# ======== Colors =========
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
black = (0, 0, 0)
orange = [255, 99, 71]
yellow = [255, 255, 0]
grey = (150, 150, 150)

def draw_apples(apples):
    for apple in apples:                # x and y tuple
        pygame.draw.circle(screen, red, apple.body.position, 50)

def static_ball(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = (410, 400)
    shape = pymunk.Circle(body, 30)
    space.add(body, shape)
    return shape

def draw_static_ball(balls):
    for ball in balls:
        pygame.draw.circle(screen, green, ball.body.position, 30)


apples, balls = [], []
balls.append(static_ball(space))
play = True
while play:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            apples.append(create_apple(space, mouse[0], mouse[1]))

    screen.fill(white)
    space.step(1/50)
    draw_apples(apples)
    draw_static_ball(balls)
    pygame.display.update()
    clock.tick(2000)
    print(clock.get_fps())


# to optimize physics in graph, every other point can be a static object 