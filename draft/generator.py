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

        try:
            archive_folder = os.listdir('archive')
        except FileNotFoundError:
            raise StructureError("archive/ folder missing. Try running generate-project to create a layout.")

        if '.DS_Store' in project_files:
            project_files.remove('.DS_Store')
        if len(project_files) > 1:
            raise StructureError("project/ folder has more than one directory:" + project_files)

    def generate_project(self, title):

        os.mkdir(title)
        os.mkdir(title + '/project')
        os.mkdir(title + '/project/' + title)

        with open(title + "/tryme.txt", "w") as file:
            file.write("# Legacy-Project\n")
            file.write('\n')
            file.write("## Section1\n")
            file.write('\n')
            file.write("### Explanation\n")
            file.write('\n')
            file.write("##### Detail\n")
            file.write('\n')
            file.write("If applicable, your legacy project goes here as a .txt file.")
            file.write('\n')
            file.write(
                "Separate out into Sections, Chapters, Sub-chapters, and "
                "Scenes to via Markdown take advantage of the Outliner "
                "functionality.\n")

            file.write("Try running `draft generate-file-tree tryme.txt` to see how you can "
                "turn a Markdown or Textfile doc into a directory.\n")

        os.mkdir(title + '/archive')
