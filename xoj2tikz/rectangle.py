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

class Rectangle:
    """
    Represents a Rectangle (identfied by its lower left and upper right corner).
    
    Note that Xournal does not save rectangles as such in its .xoj files.
    We need to do our best to recognize them.
    """
    def __init__(self, color=None, x1=-1.0, y1=-1.0, x2=-1.0, y2=-1.0, width=0):
        """
        Constructor
        
        Keyword arguments:
        color -- Rectangle color, tuple of red, green, blue and opacity (default (0,0,0,1.0))
        x1 -- x-Coordinate of lower left corner (default -1.0)
        y1 -- y-Coordinate of lower left corner (default -1.0)
        x2 -- x-Coordinate of upper right corner (default -1.0)
        y2 -- y-Coordinate of upper right corner (default -1.0)
        width -- Width of the stroke in pt (default 0)
        """
        self.color = color
        if color is None:
            self.color = (0, 0, 0, 1.0)
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.width = width
        
    def __copy__(self):
        return Rectangle(color=self.color, x1=self.x1, y1=self.y1,
                         x2=self.x2, y2=self.y2, width=self.width)
    
    def __str__(self):
        return "Rectangle at ({},{}) to ({},{}) with color '{}' and width {}pt"\
               .format(self.x1, self.y1, self.x2, self.y2, self.color,
                       self.width)

    def print(self, prefix=""):
        """
        Print a short description of the object.
        (for debugging purposes)
        
        Keyword arguments:
        prefix -- Prefix output with this string (default "")
        """
        print("{}Rectangle at ({},{}) to ({},{}) with color '{}' and width {}pt"\
              .format(prefix, self.x1, self.y1, self.x2, self.y2, self.color,
                      self.width))
