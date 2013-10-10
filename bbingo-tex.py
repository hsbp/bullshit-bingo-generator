#!/usr/bin/env python

import requests
from lxml import etree
from random import shuffle

LATEX_HEADER = r"""
\documentclass[a4paper,9pt]{article}

\sloppy
\frenchspacing

\usepackage[left=0.5cm,top=0.5cm,right=0.5cm,bottom=2cm,nohead,nofoot]{geometry}
\usepackage[utf8x]{inputenc}
\usepackage{default}
\usepackage{tabulary}
\usepackage{libertine}
\usepackage{multicol}
\usepackage[english]{babel}
\usepackage[
  unicode=true,
  colorlinks=false,
  pdfborder={0 0 0 0},
  pdfauthor={H.A.C.K.},
  pdftitle={Buzzword Bingo}
]{hyperref}

\pagestyle{empty}
\renewcommand*\familydefault{\sfdefault}

\newcommand{\nullword}{\hspace{0pt}\ignorespaces}
\hyphenation{app-li-ca-ti-on}

\begin{document}
\begin{multicols}{2}
"""

tree = etree.HTML(requests.get('http://hsbp.org/hacktivity2013').content)
buzzwords = [s.strip() for s in tree.xpath('//h2[@id="buzzword_bullshit_bingo_for_product_demos_"]/following-sibling::ul/li/text()')]

def draw_single_table(words):
	shuffle(words)
	table = words[:24]
	table.insert(12, "\\textbf{BULLSHIT BINGO}\n\n\\footnotesize{(free square)}")
	retval = ['\\vbox{\\begin{center}\\textbf{Bullshit bingo provided by Hackerspace Budapest}\\end{center}\n\\noindent\nCheck off each block when you hear these words during the product demo. When you get five blocks horizontally, vertically, or diagonally, stand up and shout ``BULLSHIT!\'\'. (Drinking game: for every block, take a sip, and finish your drink for five blocks in a row.)\n\n\\medskip\n\\noindent\n\\begin{tabular}{ |m{0.152\columnwidth}|m{0.152\columnwidth}|m{0.152\columnwidth}|m{0.152\columnwidth}|m{0.152\columnwidth}| }\n\\hline\n\\begin{center}\\nullword ']
	retval.extend('\\end{center}\\\\\n\\hline\n\\begin{center}\\nullword '.join(
		r'\end{center} & \begin{center}\nullword '.join(table[row * 5:(row + 1) * 5]) for row in xrange(5)))
	retval.append('\\end{center}\\\\\n\hline\n\end{tabular}}\n\n')
	return ''.join(retval)

print LATEX_HEADER
for _ in xrange(60):
	print draw_single_table(buzzwords)
print '\\end{multicols}\n\\end{document}'
