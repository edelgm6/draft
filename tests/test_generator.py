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

        os.mkdir("project")
        dsstore = open("project/.DS_Store", "w")
        dsstore.write("whatever")
        dsstore.close()

        generator = Generator()
        generator.confirm_project_layout()

        rmtree("project")

    def test_multiple_dirs_in_project_raises_error(self):

        os.mkdir("project")
        dsstore = open("project/.DS_Store", "w")
        dsstore.write("whatever")
        dsstore.close()

        whatever = open("project/whatever", "w")
        whatever.write("whatever")
        whatever.close()

        os.mkdir("project/jaunt")

        generator = Generator()

        with self.assertRaises(StructureError):
            generator.confirm_project_layout()

        rmtree("project")

class TestFileTree(TestCase):

    def tearDown(self):
        try:
            os.remove("gatsby/settings.yml")
        except:
            pass

        try:
            rmtree("Gatsby")
        except:
            try:
                rmtree("great-gatsby")
            except:
                pass

    def test_file_names_sanitized(self):
        generator = Generator()
        generator.generate_project("The Great Gatsby!")

        self.assertTrue(os.path.isdir("great-gatsby/project/The Great Gatsby/"))

    def test_simple_name_removes_articles(self):

        titles = [
            ("The Great Gatsby","great-gatsby"),
            ("Catcher In The Rye","catcher-rye"),
            ("A Light In August","light-august"),
            ("On Writing","writing"),
            ("Of Mice And Men","mice-men"),
            ("Gatsby","gatsby")
        ]

        generator = Generator()

        for title in titles:
            shortened = generator._create_simple_name(title[0])
            self.assertEqual(shortened, title[1])

    def test_root_is_shortened_title(self):
        generator = Generator()
        generator.generate_project("The Great Gatsby")

        self.assertTrue(os.path.isdir("great-gatsby/project/The Great Gatsby/"))

    def test_generate_file_tree_does_not_overwrite_existing_files(self):

        os.mkdir("gatsby")
        os.mkdir("gatsby/project")
        os.mkdir("gatsby/project/arbitrary")
        with open("gatsby/project/arbitrary/whatever.txt", "w") as test:
            test.write("whatever")

        generator = Generator()
        generator.generate_project("Gatsby2")

        self.assertTrue(os.path.isdir("gatsby/project/arbitrary/"))
        self.assertTrue(os.path.isfile("gatsby/project/arbitrary/whatever.txt"))

        with self.assertRaises(FileExistsError):
            generator.generate_project("Gatsby")

        rmtree("gatsby2")

    def test_generate_file_tree(self):
        generator = Generator()
        generator.generate_project("Gatsby")

        self.assertTrue(os.path.isdir("gatsby/project/Gatsby/"))
        self.assertTrue(os.path.isfile("gatsby/settings.yml"))
        self.assertTrue(os.path.isfile("gatsby/.gitignore"))

        rmtree("gatsby")
