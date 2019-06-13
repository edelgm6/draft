import os
from draft.helpers import clean_filename

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class StructureError(Error):
    """Exception raised for errors in the project Structure.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message

class Generator():

    def _create_simple_name(self, title):
        articles = ["the","a","on","with","of","in","and"]
        title = clean_filename(title)

        split_title = title.lower().split()

        clean_split = [word for word in split_title if word not in articles]
        if len(clean_split) > 0:
            split_title = clean_split

        new_title = ("-").join(split_title[:2])
        return new_title

    def confirm_project_layout(self):

        try:
            project_files = os.listdir('project')
        except FileNotFoundError:
            raise StructureError("project/ folder missing. Try running generate-project to create a layout.")

        if '.DS_Store' in project_files:
            project_files.remove('.DS_Store')
        if len(project_files) > 1:
            raise StructureError("project/ folder has more than one directory:" + str(project_files))

    def generate_project(self, title):
        root = self._create_simple_name(title)
        title = clean_filename(title)
        os.mkdir(root)
        os.mkdir(root + '/project')
        os.mkdir(root + '/project/' + title)

        with open("draft/settings.yml","r") as yaml:
            text = yaml.read()

        with open(root + "/settings.yml", "w+") as yaml:
            yaml.write(text)
