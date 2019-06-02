from unittest import TestCase
from draft.archiver import Archiver
import os
import datetime
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
        file = open('project/Gatsby/jaunt.txt', 'w')
        file.write('whatever')
        file.close()

        file = open('project/jaunt.txt', 'w')
        file.write('whatever')
        file.close()

        file = open('project/.DS_Store', 'w')
        file.write('whatever')
        file.close()

        file = open('project/Gatsby/.DS_Store', 'w')
        file.write('whatever')
        file.close()

        archiver = Archiver()
        destination = archiver.archive_directory()

        for dir in ['project', destination]:
            self.assertTrue(os.path.isdir(dir + '/Gatsby/'))

        archive_record = os.listdir('archive')[0]
        self.assertTrue(os.path.isfile('archive/' + archive_record + '/Gatsby/jaunt.txt'))
        self.assertFalse(os.path.isfile('archive/' + archive_record + '/Gatsby/.DS_Store.txt'))
        self.assertFalse(os.path.isfile('archive/' + archive_record + '/.DS_Store.txt'))
        self.assertTrue(os.path.isfile('archive/' + archive_record + '/jaunt.txt'))

        self.assertTrue(os.path.isdir('archive'))
