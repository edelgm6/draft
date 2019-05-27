import os
import datetime
import shutil
from draft.generator import Generator

class Archiver():

    def __init__(self):
        generator = Generator()
        generator.confirm_project_layout()

    def archive_directory(self, type):
        options = ['project', 'legacy-project']
        if type not in options:
            raise ValueError("Type must be project or legacy-project.")

        time_utc = datetime.datetime.utcnow()

        destination = time_utc.replace(microsecond=0)
        destination = 'archive/' + type + "/" + str(destination)

        self._copytree(type, destination)

        return destination

    """
    Source:
    https://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-
    directory-of-files-into-an-existing-directory-using-pyth/31039095
    """
    def _copytree(self, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
