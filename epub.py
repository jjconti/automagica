"""
Generate .epub file
"""

import os
import subprocess

from utils import filepath, show_file

test = 1
def generate_epub(book_path, base_filename, tex_file):
    epub_file = filepath(book_path, base_filename, 'epub')
    cmd = ['pandoc', '--from=latex', '-o', epub_file, tex_file]

    proc = subprocess.Popen(cmd)
    proc.communicate()

    retcode = proc.returncode

    if not retcode == 0:
        os.unlink(epub_file)
        raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))
    else:
        show_file(epub_file)
