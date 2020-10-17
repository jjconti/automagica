# -*- coding: utf-8 -*-
from datetime import datetime

CONFIGS = dict(

    BASE_FILENAME='jungla',
    book_path='.',
    no_split=True,
    pdf=True,
    booklet=False,
    epub=False,
    only_tex=False,
    sections=False,
    new_page_before_sections=True,
    TITLE="TITLE",
    SUBTITLE="",
    AUTHOR="AUTHOR",
    FONT_SIZE=11,
    PAGE_SIZE='a5paper',
    YEAR=datetime.now().year,
    URL='http://www.ellibrodelajungla.com',
    exclude_index=False,
    no_open=False
)
