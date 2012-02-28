#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of xoj2tikz.
# Copyright (C) 2012 Fabian Henze
# 
# xoj2tikz is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# xoj2tikz is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with xoj2tikz.  If not, see <http://www.gnu.org/licenses/>.

from copy import copy

class Circle:
    """
    Represents a Circle (center and radius).
    
    Note that Xournal does not save circles as such in their .xoj files.
    We need to do our best to recognize them.
    """
    def __init__(self, color=None, x=-1.0, y=-1.0, radius=0, width=0):
        """
        Constructor
        
        Keyword arguments:
        color -- Circle color, tuple of red, green, blue and opacity (default (0,0,0,1.0))
        x -- x-Coordinate of the center (default -1.0)
        y -- y-Coordinate of the center (default -1.0)
        radius -- Radius of the circle in pt (default 0)
        width -- Width of the stroke in pt (default 0)
        """
        self.color = color
        if color is None:
            self.color = (0, 0, 0, 1.0)
        self.x = x
        self.y = y
        self.radius = radius
        self.width = width
        
    def __copy__(self):
        return Circle(color=self.color, x=self.x, y=self.y, radius=self.radius,
                      width=self.width)
    
    def __str__(self):
        return "Circle at ({},{}) with radius {}pt, color '{}' and width {}pt"\
               .format(self.x, self.y, self.radius, self.color, self.width)

    def print(self, prefix=""):
        """
        Print a short description of the object.
        (for debugging purposes)
        
        Keyword arguments:
        prefix -- Prefix output with this string (default "")
        """
        print("{}Circle at ({},{}) with radius {}pt, color '{}' and width {}pt"\
              .format(prefix, self.x, self.y, self.radius, self.color,
                      self.width))
