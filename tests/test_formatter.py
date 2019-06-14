from unittest import TestCase
from draft.formatter import Formatter
from draft.generator import Generator
import os
from shutil import rmtree

class TestCleanSpaces(TestCase):

    def setUp(self):
        os.mkdir("project")
        os.mkdir("project/Gatsby")
        os.mkdir("archive")

    def tearDown(self):
        try:
            os.remove("testfile.txt")
        except:
            pass
        rmtree("project")
        rmtree("archive")

    def test_clean_spaces(self):
        fp = open("testfile.txt","w+")
        fp.write("\"     It's the end of the world as  we know it.\" \"And I    feel fine.     \"")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.remove_duplicate_spaces()

        fp = open("testfile.txt","r")
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\" It's the end of the world as we know it.\" \"And I feel fine. \"")

    def test_clean_spaces_no_args(self):
        fp = open("project/testfile.md","w+")
        fp.write("\"     It's the end of the world as  we know it.\" \"And I    feel fine.     \"")
        fp.close()
        formatter = Formatter(None)
        formatter.remove_duplicate_spaces()

        fp = open("project/testfile.md","r")
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\" It's the end of the world as we know it.\" \"And I feel fine. \"")

class TestSplitSentences(TestCase):

    def setUp(self):
        os.mkdir("project")
        os.mkdir("project/Gatsby")
        os.mkdir("archive")

    def tearDown(self):
        try:
            os.remove("testfile.txt")
        except:
            pass
        rmtree("project")
        rmtree("archive")

    def test_split_sentences_skips_already_split_file(self):
        fp = open("project/testfile.md","w+")
        fp.write('She blushed-automatically conferring on me the social poise I\'d\nbeen missing. "Well. Most of the Americans I\'ve seen act like\nanimals. They\'re forever punching one another about, and insulting\neveryone, and--You know what one of them did?"\nI shook my head.\n"One of them threw an empty whiskey bottle through my aunt\'s\nwindow. Fortunately, the window was open. But does that sound\nvery intelligent to you?"\nIt didn\'t especially, but I didn\'t say so. I said that many soldiers, all\nover the world, were a long way from home, and that few of them\nhad had many real advantages in life. I said I\'d thought that most\npeople could figure that out for themselves.\n')
        fp.close()
        formatter = Formatter(None)
        formatter.split_sentences()

        fp = open("project/testfile.md","r")
        text = fp.read()
        fp.close()

        self.assertEqual(text, 'She blushed-automatically conferring on me the social poise I\'d\n\nbeen missing.\n"Well.\nMost of the Americans I\'ve seen act like\n\nanimals.\nThey\'re forever punching one another about, and insulting\n\neveryone, and--You know what one of them did?"\n\nI shook my head.\n\n"One of them threw an empty whiskey bottle through my aunt\'s\n\nwindow.\nFortunately, the window was open.\nBut does that sound\n\nvery intelligent to you?"\n\nIt didn\'t especially, but I didn\'t say so.\nI said that many soldiers, all\n\nover the world, were a long way from home, and that few of them\n\nhad had many real advantages in life.\nI said I\'d thought that most\n\npeople could figure that out for themselves.\n\n')

    def test_split_sentences_in_full_project(self):
        fp = open("project/testfile.md","w+")
        fp.write("\"It's the end of the world as we know it.\" \"And I feel fine.\"")
        fp.write(" \"You are nice!\" she said.")
        fp.close()
        formatter = Formatter(None)
        formatter.split_sentences()

        fp = open("project/testfile.md","r")

        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\"It's the end of the world as we know it.\"\n")
        self.assertEqual(lines[1],"\"And I feel fine.\"\n")
        self.assertEqual(lines[2],"\"You are nice!\" she said.")
        self.assertEqual(len(lines), 3)

        fp = open("project/testfile1.md","w+")
        fp.write("It's the end of the world as we know it. And I feel fine.")
        fp.close()
        formatter = Formatter(None)
        formatter.split_sentences()

        fp = open("project/testfile1.md","r")
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"It's the end of the world as we know it.\n")
        self.assertEqual(lines[1],"And I feel fine.")
        self.assertEqual(len(lines), 2)

    def test_split_sentences_on_quotes_within_a_sentence(self):

        fp = open("testfile.txt","w+")
        fp.write("\"It's the end of the world as we know it.\" \"And I feel fine.\"")
        fp.write(" \"You are nice!\" she said.")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.split_sentences()

        fp = open("testfile.txt","r")

        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\"It's the end of the world as we know it.\"\n")
        self.assertEqual(lines[1],"\"And I feel fine.\"\n")
        self.assertEqual(lines[2],"\"You are nice!\" she said.")
        self.assertEqual(len(lines), 3)


    def test_split_sentences_on_quotes(self):

        fp = open("testfile.txt","w+")
        fp.write("\"It's the end of the world as we know it.\" \"And I feel fine.\"")
        fp.write(" \"You are nice,\" she said.")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.split_sentences()

        fp = open("testfile.txt","r")
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\"It's the end of the world as we know it.\"\n")
        self.assertEqual(lines[1],"\"And I feel fine.\"\n")
        self.assertEqual(lines[2],"\"You are nice,\" she said.")
        self.assertEqual(len(lines), 3)


    def test_split_sentences_on_period(self):

        fp = open("testfile.txt","w+")
        fp.write("It's the end of the world as we know it. And I feel fine.")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.split_sentences()

        fp = open("testfile.txt","r")
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"It's the end of the world as we know it.\n")
        self.assertEqual(lines[1],"And I feel fine.")
        self.assertEqual(len(lines), 2)

    def test_split_sentences_on_question_mark(self):

        fp = open("testfile.txt","w+")
        fp.write("It's the end of the world as we know it? And I feel fine.")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.split_sentences()

        fp = open("testfile.txt","r")
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"It's the end of the world as we know it?\n")
        self.assertEqual(lines[1],"And I feel fine.")
        self.assertEqual(len(lines), 2)


    def test_split_sentences_on_abbreviations(self):

        fp = open("testfile.txt","w+")
        fp.write("It's the end of the world as we know it, etc.? And I feel fine Mrs. Miller, seriously. I.e., don't do anything stupid.")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.split_sentences()

        fp = open("testfile.txt","r")
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"It's the end of the world as we know it, etc.?\n")
        self.assertEqual(lines[1],"And I feel fine Mrs. Miller, seriously.\n")
        self.assertEqual(lines[2],"I.e., don't do anything stupid.")
        self.assertEqual(len(lines), 3)
