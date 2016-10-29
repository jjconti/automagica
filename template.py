# -*- coding: utf-8 -*-


from __future__ import division, print_function, unicode_literals

import os

import jinja2

latex_env = jinja2.Environment(
    block_start_string='block{',
    block_end_string='}',
    variable_start_string='var{',
    variable_end_string='}',
    comment_start_string='#{',
    comment_end_string='}',
    line_statement_prefix='%%',
    line_comment_prefix='%#',
    trim_blocks=True,
    autoescape=False,
    loader=jinja2.FileSystemLoader(os.path.abspath('.'))
)
