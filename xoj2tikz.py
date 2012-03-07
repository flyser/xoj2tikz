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
import argparse

from xml.etree.ElementTree import XMLParser

from xojtools import XournalParser, optimizations
from xojtools import outputmodules as Output

DEBUG = False
VERSION = "0.3-pre"

class CmdlineParser():
    """
    Parse commandline options. Results are available as attributes of this class
    """
    def __init__(self):
        self.inputfile = None
        self.optimize = True
        self.outputfile = sys.stdout
        
    def parse(self):
        """
        Parse commandline options.
        """
        parser = argparse.ArgumentParser(
                    description="Converts Xournal .xoj files to TikZ.",
                    epilog="e.g.: %(prog)s input.xoj -o output.tikz")
        parser.add_argument("input", help=".xoj input file")
        parser.add_argument("-o", "--output", nargs=1, default=[sys.stdout],
                                help="TikZ output file")
        parser.add_argument("-n", "--dont-optimize", dest="optimize",
                            action="store_false",
                            help="Don't optimize the tikz output at all")
        parser.add_argument("-v", "--version", action="version",
                            version="%(prog)s " + VERSION)
        args = parser.parse_args()
        
        if args.input == "-":
            self.inputfile = sys.stdin
        else:
            try:
                self.inputfile = gzip.open(args.input)
            except IOError as err:
                print("Failed to open input file '{}':\n  {}"
                      .format(args.input, err.strerror))
                sys.exit(1)
                
        
        if args.output[0] == sys.stdout or args.output[0] == "-":
            self.outputfile = sys.stdout
        else:
            try:
                self.outputfile = open(args.output[0], 'w')
            except IOError as err:
                print("Failed to open output file '{}':\n  {}"
                      .format(args.output[0], err.strerror))
                sys.exit(1)
        
        self.optimize = args.optimize
        return self


def main():
    """
    Convert a .xoj file to tikz.
    
    1. Parse commandline arguments and get input and output file
    2. Read inputfile
    3. Parse the input file with a XML parser and store the document in memory
    4. Optimize/Simplify internal representation of the xournal document
    5. Convert the internal representation to TikZ code and write the output
       file
    """
    args = CmdlineParser().parse()
    inputData = args.inputfile.read()

    parser = XMLParser(target=XournalParser())
    parser.feed(inputData)
    document = parser.close()
    
    if args.optimize:
        optimizations.runAll(document)
    
    if DEBUG:
        output = Output.TikzDebug(document, output=args.outputfile)
    else:
        output = Output.TikzLineWidth(document, output=args.outputfile)
    output.printAll()
    
    if args.outputfile is not sys.stdout and not args.outputfile.isatty():
        args.outputfile.close()
    if args.inputfile is not sys.stdin and not args.inputfile.isatty():
        args.inputfile.close()

if __name__ == "__main__":
    sys.exit(main())
