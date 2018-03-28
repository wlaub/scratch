import pygame
from pygame.locals import *
import sys, time, math, random

size = (500,500)
center = (size[0]/2, size[1]/2)

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 18)
font = pygame.font.SysFont('ubuntumono', 16)

screen = pygame.display.set_mode(size)
canvas = pygame.Surface(size,SRCALPHA)

fades = [(0,128,0,1), (128,0,128,1)]
fades = [(0,0,128,1)]
f_canvas = [pygame.Surface(size,SRCALPHA) for x in fades]

mcount=0
scount=0

class Turtle():
    """
    Does a random walk and stuff
    """

    r_split = 50
    c_x = [-1,0,1]
    c_y = [-1,0,1]

    def __init__(self, x = 250, y=250):
        self.g=5
        self.x=x
        self.y=y

    def update(self, turtles):
        if self.g > 0: self.g-=1
        global mcount, scount
        local = [x for x in turtles if x.g == 0 and abs(x.x - self.x) < 2 and abs(x.y - self.y)<2]
        if len(local) > 1:
            turtles.remove(self)
            mcount+=1
        else:
            if len(turtles) < 420 and random.randint(0,self.r_split) == 0:
                scount+=1
                turtles.append(Turtle(self.x, self.y))

            xstep = random.choice(self.c_x)
            ystep = random.choice(self.c_y)
            self.x = max(0,min(self.x+xstep, 500))
            self.y = max(0,min(self.y+ystep, 500))


turtles = [Turtle()]
bg = (0,0,0)
fg = (255,255,255,128)
counter = 0
n=0
debug = True

while 1:
#    time.sleep(.01)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    start = time.time()

    Turtle.c_x = [max(-1,min(x+2*random.randint(-1,1),1)) for x in Turtle.c_x]
    Turtle.c_y = [max(-1,min(x+2*random.randint(-1,1),1)) for x in Turtle.c_y]

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
        pygame.draw.rect(canvas, fg, (int(t.x-1),int(t.y-1),3,3))
#        canvas.set_at((t.x, t.y), fg)

    for f in f_canvas:
        f.blit(canvas,(0,0))
        screen.blit(f,(0,0))

    stop = time.time()
    if debug:
        num = float(len(turtles))
        text = font.render("{:03} | {} | {} | {} | {:04.1f}".format(int(num), n, mcount, scount, 1E6*(stop-start)/num), True, fg, bg)
        screen.blit(text, (0,0))


    pygame.display.flip()
    n+=1





