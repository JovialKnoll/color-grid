#Brett Kaplan
#November 12, 2012

import pygame, sys

COLOR_FRICTION = .001

class Pixel(object):
    def __init__(self, setx, sety, setr, setg, setb):
        """give setr, setg, setb from 0 to 255"""
        self.position = (setx, sety)
        self.setColor(setr, setg, setb, (0,0,0))
        
    def setColor(self, setr, setg, setb, setcolor_vel):
        self.color = pygame.Color(setr, setg, setb)
        self.color_vel = setcolor_vel
        #color_vel values go from -127 to 127
        
    def update(self, t, pixels):
        """return a tuple for updating the object with respect to neighbors"""
        #t is number of milliseconds since last frame
        #pixels is list of lists of pixels (including this pixel)
        pixels[self.position[0]][self.position[1]]
        
        
        color_vel[0]+  color_vel[0]- math.copysign(COLOR_FRICTION*t, color_vel[0])
        temp = math.fabs(color_vel[0])-(COLOR_FRICTION*t)
        if (temp>=0):
            tempr=self.color.r + ((color_vel[0] + math.copysign(temp,color_vel[0])) * COLOR_FRICTION*t * 0.5)
        else:
            tempr=self.color.r + ((color_vel[0] + 0) * (COLOR_FRICTION*t + temp ) * 0.5)
                                                       (math.fabs(color_vel[0]) )
                                                       
        self.color_vel