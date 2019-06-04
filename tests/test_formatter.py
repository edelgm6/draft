from unittest import TestCase
from draft.formatter import Formatter
from draft.generator import Generator
import os
from shutil import rmtree

class TestCleanSpaces(TestCase):

    def setUp(self):
        os.mkdir('project')
        os.mkdir('project/Gatsby')
        os.mkdir('archive')

    def tearDown(self):
        os.remove('testfile.txt')
        rmtree('project')
        rmtree('archive')

    def test_clean_spaces(self):
        fp = open('testfile.txt','w+')
        fp.write("\"     It's the end of the world as  we know it.\" \"And I    feel fine.     \"")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.remove_duplicate_spaces()

        fp = open('testfile.txt','r')
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\" It's the end of the world as we know it.\" \"And I feel fine. \"")

class TestSplitSentences(TestCase):

    def setUp(self):
        os.mkdir('project')
        os.mkdir('project/Gatsby')
        os.mkdir('archive')

    def tearDown(self):
        os.remove('testfile.txt')
        rmtree('project')
        rmtree('archive')

    def test_split_sentences_on_quotes_within_a_sentence(self):

        fp = open('testfile.txt','w+')
        fp.write("\"It's the end of the world as we know it.\" \"And I feel fine.\"")
        fp.write(" \"You are nice!\" she said.")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.split_sentences()

        fp = open('testfile.txt','r')

        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\"It's the end of the world as we know it.\"\n")
        self.assertEqual(lines[1],"\"And I feel fine.\"\n")
        self.assertEqual(lines[2],"\"You are nice!\" she said.")
        self.assertEqual(len(lines), 3)


    def test_split_sentences_on_quotes(self):

        fp = open('testfile.txt','w+')
        fp.write("\"It's the end of the world as we know it.\" \"And I feel fine.\"")
        fp.write(" \"You are nice,\" she said.")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.split_sentences()

        fp = open('testfile.txt','r')
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\"It's the end of the world as we know it.\"\n")
        self.assertEqual(lines[1],"\"And I feel fine.\"\n")
        self.assertEqual(lines[2],"\"You are nice,\" she said.")
        self.assertEqual(len(lines), 3)


    def test_split_sentences_on_period(self):

        fp = open('testfile.txt','w+')
        fp.write("It's the end of the world as we know it. And I feel fine.")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.split_sentences()

        fp = open('testfile.txt','r')
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"It's the end of the world as we know it.\n")
        self.assertEqual(lines[1],"And I feel fine.")
        self.assertEqual(len(lines), 2)

    def test_split_sentences_on_question_mark(self):

        fp = open('testfile.txt','w+')
        fp.write("It's the end of the world as we know it? And I feel fine.")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.split_sentences()

        fp = open('testfile.txt','r')
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"It's the end of the world as we know it?\n")
        self.assertEqual(lines[1],"And I feel fine.")
        self.assertEqual(len(lines), 2)


    def test_split_sentences_on_abbreviations(self):

        fp = open('testfile.txt','w+')
        fp.write("It's the end of the world as we know it, etc.? And I feel fine Mrs. Miller, seriously. I.e., don't do anything stupid.")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.split_sentences()

        fp = open('testfile.txt','r')
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"It's the end of the world as we know it, etc.?\n")
        self.assertEqual(lines[1],"And I feel fine Mrs. Miller, seriously.\n")
        self.assertEqual(lines[2],"I.e., don't do anything stupid.")
        self.assertEqual(len(lines), 3)

    """
    def test_archive_created_if_in_project_path(self):

        fp = open('project/Gatsby/testfile.txt','w+')
        fp.write("It's the end of the world as we know it, etc.? And I feel fine Mrs. Miller, seriously. I.e., don't do anything stupid.")
        fp.close()
        formatter = Formatter(fp.name)
        formatter.split_sentences()

        fp = open('project/Gatsby/testfile.txt','r')
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"It's the end of the world as we know it, etc.?\n")
        self.assertEqual(lines[1],"And I feel fine Mrs. Miller, seriously.\n")
        self.assertEqual(lines[2],"I.e., don't do anything stupid.")
        self.assertEqual(len(lines), 3)
        archive_record = os.listdir('archive/')[0]
        self.assertTrue(os.path.isfile('archive/' + archive_record + '/Gatsby/testfile.txt'))
    """
