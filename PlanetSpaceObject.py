#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Jonathan Grimm"
__date__ = "12.06.18"
__IDE__ = "PyCharm Community Edition"

from PlanetVector import Vector
import math
import numpy as np



class SpaceObject:
    def __init__(self, name, x, y, mass, velocityVector, radius, colour):
        self.name = name
        self.x = x # real value coordinates
        self.xnew = 0
        self.drawx = 0 # coordinates on the canvas
        self.y = y # real value coordinates
        self.ynew = 0
        self.drawy = 0 # coordinates on the canvas

        self.pv = Vector(self.x, self.y) # positional vector

        self.mass = mass # mass of the space object
        self.velocityVector = velocityVector # vector of the velocity of the space object
        self.vVnew = Vector()
        self.radius = radius #radius
        self.colour = colour

        self.trajectory = []# np.array([])#([[self.x,self.y]])
        self.trajectory2 = []
        # self.screen = Window.screen
        # self.scaling = Window.scaling

        # proportion scaling
        # self.prop=3.0 / math.pow(10, 9)
        self.prop = 1.0 / math.pow(10, 9) # value to scale down the real values to a format that can be projected on a canvas in pixel
        # if self.name=="moon":
        #    self.prop=3.0 / math.pow(10, 6)
