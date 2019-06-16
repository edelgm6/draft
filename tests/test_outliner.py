from unittest import TestCase, skip
from draft.outliner import Outliner
from draft.generator import Generator, StructureError
from draft.helpers import get_settings
import os
import yaml
from shutil import rmtree

class TestStatistics(TestCase):
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
        os.mkdir("project/Gatsby/01-Part 2/01-Chapter 2/01-Sub-Chapter3")

        base = "project/Gatsby/01-Part 2/01-Chapter 1/"
        for file in ["01-Scene 1.md","01-Scene 2.md"]:
            fp = open(base + file, "w")
            fp.write("***\n")
            fp.write("This is an outline\n")
            fp.write("***\n")
            fp.write("**" + file + "**: the _world_ beckons!")
            fp.close()

    def test_get_statistics(self):
        outliner = Outliner()
        word_count, scene_count, sub_chapter_count, chapter_count, section_count = outliner.get_statistics()

        self.assertEqual(word_count, 10)
        self.assertEqual(scene_count, 2)
        self.assertEqual(sub_chapter_count, 1)
        self.assertEqual(chapter_count, 2)
        self.assertEqual(section_count, 2)

class TestCompileProject(TestCase):

    def tearDown(self):
        rmtree("project")

    def setUp(self):
        os.mkdir("project")
        os.mkdir("project/Gatsby")

        os.mkdir("project/Gatsby/01-Part 1")
        os.mkdir("project/Gatsby/01-Part 2")
        os.mkdir("project/Gatsby/01-Part 2/01-Chapter 1")
        os.mkdir("project/Gatsby/01-Part 2/01-Chapter 1/01-SubChapter 1")
        os.mkdir("project/Gatsby/01-Part 2/01-Chapter 2")

        base = "project/Gatsby/01-Part 2/01-Chapter 1/01-SubChapter 1/"
        for file in ["01-Scene 1.md","01-Scene 2.md"]:
            fp = open(base + file, "w")
            fp.write("***\n")
            fp.write("This is an outline\n")
            fp.write("***\n")
            fp.write("**" + file + "**: the _world_ beckons!")
            fp.close()

    def test_creates_outline(self):
        outliner = Outliner()
        outliner.compile_project(draft=False)

        gatsby = open("01-outline.md", "r")
        text = gatsby.read()
        gatsby.close()
        os.remove("01-outline.md")

        self.assertEqual(text,"# Gatsby\n\n## Part 1\n\n## Part 2\n\n### Chapter 1\n\n#### SubChapter 1\n\n**Scene 1**: This is an outline\n\n**Scene 2**: This is an outline\n\n### Chapter 2\n\n")

    def test_increments_outline_if_exists(self):
        with open("02-outline.md", "w") as outline:
            outline.write("whatever")

        outliner = Outliner()
        outliner.compile_project(draft=False)

        gatsby = open("03-outline.md", "r")
        text = gatsby.read()
        gatsby.close()

        self.assertTrue(os.path.exists("03-outline.md"))
        self.assertEqual(text,"# Gatsby\n\n## Part 1\n\n## Part 2\n\n### Chapter 1\n\n#### SubChapter 1\n\n**Scene 1**: This is an outline\n\n**Scene 2**: This is an outline\n\n### Chapter 2\n\n")
        os.remove("03-outline.md")
        os.remove("02-outline.md")

    def test_outline_unaffected_by_header_settings(self):
        with open("settings.yml","w+") as settings_file:
            settings = {
                "headers": {
                    "section": False,
                    "chapter": False,
                    "sub_chapter": False
                }
            }
            settings_file.write(yaml.dump(settings))

        outliner = Outliner()
        outliner.compile_project(draft=False)

        gatsby = open("01-outline.md", "r")
        text = gatsby.read()
        gatsby.close()
        os.remove("01-outline.md")
        os.remove("settings.yml")

        self.assertEqual(text,"# Gatsby\n\n## Part 1\n\n## Part 2\n\n### Chapter 1\n\n#### SubChapter 1\n\n**Scene 1**: This is an outline\n\n**Scene 2**: This is an outline\n\n### Chapter 2\n\n")

    def test_compiles_project(self):
        outliner = Outliner()
        outliner.compile_project(draft=True)

        gatsby = open("01-Gatsby.md", "r")
        text = gatsby.read()
        gatsby.close()
        os.remove("01-Gatsby.md")

        self.assertEqual(text,"# Gatsby\n\n## Part 1\n\n## Part 2\n\n### Chapter 1\n\n#### SubChapter 1\n\n**01-Scene 1.md**: the _world_ beckons!\n\n</br>\n\n**01-Scene 2.md**: the _world_ beckons!\n\n</br>\n\n### Chapter 2\n\n")

    def test_headers_ignored_if_compiled_project(self):
        with open("settings.yml","w+") as settings_file:
            settings = {
                "headers": {
                    "section": False,
                    "chapter": False,
                    "sub_chapter": False
                }
            }
            settings_file.write(yaml.dump(settings))

        outliner = Outliner()
        outliner.compile_project(draft=True)

        gatsby = open("01-Gatsby.md", "r")
        text = gatsby.read()
        gatsby.close()
        os.remove("01-Gatsby.md")

        self.assertEqual(text,"# Gatsby\n\n</br>\n\n</br>\n\n</br>\n\n</br>\n\n**01-Scene 1.md**: the _world_ beckons!\n\n</br>\n\n**01-Scene 2.md**: the _world_ beckons!\n\n</br>\n\n</br>\n\n")

        os.remove("settings.yml")

    def test_headers_overridden(self):
        with open("settings.yml","w+") as settings_file:
            settings = {
                "overrides": {
                    "Gatsby": "The Great Gatsby",
                    "Chapter 1": "Chapter 1: Word",
                }
            }
            settings_file.write(yaml.dump(settings))

        outliner = Outliner()
        outliner.compile_project(draft=True)

        gatsby = open("01-Gatsby.md", "r")
        text = gatsby.read()
        gatsby.close()
        os.remove("01-Gatsby.md")
        os.remove("settings.yml")

        self.assertEqual(text,"# The Great Gatsby\n\n## Part 1\n\n## Part 2\n\n### Chapter 1: Word\n\n#### SubChapter 1\n\n**01-Scene 1.md**: the _world_ beckons!\n\n</br>\n\n**01-Scene 2.md**: the _world_ beckons!\n\n</br>\n\n### Chapter 2\n\n")

