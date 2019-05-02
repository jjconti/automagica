#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://en.wikibooks.org/wiki/LaTeX/Colors

from __future__ import division, print_function, unicode_literals

import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")

import glob
import os
import sys

from pdf import generate_pdf
from template import latex_env
from utils import filepath, latex_single

import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")
from gooey import Gooey, GooeyParser

reload(sys)
sys.setdefaultencoding('utf8')


def add_color(value, colors):
    color_name = 'color_{}'.format(len(colors))
    colors.append('\definecolor{{{}}}{}'.format(color_name, value))
    return color_name


@Gooey(program_name="Automágica newspaper", program_description="Generá un diario listo para imprimir", language='spanish',
       image_dir='images',  default_size=(810, 570))
def main():
    parser = GooeyParser()
    parser.add_argument('--BASE_FILENAME', default='diario', metavar="Nombre base de los archivos generados")
    parser.add_argument('book_path', help='Carpeta dónde se genera la salida.', metavar='Carpeta', widget='DirChooser'
                        ,default='/Users/juanjo/automagica/trabajos/ies/')
    parser.add_argument('--COLUMNS', default='3', metavar="Columnas")
    parser.add_argument('--TITLE', default='Diario', metavar="Título")
    parser.add_argument('--CITY', default='Santa Fe, Argentina', metavar="City")
    parser.add_argument('--PRICE', default='Distrib. Gratuita', help="Precio del diario")
    parser.add_argument('--VOLUME', default='1', help="Volumen del diario.")
    parser.add_argument('--ISSUE', default='1', help="Número del diario.")
    parser.add_argument('--SLOGAN', default='Noticias del instituto y su comunidad', help='Slogan del diario.')
    parser.add_argument('--DATE', default='FECHA', help="Fecha del diario.")

    args = parser.parse_args()
    book_path = args.book_path

    VARS = {}
    for k, v in args._get_kwargs():
        if not VARS.get(k):
            VARS[k] = v

    text_files = [f for f in glob.glob(os.path.join(book_path, '*.txt')) if not f.endswith('words.txt')]
    if text_files:
        VARS['CONTENT'] = latex_single(text_files[0], True)

    TEMPLATE = os.path.join('newspaper', 'newspaper_template.tex')

    template = latex_env.get_template(TEMPLATE)

    base_filename = VARS['BASE_FILENAME']
    tex_file = filepath(book_path, base_filename, 'tex')

    with open(tex_file, 'w') as f:
        f.write(template.render(**VARS))

    generate_pdf(book_path, base_filename, tex_file)

if __name__ == '__main__':
    main()