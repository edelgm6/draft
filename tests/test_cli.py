import os
import click
from click.testing import CliRunner
from shutil import rmtree
from unittest import TestCase
from draft import cli
from draft.cli import stats, sequence, parse, split, trim, create_project, outline, compile
import datetime
import traceback
from draft.outliner import Outliner

class TestGetMDFiles(TestCase):

    def test_get_filepaths_raises_error_if_multiple(self):
        file = open("whatever.md", "w")
        file.close()
        os.mkdir("project")
        file = open("project/whatever.md", "w")
        file.close()

        outliner = Outliner()
        with self.assertRaises(click.ClickException):
            files = cli._get_filepath("whatever.md")

        os.remove("whatever.md")
        rmtree("project")

    def test_get_filepaths_raises_error_if_none(self):
        os.mkdir("project")
        file = open("project/whatever.md", "w")
        file.close()

        outliner = Outliner()
        with self.assertRaises(click.ClickException):
            files = cli._get_filepath("whatevers.md")

        rmtree("project")

    def test_get_filepaths_returns_file_if_single(self):
        os.mkdir("project")
        file = open("project/whatever.md", "w")
        file.close()

        outliner = Outliner()
        file = cli._get_filepath("whatever.md")

        rmtree("project")
        self.assertEqual(file, "project/whatever.md")

class TestOutliners(TestCase):

    def tearDown(self):
        rmtree("project")
        rmtree("archive")

    def setUp(self):
        os.mkdir("project")
        os.mkdir("project/Gatsby")
        os.mkdir("archive")

        os.mkdir("project/Gatsby/01-Part 1")
        os.mkdir("project/Gatsby/01-Part 2")
        os.mkdir("project/Gatsby/01-Part 2/01-Chapter 1")
        os.mkdir("project/Gatsby/01-Part 2/01-Chapter 2")

        base = "project/Gatsby/01-Part 2/01-Chapter 1/"
        for file in ["01-Scene 1.md","01-Scene 2.md"]:
            fp = open(base + file, "w")
            fp.write("***\n")
            fp.write("This is an outline\n")
            fp.write("***\n")
            fp.write("**" + file + "**: the _world_ beckons!")
            fp.close()

    def test_outline(self):
        runner = CliRunner()
        result = runner.invoke(outline, input="y\n")
        self.assertEqual(result.exit_code, 0)

        gatsby = open("outline.md", "r")
        text = gatsby.read()
        gatsby.close()
        os.remove("outline.md")

        self.assertEqual(text,"# Gatsby\n\n## Part 1\n\n## Part 2\n\n### Chapter 1\n\n**Scene 1**: This is an outline\n\n**Scene 2**: This is an outline\n\n### Chapter 2\n\n")

    def test_compile(self):
        runner = CliRunner()
        result = runner.invoke(compile, input="y\n")
        self.assertEqual(result.exit_code, 0)

        gatsby = open("Gatsby.md", "r")
        text = gatsby.read()
        gatsby.close()
        os.remove("Gatsby.md")

        self.assertEqual(text,"# Gatsby\n\n## Part 1\n\n## Part 2\n\n### Chapter 1\n\n**01-Scene 1.md**: the _world_ beckons!\n\n</br>\n\n**01-Scene 2.md**: the _world_ beckons!\n\n</br>\n\n### Chapter 2\n\n")

class TestGenerateProject(TestCase):

    def test_generate_file_tree(self):

        runner = CliRunner()
        result = runner.invoke(create_project, ["Gatsby"], input="y\n")
        self.assertEqual(result.exit_code, 0)

        self.assertTrue(os.path.isdir("gatsby/project/Gatsby/"))
        rmtree("gatsby")

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

        runner = CliRunner()
        result = runner.invoke(trim, ["testfile.txt"], input="y\n")
        self.assertEqual(result.exit_code, 0)

        fp = open("testfile.txt","r")
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\" It's the end of the world as we know it.\" \"And I feel fine. \"")

    def test_clean_spaces_no_args(self):
        with open("settings.yml", "w+") as settings:
            settings.write("warnings:\n  trim: yes")

        fp = open("project/Gatsby/testfile.md","w+")
        fp.write("\"     It's the end of the world as  we know it.\" \"And I    feel fine.     \"")
        fp.close()

        runner = CliRunner()
        result = runner.invoke(trim, input="y\n")
        self.assertEqual(result.exit_code, 0)

        fp = open("project/Gatsby/testfile.md","r")
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\" It's the end of the world as we know it.\" \"And I feel fine. \"")
        os.remove("settings.yml")

    def test_clean_spaces_runs_when_warning_disabled(self):
        fp = open("project/Gatsby/testfile.md","w+")
        fp.write("\"     It's the end of the world as  we know it.\" \"And I    feel fine.     \"")
        fp.close()

        with open("settings.yml", "w+") as settings:
            settings.write("warnings:\n  trim: no")

        runner = CliRunner()
        result = runner.invoke(trim)
        self.assertEqual(result.exit_code, 0)

        fp = open("project/Gatsby/testfile.md","r")
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\" It's the end of the world as we know it.\" \"And I feel fine. \"")
        os.remove("settings.yml")

