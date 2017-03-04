# -*- coding: utf-8 -*-


from __future__ import division, print_function, unicode_literals

import os
import subprocess
import sys


def show_file(filepath):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', filepath))
    elif os.name == 'nt':
        os.startfile(filepath)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', filepath))


def filepath(path, base_name, ext):
    return os.path.join(path, '{}.{}'.format(base_name, ext))


def latex_chapter_title(title, index_title=None):
    if not index_title:
        index_title = title
    return '\n\n\chapter*{{{title}}} \\addcontentsline{{toc}}{{chapter}}{{{index_title}}}'.format(
        title=title.strip(), index_title=index_title.strip())


def latex_section_title(title, index_title=None, new_page_before_sections=False):
    if not index_title:
        index_title = title
    np = '\n\n\\newpage' if new_page_before_sections else ''
    return np + '\n\n\section*{{{title}}} \\addcontentsline{{toc}}{{section}}{{{index_title}}}'.format(
        title=title.strip(), index_title=index_title.strip())


def latex_subsection_title(title, index_title=None):
    return '\n\n\subsection*{{{title}}}'.format(title=title)


def latex_part_title(title, index_title=None):
    return '\n\n\part*{{{title}}}'.format(title=title)


def latex_chapter(path, split_paragraphs=False):
    with open(path, 'r') as f:
        lines = f.readlines()
        lines[0] = latex_chapter_title(lines[0])
        sep = '\n' if split_paragraphs else ' '
        return sep.join(lines).replace('&', '\&')


def is_title(i, lines):
    return i and lines[i] and not lines[i-1] and not lines[i+1] and len(lines[i]) < 60 and "\\" not in lines[i]


def latex_single(path, split_paragraphs=False, use_sections=False, new_page_before_sections=False):
    with open(path, 'r') as f:
        lines = [''] + [l.strip() for l in f.readlines()] + ['']
        for (i, line) in enumerate(lines):
            if is_title(i, lines):
                if use_sections:
                    lines[i] = latex_section_title(lines[i], new_page_before_sections=new_page_before_sections)
                else:
                    lines[i] = latex_chapter_title(lines[i])
        sep = '\n\n' if split_paragraphs else ' '
        return sep.join(lines).replace('&', '\&')


def latex_hyphenation(word):
    return '\hyphenation{{{word}}}'.format(word=word)
