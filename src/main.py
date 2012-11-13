#Brett Kaplan
#November 12, 2012

import pygame, sys, math, random

random.seed()
COLOR_FRICTION = 0.001
COLOR_CHANGE = 100.0
SCREEN_WIDTH = 64

def roundin(num):
    if math.fabs(num) < 4:
        return 0
    return math.copysign(math.floor(math.fabs(num)),num)

class Pixel(object):
    def __init__(self, setx, sety, setr, setg, setb):
        """give setr, setg, setb from 0 to 255"""
        self.xy = (setx, sety)
        self.setColor( (setr, setg, setb, 0, 0, 0) )
        #self.setColor(setrgb, (0,0,0))
        
    def setColor(self, setcolor_info):
    #def setColor(self, setcolor, setcolor_vel):
        self.color = pygame.Color(int(min(255,max(0,setcolor_info[0]))), int(min(255,max(0,setcolor_info[1]))), int(min(255,max(0,setcolor_info[2]))))
        #self.color = pygame.Color(*setcolor)
        self.color_vel = (min(127,max(-127,setcolor_info[3])), min(127,max(-127,setcolor_info[4])), min(127,max(-127,setcolor_info[5])))
        #self.color_vel = setcolor_vel
        #color_vel values go from -127 to 127
        #self.jiggle(-2,2)
        
    def jiggle(self, r1, r2):
        self.color_vel = (random.randint(r1,r2), random.randint(r1,r2), random.randint(r1,r2))
        
    def update(self, t, pixels):
        """return a tuple for updating the object with respect to neighbors"""
        #t is number of milliseconds since last frame
        #pixels is list of lists of pixels (including this pixel)
        neighbors = [pixels[(self.xy[0]-1) % SCREEN_WIDTH][self.xy[1]], pixels[(self.xy[0]+1) % SCREEN_WIDTH][self.xy[1]], pixels[self.xy[0]][(self.xy[1]-1) % SCREEN_WIDTH], pixels[self.xy[0]][(self.xy[1]+1) % SCREEN_WIDTH]]
        tempcol_list = [self.color.r, self.color.g, self.color.b]
        tempvel_list = [0,0,0]
        for n in range(3):
            for pix in neighbors:
                tempvel = pix.color_vel[n]
                temp = math.fabs(tempvel)-(COLOR_FRICTION*t)
                if (temp>0):
                    tempcol_list[n] += (tempvel + math.copysign(temp,tempvel)) * COLOR_FRICTION*t * 0.5 * 0.125 * COLOR_CHANGE
                    tempvel_list[n] += math.copysign(temp,tempvel)
                else:
                    tempcol_list[n] += tempvel * math.fabs(tempvel) * 0.5 * 0.125 * COLOR_CHANGE
            tempvel_list[n] *= 0.25
            
            tempvel = self.color_vel[n]
            temp = math.fabs(tempvel)-(COLOR_FRICTION*t)
            if (temp>=0):
                tempcol_list[n] += (tempvel + math.copysign(temp,tempvel)) * COLOR_FRICTION*t * 0.5 * COLOR_CHANGE
                tempvel_list[n] += math.copysign(temp,tempvel) * 3.0
            else:
                tempcol_list[n] += tempvel * math.fabs(tempvel) * 0.5 * COLOR_CHANGE
            tempvel_list[n] *= 0.25
        #for tcl in tempcol_list:
        #    tcl = min(255,max(0,tcl))
        #for tvl in tempvel_list:
        #    tvl = min(127,max(-127,tvl))
        return (tempcol_list[0], tempcol_list[1], tempcol_list[2], roundin(tempvel_list[0]), roundin(tempvel_list[1]), roundin(tempvel_list[2]))
        #return (tuple(tempcol_list), tuple(tempvel_list))
        
    def draw(self, draw_surface):
        draw_surface.set_at(self.xy, self.color)
        
class Visual(object):
    def __init__(self, setw, seth):
        self.screen = pygame.display.set_mode((setw, seth), pygame.FULLSCREEN)
        #self.screen = pygame.display.set_mode((setw, seth))#, pygame.NOFRAME) perhaps
        self.w = setw
        self.h = seth
        self.pixel_sets = [[[Pixel(x, y, max(0,(x-y)*256/SCREEN_WIDTH), max(0,(x+y-SCREEN_WIDTH)*256/SCREEN_WIDTH), max(0,(y-x)*256/SCREEN_WIDTH)) for y in range(seth)] for x in range(setw)] for n in range(2)]
        self.current_set = 0
        
    def update(self, t):
        for x in range(self.w):
            for y in range(self.h):
                self.pixel_sets[not self.current_set][x][y].setColor( self.pixel_sets[self.current_set][x][y].update(t, self.pixel_sets[self.current_set]) )
                #self.pixel_sets[not self.current_set][x][y].setColor( *self.pixel_sets[self.current_set][x][y].update(t, self.pixel_sets[self.current_set]) )
        self.current_set = not self.current_set
        
    def draw(self):
        for columns in self.pixel_sets[self.current_set]:
            for pixels in columns:
                pixels.draw(self.screen)
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
            my_visual.pixel_sets[my_visual.current_set][mxy[0]][mxy[1]].jiggle(-127,127)
    my_visual.update(my_clock.tick())
    my_visual.draw()
pygame.quit()
sys.exit()