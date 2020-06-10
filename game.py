import pygame
import random
import sys
import pathlib
import os
import time

TITLE = "Apple Snake"
FRAME_RATE = 10
MAX_FRAME_RATE = 16
SLOW_FRAME_RATE = 6
CUBE_WIDTH = 60
GRID_LENGTH = 13
SPEED = CUBE_WIDTH
WIDTH = CUBE_WIDTH*GRID_LENGTH
HEIGHT = CUBE_WIDTH*GRID_LENGTH
SCORE = 0
ORIGINAL_LENGTH = 2

# Define colours:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

BG_COLOUR = BLACK
HEAD_COLOUR = pygame.color.Color('green')
APPLE_COLOUR = RED

# Setting game assets:
current_folder = pathlib.Path().parent.resolve()
print(current_folder)
image_f = current_folder / 'Images'
sound_f = current_folder / 'Sounds'


# classes
class Cube:
    def __init__(self, x, y, direc):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.direc = direc

    def draw(self, pics=None, no_img=False):
        pygame.draw.rect(screen, BLACK, pygame.Rect(self.x, self.y, CUBE_WIDTH, CUBE_WIDTH))
        if not no_img:
            screen.blit(pics[self.direc], (self.x, self.y))


class Apple:
    def __init__(self, image, red=True):
        if red:
            self.x, self.y = self.get_random_cor_red_apple()
        else:
            self.x, self.y = self.get_random_cor_purple_apple()

        self.spawning = False
        self.image = image
        self.purple_apple_start_time = time.time()
        self.purple_apple_current_time = 0

    def draw(self):
        self.disappear()
        screen.blit(self.image, (self.x, self.y))

    def get_random_cor(self):

        x = CUBE_WIDTH*(random.randrange(0,GRID_LENGTH))
        y = CUBE_WIDTH*(random.randrange(0,GRID_LENGTH))

        for cube in snake.trail:
            if (cube.x, cube.y) == (x,y):
                x,y = self.get_random_cor()

        return x,y

    def get_random_cor_purple_apple(self):
        x,y = self.get_random_cor()
        if (x,y) == (red_apple.x, red_apple.y):
            x,y = self.get_random_cor_purple_apple()

        return x,y

    def get_random_cor_red_apple(self):
        x, y = self.get_random_cor()
        try:
            if (x, y) == (purple_apple.x, purple_apple.y):
                x, y = self.get_random_cor_red_apple()
        except NameError:
            pass

        return x, y

    def disappear(self):
        pygame.draw.rect(screen, BLACK, pygame.Rect(self.x, self.y, CUBE_WIDTH, CUBE_WIDTH))


