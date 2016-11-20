#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import argparse
import imp
import glob
import os
import sys
from datetime import datetime

from epub import generate_epub
from pdf import generate_pdf
from pdf.booklet import generate_booklet
from template import latex_env
from utils import filepath, latex_hyphenation, latex_chapter, latex_single

reload(sys)
sys.setdefaultencoding('utf8')

DEFAULTS = dict(
    PAGE_SIZE='a5paper',
    YEAR=datetime.now().year,
    URL='',
    INCLUDE_INDEX=True,
    INDEX_TITLE='Índice',
    HYPHENATION='',
    CONTENT='',
)


parser = argparse.ArgumentParser()
parser.add_argument('--BASE_FILENAME', default='default')
parser.add_argument('book_path', help='Carpeta con archivos para un libro.', metavar='carpeta')
parser.add_argument('--no-split', help='No separar párrafos.', action='store_true')
parser.add_argument('--pdf', help='Genera la versión pdf del libro.', action='store_true')
parser.add_argument('--booklet', help='Genera la versión booklet del pdf.', action='store_true')
parser.add_argument('--epub', help='Genera la versión epub del libro.', action='store_true')
parser.add_argument('--only-tex', help='Solo genera el archivo latex.', action='store_true')
parser.add_argument('--sections', help='Usar secciones en lugar de capítulos como elemento principal.', action='store_true')
parser.add_argument('--TITLE', default='TITLE')
parser.add_argument('--AUTHOR', default='AUTHOR')
parser.add_argument('--FONT_SIZE', default=11)
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
                content += latex_single(os.path.join(book_path, filename).strip(), split_paragraphs, VARS['sections'])
        VARS['CONTENT'] = content
else:
    text_files = [f for f in glob.glob(os.path.join(book_path, '*.txt')) if not f.endswith('words.txt')]
    if text_files:
        VARS['CONTENT'] = latex_single(text_files[0], split_paragraphs, VARS['sections'])

# TODO: use IF in template
if VARS['INCLUDE_INDEX']:
    VARS['INDEX'] = '\\renewcommand*\\contentsname{{{INDEX_TITLE}}}'.format(**VARS)
    VARS['INDEX'] += '\n'
    VARS['INDEX'] += '\\tableofcontents'

sep_path = os.path.join(book_path, 'words.txt')
if os.path.isfile(sep_path):
    with open(sep_path, 'r') as f:
        hyphenation = ''
        for word in f.readlines():
            hyphenation += latex_hyphenation(word.strip())
        VARS['HYPHENATION'] = hyphenation

TEMPLATE = 'template.tex'

template = latex_env.get_template(TEMPLATE)

base_filename = VARS['BASE_FILENAME']
tex_file = filepath(book_path, base_filename, 'tex')

with open(tex_file, 'w') as f:
    f.write(template.render(**VARS))

if not args.only_tex:
    if args.pdf or not args.epub:
        pdf_file = generate_pdf(book_path, base_filename, tex_file)
        if args.booklet:
            generate_booklet(pdf_file, filepath(book_path, base_filename, 'booklet.pdf'))
    if args.epub:
        generate_epub(book_path, base_filename, tex_file)
