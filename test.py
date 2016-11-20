#!/usr/bin/env python
# -*- coding: utf-8 -*-

TESTS_DIR = 'tests_data'
EXAMPLES = {'ejemplo': ['--no-split'],
            'ejemplo_2': [],
            'ejemplo_single': []}

import glob
import shutil
import os
import subprocess


def run_and_assert(cmd):
    print("Running: {}".format(cmd))
    proc = subprocess.Popen(cmd)
    proc.communicate()
    retcode = proc.returncode
    assert retcode == 0


def clean():
    for ex in EXAMPLES.keys():
        dir = os.path.join(TESTS_DIR, ex)
        if os.path.isdir(dir):
            shutil.rmtree(dir)


def run_tests():
    for ex in EXAMPLES.keys():
        new_dir = os.path.join(TESTS_DIR, ex)
        os.mkdir(new_dir)
        for f in glob.glob(os.path.join(ex, '*.txt')) + [os.path.join(ex, 'config.py')]:
            if os.path.isfile(f):
                shutil.copy(f, new_dir)
        cmd = ['python', 'automagica.py', '--only-tex'] + EXAMPLES[ex] + [os.path.join(TESTS_DIR, ex)]
        run_and_assert(cmd)

    cmd = ['diff', 'tests_data/ejemplo/jungla.tex', 'tests_data/jungla.tex']
    run_and_assert(cmd)
    cmd = ['diff', 'tests_data/ejemplo_2/sueltos.tex', 'tests_data/sueltos.tex']
    run_and_assert(cmd)
    cmd = ['diff', 'tests_data/ejemplo_single/default.tex', 'tests_data/default.tex']
    run_and_assert(cmd)
    clean()


if __name__ == '__main__':
    try:
        run_tests()
    except Exception as e:
        print e
        clean()