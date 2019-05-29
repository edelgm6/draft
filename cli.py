import click
from draft.formatter import Formatter
from draft.generator import Generator
from draft.outliner import Outliner

@click.group()
def main():
    generator = Generator()
    generator.confirm_project_layout()
    pass

@main.command()
def resequence_project(filepath):
    """
    Resets indices in folders and files and resolves duplicates.
    """

    outliner = Outliner()
    outliner.update_file_sequence()

@main.command()
@click.argument('filepath', type=click.Path(exists=True, dir_okay=False))
def generate_file_tree(filepath):
    """
    Generates a project tree based on a Markdown formatted .md or .txt file.

    Useful for generating project trees based on legacy projects or an
    outline file.
    """

    outliner = Outliner()
    outliner.generate_file_tree(filepath)

@main.command()
@click.argument('filename', type=click.Path(exists=True))
def split_sentences(filename):
    """
    Splits multi-line sentences into separate lines.

    Takes a FILENAME as the argument. File must be in the to-process folder.
    """

    Formatter.split_sentences(filename)

@main.command()
@click.argument('filename', type=click.Path(exists=True))
def remove_duplicate_spaces(filename):
    """
    Removes all duplicate spaces from text file.

    Takes a FILENAME as the argument. File must be in the to-process folder.
    """
    Formatter.remove_duplicate_spaces(filename)

@main.command()
@click.argument('title', type=click.STRING)
def create_project(title):
    """
    Generates a project structure.

    Takes a TITLE as the argument.
    """
    generator = Generator()
    generator.generate_project(title)

@main.command()
def update_outline():
    """
    Generates or updates a project outline.
    """
    outliner = Outliner()
    outliner.update_outline()

"""
if __name__ == "__main__":
    main()
"""
