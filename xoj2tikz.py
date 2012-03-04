#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# xoj2tikz: Converts Xournal .xoj files to TikZ.
# Copyright (C) 2012 Fabian Henze
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import gzip

from xml.etree.ElementTree import XMLParser

from xoj2tikz.xournalparser import XournalParser
from xoj2tikz.outputmodules.tikzlinewidth import TikzLineWidth
from xoj2tikz.outputmodules.tikzdebug import TikzDebug
from xoj2tikz import optimizations

DEBUG = False
VERSION = "0.1"

def main():
    #TODO: use argparse
    if (len(sys.argv) < 2):
        print("Usage: "+sys.argv[0]+" filename.xoj", file=sys.stderr)
        sys.exit(1)
    
    xojFile = gzip.open(sys.argv[1])
    document = xojFile.read()

    parser = XMLParser(target=XournalParser())
    parser.feed(document)
    document = parser.close()
    
    optimizations.runAll(document)
    
    if DEBUG:
        output = TikzDebug(document, output=sys.stdout)
    else:
        output = TikzLineWidth(document, output=sys.stdout)
    output.printAll()

if __name__ == "__main__":
    sys.exit(main())
