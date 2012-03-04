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

from .stroke import Stroke
from .textbox import TextBox
from .rectangle import Rectangle
from .circle import Circle

COLOR_PREFIX = "xou"

class OutputModule:
    """
    Abstract class for output classes.
    
    Subclasses should implement at least:
     * name()
     * header()
     * stroke()
     * textbox()
     * footer()
    and optionally:
     * page()
     * layer()
    """
    @staticmethod
    def name():
        """
        Return the name of the output module, this can be presented to the user.
        """
        raise NotImplementedError
        
    def __init__(self, document, output=sys.stdout):
        """
        Constructor
        
        Keyword arguments:
        document -- List of 'Page' objects (default [])
        output -- Where to write the TikZ code to (default sys.stdout)
        """
        self.output = output
        self.document = document
        self.currentPage = None
        self.currentLayer = None
    
    @staticmethod
    def toTexColor(tup):
        """
        Convert a color to an unique string for use in a TeX document.

        Keyword arguments:
        tup -- Tuple of (red, green, blue, opacity)
        """
        (r, g, b, o) = tup
        if (r, g, b) == (0, 0, 0):
            return "black"
        elif (r, g, b) == (255, 255, 255):
            return "white"
        elif (r, g, b) == (255, 0, 0):
            return "red"
        elif (r, g, b) == (0, 255, 0):
            return "green"
        elif (r, g, b) == (0, 0, 255):
            return "blue"
        elif (r, g, b) == (0, 173, 239):
            return "cyan"
        elif (r, g, b) == (236, 0, 140):
            return "magenta"
        elif (r, g, b) == (255, 242, 0):
            return "yellow"
        else:
            return "{}{:02x}{:02x}{:02x}".format(COLOR_PREFIX, r, g, b)
      
    def write(self, value):
        """print() wrapper function. Writes the value to output file."""
        print(value, file=self.output, end="")
        
    def errorMsg(self, value):
        """
        print() wrapper function. Writes value as a LaTeX comment, if the
        output is a terminal, else to stderr.
        """
        if self.output.isatty() or self.output == sys.stderr:
            print("% " + value, file=sys.stderr)
        else:
            print(value, file=sys.stderr)
      
    def printAll(self):
        """Write the header, body and footer of the output file."""
        self.header()
        self.body()
        self.footer()

    def header(self):
        """
        Write the header of the output file.
        
        Override this, if you want to write an output module.
        """
        pass
      
    def body(self):
        """
        Write the body of the output file, by iterating over all pages and
        print them.
        
        You may optionally override this function, if you want to write an
        output module.
        """
        for page in self.document:
            self.page(page)
            
    def page(self, page):
        """
        Write a Page to the output file, by iterating over all its layers and
        printing them.
        
        You may optionally override this function, if you want to write an
        output module.
        """
        self.currentPage = page
        for layer in page.layerList:
            self.layer(layer)
            
    def layer(self, layer):
        """
        Write a Layer to the output file, by iterating over all its items and
        print them.
        
        You may optionally override this function, if you want to write an
        output module.
        """
        self.currentLayer = layer
        for item in layer.itemList:
            if isinstance(item, Stroke):
                self.stroke(item)
            elif isinstance(item, TextBox):
                self.textbox(item)
            elif isinstance(item, Circle):
                self.circle(item)
            elif isinstance(item, Rectangle):
                self.rectangle(item)
            else:
                self.errorMsg("Warning: Unknown Object in itemList of {} on {}"
                              .format(layer, self.currentPage))
        
    def stroke(self, stroke):
        """
        Write a stroke in the output file.
        
        Override this, if you want to write an output module.
        """
        pass

    def textbox(self, textbox):
        """
        Write a text box in the output file.
        
        Override this, if you want to write an output module.
        """
        pass

    def circle(self, circle):
        """
        Write a circle in the output file.
        
        Override this, if you want to write an output module.
        """
        pass
      
    def rectangle(self, rect):
        """
        Write a rectangle in the output file.
        
        Override this, if you want to write an output module.
        """
        pass

    def footer(self):
        """
        Write a footer in the output file.
        
        Override this, if you want to write an output module.
        """
        pass
