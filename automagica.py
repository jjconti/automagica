# -*- coding: utf-8 -*-


import argparse
from datetime import datetime
import imp
import os

from epub import generate_epub
from pdf import generate_pdf
from utils import latex_chapter, filepath

DEFAULTS = dict(
    TITLE="TITLE",
    AUTHOR="AUTHOR",
    FONT_SIZE=11,
    PAGE_SIZE='a5paper',
    YEAR=datetime.now().year,
    URL='',
    INDEX_TITLE="Índice",
)

parser = argparse.ArgumentParser()
parser.add_argument('book_path', help="Carpeta con archivos para un libro.", metavar='carpeta')
parser.add_argument('--split-paragraphs', help="Separar párrafos.", action='store_true')
parser.add_argument('--pdf', help="Genera la versión pdf del libro.", action='store_true')
parser.add_argument('--epub', help="Genera la versión epub del libro.", action='store_true')
args = parser.parse_args()
book_path = args.book_path

if not os.path.isdir(book_path):
    print("El argumento debe ser un directorio")
    exit()
config = imp.load_source('config', os.path.join(book_path, 'config.py'))

VARS = DEFAULTS.copy()
VARS.update(config.CONFIGS)

index_path = os.path.join(book_path, 'index.txt')
with open(index_path, 'r') as f:
    content = ""
    for filename in f.readlines():
        content += latex_chapter(os.path.join(book_path, filename).strip(), args.split_paragraphs)
    VARS['CONTENT'] = content

TEMPLATE = 'template.tex'

with open(TEMPLATE, 'r') as f:
    template = f.read()

tex_file = filepath(book_path, config.BASE_FILENAME, 'tex')

with open(tex_file, 'w') as f:
    f.write(template.format(**VARS))

if args.pdf or not args.epub:
    generate_pdf(book_path, config.BASE_FILENAME, tex_file)
if args.epub:
    generate_epub(book_path, config.BASE_FILENAME, tex_file)
