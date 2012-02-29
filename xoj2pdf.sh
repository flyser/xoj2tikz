#!/bin/sh
# xoj2pdf.sh -- converts a .xoj file to a pdf using latexmk and pdflatex
set -i

TEMPFILE="$(mktemp --tmpdir=/tmp xoj2pdf-XXXXXXXX.tex)"

cd "$(dirname "$0")"
WORKDIR="$(pwd)"

cat << EOF > "${TEMPFILE}"
\documentclass[12pt]{article}
\usepackage[ngerman]{babel}
\usepackage[utf8]{inputenc}
\usepackage{cmap}
\usepackage[T1]{fontenc}
\usepackage{tikz}
\usepackage{pgf}
\usepackage[active,pdftex,tightpage]{preview}
\PreviewEnvironment[]{tikzpicture}
\PreviewEnvironment[]{pgfpicture}
\begin{document}
EOF

./xoj2tikz.py "$1" >> "${TEMPFILE}" || exit 1

echo "\\end{document}" >> "${TEMPFILE}"

cd "$(dirname "$TEMPFILE")"

latexmk -f -silent -pdf "$TEMPFILE" >/dev/null
if which rubber-info >/dev/null; then
  echo
  rubber-info "${TEMPFILE%.tex}.log"
  echo
fi
latexmk -c "$TEMPFILE" &>/dev/null
rm "$TEMPFILE"
mv -v "${TEMPFILE%.tex}.pdf" "${WORKDIR}/${1%.xoj}.pdf"
