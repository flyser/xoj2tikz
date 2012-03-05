xoj2tikz converts Xournal .xoj files to TikZ code for use in LaTeX documents.

## Usage ##

    xoj2tikz.py inputfile [-n] [-o OUTPUT]

For an explanation of all options see:

    xoj2tikz.py --help

    
## Feature List ##

 * Basic strokes: **YES**
 * Pressure sensitivity: **YES**
 * Text: **YES** (It ignores the font you selected in Xournal, but otherwise its
   fine)
 * Eraser: **YES**
 * Highlighter: **YES**
 * Colours: **YES**
 * Multi-page Xournal files: **NO** (good candidate for a major release ;-))
 * Background: **NO** (and no plans either ... maybe one day. or if someone has
   a patch for that)
 * Embedded PDFs: **NO** (not really the purpose of this tool. It might be
   possible to build a tool based on xoj2tikz to do that)

## I really ran out of ideas ... ##

... while writing this readme. If you come up with something that should
totally be explained here, please raise your voice.
