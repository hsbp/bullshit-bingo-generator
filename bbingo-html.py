#!/usr/bin/env python

import requests
from lxml import etree
from random import shuffle

HTML_HEADER = """
<html>
<head>
<title>Buzzword Bingo</title>
<style>
	body, td {
		font-family: sans-serif;
		font-size: 8pt;
	}
	td {
		font-weight: bold;
		width: 1.5cm;
		height: 1.5cm;
		text-align: center;
		border: 1pt solid black;
		padding: 2pt;
	}
	table {
		border: 2pt solid black;
		border-collapse:collapse;
		margin: 6pt;
		float: left;
	}
</style>
</head>
<body>
"""

tree = etree.HTML(requests.get('http://hsbp.org/hacktivity2013').content)
buzzwords = [s.strip() for s in tree.xpath('//h2[@id="buzzword_bullshit_bingo_for_product_demos_"]/following-sibling::ul/li/text()')]

def draw_single_table(words):
	shuffle(words)
	table = words[:24]
	table.insert(12, "BULLSHIT BINGO<br />(free square)")
	retval = ['<table><td colspan="5">Bullshit bingo provided by Hackerspace Budapest (hsbp.org)<br /><br />Check off each block when you hear these words during the product demo. When you get five blocks horizontally, vertically, or diagonally, stand up and shout "BULLSHIT!!!". Or play as a drinking game and for every block you mark off, take a sip, and finish your drink each time you get five blocks in a row.</td></tr><tr><td>']
	retval.extend('</td></tr><tr><td>'.join('</td><td>'.join(table[row * 5:(row + 1) * 5]) for row in xrange(5)))
	retval.append('</td></tr></table>')
	return ''.join(retval)

print HTML_HEADER
for _ in xrange(5):
	print draw_single_table(buzzwords)
print '</body></html>'
