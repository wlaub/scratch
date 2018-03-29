import random, math, time
from matplotlib import pyplot as plt

import pygame
from pygame.locals import *

import colorsys

def colormap(val):
    """
    val from 0 to 1 maps to a color
    """
    return map(lambda x: int(x*255), colorsys.hsv_to_rgb(val,1,1))


class Unit():


    def __init__(self, hrank, srank=100, color = (0,0,0)):
        self.hrank = hrank
        self.srank = srank
        self.w = 0
        self.l = 0
        self.color = color

    def improve(self, other):
        return
        if other.hrank > self.hrank:
            self.hrank += math.exp(-other.hrank + self.hrank)

    def win(self, upval):
        self.w += 1.
#        self.srank += upval

    def lose(self, upval):
        self.l += 1.
#        self.srank -= upval

class Group():
    noise = 10

    def __init__(self, size):
        self.units = [Unit(x, random.randint(0,size), colormap(x/float(size))) for x in range(size)]
        self.perfect = sorted(self.units, key = lambda x: x.hrank)


    def compare(self, left, right):
        return left.hrank-right.hrank

    def fuzz(self, val):
        return val + (.5-random.random())*2*self.noise

    def gate(self, val, rate = 1):
#        return 2*(1/(1+math.exp(-rate*val))-.5)
        return 1 if val > 0 else -1

    def tick(self, idx, rate = 1):
        left = self.units[idx]
        dist = 10000000
        for unit in self.units:
            tdist = abs(left.srank-unit.srank)
            if tdist < dist and unit != left:
                right = unit
                dist = tdist
        upval = self.compare(left, right)
        upval = self.fuzz(upval)
        upval = self.gate(upval)
        upval *= rate

        if upval > 0:
            left.win(upval)
            right.lose(upval)
        else:
            right.win(upval)
            left.lose(upval)

        left.srank += upval
        right.srank -= upval
        
        left.improve(right)
        right.improve(left)
       

    def tick_all(self, rate = 1):
        for i in range(len(self.units)):
            self.tick(i, rate)
        return self.error()

    def get_ranking(self):
        return sorted(self.units, key=lambda x: x.srank)

    def get_winrates(self):
        return map(lambda x: x.w/(x.w+x.l), self.get_ranking())

    def error(self):
        rankings = self.get_ranking()
        avg = 0
        for i, l in enumerate(rankings):
            j = self.perfect.index(l)
            avg += abs(i-j)
        avg = avg/float(len(self.perfect))

        dev = 0
        for i, l in enumerate(rankings):
            j = self.perfect.index(l)
            dev += (abs(i-j)-avg)**2
        dev = math.sqrt(dev/len(self.perfect))

        return avg, dev

    def draw(self, screen, xpos = 0):
        rankings = self.get_ranking()
        for i, u in enumerate(rankings):
            screen.set_at((xpos, i), u.color)


scale = 4

N = 32
M = 32

noise = range(M)
noise = [N/4.]*M

groups = [Group(N) for x in range(M)]
for n,g in zip(noise,groups): g.noise = n*float(N)/M

size = (M+1,N+1)
center = (size[0]/2, size[1]/2)

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 18)
font = pygame.font.SysFont('ubuntumono', 16)

screen = pygame.display.set_mode(map(lambda x: x*scale, size))
canvas = pygame.Surface(size)

tidx= 0
ticks = 1

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    
    canvas.fill((0,0,0))

    

    start = time.time()
    for i in range(ticks):
        for g in groups:
            g.tick(tidx)
        canvas.set_at((M, tidx), (255,255,255))
        tidx = random.randint(0,N)
        tidx %= N
        if tidx == N: tidx = 0
    stop = time.time()
    if stop-start < .005: ticks+=1
    elif stop-start > .02: ticks = max(1, ticks-1)

    sleeptime = .02-(stop-start)
    print(ticks) 

    for i,g in enumerate(groups):
        g.draw(canvas,i)



    pygame.transform.scale(canvas, screen.get_size(), screen)

    pygame.display.flip()

    if sleeptime > 0: time.sleep(sleeptime)

"""
for noise in [50]:
    g = Group(N)
    g.noise = noise
#    errs = [g.tick_all(10./(i+1)) for i in range(100)]
    errs = [g.tick_all(1)[0] for i in range(200)]   
    plt.plot(errs)
    vals = g.get_ranking()
#    plt.plot(range(len(vals)), map(lambda x: x.srank, vals))
#    plt.plot(map(lambda x: x.srank, vals), g.get_winrates())   

plt.show()
"""
