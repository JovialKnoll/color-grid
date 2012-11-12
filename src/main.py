#Brett Kaplan
#November 12, 2012

import pygame, sys

class Pixel(object):
    def __init__(self, x, y):
        """give x and y from 0 to 1"""
        #set color based on x and y floats