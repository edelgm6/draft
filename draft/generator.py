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

        if len(project_files) != 1:
            raise StructureError("project/ folder has more than one directory.")

        try:
            archive_folder = os.listdir('archive')
        except FileNotFoundError:
            raise StructureError("archive/ folder missing. Try running generate-project to create a layout.")

        if len(project_files) != 1:
            raise StructureError("project/ folder has more than one directory.")

    def generate_project(self, title):

        os.mkdir('project')
        os.mkdir('project/' + title)
        os.mkdir('project/' + title + "/01-Section 1")
        os.mkdir('project/' + title + "/01-Section 1/01-Chapter 1")
        os.mkdir('project/' + title + "/01-Section 1/01-Chapter 1/01-Sub-Chapter 1")

        with open('project/' + title + "/01-Section 1/01-Chapter 1/01-Sub-Chapter 1/01-Scene 1.md", "w") as file:
            file.write('======\n')
            file.write('In this scene shit gets real.\n')
            file.write('======\n')
            file.write('#### Scene 1\n')
            file.write('\n')
            file.write('Your genius awaits.')

        os.mkdir("legacy-project")
        with open("legacy-project/legacy.txt", "w") as file:
            file.write("If applicable, your legacy project goes here as a .txt file.")
            file.write('\n')
            file.write(
                "Separate out into Sections (e.g., # Section), Chapters \n"
                "(e.g., ## Chapter), Sub-chapters (e.g., ### Sub-chapter), and \n"
                "Scenes (e.g., ####) to take advantage of the Outliner \n"
                "functionality.")

        os.mkdir('archive')
        os.mkdir('archive/project')
        os.mkdir('archive/legacy-project')