class TestSplitSentences(TestCase):

    def test_split_sentences_with_arg(self):
        fp = open("testfile.txt","w+")
        fp.write("\"It's the end of the world as we know it.\" \"And I feel fine.\"")
        fp.write(" \"You are nice!\" she said.")
        fp.close()

        runner = CliRunner()
        result = runner.invoke(split, ["testfile.txt"], input="y\n")
        self.assertEqual(result.exit_code, 0)
        fp = open("testfile.txt","r")

        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\"It's the end of the world as we know it.\"\n")
        self.assertEqual(lines[1],"\"And I feel fine.\"\n")
        self.assertEqual(lines[2],"\"You are nice!\" she said.")
        self.assertEqual(len(lines), 3)

        os.remove("testfile.txt")

    def test_split_sentences_without_arg(self):
        os.mkdir("project")
        fp = open("project/testfile.md","w+")
        fp.write("\"It's the end of the world as we know it.\" \"And I feel fine.\"")
        fp.write(" \"You are nice!\" she said.")
        fp.close()

        with open("settings.yml", "w+") as settings:
            settings.write("warnings:\n  split: yes")

        runner = CliRunner()
        result = runner.invoke(split, input="y\n")
        self.assertEqual(result.exit_code, 0)
        fp = open("project/testfile.md","r")

        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\"It's the end of the world as we know it.\"\n")
        self.assertEqual(lines[1],"\"And I feel fine.\"\n")
        self.assertEqual(lines[2],"\"You are nice!\" she said.")
        self.assertEqual(len(lines), 3)

        rmtree("project")
        os.remove("settings.yml")

    def test_split_sentences_runs_without_warning(self):
        os.mkdir("project")
        fp = open("project/testfile.md","w+")
        fp.write("\"It's the end of the world as we know it.\" \"And I feel fine.\"")
        fp.write(" \"You are nice!\" she said.")
        fp.close()

        with open("settings.yml", "w+") as settings:
            settings.write("warnings:\n  split: no")

        runner = CliRunner()
        result = runner.invoke(split)
        self.assertEqual(result.exit_code, 0)
        fp = open("project/testfile.md","r")

        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\"It's the end of the world as we know it.\"\n")
        self.assertEqual(lines[1],"\"And I feel fine.\"\n")
        self.assertEqual(lines[2],"\"You are nice!\" she said.")
        self.assertEqual(len(lines), 3)

        rmtree("project")
        os.remove("settings.yml")

