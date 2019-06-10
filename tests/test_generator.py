from unittest import TestCase
from draft.generator import Generator, StructureError
import os
from shutil import rmtree

class TestProjectLayout(TestCase):

    def test_blank_project_raises_error_in_blank_project(self):

        generator = Generator()
        with self.assertRaises(StructureError):
            generator.confirm_project_layout()

    def test_missing_project_returns_error(self):

        generator = Generator()
        with self.assertRaises(StructureError):
            generator.confirm_project_layout()

    def test_generator_succeeds_with_dsstore(self):

        os.mkdir('project')
        dsstore = open('project/.DS_Store', 'w')
        dsstore.write('whatever')
        dsstore.close()

        generator = Generator()
        generator.confirm_project_layout()

        rmtree('project')

    def test_multiple_dirs_in_project_raises_error(self):

        os.mkdir('project')
        dsstore = open('project/.DS_Store', 'w')
        dsstore.write('whatever')
        dsstore.close()

        whatever = open('project/whatever', 'w')
        whatever.write('whatever')
        whatever.close()

        os.mkdir('project/jaunt')

        generator = Generator()

        with self.assertRaises(StructureError):
            generator.confirm_project_layout()

        rmtree('project')

class TestFileTree(TestCase):

    def tearDown(self):
        rmtree('Gatsby')

    def test_generate_file_tree_does_not_overwrite_existing_files(self):

        os.mkdir('Gatsby')
        os.mkdir('Gatsby/project')
        os.mkdir('Gatsby/project/arbitrary')
        with open('Gatsby/project/arbitrary/whatever.txt', 'w') as test:
            test.write('whatever')

        generator = Generator()
        generator.generate_project('Gatsby2')

        self.assertTrue(os.path.isdir('Gatsby/project/arbitrary/'))
        self.assertTrue(os.path.isfile('Gatsby/project/arbitrary/whatever.txt'))

        with self.assertRaises(FileExistsError):
            generator.generate_project('Gatsby')

        rmtree('Gatsby2')

    def test_generate_file_tree(self):

        generator = Generator()
        generator.generate_project('Gatsby')

        self.assertTrue(os.path.isdir('Gatsby/project/Gatsby/'))
