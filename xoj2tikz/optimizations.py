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

import sys

from .page import Page
from .layer import Layer
from .stroke import Stroke
from .textbox import TextBox
from .rectangle import Rectangle
from .circle import Circle

"""
This is a collection of functions to simplify Strokes and detect shapes to
improve the quality of the output file.
"""

def detectCircle(stroke):
    pass

def detectRectangle(stroke):
    pass

def simplifyStrokes(stroke):
    pass


def runAll(obj):
    """
    This is a recursive function. You can throw any list or instance of
    Page, Layer, Stroke and so on at it and it will run all optimization
    algorithms on it.
    """
    if isinstance(obj, list):
        for item in obj:
            runAll(item)
    elif isinstance(obj, Page):
        runAll(obj.layerList)
    elif isinstance(obj, Layer):
        runAll(obj.itemList)
    elif isinstance(obj, Stroke):
        detectCircle(obj)
        detectRectangle(obj)
        simplifyStrokes(obj)
    elif isinstance(obj, TextBox):
        pass
    elif isinstance(obj, Rectangle):
        pass
    elif isinstance(obj, Circle):
        pass
    else:
        print("Warning: Unknown Type, not optimizing", file=sys.stderr)
