# -*- coding: utf-8 -*-

import glob
import shutil
import os
import subprocess
from unittest import TestCase


# legacy tests
# don't blame me :P


class BuildTest(TestCase):

    TESTS_DIR = 'tests_data'
    EXAMPLES = {
        'ejemplo': [['--YEAR=2016']],
        'ejemplo_no_config': [['--YEAR=2016']],
        'ejemplo_2': [['--YEAR=2016']],
        'ejemplo_single': [['--YEAR=2016'], ['--YEAR=2016', '--exclude-index', '--BASE_FILENAME=index_excluded']]
    }

    @classmethod
    def tearDownClass(cls):
        for ex in cls.EXAMPLES.keys():
            dir = os.path.join(cls.TESTS_DIR, ex)
            if os.path.isdir(dir):
                shutil.rmtree(dir)

    @staticmethod
    def run_and_assert(cmd):
        print("Running: {}".format(cmd))
        proc = subprocess.Popen(cmd)
        proc.communicate()
        return proc.returncode

    def test_build(self):
        for ex in self.EXAMPLES.keys():
            new_dir = os.path.join(self.TESTS_DIR, ex)
            os.mkdir(new_dir)
            for f in glob.glob(os.path.join(ex, '*.txt')) + [os.path.join(ex, 'config.py')]:
                if os.path.isfile(f):
                    shutil.copy(f, new_dir)
            for params in self.EXAMPLES[ex]:
                cmd = ['python', 'automagica.py', '--ignore-gooey', '--only-tex'] + params + [os.path.join(self.TESTS_DIR, ex)]
                self.run_and_assert(cmd)

        cmd = ['diff', 'tests_data/ejemplo/jungla.tex', 'tests_data/jungla.tex']
        self.assertEqual(self.run_and_assert(cmd), 0, msg="Failed jungla.tex")
        cmd = ['diff', 'tests_data/ejemplo_2/sueltos.tex', 'tests_data/sueltos.tex']
        self.assertEqual(self.run_and_assert(cmd), 0, msg="Failed sueltos.tex")
        cmd = ['diff', 'tests_data/ejemplo_single/libro.tex', 'tests_data/libro.tex']
        self.assertEqual(self.run_and_assert(cmd), 0, msg="Failed libro.tex")
        cmd = ['diff', 'tests_data/ejemplo_single/index_excluded.tex', 'tests_data/index_excluded.tex']
        self.assertEqual(self.run_and_assert(cmd), 0, msg="Failed index_excluded.tex")
