from unittest import TestCase
from draft.outliner import Outliner
from draft.generator import Generator
import os
from shutil import rmtree

class TestUpdateSequence(TestCase):

    def tearDown(self):
        rmtree('project')
        rmtree('archive')
        os.remove('legacy.txt')

    def setUp(self):
        generator = Generator()
        generator.generate_project('Gatsby')

        os.mkdir('project/Gatsby/01-Part 1')
        os.mkdir('project/Gatsby/01-Part 2')
        os.mkdir('project/Gatsby/01-Part 2/01-Chapter 1')
        os.mkdir('project/Gatsby/01-Part 2/01-Chapter 2')
        os.mkdir('project/Gatsby/01-Part 2/05-Chapter 3')
        os.mkdir('project/Gatsby/01-Part 2/05-Chapter 4')
        os.mkdir('project/Gatsby/03-Part 3')
        os.mkdir('project/Gatsby/04-Part 4')
        os.mkdir('project/Gatsby/04-Part 5')
        os.mkdir('project/Gatsby/04-Part 6')
        os.mkdir('project/Gatsby/05-Part 7')

    def test_sequence_is_reset(self):

        """
        TODO: Test with markdown files
        """

        outliner = Outliner()
        outliner.update_file_sequence()

        tree = outliner._get_file_tree()

        for branch in tree:
            print(branch)

        """
        TODO: Add assertions
        """

class TestUpdateOutline(TestCase):

    def tearDown(self):
        rmtree('project/')
        rmtree('archive')
        os.remove('outline.md')
        os.remove('legacy.txt')


    def test_update_outline(self):
        generator = Generator()
        generator.generate_project('Gatsby')

        outliner = Outliner()
        outliner.update_outline()

class TestFileTree(TestCase):

    def tearDown(self):
        rmtree('project/')
        rmtree('archive')
        os.remove('legacy.txt')

    def test_generate_file_tree(self):
        generator = Generator()
        generator.generate_project('Gatsby')

        fp = open('legacy.txt','w+')
        fp.write("# Gatsby\n")
        fp.write("\n")
        fp.write("## Part 1: The Reckoning\n")
        fp.write("\n")
        fp.write("### Chapter 1: The Promise\n")
        fp.write("\n")
        fp.write("#### New York, 1942\n")
        fp.write("\n")
        fp.write("## Part 2: The Whatever\n")
        fp.write("\n")

        fp.write("##### The Bar\n")
        fp.write("\n")
        fp.write("It was a fall day.\n")
        fp.write("It was cold.\n")
        fp.write("## Part 3: Tomorrow\n")
        fp.write("\n")
        fp.write("##### The Next Day\n")
        fp.write("\n")
        fp.write("Now it's tomorrow.\n")
        fp.write("It's still cold.\n")

        fp.close()

        outliner = Outliner()
        outliner.generate_file_tree('legacy.txt')

        self.assertEqual(len(os.listdir('project/Gatsby/')),3)

        self.assertTrue(os.path.isdir('project/Gatsby/01-Part 1: The Reckoning'))
        self.assertTrue(os.path.isdir('project/Gatsby/01-Part 1: The Reckoning/01-Chapter 1: The Promise'))
        self.assertTrue(os.path.isdir('project/Gatsby/01-Part 1: The Reckoning/01-Chapter 1: The Promise/01-New York, 1942'))
        self.assertTrue(os.path.isdir('project/Gatsby/02-Part 2: The Whatever'))
        self.assertTrue(os.path.isdir('project/Gatsby/03-Part 3: Tomorrow'))
        self.assertTrue(os.path.isfile('project/Gatsby/02-Part 2: The Whatever/01-The Bar.md'))

        with open('project/Gatsby/02-Part 2: The Whatever/01-The Bar.md', 'r') as fp:
            lines = fp.readlines()
            self.assertEqual(lines[0],"It was a fall day.\n")
            self.assertEqual(lines[1],"It was cold.\n")
            self.assertEqual(len(lines), 2)
