#Brett Kaplan
#November 12, 2012

import pygame, sys, math, random

random.seed()
SCREEN_WIDTH = 256
SHIFT_AMOUNT = 8
FRAMERATE = 60

class Pixel(object):
    def __init__(self, setx, sety, setr, setg, setb):
        """give setr, setg, setb from 0 to 255"""
        self.xy = (setx, sety)
        self.color = pygame.Color(setr, setg, setb)
        
    def shiftColor(self, base, shift):
        #print int((base.r+shift)%255), int((base.g+shift)%255), int((base.b+shift)%255)
        self.color = pygame.Color(int((base.r+shift)%255), int((base.g+shift)%255), int((base.b+shift)%255))
        return self
        
    def draw(self, draw_surface):
        draw_surface.set_at(self.xy, self.color)
        
class Visual(object):
    def __init__(self, setw, seth):
        self.screen = pygame.display.set_mode((setw, seth))#, pygame.FULLSCREEN)
        #self.screen = pygame.display.set_mode((setw, seth))#, pygame.NOFRAME) perhaps
        self.w = setw
        self.h = seth
        self.pixel_sets = [[[Pixel(x, y, max(0,(x-y)*256/SCREEN_WIDTH), max(0,(x+y-SCREEN_WIDTH)*256/SCREEN_WIDTH), max(0,(y-x)*256/SCREEN_WIDTH)) for y in range(seth)] for x in range(setw)] for n in range(2)]
        self.current_set = 0
        self.awaiting_update = [dict() for n in range(2)]#list of dicts; (x,y):s
        self.awaiting_draw = sum( self.pixel_sets[self.current_set] ,[])
        #self.draw()
        
    def update(self, t):
        if len(self.awaiting_update[self.current_set]) > 0:
            for pxy, shift in self.awaiting_update[self.current_set].iteritems():
                if shift == 0:
                    continue
                self.awaiting_draw.append(self.pixel_sets[not self.current_set][pxy[0]][pxy[1]].shiftColor(self.pixel_sets[self.current_set][pxy[0]][pxy[1]].color, shift))
                txy = ((pxy[0]-1)%SCREEN_WIDTH,pxy[1])
                if txy in self.awaiting_update[not self.current_set]:
                    if self.awaiting_update[not self.current_set][txy] > 0:
                        #self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+math.fabs(shift))/-2#shift, maybe no fabs
                        self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+shift)/-2
                    else:
                        del self.awaiting_update[not self.current_set][txy]
                else:
                    self.awaiting_update[not self.current_set][txy] = shift/2#math.fabs(shift)/2
                
                txy = ((pxy[0]+1)%SCREEN_WIDTH,pxy[1])
                if txy in self.awaiting_update[not self.current_set]:
                    if self.awaiting_update[not self.current_set][txy] > 0:
                        #self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+math.fabs(shift))/-2#shift, maybe no fabs
                        self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+shift)/-2
                    else:
                        del self.awaiting_update[not self.current_set][txy]
                else:
                    self.awaiting_update[not self.current_set][txy] = shift/2#math.fabs(shift)/2
                
                txy = (pxy[0],(pxy[1]-1)%SCREEN_WIDTH)
                if txy in self.awaiting_update[not self.current_set]:
                    if self.awaiting_update[not self.current_set][txy] > 0:
                        #self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+math.fabs(shift))/-2#shift, maybe no fabs
                        self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+shift)/-2
                    else:
                        del self.awaiting_update[not self.current_set][txy]
                else:
                    self.awaiting_update[not self.current_set][txy] = shift/2#math.fabs(shift)/2
                
                txy = (pxy[0],(pxy[1]+1)%SCREEN_WIDTH)
                if txy in self.awaiting_update[not self.current_set]:
                    if self.awaiting_update[not self.current_set][txy] > 0:
                        #self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+math.fabs(shift))/-2#shift, maybe no fabs
                        self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+shift)/-2
                    else:
                        del self.awaiting_update[not self.current_set][txy]
                else:
                    self.awaiting_update[not self.current_set][txy] = shift/2#math.fabs(shift)/2
            self.awaiting_update[self.current_set].clear()
            self.current_set = not self.current_set
        
    def draw(self):
        for pixels in self.awaiting_draw:
            pixels.draw(self.screen)
        self.awaiting_draw = []
        pygame.display.flip()
        
on = True
pygame.init()
my_visual = Visual(SCREEN_WIDTH,SCREEN_WIDTH)
my_clock = pygame.time.Clock()
while on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            on = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                on = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mxy = event.pos
            my_visual.awaiting_update[my_visual.current_set][mxy] = SHIFT_AMOUNT
    my_visual.update(my_clock.tick(FRAMERATE))
    my_visual.draw()
pygame.quit()
sys.exit()