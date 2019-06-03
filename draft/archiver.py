import os
import datetime
import shutil
import click
from draft.generator import Generator

class Archiver():

    def archive_directory(self):
        time_utc = datetime.datetime.utcnow()

        destination = time_utc.replace(microsecond=0)
        destination = 'archive/' + str(destination)

        self._copytree('project/', destination)

        return destination

    """
    Source:
    https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-
    directory-of-files-into-an-existing-directory-using-pyth/31039095
    """

    def _copytree(self, src, dst, symlinks=False, ignore=shutil.ignore_patterns('*.DS_Store')):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                d = os.path.abspath(d)
                try:
                    shutil.copytree(s, d, symlinks, ignore)
                except FileExistsError: # pragma: no cover
                    d = os.path.join(dst + '-02', item)
                    shutil.copytree(s, d, symlinks, ignore)
            else:
                if item != '.DS_Store':
                    fp = open(d, 'w')
                    fp.close()
                    shutil.copy2(s, d)

    def restore_directory(self):
        archives = os.listdir('archive')
        if len(archives) == 0:
            click.echo("You don't have any archives yet.")
        else:
            archives.sort()
            for index, archive in enumerate(archives):
                click.echo(str(len(archives) - index) + ") " + str(archive))

            value = 0
            while int(value) <= 0 or value > len(archives):
                value = click.prompt("Choose the number of the archive to restore (1-" + str(len(archives)) + "):", type=int)

            index = len(archives) - int(value)
            archive = 'archive/' + archives[index]

            self.archive_directory()
            shutil.rmtree('project')
            os.mkdir('project')
            self._copytree(archive, 'project/')
