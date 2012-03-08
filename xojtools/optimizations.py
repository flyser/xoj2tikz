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

from math import sqrt, floor, ceil

from . import Page, Layer, Stroke, Rectangle, Circle, Ellipse

"""
This is a collection of functions to simplify strokes and detect shapes to
improve the quality and size of the output file.
"""

def detectCircle(stroke, increasedTolerance=False):
    """
    Detect, whether the input stroke is a circle and calculate its radius and
    center.
    
    Keyword arguments:
    stroke -- The Stroke that should be analyzed and possibly replaced.
    increasedTolerance -- True if a varying distance between the individual
                          points of a stroke should not be an indicator of
                          the stroke not being a circle.
    """
    
    if (not isinstance(stroke, Stroke) or len(stroke.coordList) < 10 or 
            stroke.coordList[-1] != stroke.coordList[0] or
            len(stroke.coordList[1]) != 2):
        return stroke

    # plural of radius ;-)
    radii = []
    # list of coordinates that might be the center of the circle
    xCoords = [] 
    yCoords = []
    distances = []
    length = len(stroke.coordList)
    
    for i in range(length):
        # Pick three points on the circle. the distance between these should be
        # maximal to increase precision.
        # (x1,y1) shall be point one, (x2,y2) point two, (x3,y3) point three
        x1 = stroke.coordList[i][0]
        y1 = stroke.coordList[i][1]
        x2 = stroke.coordList[(i+floor(length/3))%length][0]
        y2 = stroke.coordList[(i+floor(length/3))%length][1]
        x3 = stroke.coordList[(i+floor(2*length/3))%length][0]
        y3 = stroke.coordList[(i+floor(2*length/3))%length][1]
        
        # Calculate the point between point one and two, lets call it 'alpha'
        x12 = (x1+x2)/2
        y12 = (y1+y2)/2
        # Calculate the point between point two and three, lets call it 'beta'
        x23 = (x2+x3)/2
        y23 = (y2+y3)/2
        
        # Calculate a point which forms a line with point alpha that is
        # perpendicular to the line between point one and two,
        # lets call it 'perp_alpha'
        perp_x12 = x12 + (y1 - y2)
        perp_y12 = y12 - (x1 - x2)
        # Calculate a point which forms a line with point beta that is
        # perpendicular to the line between point two and three,
        # lets call it 'perp_beta'
        perp_x23 = x23 + (y2 - y3)
        perp_y23 = y23 - (x2 - x3)
        
        # Now we calculate the intersection of the lines (alpha, perp_alpha) 
        # and (beta, perp_beta). This is the center of our circle.
        x = (((x12*perp_y12 - y12*perp_x12)*(x23 - perp_x23) - (x12 - perp_x12)*(x23*perp_y23 - y23*perp_x23)) /
             ((x12 - perp_x12)*(y23 - perp_y23) - (y12 - perp_y12)*(x23 - perp_x23)))
        y = (((x12*perp_y12 - y12*perp_x12)*(y23 - perp_y23) - (y12 - perp_y12)*(x23*perp_y23 - y23*perp_x23)) /
             ((x12 - perp_x12)*(y23 - perp_y23) - (y12 - perp_y12)*(x23 - perp_x23)))
        xCoords.append(x)
        yCoords.append(y)
    
    xAvg = sum(xCoords)/len(xCoords)
    yAvg = sum(yCoords)/len(yCoords)

    # Calculate the radius
    for i in range(length-1):
        x1 = stroke.coordList[i][0]
        y1 = stroke.coordList[i][1]
        x2 = stroke.coordList[i+1][0]
        y2 = stroke.coordList[i+1][1]
        x12 = (x1+x2)/2
        y12 = (y1+y2)/2
        
        # Distance between point one and two
        distances.append(sqrt((x1-x2)**2 + (y1-y2)**2))
        
        # Calculate two radii and store the average of the two:
        # radius1: Distance from the center to point one
        # radius2: Distance from the center to the line between point one and two
        radius1 = sqrt((x1-xAvg)**2 + (y1-yAvg)**2)
        radius2 = sqrt((x12-xAvg)**2 + (y12-yAvg)**2)
        radii.append((radius1+radius2)/2)
    radius = sum(radii)/len(radii)
    
    # If the distances between the individual coordinates of the stroke are too
    # high or the distance varies too much, it might not be a circle.
    # e1 and e2 were empirically determined
    if increasedTolerance:
        e1 = 0.5
        e2 = 10
    else:
        e1 = 0.04
        e2 = 3.5
    
    if (max(distances) - min(distances) > e1 or
            sum(distances) / len(distances) > e2):
        # Special case: If the circle is *very* large, stroke simplication
        # might have kicked in and removed some coordinates of the stroke.
        # 275 was chosen, because stroke simplification seems to remove
        # coordinates if the radius of the circle is bigger than ~300.
        if (radius/275 < 1 or
                ceil(radius/275)*e2 < sum(distances)/len(distances)):
            return stroke
    
    # If the possible centers of the circle vary too much, then it may not be a
    # circle after all.
    # 0.02 is an empirically determined epsilon.
    if max(xCoords) - min(xCoords) > 0.02 or max(yCoords) - min(yCoords) > 0.02:
        return stroke
    
    # If the possible radii vary too much, it is not a circle.
    # 0.02 is again an empirically determined epsilon.
    if max(radii) - min(radii) > 0.02:
        return stroke
        
    return Circle(color=stroke.color, x=xAvg, y=yAvg,
                  radius=radius, width=stroke.width)
    
