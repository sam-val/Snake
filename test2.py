import pygame
import random
import sys
import pathlib

WIDTH = 500
HEIGHT = 500
TITLE = "MY GAME"
FRAME_RATE = 5

# Define colours:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BG_COLOUR = BLACK


# Setting game assets:

# classes
class Foo(pygame.sprite.Sprite):
    def __init__(self):
        # super takes in a class as first arg, finds its superclass/parent, then apply __init__() on the 2nd arg
        super(Foo, self).__init__()
        # creating rects

    def update(self):
        pass

class Square:
    SPEED = 30
    WIDTH = 30
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.show(pygame.Color('white'))
        self.speedx = 0
        self.speedy = 0

    def show(self, colour):
        pygame.draw.rect(screen, colour, pygame.Rect((self.x,self.y, self.WIDTH,self.WIDTH) ))

    def update(self):
        # self.speedx = 0
        # self.speedy = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx = -self.SPEED
            self.speedy = 0
        if keys[pygame.K_RIGHT]:
            self.speedx = self.SPEED
            self.speedy = 0
        if keys[pygame.K_UP]:
            self.speedy = -self.SPEED
            self.speedx = 0
        if keys[pygame.K_DOWN]:
            self.speedy = self.SPEED
            self.speedx = 0

        if self.y < -self.WIDTH:
            self.y = HEIGHT
        if self.y > HEIGHT:
            self.y = -self.WIDTH
        if self.x < -self.WIDTH:
            self.x = WIDTH
        if self.x > WIDTH+self.WIDTH:
            self.x = 0


    def draw(self):

        self.show(pygame.Color('black'))
        self.x += self.speedx
        self.y += self.speedy

        self.show(pygame.Color('white'))


# Initialise game and create window:
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BG_COLOUR)
pygame.display.flip()
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Sprites
all_sprites = pygame.sprite.Group()
square = Square(WIDTH//2, HEIGHT//2)
# Main Game loop
running = True
while running:
    clock.tick(FRAME_RATE)
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False

    # Update
    square.update()
    # Draw & render
    square.draw()

    # flip when done with drawing/updating
    pygame.display.flip()

pygame.quit()


