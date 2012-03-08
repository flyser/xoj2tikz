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

class Ellipse:
    """
    Represents an Ellipse (identfied its bounding rectangle).
    
    Note that Xournal does not save ellipses as such in its .xoj files.
    We need to do our best to recognize them.
    """
    def __init__(self, color=None, left=-1.0, right=-1.0, top=-1.0, bottom=-1.0,
                 width=0):
        """
        Constructor
        
        Keyword arguments:
        color -- Ellipse color, tuple of red, green, blue and opacity (default (0,0,0,1.0))
        left -- x-Coordinate of the left edge (default -1.0)
        right -- x-Coordinate of the right edge (default -1.0)
        top -- y-Coordinate of the upper edge (default -1.0)
        bottom -- y-Coordinate of lower edge (default -1.0)
        width -- Width of the stroke in pt (default 0)
        """
        self.color = color
        if color is None:
            self.color = (0, 0, 0, 1.0)
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.width = width
        
    def __copy__(self):
        return Ellipse(color=self.color, left=self.left, right=self.right,
                       top=self.top, bottom=self.bottom, width=self.width)
    
    def __str__(self):
        return "Ellipse at ({},{}) to ({},{}) with color '{}' and width {}pt"\
               .format(self.left, self.bottom, self.right, self.top, self.color,
                       self.width)

    def print(self, prefix=""):
        """
        Print a short description of the object.
        (for debugging purposes)
        
        Keyword arguments:
        prefix -- Prefix output with this string (default "")
        """
        print("{}Ellipse at ({},{}) to ({},{}) with color '{}' and width {}pt"\
               .format(self.left, self.bottom, self.right, self.top, self.color,
                       self.width))
