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

from ..outputmodule import OutputModule, COLOR_PREFIX

class TikzLineWidth(OutputModule):
    """An output module that supports lines with variable width."""
    @staticmethod
    def name():
        """
        Return the name of this output module, this can be presented to the user.
        """
        return "variable line width"

    def header(self):
        """
        Open a tikzpicture environment and define a style for variable width
        lines.
        """
        colorList = []
        newline = ""
        self.write(\
"""\\tikzset{
  vlw/.style={
    to path={%
      \pgfextra{%
        \draw[#1,line width=\pgfkeysvalueof{/tikz/t}] (\\tikztostart) -- (\\tikztotarget);
      }%
      (\\tikztotarget)
    },
  },
  t/.initial=0.4pt,
}
\\begin{tikzpicture}[yscale=-1, y=1pt, x=1pt, every path/.style={line cap=round, line join=round}]\n""")
        for page in self.document:
            for layer in page.layerList:
                for item in layer.itemList:
                    texColor = self.toTexColor(item.color)
                    if texColor not in colorList and texColor.startswith(COLOR_PREFIX):
                        r = item.color[0]/255.0
                        g = item.color[1]/255.0
                        b = item.color[2]/255.0
                        self.write("  \\definecolor{{{}}}{{rgb}}{{{:.4},{:.4},"
                                   "{:.4}}}\n".format(self.toTexColor(item.color),
                                                      r, g, b))
                        colorList.append(self.toTexColor(item.color))
                        newline = '\n'
        self.write(newline)


    def stroke(self, stroke):
        """
        Write a stroke in the output file.
        
        The output will look similar to this:
          \draw[vlw=color] (x1,y1) to[t=width1] (x2,y2) to[t=width2] ... ;
        or
          \draw[color,line width=1pt,opacity=0.555] (x1,y1) -- (x2,y2) -- ... ;
        """
        texColor = self.toTexColor(stroke.color)
        opacity = stroke.color[3]
        firstX = stroke.coordList[0][0]
        firstY = stroke.coordList[0][1]
        coordList = stroke.coordList[1:]
        width = stroke.width
        
        self.write("  \\draw[")
        if len(coordList[0]) == 3:
            # Stroke has variable width:
            if opacity == 1.0:
                self.write("vlw={}".format(texColor))
            else:
                self.write("vlw={{{},opacity={:.3}}}".format(texColor,
                                                              opacity))
            self.write("] ({}, {})".format(firstX, firstY))
            for x, y, width in coordList:
                self.write(" to[t={}pt] ({}, {})".format(width, x, y))
        else:
            # Stroke has fixed width:
            self.write("{},line width={}pt".format(texColor, width))
            if opacity != 1.0:
                self.write(",opacity={:.3}".format(opacity))
            self.write("] ({}, {})".format(firstX, firstY))
            
            for x, y in coordList[:-1]:
                self.write(" -- ({}, {})".format(x, y))
            
            # If a stroke is closed, end it with "-- cycle".
            lastX = coordList[-1][0]
            lastY = coordList[-1][1]
            if firstX == lastX and firstY == lastY:
                self.write(" -- cycle")
            else:
                self.write(" -- ({}, {})".format(lastX, lastY))
        self.write(";\n")
        
    def textbox(self, textbox):
        """
        Write a text box in the output file.
        
        The output will look similar to this:
          \node[align=left, below right, inner sep=0pt] at (x,y) {multi\\line};
        """
        coordX = textbox.x
        coordY = textbox.y + 2.5  # shift down by 2.5pt to match Xournals output
        texColor = self.toTexColor(textbox.color)
        opacity = textbox.color[3]
        text = textbox.text.replace('\n', "\\\\")

        self.write("  \\node[align=left, below right, inner sep=0pt")
        if texColor != "black":
            self.write("," + texColor)
        if opacity != 1.0:
            self.write(",opacity={:.3}".format(opacity))
        self.write("] at ({},{}) {{{}}};\n".format(coordX, coordY, text))

    def circle(self, circle):
        """
        Write a circle in the output file.
        
        The output will look similar to this:
          \draw[line width=width, color, opacity=0.5] (x,y) circle (radius);
        """
        coordX = circle.x
        coordY = circle.y
        width = circle.width
        texColor = self.toTexColor(circle.color)
        opacity = circle.color[3]
        radius = circle.radius

        self.write("  \\draw[line width={}pt".format(width))
        if texColor != "black":
            self.write("," + texColor)
        if opacity != 1.0:
            self.write(",opacity={:.3}".format(opacity))
        self.write("] ({},{}) circle ({});\n".format(coordX, coordY, radius))

    def rectangle(self, rect):
        """
        Write a rectangle in the output file.
        
        The output will look similar to this:
          \draw[line width=width, color, opacity=0.5] (x1,y1) rectangle (x2,y2);
        """
        firstX = rect.x1
        firstY = rect.y1
        secondX = rect.x2
        secondY = rect.y2
        width = rect.width
        texColor = self.toTexColor(rect.color)
        opacity = rect.color[3]

        self.write("  \\draw[line width={}pt".format(width))
        if texColor != "black":
            self.write("," + texColor)
        if opacity != 1.0:
            self.write(",opacity={:.3}".format(opacity))
        self.write("] ({},{}) rectangle ({},{});\n".format(firstX, firstY,
                                                           secondX, secondY))

    def footer(self):
        """Close the tikzpicture environment."""
        self.write("\\end{tikzpicture}\n")
