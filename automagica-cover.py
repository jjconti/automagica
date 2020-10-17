#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://en.wikibooks.org/wiki/LaTeX/Colors

from __future__ import division, print_function, unicode_literals


import argparse
import os
import sys

from pdf import generate_pdf
from template import latex_env
from utils import filepath


def add_color(value, colors):
    color_name = 'color_{}'.format(len(colors))
    colors.append('\definecolor{{{}}}{}'.format(color_name, value))
    return color_name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--BASE_FILENAME', default='tapa', metavar="Nombre base de los archivos generados")
    parser.add_argument('book_path', help='Carpeta dónde se genera la salida.', metavar='Carpeta', default='ejemplo')
    parser.add_argument('--TITLE', default='Xolopes', metavar="Título")
    parser.add_argument('--AUTHOR', default='Juanjo Conti', metavar="Autor")
    parser.add_argument('--COVER_WIDTH', default='12cm', help="Ancho de la tapa. Ej: 12cm.")
    parser.add_argument('--COVER_HEIGHT', default='20cm', help="Ancho del lomo. Ej: 20cm.")
    parser.add_argument('--SPINE_WIDTH', default='7mm', help="Ancho del lomo. Ej: 10mm.")
    parser.add_argument('--SPINE_INTERTEXT_SPACE', default='2cm', help="Separación en el lomo. Ej: cmm.")
    parser.add_argument('--TITLE_COLOR', default='{RGB}{176,216,241}', help='Color del título y el nombre del autor.')
    parser.add_argument('--TITLE_VSPACE', default='20mm', help="Espacio vertical antes del título. Ej: 20mm.",
                        metavar='Espacio vertical título')
    parser.add_argument('--AUTHOR_VSPACE', default='20mm', help="Espacio vertical antes del nombre del autor. Ej: 20mm.",
                        metavar='Espacio vertical autor')
    parser.add_argument('--COVER_COLOR', default='black', help="Color de fondo de la tapa.")
    parser.add_argument('--IMAGE_WIDTH', default='8cm', help="Ancho de la imagen de tapa. Ej: 8cm.",
                        metavar='Ancho de la imagen')
    parser.add_argument('--IMAGE_PATH', help='Imagen de tapa.', metavar='Imagen', default='ejemplo/imagen.jpg')
    parser.add_argument('--LOGO_WIDTH', default='3cm', help="Ancho del logo de la editorial. Ej: 4cm.",
                        metavar='Ancho del logo')
    parser.add_argument('--LOGO_PATH', help='Logo de la editorial.', metavar='Logo',default='cover/figures/automagica-celeste.png')
    parser.add_argument('--SPINE_LOGO_PATH', help='Logo de la editorial para el lomo.', metavar='Logo en lomo', default='cover/figures/logo-celeste.png')
    parser.add_argument('--SPINE_LOGO_WIDTH', help='Ancho del logo de la editorial para el lomo.', default='3mm')
    parser.add_argument('--IMAGE_VSPACE', default='90mm', help="Espacio vertical antes de la imagen de tapa. Ej: 90mm.",
                        metavar='Espacio vertical imagen')
    parser.add_argument('--BACK_TEXT', help='Texto de la contratapa.', metavar='Contratapa', default='ejemplo/contratapa.txt')
    parser.add_argument('--BACK_TEXT_COLOR', default='{RGB}{176,216,241}', help='Color del texto de la contratapa.')
    parser.add_argument('--BACK_VSPACE', default='20mm', help="Espacio vertical antes del texto de contratapa. Ej: 20mm.",
                        metavar='Espacio vertical contratapa')
    args = parser.parse_args()
    book_path = args.book_path

    VARS = {}
    if args.BACK_TEXT:
        with open(args.BACK_TEXT, 'r') as back_text_file:
            VARS['BACK_TEXT'] = back_text_file.read()
    else:
        VARS['BACK_TEXT'] = ''
    new_colors = []
    for k, v in args._get_kwargs():
        if not VARS.get(k):
            VARS[k] = v
            if v:
                if v.startswith('{gray}') or v.startswith('{rgb}') or v.startswith('{RGB}')or v.startswith('{HTML}') or v.startswith('{cmyk}'):
                    VARS[k] = add_color(v, new_colors)


    VARS['DEFINED_COLORS'] = '\n'.join(new_colors)

    TEMPLATE = os.path.join('cover', 'cover_template.tex')

    template = latex_env.get_template(TEMPLATE)

    base_filename = VARS['BASE_FILENAME']
    VARS['DESCRIPTION'] = VARS['BASE_FILENAME'].title()
    tex_file = filepath(book_path, base_filename, 'tex')

    with open(tex_file, 'w') as f:
        f.write(template.render(**VARS))

    generate_pdf(book_path, base_filename, tex_file)

if __name__ == '__main__':
    main()