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
        self.x = x
        self.xnew = 0
        self.drawx = 0
        self.y = y
        self.ynew = 0
        self.drawy = 0
        # positional vector
        self.pv = Vector(self.x, self.y)

        self.mass = mass
        self.velocityVector = velocityVector
        self.vVnew = Vector()

        self.radius = radius
        self.colour = colour

        self.trajectory = []#np.array([])#([[self.x,self.y]])
        self.trajectory2 = []
        # self.screen = Window.screen
        # self.scaling = Window.scaling

        # proportion scaling
        # self.prop=3.0 / math.pow(10, 9)
        self.prop = 1.0 / math.pow(10, 9)
        # if self.name=="moon":
        #    self.prop=3.0 / math.pow(10, 6)


    ## this probably needs tp move
    def display(self):
        pygame.draw.circle(self.window.screen, self.colour, (
            int((self.x - self.window.focus.x) * self.prop + self.window.scaling[0]),
            int((self.y - self.window.focus.y) * self.prop + self.window.scaling[1])),
                           self.radius, 0)

        if self.window.trajectory:
            traj=np.array([[self.x, self.y]])
            if self.window.planetozentrisch:
                traj=traj - (self.window.focus.x, self.window.focus.y)
            try:
                self.trajectory=np.append(self.trajectory, traj,axis=0)
            except ValueError:
                self.trajectory=traj
            #print so.trajectory
            if len(self.trajectory) > self.window.traj_length:
                self.trajectory = np.delete(self.trajectory, 0,0)

        #print self.Window.trajectory,len(self.trajectory)
        if self.window.trajectory and len(self.trajectory) > 1:
            #print "duh"
            #print self.trajectory
            if self.window.planetozentrisch:
                pygame.draw.lines(self.window.screen, self.colour, False,
                              (self.trajectory) * self.prop +
                              self.window.scaling[0])
            else:
                pygame.draw.lines(self.window.screen, self.colour, False,
                              (self.trajectory- (self.window.focus.x, self.window.focus.y)) * self.prop +
                              self.window.scaling[0])