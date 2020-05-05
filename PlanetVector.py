#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division

__author__ = "Jonathan Grimm"
__date__ = "12.06.18"
__IDE__ = "PyCharm Community Edition"

import numpy as np


class Vector:
    def __init__(self, x=0.0, y=0.0, norm=None, v=None):
        """
        :param x: float: x coordinate of directional vector
        :param y: float: y coordinate of directional vector
        :param norm: float: length of the vector
        :param v: numpy array: np array of the vector
        :return:
        """
        if type(v) == type(np.array([])):
            self.v = v
        else:
            self.v = np.array([x, y])
        if norm is None:
            self.norm = np.linalg.norm(self.v)
        else:
            self.norm = norm
            n = self.norm / np.linalg.norm(self.v)
            self.v = self.v * n

    def getnorm(self):
        return np.linalg.norm(self.v)

    def __add__(self, other):
        return Vector(v=self.v + other.v)

    def __sub__(self, other):
        return Vector(v=self.v - other.v)

    def __mul__(self, other):
        if type(other) in (type(int()), type(float())):
            return Vector(v=self.v * other)
        elif isinstance(other, Vector):
            return Vector(v=self.v * other.v)
        else:
            print("smth went wong")
            return "this wont work"

    def __truediv__(self, other):
        if type(other) in (type(int()), type(float())):
            return Vector(v=self.v / other)
        else:
            print("smth went wong")
            return "this wont work"

    def __call__(self, *args, **kwargs):
        """
        callable function of the object
        :return: numpy array: np array of the vector
        """
        return self.v

    def x(self):
        return self.v[0]

    def y(self):
        return self.v[1]