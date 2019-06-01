import os
from click.testing import CliRunner
from shutil import rmtree
from unittest import TestCase
from draft.cli import stats, sequence, make_tree, split_sentences, dupe_spaces, create_project, outline, compile

class TestOutliners(TestCase):

    def tearDown(self):
        rmtree('project')
        rmtree('archive')

    def setUp(self):
        os.mkdir('project')
        os.mkdir('project/Gatsby')
        os.mkdir('archive')

        os.mkdir('project/Gatsby/01-Part 1')
        os.mkdir('project/Gatsby/01-Part 2')
        os.mkdir('project/Gatsby/01-Part 2/01-Chapter 1')
        os.mkdir('project/Gatsby/01-Part 2/01-Chapter 2')

        base = 'project/Gatsby/01-Part 2/01-Chapter 1/'
        for file in ['01-Scene 1.md','01-Scene 2.md']:
            fp = open(base + file, 'w')
            fp.write("***\n")
            fp.write("This is an outline\n")
            fp.write("***\n")
            fp.write("**" + file + "**: the _world_ beckons!")
            fp.close()

    def test_outline(self):
        runner = CliRunner()
        result = runner.invoke(outline)
        self.assertEqual(result.exit_code, 0)

        gatsby = open('outline.md', 'r')
        text = gatsby.read()
        gatsby.close()
        os.remove('outline.md')

        self.assertEqual(text,'# Gatsby\n\n## Part 1\n\n## Part 2\n\n### Chapter 1\n\n**Scene 1**: This is an outline\n\n**Scene 2**: This is an outline\n\n### Chapter 2\n\n')

    def test_compile(self):
        runner = CliRunner()
        result = runner.invoke(compile)
        self.assertEqual(result.exit_code, 0)

        gatsby = open('Gatsby.md', 'r')
        text = gatsby.read()
        gatsby.close()
        os.remove('Gatsby.md')

        self.assertEqual(text,'# Gatsby\n\n## Part 1\n\n## Part 2\n\n### Chapter 1\n\n**01-Scene 1.md**: the _world_ beckons!\n\n**01-Scene 2.md**: the _world_ beckons!\n\n### Chapter 2\n\n')

class TestGenerateProject(TestCase):

    def test_generate_file_tree(self):

        runner = CliRunner()
        result = runner.invoke(create_project, ['Gatsby'])
        self.assertEqual(result.exit_code, 0)

        self.assertTrue(os.path.isdir('Gatsby/project/Gatsby/'))
        self.assertTrue(os.path.isdir('Gatsby/archive'))
        rmtree('Gatsby')

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

        runner = CliRunner()
        result = runner.invoke(dupe_spaces, ['testfile.txt'])
        self.assertEqual(result.exit_code, 0)

        fp = open('testfile.txt','r')
        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\" It's the end of the world as we know it.\" \"And I feel fine. \"")

class TestSplitSentences(TestCase):

    def test_split_sentences(self):
        fp = open('testfile.txt','w+')
        fp.write("\"It's the end of the world as we know it.\" \"And I feel fine.\"")
        fp.write(" \"You are nice!\" she said.")
        fp.close()

        runner = CliRunner()
        result = runner.invoke(split_sentences, ['testfile.txt'])
        self.assertEqual(result.exit_code, 0)
        fp = open('testfile.txt','r')

        lines = fp.readlines()
        fp.close()

        self.assertEqual(lines[0],"\"It's the end of the world as we know it.\"\n")
        self.assertEqual(lines[1],"\"And I feel fine.\"\n")
        self.assertEqual(lines[2],"\"You are nice!\" she said.")
        self.assertEqual(len(lines), 3)

        os.remove('testfile.txt')

class TestFileTree(TestCase):

    def setUp(self):
        os.mkdir('project')
        os.mkdir('project/Gatsby')
        os.mkdir('archive')

    def tearDown(self):
        rmtree('project/')
        rmtree('archive')
        os.remove('legacy.txt')

    def test_generate_file_tree(self):

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

        runner = CliRunner()
        result = runner.invoke(make_tree, ['legacy.txt'])
        self.assertEqual(result.exit_code, 0)

        self.assertEqual(len(os.listdir('project/Gatsby/')), 3)

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

class TestSequence(TestCase):

    def tearDown(self):
        rmtree('project')
        rmtree('archive')

    def setUp(self):
        os.mkdir('project')
        os.mkdir('project/Gatsby')
        os.mkdir('archive')

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

        base = 'project/Gatsby/01-Part 2/01-Chapter 1/'
        for file in ['01-Scene 1.md','01-Scene 2.md','01-Scene 3.md','01-Scene 4.md']:
            fp = open(base + file, 'w')
            fp.close()

    def test_sequence(self):

        runner = CliRunner()
        result = runner.invoke(sequence, input='1\n2\n3\n1\n1\n1\n1\n2')
        self.assertEqual(result.exit_code, 0)

        self.assertTrue(os.path.isdir('project/Gatsby/01-Part 1'))
        self.assertTrue(os.path.isdir('project/Gatsby/02-Part 2'))
        self.assertTrue(os.path.isdir('project/Gatsby/02-Part 2/01-Chapter 1'))
        self.assertTrue(os.path.isdir('project/Gatsby/02-Part 2/02-Chapter 2'))
        self.assertTrue(os.path.isdir('project/Gatsby/02-Part 2/03-Chapter 3'))
        self.assertTrue(os.path.isdir('project/Gatsby/02-Part 2/04-Chapter 4'))
        self.assertTrue(os.path.isdir('project/Gatsby/03-Part 3'))
        self.assertTrue(os.path.isdir('project/Gatsby/04-Part 4'))
        self.assertTrue(os.path.isdir('project/Gatsby/05-Part 5'))
        self.assertTrue(os.path.isdir('project/Gatsby/06-Part 6'))
        self.assertTrue(os.path.isdir('project/Gatsby/07-Part 7'))

class TestStats(TestCase):

    def tearDown(self):
        rmtree('project')
        rmtree('archive')

    def setUp(self):
        os.mkdir('project')
        os.mkdir('project/Gatsby')
        os.mkdir('archive')

        os.mkdir('project/Gatsby/01-Part 1')
        os.mkdir('project/Gatsby/01-Part 2')
        os.mkdir('project/Gatsby/01-Part 2/01-Chapter 1')
        os.mkdir('project/Gatsby/01-Part 2/01-Chapter 2')
        os.mkdir('project/Gatsby/01-Part 2/01-Chapter 2/whatever')

        base = 'project/Gatsby/01-Part 2/01-Chapter 1/'
        for file in ['01-Scene 1.md','01-Scene 2.md']:
            fp = open(base + file, 'w')
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
