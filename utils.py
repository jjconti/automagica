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
    return "\chapter*{{{title}}} \\addcontentsline{{toc}}{{chapter}}{{{index_title}}}".format(
        title=title, index_title=index_title)


def latex_section_title(title, index_title=None):
    return "\section*{{{title}}}".format(title=title)


def latex_subsection_title(title, index_title=None):
    return "\subsection*{{{title}}}".format(title=title)


def latex_part_title(title, index_title=None):
    return "\part*{{{title}}}".format(title=title)


def latex_chapter(path, split_paragraphs=False):
    with open(path, 'r') as f:
        lines = f.readlines()
        lines[0] = latex_chapter_title(lines[0])
        sep = "\n" if split_paragraphs else " "
        return sep.join(lines).replace('&', '\&')


def is_title(i, lines, subtitle=False):
    l = len(lines[i])
    single = i and lines[i] and not lines[i-1] and not lines[i+1]
    if single:
        if subtitle:
            return l <= 3
        else:
            return 3 < l < 50


def is_space(i, lines):
    return i and not lines[i] #and lines[i-1] and not is_title(i-1, lines) and lines[i+1] and not is_title(i+1, lines)


def latex_part(path, split_paragraphs=False):
    with open(path, 'r') as f:
        lines = [''] + [l.strip() for l in f.readlines()]
        #lines[0] = latex_part_title(lines[0])
        for (i, line) in enumerate(lines):
            if is_title(i, lines):
                #lines[i] = latex_section_title(lines[i])
                lines[i] = latex_chapter_title(lines[i])
            elif is_title(i, lines, subtitle=True):
                #lines[i] = latex_subsection_title(lines[i])
                lines[i] = latex_chapter_title(lines[i])
            elif is_space(i, lines):
                lines[i] = '\\bigbreak'
        sep = '\n\n' if split_paragraphs else ' '
        return sep.join(lines).replace('&', '\&')


def latex_hyphenation(word):
    return "\hyphenation{{{word}}}".format(word=word)
