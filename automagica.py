#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import site; site.addsitedir("/usr/local/lib/python2.7/site-packages")

import imp
import glob
import os
import sys
from datetime import datetime

from epub import generate_epub
from pdf import generate_pdf
from pdf.booklet import generate_booklet
from template import latex_env
from utils import filepath, latex_hyphenation, latex_chapter, latex_single, show_file

try:
    from gooey import Gooey, GooeyParser
except ImportError:
    # cat exceptin in travis-ci
    # gui not used when running tests
    pass

reload(sys)
sys.setdefaultencoding('utf8')

DEFAULTS = dict(
    HYPHENATION='',
    CONTENT='',
)


@Gooey(program_name="Automágica", program_description="Generá libros listos para imprimir en base a tus originales",
       language='spanish', image_dir='images',  default_size=(810, 570))
def main():
    parser = GooeyParser()
    parser.add_argument('--BASE_FILENAME', default='libro', metavar="Nombre base de los archivos generados")
    parser.add_argument('book_path', help='Carpeta con archivos para un libro y dónde se genera la salida.',
                        metavar='Carpeta', widget='DirChooser')
    parser.add_argument('--no-split', help='No separar párrafos.', action='store_true',)
    parser.add_argument('--pdf', help='Genera la versión pdf del libro.', action='store_true')
    parser.add_argument('--booklet', help='Genera la versión booklet del pdf.', action='store_true')
    parser.add_argument('--epub', help='Genera la versión epub del libro.', action='store_true')
    parser.add_argument('--only-tex', help='Solo genera el archivo latex.', action='store_true')
    parser.add_argument('--sections', help='Usar secciones en lugar de capítulos como elemento principal.', action='store_true')
    parser.add_argument('--new-page-before-sections', help='Forzar página nueva en las secciones principales.', action='store_true')
    parser.add_argument('--TITLE', default='TÍTULO', metavar="Título")
    parser.add_argument('--SUBTITLE', default='', metavar="Subtítulo")
    parser.add_argument('--AUTHOR', default='AUTOR', metavar="Autor")
    parser.add_argument('--FONT_SIZE', default=11, metavar="Tamaño de la fuente")
    parser.add_argument('--SPACING', default=1.1, metavar="Interlineado")
    parser.add_argument('--PAGE_SIZE', default='a5paper', metavar="Tamaño de la página")
    parser.add_argument('--YEAR', default=datetime.now().year, metavar="Año")
    parser.add_argument('--URL', default='', metavar="Página web")
    parser.add_argument('--exclude-index', action='store_true', help="No incluir índice.")
    parser.add_argument('--INDEX_TITLE', default='Índice', metavar="Título del índice")
    parser.add_argument('--no-open', help='No intenta abrir el booklet para verlo.', action='store_true')
    args = parser.parse_args()
    book_path = args.book_path

    class EmptyConfig(object):
        pass

    if not os.path.isdir(book_path):
        print('El argumento debe ser un directorio')
        exit()
    config_file = os.path.join(book_path, 'config.py')
    if os.path.isfile(config_file):
        config = imp.load_source('config', config_file)
    else:
        config = EmptyConfig()
        config.CONFIGS = {}

    VARS = DEFAULTS.copy()
    VARS.update(config.CONFIGS)
    for k,v in args._get_kwargs():
        if not VARS.get(k):
            VARS[k] = v

    index_path = os.path.join(book_path, 'index.txt')

    split_paragraphs = not VARS['no_split']
    if os.path.isfile(index_path):
        with open(index_path, 'r') as f:
            content = ''
            for filename in f.readlines():
                if VARS['no_split']:
                    content += latex_chapter(os.path.join(book_path, filename).strip(), split_paragraphs)
                else:
                    content += latex_single(os.path.join(book_path, filename).strip(), split_paragraphs, VARS['sections'], VARS['new_page_before_sections'])
            VARS['CONTENT'] = content
    else:
        text_files = [f for f in glob.glob(os.path.join(book_path, '*.txt')) if not f.endswith('words.txt')]
        if text_files:
            VARS['CONTENT'] = latex_single(text_files[0], split_paragraphs, VARS['sections'], VARS['new_page_before_sections'])

    sep_path = os.path.join(book_path, 'words.txt')
    if os.path.isfile(sep_path):
        with open(sep_path, 'r') as f:
            hyphenation = ''
            for word in f.readlines():
                hyphenation += latex_hyphenation(word.strip())
            VARS['HYPHENATION'] = hyphenation

    TEMPLATE = 'template.tex'
    local_template_path = os.path.join(book_path, 'template.tex')
    if os.path.isfile(local_template_path):
        template = latex_env.from_string(open(local_template_path).read())
    else:
        template = latex_env.get_template(TEMPLATE)

    base_filename = VARS['BASE_FILENAME']
    tex_file = filepath(book_path, base_filename, 'tex')

    with open(tex_file, 'w') as f:
        f.write(template.render(**VARS))

    if not args.only_tex:
        if args.pdf or not args.epub:
            pdf_file = generate_pdf(book_path, base_filename, tex_file)
            if not args.no_open:
                show_file(pdf_file)
            if args.booklet:
                output_file = filepath(book_path, base_filename, 'booklet.pdf')
                generate_booklet(pdf_file, output_file)
                if not args.no_open:
                    show_file(output_file)
        if args.epub:
            generate_epub(book_path, base_filename, tex_file)
            epub_file = filepath(book_path, base_filename, 'epub')
            if not args.no_open:
                show_file(epub_file)


if __name__ == '__main__':
    main()