class Snake:
    SNAKE_LENGTH = ORIGINAL_LENGTH

    def __init__(self, length):
        self.posx = CUBE_WIDTH*(GRID_LENGTH//2)
        self.posy = CUBE_WIDTH*(GRID_LENGTH//2)
        self.vx = 0
        self.vy = 0
        self.trail = []
        self.direc = 'up'
        for i in range(length):
            self.trail.append(Cube(self.posx, self.posy, self.direc))

    def update(self):
        global FRAME_RATE
        self.posx += self.vx
        self.posy += self.vy

        # bind arrow keys:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] or keys[pygame.K_UP]:
            # only do somthing if we are moving horizontally
            if self.vy == 0:
                if not purple_apple.spawning:
                    purple_apple.spawning = True
                    purple_apple.purple_apple_start_time = time.time()
                self.vy = SPEED if keys[pygame.K_DOWN] else -SPEED
                self.direc = 'down' if keys[pygame.K_DOWN] else 'up'
                self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            if self.vx == 0:
                if not purple_apple.spawning:
                    purple_apple.spawning = True
                    purple_apple.purple_apple_start_time = time.time()
                self.vx = SPEED if keys[pygame.K_RIGHT] else -SPEED
                self.direc = 'right' if keys[pygame.K_RIGHT] else 'left'
                self.vy = 0

        # Deal with wall collisions:
        if self.posx < 0:
            self.posx = WIDTH-CUBE_WIDTH
        elif self.posx == WIDTH:
            self.posx = 0
        elif self.posy < 0:
            self.posy = HEIGHT-CUBE_WIDTH
        elif self.posy >= HEIGHT:
            self.posy =  0

        # Adding a new cube every frame to the trail and remove the oldest cube
        new_head = Cube(self.posx, self.posy, direc=self.direc)
        self.trail.append(new_head)
        while len(self.trail) > self.SNAKE_LENGTH:
            remove = self.trail.pop(0)
            remove.draw(no_img=True)
            del remove

        # drawing the cubes
        for i,cube in enumerate(self.trail):
            # if it's the head:
            if i == len(self.trail)-1:
                cube.draw(pics=snake_heads)
            elif i == 0:
                cube.draw(pics=snake_tails)
            else:
                if (self.posx, self.posy) == (cube.x, cube.y):
                    if self.SNAKE_LENGTH != ORIGINAL_LENGTH:
                        whoosh.play()
                    self.SNAKE_LENGTH = ORIGINAL_LENGTH

                cube.draw(pics=snake_bodies)


        # collsion with apples
        if (self.posx, self.posy) == (red_apple.x, red_apple.y):
            eat.play()
            red_apple.__init__(red_apple_img)
            self.SNAKE_LENGTH += 1
            if FRAME_RATE < MAX_FRAME_RATE:
                FRAME_RATE += 1

        if (self.posx, self.posy) == (purple_apple.x, purple_apple.y):
            vomit.play()
            purple_apple.__init__(purple_apple_img, red=False)
            purple_apple.spawning = True
            FRAME_RATE = SLOW_FRAME_RATE
            if self.SNAKE_LENGTH > ORIGINAL_LENGTH:
                self.SNAKE_LENGTH -= 1
            global vomitted
            vomitted += 1


        red_apple.draw()
        purple_apple.draw()

def rotate_image(image):
    # pass in image (down version)
    down = pygame.transform.scale(image, (CUBE_WIDTH, CUBE_WIDTH))
    up = pygame.transform.rotate(down, 180)
    left = pygame.transform.rotate(down, 270)
    right = pygame.transform.rotate(down, 90)

    return up,down, left, right

def show(text, x, y, surface, colour=pygame.Color('white'), bg=None):
    text_w, text_h = my_font.size(text)

    # bg_text = " "*len(text)
    # bg = my_font.render(bg_text, False, pygame.Color(bg), pygame.Color(bg))
    # screen.blit(bg, (x, y))
    sur = my_font.render(text, False, colour, bg)
    surface.blit(sur, (x-text_w//2, y-text_h//2))


# Initialise game and create window:
os.environ['SDL_VIDEO_WINDOW_POS'] = '{},{}'.format(500,100)
pygame.init()
pygame.font.init()
pygame.mixer.init(frequency=48000, size=-16, buffer=12, channels=1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill(BG_COLOUR)
pygame.display.flip()
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

font_name = 'ubuntumono'
my_font = pygame.font.SysFont(font_name, 20, bold=True)

    # set up images:
head_img_down_original = pygame.image.load(str(image_f / 'head_crop.png')).convert_alpha()
head_up, head_down, head_left, head_right = rotate_image(head_img_down_original)

tail_img_down_original = pygame.image.load(str(image_f / 'body.png')).convert_alpha()
tail_up, tail_down, tail_left, tail_right = rotate_image(tail_img_down_original)

body_img_down_original = pygame.image.load(str(image_f / 'crop_apple2.png')).convert_alpha()
body_up, body_down, body_left, body_right = rotate_image(body_img_down_original)

# store snake body-parts images in a dict for later usage
snake_heads = {'up':head_up, 'down': head_down, 'left':head_left, 'right': head_right}
snake_tails = {'up':tail_up, 'down': tail_down, 'left':tail_left, 'right': tail_right}
snake_bodies = {'up':body_up, 'down': body_down, 'left':body_left, 'right': body_right}


        # apple image:
red_apple_img = pygame.image.load(str(image_f / 'crop_apple2.png')).convert_alpha()
red_apple_img = pygame.transform.scale(red_apple_img, (CUBE_WIDTH, CUBE_WIDTH))
purple_apple_img = pygame.image.load(str(image_f / 'purple_apple.png')).convert()
purple_apple_img = pygame.transform.scale(purple_apple_img, (CUBE_WIDTH, CUBE_WIDTH))
purple_apple_img.set_colorkey()

    # sounds:
eat = pygame.mixer.Sound(str(sound_f / 'snake_eat.wav'))
whoosh = pygame.mixer.Sound(str(sound_f / 'whoosh.wav'))
vomit = pygame.mixer.Sound(str(sound_f / 'snake_vomit.wav'))

snake = Snake(Snake.SNAKE_LENGTH)

red_apple = Apple(red_apple_img)
purple_apple = Apple(purple_apple_img, red=False)

# Main Game loop
running = True
paused = False
high_score = 0
vomitted = 0

green_apple_duration = 5
while running:
    clock.tick(FRAME_RATE)

    # the next 2 lines just paint over the scores of the previous frame:
    show("  ", x=WIDTH//2-my_font.size(" "*9)[0], y = CUBE_WIDTH,colour=pygame.Color('black'), surface=screen, bg=pygame.Color('black'))
    show("  ", x=WIDTH//2+my_font.size(" "*2)[0], y = CUBE_WIDTH,colour=pygame.Color('black'), surface=screen, bg=pygame.Color('black'))
    show("  ", x=WIDTH//2+my_font.size(" "*18)[0], y = CUBE_WIDTH,colour=pygame.Color('black'), surface=screen, bg=pygame.Color('black'))

    score = snake.SNAKE_LENGTH - ORIGINAL_LENGTH
    if score > high_score:
        high_score = score
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p:
                paused = not paused

    # Update & Draw
    if not paused:
        # reset green apple:
        if purple_apple.spawning:
            purple_apple.purple_apple_current_time = time.time() - purple_apple.purple_apple_start_time
            if purple_apple.purple_apple_current_time > green_apple_duration:
                purple_apple.disappear()
                purple_apple.__init__(purple_apple_img, red=False)
                purple_apple.spawning = True
        snake.update() ### update method both updates and draws
    else:
        if purple_apple.spawning:
            purple_apple.purple_apple_start_time = time.time() - purple_apple.purple_apple_current_time

        # draw the scores:
    show("vomited:   , eaten:   , most eaten:  ", x=WIDTH//2, y = CUBE_WIDTH,colour=pygame.Color('white'), surface=screen)
    show(" {} ".format(vomitted), x=WIDTH//2-my_font.size(" "*9)[0], y = CUBE_WIDTH,colour=pygame.Color('red'), surface=screen)
    show(" {} ".format(score), x=WIDTH//2+my_font.size(" "*2)[0], y = CUBE_WIDTH,colour=pygame.Color('red'), surface=screen)
    show(" {} ".format(high_score), x=WIDTH//2+my_font.size(" "*18)[0], y = CUBE_WIDTH,colour=pygame.Color('red'), surface=screen)

    # flip when done with drawing/updating
    pygame.display.flip()

pygame.quit()


