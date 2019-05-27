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

        for dir in ['project', destination]:
            self.assertTrue(os.path.isdir(dir + '/Gatsby/'))

        self.assertTrue(os.path.isdir('archive'))
        self.assertTrue(os.path.isdir('archive/project'))
        self.assertTrue(os.path.isdir('archive/legacy-project'))
