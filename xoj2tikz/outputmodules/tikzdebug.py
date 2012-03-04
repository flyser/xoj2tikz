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

from .tikzlinewidth import TikzLineWidth

class TikzDebug(TikzLineWidth):
    """An output module that supports lines with variable width."""
    @staticmethod
    def name():
        """
        Return the name of this output module, this can be presented to the user.
        """
        return "variable line width with debugging"

    def stroke(self, stroke):
        """
        After writing a stroke to the output file, also draw dots at every
        coordinate used to construct the stroke.
        """
        super(TikzDebug, self).stroke(stroke)
        
        if len(stroke.coordList[0]) == 3:
            for x, y, w in stroke.coordList:
                self.write("  \\draw[red, line width=1pt] ({}, {}) -- cycle;\n"
                           .format(x, y))
        elif len(stroke.coordList[0]) == 2:
            for x, y in stroke.coordList:
                self.write("  \\draw[red, line width=1pt] ({}, {}) -- cycle;\n"
                           .format(x, y))
