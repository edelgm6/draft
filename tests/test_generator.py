from unittest import TestCase
from draft.generator import Generator
import os
from shutil import rmtree

class TestFileTree(TestCase):

    def tearDown(self):
        rmtree('legacy-project')
        rmtree('project')

    def test_generate_file_tree(self):

        generator = Generator()
        generator.generate_project('Gatsby')

        self.assertEqual(len(os.listdir('project/Gatsby/')),1)

        self.assertTrue(os.path.isdir('project/Gatsby/01-Section 1'))
        self.assertTrue(os.path.isdir('project/Gatsby/01-Section 1/01-Chapter 1'))
        self.assertTrue(os.path.isdir('project/Gatsby/01-Section 1/01-Chapter 1/01-Sub-Chapter 1'))
        self.assertTrue(os.path.isfile('project/Gatsby/01-Section 1/01-Chapter 1/01-Sub-Chapter 1/01-Scene 1.md'))