def detectEllipse(stroke):
    """
    Detect, whether the input stroke is an ellipse and calculate its center and
    dimensions
    
    Make sure that ellipse detection is run *after* circle detection, as
    ellipses are circles too ;-)
    """
    if (not isinstance(stroke, Stroke) or len(stroke.coordList[1]) != 2 or 
            stroke.coordList[-1] != stroke.coordList[0]):
        return stroke
    
    normalizedCoords = []
    xList = [x for x, y in stroke.coordList]
    yList = [y for x, y in stroke.coordList]
    
    # Determine bounding rectangle
    xMax = max(xList)
    xMin = min(xList)
    yMax = max(yList)
    yMin = min(yList)
    width = xMax - xMin
    height = yMax - yMin
    
    # Prevent division by zero
    if height == 0 or width == 0:
        return stroke
    
    # Normalize the bounding rectangle to a square, so we can run the circle
    # detection code on it.
    if height < width:
        factor = height/width
        newXList = [xMin + factor*(x - xMin) for x in xList]
        newYList = yList
    else: # width < height
        factor = width/height
        newXList = xList
        newYList = [yMin + factor*(y - yMin) for y in yList]
    for i,j in zip(newXList,newYList):
        normalizedCoords.append([i,j])
    
    # If a stroke, that was transformed to fit into a square is a circle, the
    # original stroke is in fact an ellipse.
    circle = detectCircle(Stroke(color=stroke.color, coordList=normalizedCoords,
                                 width=stroke.width), increasedTolerance=True)
    if isinstance(circle, Circle):
        return Ellipse(color=stroke.color, left=xMin, right=xMax, top=yMax,
                       bottom=yMin, width=stroke.width)
    else:
        return stroke
    
def detectRectangle(stroke):
    """
    Detect Rectangles, input should be a Stroke that has already been
    simplified.
    """
    
    #TODO: support strokes that do not have a length of 5
    if (not isinstance(stroke, Stroke) or len(stroke.coordList) != 5 or 
            stroke.coordList[-1] != stroke.coordList[0] or
            len(stroke.coordList[1]) != 2):
        return stroke
    
    coords = stroke.coordList

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
            inplace_map(detectRectangle, layer.itemList)
            inplace_map(detectCircle, layer.itemList)
            inplace_map(detectEllipse, layer.itemList)

def inplace_map(function, iterable):
    """Similar to pythons map() builtin, but it works in-place."""
    for i, item in enumerate(iterable):
        iterable[i] = function(item)
