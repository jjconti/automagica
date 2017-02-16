#!/usr/bin/env python
# -*- coding: utf-8 -*-

# https://en.wikibooks.org/wiki/LaTeX/Colors

from __future__ import division, print_function, unicode_literals

import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")

import os
import sys

from pdf import generate_pdf
from template import latex_env
from utils import filepath

import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")
from gooey import Gooey, GooeyParser

reload(sys)
sys.setdefaultencoding('utf8')


def add_color(value, colors):
    color_name = 'color_{}'.format(len(colors))
    colors.append('\definecolor{{{}}}{}'.format(color_name, value))
    return color_name


@Gooey(program_name="Automágica covers", program_description="Generá tapas listas para imprimir", language='spanish',
       image_dir='images',  default_size=(810, 570))
def main():
    parser = GooeyParser()
    parser.add_argument('--BASE_FILENAME', default='tapa', metavar="Nombre base de los archivos generados")
    parser.add_argument('book_path', help='Carpeta dónde se genera la salida.', metavar='Carpeta', widget='DirChooser'


                        ,default='/Users/juanjo/automagica/xolopes')
    parser.add_argument('--TITLE', default='TÍTULO', metavar="Título")
    parser.add_argument('--AUTHOR', default='AUTOR', metavar="Autor")
    parser.add_argument('--COVER_WIDTH', default='12cm', help="Ancho del lomo. Ej: 12cm.")
    parser.add_argument('--COVER_HEIGHT', default='20cm', help="Ancho del lomo. Ej: 20cm.")
    parser.add_argument('--SPINE_WIDTH', default='10mm', help="Ancho del lomo. Ej: 10mm.")
    parser.add_argument('--SPINE_INTERTEXT_SPACE', default='2cm', help="Separación en el lomo. Ej: cmm.")
    parser.add_argument('--TITLE_COLOR', default='yellow', help='Color del título y el nombre del autor.')
    parser.add_argument('--TITLE_VSPACE', default='20mm', help="Espacio vertical antes del título. Ej: 20mm.",
                        metavar='Espacio vertical título')
    parser.add_argument('--AUTHOR_VSPACE', default='20mm', help="Espacio vertical antes del nombre del autor. Ej: 20mm.",
                        metavar='Espacio vertical autor')
    parser.add_argument('--COVER_COLOR', default='red', help="Color de fondo de la tapa.")
    parser.add_argument('--IMAGE_WIDTH', default='8cm', help="Ancho de la imagen de tapa. Ej: 8cm.",
                        metavar='Ancho de la imagen')
    parser.add_argument('--IMAGE_PATH', help='Imagen de tapa.', metavar='Imagen', widget='FileChooser'

                        ,default='/Users/juanjo/automagica/cover/figures/tigrebyn.png')
    parser.add_argument('--IMAGE_VSPACE', default='90mm', help="Espacio vertical antes de la imagen de tapa. Ej: 90mm.",
                        metavar='Espacio vertical imagen')
    parser.add_argument('--BACK_TEXT', help='Texto de la contratapa.', metavar='Contratapa',
                        widget='FileChooser'

                        ,default='/Users/juanjo/automagica/xolopes/contratapa.txt')
    parser.add_argument('--BACK_TEXT_COLOR', default='black', help='Color del texto de la contratapa.')
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
        if not VARS.get(k)  :
            if v.startswith('{gray}') or v.startswith('{rgb}') or v.startswith('{RGB}')or v.startswith('{HTML}') or v.startswith('{cmyk}'):
                VARS[k] = add_color(v, new_colors)
            else:
                VARS[k] = v

    VARS['DEFINED_COLORS'] = '\n'.join(new_colors)

    TEMPLATE = os.path.join('cover', 'cover_template.tex')

    template = latex_env.get_template(TEMPLATE)

    base_filename = VARS['BASE_FILENAME']
    tex_file = filepath(book_path, base_filename, 'tex')

    with open(tex_file, 'w') as f:
        f.write(template.render(**VARS))

    generate_pdf(book_path, base_filename, tex_file)

if __name__ == '__main__':
    main()