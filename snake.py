import pygame
import random
import sys
import time
import pathlib

WIDTH = 800
HEIGHT = 700
TITLE = "snake"
FRAME_RATE = 1

INITIAL_SEGMENTS = 3

# Define colours:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BG_COLOUR = BLACK

# Setting up game assets (images, sounds)
game_folder = pathlib.Path(__file__).parent.resolve()
images_folder = game_folder / 'Images'
sounds_folder = game_folder / 'Sounds'


# functions:
def keep_cube_in_frame(cube):
    if cube.rect.left > WIDTH:
        cube.rect.right = 0
    elif cube.rect.right < 0:
        cube.rect.left = WIDTH
    elif cube.rect.top > HEIGHT:
        cube.rect.bottom = 0
    elif cube.rect.bottom < 0:
        cube.rect.top = HEIGHT


# classes
class Segment(pygame.sprite.Sprite):
    SIDE = 40

    def __init__(self):
        # super takes in a class as first arg, finds its superclass/parent, then apply __init__() on the 2nd arg
        super(Segment, self).__init__()
        self.image = pygame.Surface((self.SIDE, self.SIDE))
        self.image.fill(BLUE)
        # creating rects
        self.rect = self.image.get_rect()
        self.previous_pos = None

    def update(self):
        global snake
        if snake.head.speedy == 0 and snake.head.speedx == 0:
            self.rect.x = - 40
            return
        else:
            self.previous_pos = self.rect.x, self.rect.y

        for i, seg in enumerate(snake.body):
            if seg == self:
                if i == 0:
                    self.rect.x = snake.head.previous_pos[0]
                    self.rect.y = snake.head.previous_pos[1]
                else:
                    self.rect.x = snake.body[i - 1].previous_pos[0]
                    self.rect.y = snake.body[i - 1].previous_pos[1]


    def add_to_snake(self, snake):
        last_seg_in_snake = list(snake)[-1]
        self.rect.top = last_seg_in_snake.rect.bottom
        self.rect.centerx = last_seg_in_snake.rect.centerx


class Head(Segment):
    SPEED = 40

    def __init__(self):
        Segment.__init__(self)
        self.image.fill(pygame.Color('black'))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speedx = 0
        self.speedy = 0
        self.previous_pos = self.rect.bottomleft

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_DOWN]:
            self.speedy = self.SPEED
            self.speedx = 0
        if pressed_keys[pygame.K_UP]:
            self.speedy = -self.SPEED
            self.speedx = 0
        if pressed_keys[pygame.K_RIGHT]:
            self.speedx = self.SPEED
            self.speedy = 0
        if pressed_keys[pygame.K_LEFT]:
            self.speedx = -self.SPEED
            self.speedy = 0

        if not (self.speedx == 0 and self.speedy == 0):
            self.previous_pos = (self.rect.x, self.rect.y)
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        keep_cube_in_frame(self)



class Snake(pygame.sprite.Group):
    def __init__(self, segments):
        pygame.sprite.Group.__init__(self)
        self.head = Head()
        self.body = []
        # generate snake parts:

        for i in range(segments):
            if i == 0:
                self.add(self.head)
            else:
                self.add_segment()

    def add_segment(self):
        seg = Segment()
        # postion seg

        # add to sprite group:
        self.body.append(seg)
        self.add(seg)


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
snake = Snake(INITIAL_SEGMENTS)
### add cubes into snake(which is a list):

print(len(snake))

all_sprites.add(snake)

# Main Game loop
running = True
while running:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # Draw & render
    screen.fill(pygame.Color('yellow'))
    all_sprites.draw(screen)

    # flip when done with drawing/updating
    # time.sleep(0.01)
    pygame.display.flip()
    pygame.time.delay(10)
    clock.tick(FRAME_RATE)

pygame.quit()
