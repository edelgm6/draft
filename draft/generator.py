import os

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

        os.mkdir(title)
        os.mkdir(title + '/project')
        os.mkdir(title + '/project/' + title)
