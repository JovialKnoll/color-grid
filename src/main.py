#Brett Kaplan
#November 12, 2012
from __future__ import division
import pygame, sys, math, random
import pygcurse
random.seed()

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
        #self.w = setw
        #self.h = seth
        #self.screen = pygame.display.set_mode((self.w, self.h))
        self.pixel_sets = [[[Pixel(x, y, max(0,int((x/setw-y/seth)*256)), max(0,int((x/setw+y/seth-1)*256)), max(0,int((y/seth-x/setw)*256))) for y in range(seth)] for x in range(setw)] for n in range(2)]
        self.current_set = 0
        self.awaiting_update = [dict() for n in range(2)]#list of dicts; (x,y):s
        #self.awaiting_draw = sum(self.pixel_sets[self.current_set] ,[])
        self.setScreen(setw, seth)
        
    def update(self, t):
        if len(self.awaiting_update[self.current_set]) > 0:
            for pxy, shift in self.awaiting_update[self.current_set].iteritems():
                if shift == 0:
                    continue
                self.awaiting_draw.append(self.pixel_sets[not self.current_set][pxy[0]][pxy[1]].shiftColor(self.pixel_sets[self.current_set][pxy[0]][pxy[1]].color, shift))
                txy = ((pxy[0]-1)%self.w,pxy[1])
                self.awaiting_draw.append(self.pixel_sets[not self.current_set][txy[0]][txy[1]])
                
                if txy in self.awaiting_update[not self.current_set]:
                    if self.awaiting_update[not self.current_set][txy] > 0:
                        #self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+math.fabs(shift))//-2#shift, maybe no fabs
                        self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+shift)//-2
                    else:
                        del self.awaiting_update[not self.current_set][txy]
                else:
                    self.awaiting_update[not self.current_set][txy] = shift//2#math.fabs(shift)//2
                
                txy = ((pxy[0]+1)%self.w,pxy[1])
                self.awaiting_draw.append(self.pixel_sets[not self.current_set][txy[0]][txy[1]])
                
                if txy in self.awaiting_update[not self.current_set]:
                    if self.awaiting_update[not self.current_set][txy] > 0:
                        #self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+math.fabs(shift))//-2#shift, maybe no fabs
                        self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+shift)//-2
                    else:
                        del self.awaiting_update[not self.current_set][txy]
                else:
                    self.awaiting_update[not self.current_set][txy] = shift//2#math.fabs(shift)//2
                
                txy = (pxy[0],(pxy[1]-1)%self.h)
                self.awaiting_draw.append(self.pixel_sets[not self.current_set][txy[0]][txy[1]])
                
                if txy in self.awaiting_update[not self.current_set]:
                    if self.awaiting_update[not self.current_set][txy] > 0:
                        #self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+math.fabs(shift))//-2#shift, maybe no fabs
                        self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+shift)//-2
                    else:
                        del self.awaiting_update[not self.current_set][txy]
                else:
                    self.awaiting_update[not self.current_set][txy] = shift//2#math.fabs(shift)//2
                
                txy = (pxy[0],(pxy[1]+1)%self.h)
                self.awaiting_draw.append(self.pixel_sets[not self.current_set][txy[0]][txy[1]])
                
                if txy in self.awaiting_update[not self.current_set]:
                    if self.awaiting_update[not self.current_set][txy] > 0:
                        #self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+math.fabs(shift))//-2#shift, maybe no fabs
                        self.awaiting_update[not self.current_set][txy] = (self.awaiting_update[not self.current_set][txy]+shift)//-2
                    else:
                        del self.awaiting_update[not self.current_set][txy]
                else:
                    self.awaiting_update[not self.current_set][txy] = shift//2#math.fabs(shift)//2
            self.awaiting_update[self.current_set].clear()
            self.current_set = not self.current_set
        
    def draw(self):
        for pixels in self.awaiting_draw:
            pixels.draw(self.screen)
        self.awaiting_draw = []
        pygame.display.flip()
        
    def setScreen(self, setw=-1, seth=-1):
        if setw > 0 and seth > 0:
            self.w = setw
            self.h = seth
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.awaiting_draw = sum(self.pixel_sets[self.current_set] ,[])
        
class Game(object):
    def __init__(self, scr_width):
        pygame.init()
        self.my_visual = Visual(scr_width,scr_width)
        self.my_clock = pygame.time.Clock()
        self.key_input = 0
        
    def __del__(self):
        pygame.quit()
        
    def run(self, shft_amt, frmrt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return 0
                elif event.key == pygame.K_RETURN:
                    #buncha stuff
                    pygame.display.quit()
                    
                    test_win = pygcurse.PygcurseWindow(40,25)
                    test_win.pygprint('give input:')
                    test_input = test_win.input()
                    print test_input
                    
                    pygame.display.init()
                    self.my_visual.setScreen()
                    #pygame.event.clear()
                    break
                #if event.key == pygame.K_m:
                #    return 2
            if event.type == pygame.MOUSEBUTTONDOWN:
                mxy = event.pos
                self.my_visual.awaiting_update[self.my_visual.current_set][mxy] = shft_amt
        self.my_visual.update(self.my_clock.tick(frmrt))
        self.my_visual.draw()
        return 1
        
SCREEN_WIDTH = 256
SHIFT_AMOUNT = 8
FRAMERATE = 60
my_game = Game(SCREEN_WIDTH)
on = 1
while on:
    if on == 1:
        on = my_game.run(SHIFT_AMOUNT, FRAMERATE)
    elif on == 2:
        del my_game
        new_width = 401
        while new_width > 400 or new_width < 4:
            try:
                new_width = int(raw_input('New screen width (less than 400):'))
            except ValueError:
                new_width = 401
        my_game = Game(new_width)
        on = my_game.run(SHIFT_AMOUNT, FRAMERATE)
    
del my_game
sys.exit()
