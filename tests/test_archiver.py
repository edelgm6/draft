from unittest import TestCase
from draft.archiver import Archiver
from draft.generator import Generator
import os
from shutil import rmtree


class TestArchiveDirectory(TestCase):

    def setUp(self):
        os.mkdir('project')
        os.mkdir('project/Gatsby')
        os.mkdir('archive')

    def tearDown(self):
        rmtree('project')
        rmtree('archive')

    def test_copies_files(self):
        archiver = Archiver()
        destination = archiver.archive_directory()

        for dir in ['project', destination]:
            self.assertTrue(os.path.isdir(dir + '/Gatsby/'))

        self.assertTrue(os.path.isdir('archive'))
