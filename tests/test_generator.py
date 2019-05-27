from unittest import TestCase
from draft.generator import Generator, StructureError
import os
from shutil import rmtree

class TestProjectLayout(TestCase):

    def test_confirm_project_layout_raises_error_in_blank_project(self):

        generator = Generator()
        with self.assertRaises(StructureError):
            generator.confirm_project_layout()

class TestFileTree(TestCase):

    def tearDown(self):
        rmtree('legacy-project')
        rmtree('project')
        rmtree('archive')

    def test_generate_file_tree(self):

        generator = Generator()
        generator.generate_project('Gatsby')

        self.assertEqual(len(os.listdir('project/Gatsby/')),1)

        self.assertTrue(os.path.isdir('project/Gatsby/01-Section 1'))
        self.assertTrue(os.path.isdir('project/Gatsby/01-Section 1/01-Chapter 1'))
        self.assertTrue(os.path.isdir('project/Gatsby/01-Section 1/01-Chapter 1/01-Sub-Chapter 1'))
        self.assertTrue(os.path.isfile('project/Gatsby/01-Section 1/01-Chapter 1/01-Sub-Chapter 1/01-Scene 1.md'))

        self.assertTrue(os.path.isdir('archive'))
        self.assertTrue(os.path.isdir('archive/project'))
        self.assertTrue(os.path.isdir('archive/legacy-project'))
