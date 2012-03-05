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

from math import sqrt

from .page import Page
from .layer import Layer
from .stroke import Stroke
from .rectangle import Rectangle
from .circle import Circle

"""
This is a collection of functions to simplify strokes and detect shapes to
improve the quality and size of the output file.
"""

def detectCircle(stroke):
    return stroke

def detectRectangle(stroke):
    """
    Detect Rectangles, input should be a Stroke that has already been
    simplified.
    """
    if (not isinstance(stroke, Stroke) or len(stroke.coordList) != 5 or 
            stroke.coordList[-1] != stroke.coordList[0] or
            len(stroke.coordList[1]) != 2):
        return stroke
    
    lowerLeft = [stroke.coordList[0][0], stroke.coordList[0][1]]
    upperRight = [stroke.coordList[0][0], stroke.coordList[0][1]]
    for s in range(len(stroke.coordList)-1):
        coordOne = stroke.coordList[s]
        coordTwo = stroke.coordList[s+1]
        lowerLeft[0] = min(lowerLeft[0], coordTwo[0])
        lowerLeft[1] = min(lowerLeft[1], coordTwo[1])
        upperRight[0] = max(upperRight[0], coordTwo[0])
        upperRight[1] = max(upperRight[1], coordTwo[1])
        if coordOne[0] != coordTwo[0] and coordOne[1] != coordTwo[1]:
            return stroke
    return Rectangle(color=stroke.color, x1=lowerLeft[0], y1=lowerLeft[1],
                     x2=upperRight[0], y2=upperRight[1], width=stroke.width)
    
def simplifyStrokes(stroke):
    """
    Detect collinear parts of a stroke and remove them.
    """
    s = 0
    
    if not isinstance(stroke, Stroke) or len(stroke.coordList[1]) != 2:
        return stroke
    
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
        if firstLength * secondLength * 0.99999 < scalarProduct:
            del stroke.coordList[s+1]
        else:
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