class TestFileTree(TestCase):

    def setUp(self):
        os.mkdir("project")
        os.mkdir("project/Gatsby")
        os.mkdir("archive")

    def tearDown(self):
        rmtree("project/")
        rmtree("archive")
        os.remove("legacy.txt")

    def test_generate_disabled_warning(self):

        fp = open("legacy.txt","w+")
        fp.write("# Gatsby\n")
        fp.write("\n")
        fp.write("## Part 1: The Reckoning\n")
        fp.write("\n")
        fp.write("### Chapter 1: The Promise\n")
        fp.write("\n")
        fp.write("#### New York, 1942\n")
        fp.write("\n")
        fp.write("## Part 2: The Whatever\n")
        fp.close()

        with open("settings.yml", "w+") as settings:
            settings.write("warnings:\n  parse: no")

        runner = CliRunner()
        result = runner.invoke(parse, ["legacy.txt"])
        self.assertEqual(result.exit_code, 0)

        self.assertEqual(len(os.listdir("project/Gatsby/")), 2)

        self.assertTrue(os.path.isdir("project/Gatsby/1-Part 1 The Reckoning"))
        self.assertTrue(os.path.isdir("project/Gatsby/1-Part 1 The Reckoning/1-Chapter 1 The Promise"))
        self.assertTrue(os.path.isdir("project/Gatsby/1-Part 1 The Reckoning/1-Chapter 1 The Promise/1-New York 1942"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2 The Whatever"))
        os.remove("settings.yml")

    def test_generate_file_tree(self):

        fp = open("legacy.txt","w+")
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

        runner = CliRunner()
        result = runner.invoke(parse, ["legacy.txt"], input="y\n")
        self.assertEqual(result.exit_code, 0)

        self.assertEqual(len(os.listdir("project/Gatsby/")), 3)

        self.assertTrue(os.path.isdir("project/Gatsby/1-Part 1 The Reckoning"))
        self.assertTrue(os.path.isdir("project/Gatsby/1-Part 1 The Reckoning/1-Chapter 1 The Promise"))
        self.assertTrue(os.path.isdir("project/Gatsby/1-Part 1 The Reckoning/1-Chapter 1 The Promise/1-New York 1942"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2 The Whatever"))
        self.assertTrue(os.path.isdir("project/Gatsby/3-Part 3 Tomorrow"))
        self.assertTrue(os.path.isfile("project/Gatsby/2-Part 2 The Whatever/1-The Bar.md"))

        with open("project/Gatsby/2-Part 2 The Whatever/1-The Bar.md", "r") as fp:
            lines = fp.readlines()
            self.assertEqual(lines[0],"It was a fall day.\n")
            self.assertEqual(lines[1],"It was cold.\n")
            self.assertEqual(len(lines), 2)

class TestSequence(TestCase):

    def tearDown(self):
        rmtree("project")
        pass

    def setUp(self):
        os.mkdir("project")
        os.mkdir("project/Gatsby")

        os.mkdir("project/Gatsby/01-Part 1")
        os.mkdir("project/Gatsby/01-Part 2")
        os.mkdir("project/Gatsby/01-Part 2/01-Chapter 1")
        os.mkdir("project/Gatsby/01-Part 2/01-Chapter 2")
        os.mkdir("project/Gatsby/01-Part 2/05-Chapter 3")
        os.mkdir("project/Gatsby/01-Part 2/05-Chapter 4")
        os.mkdir("project/Gatsby/03-Part 3")
        os.mkdir("project/Gatsby/04-Part 4/")
        os.mkdir("project/Gatsby/04-Part 4/01-Chapter 1")
        os.mkdir("project/Gatsby/04-Part 5")
        os.mkdir("project/Gatsby/04-Part 6")
        os.mkdir("project/Gatsby/05-Part 7")

        base = "project/Gatsby/01-Part 2/01-Chapter 1/"
        for file in ["01-Scene 1.md","01-Scene 2.md","01-Scene 3.md","01-Scene 4.md"]:
            fp = open(base + file, "w")
            fp.close()

        fp = open("project/Gatsby/04-Part 4/01-Chapter 1/02-Scene 5.md", "w")
        fp.close()

        fp = open("project/Gatsby/05-Part 7/09-Scene 6.md", "w")
        fp.close()

    def test_disabled_warning_disables_prompt(self):
        with open("settings.yml", "w+") as settings:
            settings.write("warnings:\n  sequence: no")

        runner = CliRunner()
        result = runner.invoke(sequence, input="5\n1\n2\n3\n1\n1\n1\n1\n2")
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2"))
        os.remove("settings.yml")

    def test_bad_choice_keeps_going(self):
        with open("settings.yml", "w+") as settings:
            settings.write("warnings:\n  sequence: yes")

        runner = CliRunner()
        result = runner.invoke(sequence, input="y\n5\n1\n2\n3\n1\n1\n1\n1\n2")
        self.assertEqual(result.exit_code, 0)

        self.assertTrue(os.path.isdir("project/Gatsby/1-Part 1"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2/1-Chapter 1"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2/2-Chapter 2"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2/3-Chapter 3"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2/4-Chapter 4"))
        self.assertTrue(os.path.isdir("project/Gatsby/3-Part 3"))
        self.assertTrue(os.path.isdir("project/Gatsby/4-Part 4"))
        self.assertTrue(os.path.isdir("project/Gatsby/4-Part 4/5-Chapter 1"))
        self.assertTrue(os.path.isdir("project/Gatsby/5-Part 5"))
        self.assertTrue(os.path.isdir("project/Gatsby/6-Part 6"))
        self.assertTrue(os.path.isdir("project/Gatsby/7-Part 7"))
        self.assertTrue(os.path.isfile("project/Gatsby/2-Part 2/1-Chapter 1/1-Scene 1.md"))
        self.assertTrue(os.path.isfile("project/Gatsby/2-Part 2/1-Chapter 1/2-Scene 2.md"))
        self.assertTrue(os.path.isfile("project/Gatsby/2-Part 2/1-Chapter 1/3-Scene 3.md"))
        self.assertTrue(os.path.isfile("project/Gatsby/2-Part 2/1-Chapter 1/4-Scene 4.md"))
        self.assertTrue(os.path.isfile("project/Gatsby/4-Part 4/5-Chapter 1/5-Scene 5.md"))
        self.assertTrue(os.path.isfile("project/Gatsby/7-Part 7/6-Scene 6.md"))
        os.remove("settings.yml")

    def test_duplicate_files_aborts(self):
        os.rename("project/Gatsby/01-Part 2/01-Chapter 1/01-Scene 3.md", "project/Gatsby/01-Part 2/01-Chapter 1/2-Scene 2.md")

        runner = CliRunner()
        result = runner.invoke(sequence, input="y\n1\n2\n3\n1\n1\n1\n1\n2")

        self.assertEqual(result.exit_code, 1)

    def test_sequence(self):

        runner = CliRunner()
        result = runner.invoke(sequence, input="y\n1\n2\n3\n1\n1\n1\n1\n2")
        tb = result.exc_info[2]
        print(traceback.print_tb(tb))
        print(result.exc_info)
        print(result.output)
        self.assertEqual(result.exit_code, 0)

        self.assertTrue(os.path.isdir("project/Gatsby/1-Part 1"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2/1-Chapter 1"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2/2-Chapter 2"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2/3-Chapter 3"))
        self.assertTrue(os.path.isdir("project/Gatsby/2-Part 2/4-Chapter 4"))
        self.assertTrue(os.path.isdir("project/Gatsby/3-Part 3"))
        self.assertTrue(os.path.isdir("project/Gatsby/4-Part 4"))
        self.assertTrue(os.path.isdir("project/Gatsby/4-Part 4/5-Chapter 1"))
        self.assertTrue(os.path.isdir("project/Gatsby/5-Part 5"))
        self.assertTrue(os.path.isdir("project/Gatsby/6-Part 6"))
        self.assertTrue(os.path.isdir("project/Gatsby/7-Part 7"))
        self.assertTrue(os.path.isfile("project/Gatsby/2-Part 2/1-Chapter 1/1-Scene 1.md"))
        self.assertTrue(os.path.isfile("project/Gatsby/2-Part 2/1-Chapter 1/2-Scene 2.md"))
        self.assertTrue(os.path.isfile("project/Gatsby/2-Part 2/1-Chapter 1/3-Scene 3.md"))
        self.assertTrue(os.path.isfile("project/Gatsby/2-Part 2/1-Chapter 1/4-Scene 4.md"))
        self.assertTrue(os.path.isfile("project/Gatsby/4-Part 4/5-Chapter 1/5-Scene 5.md"))
        self.assertTrue(os.path.isfile("project/Gatsby/7-Part 7/6-Scene 6.md"))

class TestStats(TestCase):

    def tearDown(self):
        rmtree("project")
        rmtree("archive")

    def setUp(self):
        os.mkdir("project")
        os.mkdir("project/Gatsby")
        os.mkdir("archive")

        os.mkdir("project/Gatsby/01-Part 1")
        os.mkdir("project/Gatsby/01-Part 2")
        os.mkdir("project/Gatsby/01-Part 2/01-Chapter 1")
        os.mkdir("project/Gatsby/01-Part 2/01-Chapter 2")
        os.mkdir("project/Gatsby/01-Part 2/01-Chapter 2/whatever")

        base = "project/Gatsby/01-Part 2/01-Chapter 1/"
        for file in ["01-Scene 1.md","01-Scene 2.md"]:
            fp = open(base + file, "w")
            fp.write("***\n")
            fp.write("This is an outline\n")
            fp.write("***\n")
            fp.write("**" + file + "**: the _world_ beckons!")
            fp.close()

    def test_stats(self):

      runner = CliRunner()
      result = runner.invoke(stats)
      self.assertEqual(result.exit_code, 0)

      self.assertEqual(result.output, "Words: 10\nScenes: 2\nSub-Chapters: 1\nChapters: 2\nSections: 2\n")
