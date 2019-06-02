import click
from draft.formatter import Formatter
from draft.generator import Generator
from draft.outliner import Outliner
from draft.archiver import Archiver

@click.group()
def main():
    pass # pragma: no cover

@main.command()
def restore():
    """
    Restore archived project copy.
    """
    generator = Generator()
    generator.confirm_project_layout()

    archiver = Archiver()
    archiver.restore_directory()

@main.command()
def stats():
    """
    Gets statistics from the project (e.g., word count, etc.)
    """
    generator = Generator()
    generator.confirm_project_layout()

    outliner = Outliner()
    word_count, scene_count, sub_chapter_count, chapter_count, section_count = outliner.get_statistics()

    click.echo("Words: " + str(word_count))
    click.echo("Scenes: " + str(scene_count))
    click.echo("Sub-Chapters: " + str(sub_chapter_count))
    click.echo("Chapters: " + str(chapter_count))
    click.echo("Sections: " + str(section_count))

@main.command()
def sequence():
    """
    Resets indices in folders and files and resolves duplicates.
    """
    generator = Generator()
    generator.confirm_project_layout()

    outliner = Outliner()
    outliner.update_file_sequence()

@main.command()
@click.argument('filepath', type=click.Path(exists=True, dir_okay=False))
def make_tree(filepath):
    """
    Generates a project tree based on a Markdown formatted .md or .txt file.

    Useful for generating project trees based on legacy projects or an
    outline file.
    """
    generator = Generator()
    generator.confirm_project_layout()

    outliner = Outliner()
    outliner.generate_file_tree(filepath)

@main.command()
@click.argument('filename', type=click.Path(exists=True))
def split_sentences(filename):
    """
    Splits multi-line sentences into separate lines.

    Takes a FILENAME as the argument.
    """
    formatter = Formatter(filename)
    formatter.split_sentences()

@main.command()
@click.argument('filename', type=click.Path(exists=True))
def dupe_spaces(filename):
    """
    Removes all duplicate spaces from text file.

    Takes a FILENAME as the argument. File must be in the to-process folder.
    """
    generator = Generator()
    generator.confirm_project_layout()

    formatter = Formatter(filename)
    formatter.remove_duplicate_spaces()

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
def outline():
    """
    Generates or updates a project outline.
    """
    generator = Generator()
    generator.confirm_project_layout()

    outliner = Outliner()
    outliner.compile_project()

@main.command()
def compile():
    """
    Generates or updates a project outline.
    """
    generator = Generator()
    generator.confirm_project_layout()

    outliner = Outliner()
    outliner.compile_project(draft=True)
