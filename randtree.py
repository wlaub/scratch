import pygame
from pygame.locals import *
import sys, time, math, random

size = (500,500)
center = (size[0]/2, size[1]/2)

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 18)

screen = pygame.display.set_mode(size)
canvas = pygame.Surface(size,SRCALPHA)

fades = [(0,128,0,1), (128,0,128,1)]
fades = [(0,128,0,1)]
f_canvas = [pygame.Surface(size,SRCALPHA) for x in fades]

c_mult = []
c_alone=[]

class Turtle():
    """
    Does a random walk and stuff
    """

    r_split = 500
    c_x = [-1,0,1]
    c_y = [-1,0,1]

    def __init__(self, x = 250, y=250):
        self.x=x
        self.y=y

    def update(self, turtles):
        global c_mult, c_alone
        local = [x for x in turtles if x.x == self.x and x.y == self.y]
        if len(local) > 1:
            turtles.remove(self)
        else:
            if len(turtles) < 500 and random.randint(0,self.r_split) == 0:
                turtles.append(Turtle(self.x, self.y))

            xstep = random.choice(self.c_x)
            ystep = random.choice(self.c_y)
            self.x = max(0,min(self.x+xstep, 500))
            self.y = max(0,min(self.y+ystep, 500))


turtles = [Turtle()]
bg = (0,0,0)
fg = (255,255,255,128)
counter = 0
debug = False

while 1:
#    time.sleep(.01)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    start = time.time()

    for t in turtles:
        t.update(turtles)

    canvas.fill((0,0,0,0))
    for f, fc in zip(f_canvas, fades):
        f.fill(fc)
        if counter == 0:
            f.fill((0,0,0,1))
    counter += 1
    if counter > 2: counter = 0


    for t in turtles:
        canvas.set_at((t.x, t.y), fg)

    for f in f_canvas:
        f.blit(canvas,(0,0))
        screen.blit(f,(0,0))

    stop = time.time()
    if debug:
        num = float(len(turtles))
        text = font.render("{} | {}".format(num, (stop-start)/num), True, fg, bg)
        screen.blit(text, (0,0))


    pygame.display.flip()





