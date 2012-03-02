#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of xoj2tikz.
# Copyright (C) 2012 Fabian Henze, Simon Vetter
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

import sys
from math import sqrt

from .page import Page
from .layer import Layer
from .stroke import Stroke
from .textbox import TextBox
from .rectangle import Rectangle
from .circle import Circle

"""
This is a collection of functions to simplify strokes and detect shapes to
improve the quality and size of the output file.
"""

def detectCircle(stroke):
    return stroke

def detectRectangle(stroke):
    return stroke

def simplifyStrokes(stroke):
    """
    Detect collinear parts of a stroke and remove them.
    """
    if isinstance(stroke, Stroke):
        s = 0
        while s < len(stroke.coordList) - 2:
            ax = stroke.coordList[s][0]
            ay = stroke.coordList[s][1]
            bx = stroke.coordList[s+1][0]
            by = stroke.coordList[s+1][1]
            cx = stroke.coordList[s+2][0]
            cy = stroke.coordList[s+2][1]
            
            # Calculate the dot / scalar product of the two vectors
            scalarProduct = (ax-bx) * (bx-cx) + (ay-by) * (by-cy)
            
            # Calculate the lengths of both vectors (from a to b, from b to c)
            firstLength = sqrt((ax-bx)**2 + (ay-by)**2)
            secondLength = sqrt((bx-cx)**2 + (by-cy)**2)
            
            # If the product of both individual lengths is 'almost equal' to
            # the scalar product, then these vectors are colinear.
            # 0.99999 is an epsilon to compensate float inaccurracy.
            # Testing has shown that this is a good value. maybe one should
            # calculate the absolute error ...
            if (firstLength * secondLength > 0.99999 * scalarProduct and
                    len(stroke.coordList[s+1]) == 2):
                del stroke.coordList[s+1]
                continue
            s += 1
    return stroke

def runAll(document):
    """
    Iterate over a list of pages and run all optimization algorithms on them.
    """
    for page in document:
        for layer in page.layerList:
            inplace_map(simplifyStrokes, layer.itemList)
            inplace_map(detectCircle, layer.itemList)
            inplace_map(detectRectangle, layer.itemList)

def inplace_map(function, iterable):
    """Similar to pythons map() builtin, but it works in-place."""
    for i, item in enumerate(iterable):
        iterable[i] = function(item)
