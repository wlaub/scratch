import random, math, time
from matplotlib import pyplot as plt

import pygame
from pygame.locals import *

import colorsys

class Poly():
    
    def __init__(self, r):
        self.r = r
        self.n = 3
        self.ccolor = (255,255,255)
        self.icolor = (255,255,255)
        self.ocolor = (255,255,255)

    @staticmethod
    def get_points(r, n, off, aoff = 0):
        a = 2*math.pi/n       
        return [[off[0]+r*math.sin(x*a+aoff), off[1]-r*math.cos(x*a+aoff)] for x in range(int(math.ceil(n)))]
 

    def get_factor(self):
        return 1./math.cos(3.14/self.n)

    def get_outer_radius(self):
        return self.r*self.get_factor()

    def draw(self, screen, offset, inner = False):

        r = self.r
        rpoly = self.get_outer_radius()

#        pygame.draw.circle(screen, self.ccolor, offset, int(r), 1)

        if inner:
            pygame.draw.polygon(screen, self.icolor, Poly.get_points(r, self.n-1, offset), 1)
        pygame.draw.polygon(screen, self.ocolor, Poly.get_points(rpoly, self.n, offset), 1)

        pass



scale = 1
w = 420
h = 420

r = 32.

reff = r

N = 32

polies = []

for i in range(N):
    npoly = Poly(reff)
    npoly.n = i+3
    polies.append(npoly)
    reff = npoly.get_outer_radius()


size = (w,h)
center = (size[0]/2, size[1]/2)

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 18)
font = pygame.font.SysFont('ubuntumono', 16)

screen = pygame.display.set_mode(map(lambda x: x*scale, size))
canvas = pygame.Surface(size)

speed = 10
rrate = .319
rstep = .001
rlast = 0

while 1:
    time.sleep(.1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for i, poly in enumerate(polies):
        poly.n+=.01*speed
        if i == 0:
            poly.r += rrate*speed
            if poly.n >= 4:

                nr = poly.r/poly.get_factor()
                npoly = Poly(r)
                tr = r*npoly.get_factor()
                rerr = poly.r - tr
                print(poly.r, tr, rerr, rrate)
                if rerr > 0:
                    if rlast < 0:
                        rstep /= 2.
                    rrate -=rstep
                else:
                    if rlast >= 0:
                        rstep /=2.
                    rrate += rstep


                npoly.n = poly.n-1
                polies.insert(0, npoly)
                polies = polies[:-1]
        else:
            poly.r = polies[i-1].get_outer_radius()
 
    canvas.fill((0,0,0))

    for i, poly in enumerate(polies):
        if i == 0:
            poly.draw(canvas, center, True)
        else:
            poly.draw(canvas, center)

    pygame.transform.scale(canvas, screen.get_size(), screen)

    pygame.display.flip()



