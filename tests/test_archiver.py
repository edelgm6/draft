from unittest import TestCase
from draft.archiver import Archiver
from draft.generator import Generator
import os
from shutil import rmtree


class TestArchiveDirectory(TestCase):

    def tearDown(self):
        rmtree('legacy-project')
        rmtree('project')
        rmtree('archive')

    def test_copies_files(self):
        generator = Generator()
        generator.generate_project('Gatsby')

        archiver = Archiver()
        destination = archiver.archive_directory('project')

        self.assertEqual(len(os.listdir('project/Gatsby/')),1)

        for dir in ['project', destination]:
            self.assertTrue(os.path.isdir(dir + '/Gatsby/01-Section 1'))
            self.assertTrue(os.path.isdir(dir + '/Gatsby/01-Section 1/01-Chapter 1'))
            self.assertTrue(os.path.isdir(dir + '/Gatsby/01-Section 1/01-Chapter 1/01-Sub-Chapter 1'))
            self.assertTrue(os.path.isfile(dir + '/Gatsby/01-Section 1/01-Chapter 1/01-Sub-Chapter 1/01-Scene 1.md'))

        self.assertTrue(os.path.isdir('archive'))
        self.assertTrue(os.path.isdir('archive/project'))
        self.assertTrue(os.path.isdir('archive/legacy-project'))
