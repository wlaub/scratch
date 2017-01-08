import pygame
from pygame.locals import *
import sys, time, math

"""
Vertex Dispenser simulator
Requires pygame
Left click to capture vertex, right click to uncapture.
Press p to replay the sequences and escape to clear.
"""

size = (500,500)
center = (size[0]/2, size[1]/2)

pygame.init()
pygame.font.init()
font = pygame.font.SysFont(pygame.font.get_default_font(), 18)

screen = pygame.display.set_mode(size)

def add_pos(pos1, pos2):
    return (pos1[0]+pos2[0], pos1[1]+pos2[1])

def floor_pos(pos):
    return (int(pos[0]), int(pos[1]))

class Cell():
    
    colormap =  [ (64,64,64)
                , (0,0,255)
                , (255,0,0)
                , (0,255,0)
                , (255,255,0)
                , (0,255,255)
                , (255,0,255)
                , (255,255,255)
                ]
    r=16
    img = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.val = 1
        self.locked = 0
        self.adj = self.get_adjacent()

    @staticmethod
    def init():
        N=6.
        r = Cell.r-.5
        c = 2*math.pi/N
        s = Cell.r

        for color in Cell.colormap:
            img = pygame.Surface((s*2,s*2), depth=32)
            img.set_colorkey((0,0,0,0))
            pygame.draw.polygon ( img, color
                                , [(s+r*math.cos(c*x), s+r*math.sin(c*x)) for x in range(int(N))] 
                                )
            Cell.img.append(img)

    def get_adjacent(self):
        off = 2*(self.x%2) -1
        return  ( (self.x, self.y+1)
                , (self.x, self.y-1)
                , (self.x+1, self.y)
                , (self.x-1, self.y)
                , (self.x+1, self.y+off)
                , (self.x-1, self.y+off)
                )

    def get_is_adj(self, cell):
        return (cell.x,cell.y) in self.adj

    def get_coords(self):
        off = (self.x%2)/2.
        return (self.x*.866*self.r*2+self.r/2., (self.y+off)*self.r*2)

    def get_hit(self, pos):
        loc = add_pos(self.get_coords(), center)
        pos = [-x for x in pos]
        diff = add_pos(loc, pos)
        dist = diff[0]*diff[0] + diff[1]*diff[1]
        return dist < self.r*self.r

    def draw(self, screen):
        text = font.render(str(self.val), True, (0,0,0))

        pos = add_pos(self.get_coords(), center)

        hoff = (-self.r,-self.r)       
        hpos = floor_pos(add_pos(pos, hoff))

        toff = (-text.get_size()[0]/2., -text.get_size()[1]/2.)
        tpos = add_pos(pos, toff)

        tpos = floor_pos(tpos)
        pos = floor_pos(pos)

        val = self.val if self.locked else 0
#        color = self.colormap[self.val] if self.locked else self.colormap[0]
#        pygame.draw.circle(screen, color, pos, self.r-2)
        screen.blit(self.img[val], hpos)
        if self.val == 0:
            return
        screen.blit(text, tpos)

    def update(self, adj):
        """
        Update value from list of adjacent locked cells
        """
        self.val = min([x for x in range(1,10) if not x in adj])


def make_board(x,y):
    result = []
    for i in range(-x,x):
        for j in range(-y,y):
            ncell = Cell(i,j)
            result.append(ncell)
    return result

def cell_on(c):
    c.locked=1
    adj = [x for x in tcells if not x.locked and c.get_is_adj(x)]
    for tc in adj:
        tadj = [x.val for x in tcells if x.locked and tc.get_is_adj(x)]
        tc.update(tadj)

def cell_off(c):
    c.locked = 0
    adj = [x.val for x in tcells if x.locked and c.get_is_adj(x)]
    c.update(adj)
    adj = [x for x in tcells if not x.locked and c.get_is_adj(x)]
    for tc in adj:
        tadj = [x.val for x in tcells if x.locked and tc.get_is_adj(x)]
        tc.update(tadj)

def do_event(event, fake=False):
    for c in tcells:
        if c.get_hit(event.pos):
            if not fake:
                seq.append(event)
            if event.button == 1:
                cell_on(c)
                break
            elif event.button == 3:
                cell_off(c)
                break
 

def draw(screen):
    screen.fill((0,0,0))

    for c in tcells:
        c.draw(screen)

    text = font.render("Moves: {}".format(len(seq)), True, (255,255,255))
    screen.blit(text, (0,0))

    pygame.display.flip()


def clear():
    for c in tcells:
        c.locked=0
        c.val=1


def play_seq():
    gif = gifimg.GIFImage("hex.gif")
    clear()
    for event in seq:
        do_event(event, True) 
        draw(screen)
        time.sleep(.5)

Cell.init()
tcells = make_board(8,7)
seq = []

while 1:
    time.sleep(.01)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            clear()
            seq=[]
        elif event.type == MOUSEBUTTONDOWN:
            do_event(event)
        elif event.type == KEYDOWN and event.key == K_p:
            play_seq()                

    draw(screen)

