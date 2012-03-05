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
    coords = stroke.coordList
    
    #TODO: support strokes that do not have a length of 5
    if (not isinstance(stroke, Stroke) or len(stroke.coordList) != 5 or 
            stroke.coordList[-1] != stroke.coordList[0] or
            len(stroke.coordList[1]) != 2):
        return stroke
    
    # Determine bounding box of the stroke:
    left = right = coords[0][0]
    top = bottom = coords[0][1]
    for coord in coords[1:]:
        left = min(left, coord[0])
        right = max(right, coord[0])
        top = max(top, coord[1])
        bottom = min(bottom, coord[1])
    
    # All edges of the bounding box should be in the stroke, otherwise its not
    # an rectangle
    if ([left, top] not in coords or [right, top] not in coords or
            [left, bottom] not in coords or [right, bottom] not in coords):
        return stroke
    
    # Every coordinate in the stroke should be on the edges, otherwise its not
    # a rectangle
    for coord in coords:
        if coord[0] not in (left, right) and coord[1] not in (top, bottom):
            return stroke
    
    return Rectangle(color=stroke.color, x1=left, y1=bottom, x2=right, y2=top,
                     width=stroke.width)
    
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
