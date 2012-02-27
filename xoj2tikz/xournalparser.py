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
import re
from copy import copy

from .page import Page
from .layer import Layer
from .stroke import Stroke
from .textbox import TextBox

class XournalParser:
    """
    A parser for Xournal files implementing the ElementTree.XMLParser
    interface.
    """
    def __init__(self):
        """Constructor"""
        self.document = []
        self.currentPage = None
        self.currentLayer = None
        self.currentItem = None
        self.workWidthList = []
        self.workCoordList = []
    
    @staticmethod
    def getColor(code, defaultOpacity=1.0):
        """
        Parse a xournal color name and return a tuple of four: (r,g,b,opacity)

        Keyword arguments:
        code -- The color string to parse (mandatory)
        defaultOpacity -- If 'code' does not contain opacity information, use
                          this. (default 1.0)
        """
        regex = re.compile(r"#([0-9a-fA-F]{2})([0-9a-fA-F]{2})"
                            r"([0-9a-fA-F]{2})([0-9a-fA-F]{2})")
        if code == "black":
            r, g, b = (0, 0, 0)
            opacity = defaultOpacity
        elif code == "blue":
            r, g, b = (51, 51, 204)
            opacity = defaultOpacity
        elif code == "red":
            r, g, b = (255, 0, 0)
            opacity = defaultOpacity
        elif code == "green":
            r, g, b = (0, 128, 0)
            opacity = defaultOpacity
        elif code == "gray":
            r, g, b = (128, 128, 128)
            opacity = defaultOpacity
        elif code == "lightblue":
            r, g, b = (0, 192, 255)
            opacity = defaultOpacity
        elif code == "lightgreen":
            r, g, b = (0, 255, 0)
            opacity = defaultOpacity
        elif code == "magenta":
            r, g, b = (255, 0, 255)
            opacity = defaultOpacity
        elif code == "orange":
            r, g, b = (255, 128, 0)
            opacity = defaultOpacity
        elif code == "yellow":
            r, g, b = (255, 255, 0)
            opacity = defaultOpacity
        elif code == "white":
            r, g, b = (255, 255, 255)
            opacity = defaultOpacity
        elif re.match(regex, code):
            r, g, b, opacity = re.match(regex, code).groups()
            r = int(r, 16)
            g = int(g, 16)
            b = int(b, 16)
            opacity = int(opacity, 16)/255.0
        else:
            raise Exception("invalid_color")
        return (r, g, b, opacity)
    
    def start(self, tag, attrib):
        """
        Called for start tags.
        
        Keyword arguments:
        tag -- Name of the XML tag as a string
        attrib -- Attributes of the XML tag as a dictionary
        """
        if tag == "xournal":
            pass
        elif tag == "title":
            pass
        elif tag == "page":
            self.currentPage = Page(width=attrib["width"],
                                    height=attrib["height"])
        elif tag == "background":
            pass
        elif tag == "layer":
            self.currentLayer = Layer()
        elif tag == "stroke":
            self.workWidthList = []
            self.workCoordList = []
            if attrib["tool"] in ("pen", "highlighter", "eraser"):
                self.workWidthList = attrib["width"].split(' ')
                if attrib["tool"] == "highlighter":
                    color = self.getColor(attrib["color"], 0.5)
                else:
                    color = self.getColor(attrib["color"])
                # Xournal files can contain negative line widths
                width = max(0.0, float(self.workWidthList.pop(0)))
                self.currentItem = Stroke(color=color, 
                                          width=width)
            else:
                self.currentItem = None
                print("Warning: Unknown tool '{0}' in stroke, ignoring."
                      .format(attrib["tool"]), file=sys.stderr)
        elif tag == "text":
            self.currentItem = TextBox(
                font  = attrib["font"],
                size  = float(attrib["size"]),
                x     = float(attrib["x"]),
                y     = float(attrib["y"]),
                color = self.getColor(attrib["color"]))
        else:
            print("Warning: Unknown tag '{0}', ignoring.".format(tag),
                  file=sys.stderr)

    def data(self, data):
        """
        Called for character data and expanded character references and entities.
        May be called more than once for each character data section.
        
        Keyword arguments:
        data -- A text string. May be either an 8-bit string containing ASCII data,
                or an Unicode string.
        """
        if isinstance(self.currentItem, Stroke):
            for coord in data.strip().split(' '):
                if len(coord) > 0:
                    self.workCoordList.append(coord)

        elif isinstance(self.currentItem, TextBox):
            self.currentItem.text += data

    def end(self, tag):
        """
        Called for end tags.
        
        Keyword arguments:
        tag -- Name of the XML tag as a string
        """
        if tag == "xournal":
            pass
        elif tag == "title":
            pass
        elif tag == "page":
            self.document.append(copy(self.currentPage))
            del self.currentPage
        elif tag == "background":
            pass
        elif tag == "layer":
            self.currentPage.layerList.append(copy(self.currentLayer))
            del self.currentLayer
        elif tag == "stroke":
            if isinstance(self.currentItem, Stroke):
                for i in range(int(len(self.workCoordList)/2)):
                    x = float(self.workCoordList[2*i])
                    y = float(self.workCoordList[2*i+1])
                    if len(self.workWidthList) > 0:
                        width = max(0.0, float(self.workWidthList[i-1]))
                        self.currentItem.coordList.append([x, y, width])
                    else:
                        self.currentItem.coordList.append([x, y])
                self.currentLayer.itemList.append(copy(self.currentItem))
            self.currentItem = None
            del self.workWidthList
            del self.workCoordList
        elif tag == "text":
            if isinstance(self.currentItem, TextBox):
                self.currentLayer.itemList.append(copy(self.currentItem))
            self.currentItem = None

        else:
            pass
          
    def close(self):
        """
        Called when the parser is done.
        
        The return value is a list of 'Page' objects.
        """
        return self.document
