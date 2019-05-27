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
        os.remove('legacy.txt')
        rmtree('project')
        rmtree('archive')

    def test_generate_file_tree(self):

        generator = Generator()
        generator.generate_project('Gatsby')

        self.assertTrue(os.path.isdir('project/Gatsby/'))

        self.assertTrue(os.path.isdir('archive'))
