#Brett Kaplan
#November 12, 2012

import pygame, sys

COLOR_FRICTION = .001
SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

class Pixel(object):
    def __init__(self, setx, sety, setr, setg, setb):
        """give setr, setg, setb from 0 to 255"""
        self.xy = (setx, sety)
        self.setColor(setr, setg, setb, (0,0,0))
        
    def setColor(self, setcolor, setcolor_vel):
        self.color = pygame.Color(*setcolor)
        self.color_vel = setcolor_vel
        #color_vel values go from -127 to 127
        
    def update(self, t, pixels):
        """return a tuple for updating the object with respect to neighbors"""
        #t is number of milliseconds since last frame
        #pixels is list of lists of pixels (including this pixel)
        neighbors = [ pixels[self.xy[0]-1][self.xy[1]], pixels[self.xy[0]+1][self.xy[1]], pixels[self.xy[0]][self.xy[1]-1], pixels[self.xy[0]][self.xy[1]+1] ]
        tempcol_list = [self.color.r, self.color.g, self.color.b]
        tempvel_list = [0,0,0]
        for n in range(3):
            for pix in neighbors:
                tempvel = pix.color_vel[n]
                temp = math.fabs(tempvel)-(COLOR_FRICTION*t)
                if (temp>0):
                    tempcol_list[n] += (tempvel + math.copysign(temp,tempvel)) * COLOR_FRICTION*t * 0.5 * 0.25
                    tempvel_list[n] += math.copysign(temp,tempvel)
                else:
                    tempcol_list[n] += tempvel * math.fabs(tempvel) * 0.5 * 0.25
            tempvel_list[n] *= 0.25
            
            tempvel = self.color_vel[n]
            temp = math.fabs(tempvel)-(COLOR_FRICTION*t)
            if (temp>=0):
                tempcol_list[n] += (tempvel + math.copysign(temp,tempvel)) * COLOR_FRICTION*t * 0.5
                tempvel_list[n] += math.copysign(temp,tempvel)
            else:
                tempcol_list[n] += tempvel * math.fabs(tempvel) * 0.5
            tempvel_list[n] *= 0.5
        for tcl in tempcol_list:
            tcl = min(255,max(0,tcl))
        for tvl in tempvel_list:
            tvl = min(127,max(-127,tvl))
        return (tuple(tempcol_list), tuple(tempvel_list))
        
    def draw(self, draw_surface):
        draw_surface.set_at(self.xy, self.color)
        
class Visual(object):
    def __init__(self, setw, seth):
        self.screen = pygame.display.set_mode(setw, seth)#, pygame.NOFRAME) perhaps
        self.w = setw
        self.h = seth
        self.pixel_sets = [[[Pixel(x,y,r,g,b) for y in range(seth)] for x in range(setw)] for n in range(2)]
        self.current_set = 0
        
    def update(self, t):
        for x in range(self.w):
            for y in range(self.h):
                self.pixel_sets[self.current_set][x][y].update(t, self.pixel_sets[self.current_set])
                self.pixel_sets[not self.current_set][x][y].setColor()