class TestFileTree(TestCase):

    def setUp(self):
        os.mkdir("project")
        os.mkdir("project/Gatsby")
        os.mkdir("archive")

    def tearDown(self):
        rmtree("project/")
        rmtree("archive")
        try:
            os.remove("legacy.txt")
        except FileNotFoundError:
            pass

    def test_non_mdtxt_raises_error(self):
        outliner = Outliner()
        with self.assertRaises(Exception):
            outliner.generate_file_tree("legacy.doc")

    def test_existing_settings_not_overwritten(self):
        fp = open("legacy.txt","w+")
        fp.write("# Gatsby\n")
        fp.write("\n")
        fp.write("## Part 1: The Reckoning\n")
        fp.write("\n")
        fp.write("### Chapter 1: The Promise\n")
        fp.write("\n")
        fp.write("#### New York, 1942\n")
        fp.write("##### The Bar\n")
        fp.write("\n")
        fp.write("It was a fall day.\n")
        fp.write("It was cold.\n")
        fp.close()

        with open("settings.yml", "w+") as settings_file:
            settings_file.write(yaml.dump(get_settings()))

        outliner = Outliner()
        outliner.generate_file_tree("legacy.txt")

        with open("settings.yml", "r") as settings_file:
            settings = yaml.safe_load(settings_file)

        self.assertEqual(settings, {"headers": {"chapter": True, "section": True, "sub_chapter": True}, "overrides": {"Chapter 1 The Promise": "Chapter 1: The Promise", "New York 1942": "New York, 1942", "Part 1 The Reckoning": "Part 1: The Reckoning"}, "warnings": {"parse": True, "sequence": True, "split": True, "trim": True}})

        os.remove("settings.yml")


    def test_returns_error_if_no_title(self):

        fp = open("legacy.txt","w+")
        fp.write("## Part 1: The Reckoning\n")
        fp.write("\n")
        fp.write("### Chapter 1: The Promise\n")
        fp.write("\n")
        fp.write("#### New York, 1942\n")
        fp.write("\n")
        fp.write("## Part 2: The Whatever\n")
        fp.write("\n")

        fp.close()

        outliner = Outliner()
        with self.assertRaises(StructureError):
            outliner.generate_file_tree("legacy.txt")

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
        fp.write("## Part 4 Test\n")

        fp.close()

        outliner = Outliner()
        outliner.generate_file_tree("legacy.txt")

        self.assertEqual(len(os.listdir("project/Gatsby/")),4)

        self.assertTrue(os.path.isdir("project/Gatsby/01-Part 1 The Reckoning"))
        self.assertTrue(os.path.isdir("project/Gatsby/01-Part 1 The Reckoning/01-Chapter 1 The Promise"))
        self.assertTrue(os.path.isdir("project/Gatsby/01-Part 1 The Reckoning/01-Chapter 1 The Promise/01-New York 1942"))
        self.assertTrue(os.path.isdir("project/Gatsby/02-Part 2 The Whatever"))
        self.assertTrue(os.path.isdir("project/Gatsby/03-Part 3 Tomorrow"))
        self.assertTrue(os.path.isfile("project/Gatsby/02-Part 2 The Whatever/01-The Bar.md"))

        with open("project/Gatsby/02-Part 2 The Whatever/01-The Bar.md", "r") as fp:
            lines = fp.readlines()
            self.assertEqual(lines[0],"It was a fall day.\n")
            self.assertEqual(lines[1],"It was cold.\n")
            self.assertEqual(len(lines), 2)

        with open("settings.yml", "r") as settings_file:
            settings = yaml.safe_load(settings_file)

        self.assertEqual(settings, {"overrides": {"Chapter 1 The Promise": "Chapter 1: The Promise", "New York 1942": "New York, 1942", "Part 1 The Reckoning": "Part 1: The Reckoning", "Part 2 The Whatever": "Part 2: The Whatever", "Part 3 Tomorrow": "Part 3: Tomorrow"}})

        os.remove("settings.yml")
