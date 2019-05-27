from unittest import TestCase
from draft.outliner import Outliner
from draft.generator import Generator
import os
from shutil import rmtree

class TestUpdateOutline(TestCase):

    def tearDown(self):
        rmtree('project/')
        rmtree('legacy-project/')
        os.remove('outline.md')

    def test_update_outline(self):
        generator = Generator()
        generator.generate_project('Gatsby')

        outliner = Outliner()
        outliner.update_outline()

class TestFileTree(TestCase):

    def tearDown(self):
        file = open('legacy-project/legacy.txt')
        file.close()
        os.remove(file.name)
        rmtree('project/')
        rmtree('legacy-project/')

    def test_generate_file_tree(self):
        generator = Generator()
        generator.generate_project('Gatsby')
        rmtree('project/Gatsby/01-Section 1')

        fp = open('legacy-project/legacy.txt','w+')
        fp.write("# Part 1: The Reckoning\n")
        fp.write("\n")
        fp.write("## Chapter 1: The Promise\n")
        fp.write("\n")
        fp.write("### New York, 1942\n")
        fp.write("\n")
        fp.write("# Part 2: The Whatever\n")
        fp.write("\n")
        fp.write("#### The Bar\n")
        fp.write("\n")
        fp.write("It was a fall day.\n")
        fp.write("It was cold.\n")
        fp.write("# Part 3: Tomorrow\n")
        fp.write("\n")
        fp.write("#### The Next Day\n")
        fp.write("Now it's tomorrow.\n")
        fp.write("It's still cold.\n")
        fp.close()

        outliner = Outliner()
        outliner.generate_file_tree()

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
