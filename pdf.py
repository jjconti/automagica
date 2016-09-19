"""
Generate .pdf file
"""

import os
import subprocess

from utils import filepath


def generate_pdf(book_path, base_filename, tex_file):
    pdf_file = filepath(book_path, base_filename, 'pdf')
    cmd = ['pdflatex', '-interaction', 'nonstopmode', '-output-directory', book_path, tex_file]

    proc = subprocess.Popen(cmd)
    proc.communicate()

    proc = subprocess.Popen(cmd)
    proc.communicate()

    os.unlink(filepath(book_path, base_filename, 'toc'))
    os.unlink(filepath(book_path, base_filename, 'log'))
    os.unlink(filepath(book_path, base_filename, 'aux'))

    retcode = proc.returncode

    if not retcode == 0:
        os.unlink(pdf_file)
        raise ValueError('Error {} executing command: {}'.format(retcode, ' '.join(cmd)))
    else:
        #os.startfile(pdf_filename)
        #subprocess.call(["xdg-open", file])
        subprocess.call(['open', pdf_file])