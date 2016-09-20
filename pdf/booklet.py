#!/usr/bin/env python

"""
usage:   booklet.py my.pdf

Creates booklet.my.pdf

Pages organized in a form suitable for booklet printing, e.g.
to print 4 8.5x11 pages using a single 11x17 sheet (double-sided).

From https://github.com/pmaupin/pdfrw/blob/master/examples/booklet.py
"""

import sys
import os

from pdfrw import PdfReader, PdfWriter, PageMerge

from utils import show_file


def fixpage(*pages):
    result = PageMerge() + (x for x in pages if x is not None)
    result[-1].x += result[0].w
    return result.render()


def generate_booklet(input_file, output_file):
    ipages = PdfReader(input_file).pages

    # Make sure we have 4*n pages
    while len(ipages) & 4:
        ipages.append(None)

    opages = []
    while len(ipages) > 2:
        opages.append(fixpage(ipages.pop(), ipages.pop(0)))
        opages.append(fixpage(ipages.pop(0), ipages.pop()))

    opages += ipages

    PdfWriter().addpages(opages).write(output_file)
    show_file(output_file)

if __name__ == '__main__':
    inpfn, = sys.argv[1:]
    outfn = 'booklet.' + os.path.basename(inpfn)
    generate_booklet(inpfn, outfn)
