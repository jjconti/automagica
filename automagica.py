#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import argparse
import imp
import os
import sys
from datetime import datetime

from epub import generate_epub
from pdf import generate_pdf
from pdf.booklet import generate_booklet
from template import latex_env
from utils import filepath, latex_hyphenation

reload(sys)
sys.setdefaultencoding('utf8')

DEFAULTS = dict(
    TITLE="TITLE",
    AUTHOR="AUTHOR",
    FONT_SIZE=11,
    PAGE_SIZE='a5paper',
    YEAR=datetime.now().year,
    URL='',
    INCLUDE_INDEX=True,
    INDEX_TITLE="Índice",
    HYPHENATION="",
    CONTENT="",
    SPLIT=True
)


parser = argparse.ArgumentParser()
parser.add_argument('book_path', help="Carpeta con archivos para un libro.", metavar='carpeta')
parser.add_argument('--no-split', help="No separar párrafos.", action='store_true')
parser.add_argument('--pdf', help="Genera la versión pdf del libro.", action='store_true')
parser.add_argument('--booklet', help="Genera la versión booklet del pdf.", action='store_true')
parser.add_argument('--epub', help="Genera la versión epub del libro.", action='store_true')
args = parser.parse_args()
book_path = args.book_path


class EmptyConfig(object):
    pass

if not os.path.isdir(book_path):
    print("El argumento debe ser un directorio")
    exit()
config_file = os.path.join(book_path, 'config.py')
if os.path.isfile(config_file):
    config = imp.load_source('config', config_file)
else:
    config = EmptyConfig()
    config.CONFIGS = {}
    config.BASE_FILENAME = 'default'

VARS = DEFAULTS.copy()
VARS.update(config.CONFIGS)

index_path = os.path.join(book_path, 'index.txt')

if os.path.isfile(index_path):
    with open(index_path, 'r') as f:
        content = ""
        for filename in f.readlines():
            content += latex_part(os.path.join(book_path, filename).strip(), not args.no_split or VARS['SPLIT'])
        VARS['CONTENT'] = content

if VARS['INCLUDE_INDEX']:
    VARS['INDEX'] = '\\renewcommand*\\contentsname{{{INDEX_TITLE}}}'.format(**VARS)
    VARS['INDEX'] += '\n'
    VARS['INDEX'] += '\\tableofcontents'

sep_path = os.path.join(book_path, 'words.txt')
if os.path.isfile(sep_path):
    with open(sep_path, 'r') as f:
        hyphenation = ""
        for word in f.readlines():
            hyphenation += latex_hyphenation(word.strip())
        VARS['HYPHENATION'] = hyphenation

TEMPLATE = 'template.tex'

template = latex_env.get_template(TEMPLATE)

tex_file = filepath(book_path, config.BASE_FILENAME, 'tex')

with open(tex_file, 'w') as f:
    f.write(template.render(**VARS))

if args.pdf or not args.epub:
    pdf_file = generate_pdf(book_path, config.BASE_FILENAME, tex_file)
    if args.booklet:
        generate_booklet(pdf_file, filepath(book_path, config.BASE_FILENAME, 'booklet.pdf'))
if args.epub:
    generate_epub(book_path, config.BASE_FILENAME, tex_file)
