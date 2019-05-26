from unittest import TestCase
from draft.outliner import Outliner
import os

class TestFileTree(TestCase):

    def tearDown(self):
        file = open('testfile.md')
        file.close()
        os.remove(file.name)

    def test_clean_spaces(self):
        fp = open('testfile.md','w+')
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
        fp.close()

        Outliner.generate_file_tree(fp.name)
