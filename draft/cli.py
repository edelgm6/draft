import os
import click
from draft.formatter import Formatter
from draft.generator import Generator
from draft.outliner import Outliner
from draft.helpers import get_settings

def _get_filepath(filename):

    outliner = Outliner()
    project_outline = outliner._get_file_tree()
    root_files = os.listdir(".")

    filepaths = [file for file in project_outline if file.split("/")[-1] == filename]

    filepaths += [file for file in root_files if file == filename]

    if len(filepaths) == 1:
        return filepaths[0]
    elif len(filepaths) == 0:
        raise click.ClickException("No files matching " + filename + " found.")
    else:
        error_msg = "Multiple files matching " + filename + " found:"
        for filepath in filepaths:
            error_msg += "\n" + filepath
        raise click.ClickException(error_msg)

@click.group()
def main():
    pass # pragma: no cover

@main.command()
def stats():
    """Gets statistics from the project (e.g., word count, etc.)

    :return: word_count, scene_count, sub_chapter_count, chapter_count, section_count
    :rtype: int

    Usage:
      >>> draft stats
      >>> Words: 54034
      >>> Scenes: 67
      >>> Sub-Chapters: 30
      >>> Chapters: 10
      >>> Sections: 3

    """

    generator = Generator()
    generator.confirm_project_layout()

    outliner = Outliner()
    word_count, scene_count, sub_chapter_count, chapter_count, section_count = outliner.get_statistics()

    click.secho("Words: " + str(word_count), fg="green")
    click.secho("Scenes: " + str(scene_count), fg="green")
    click.secho("Sub-Chapters: " + str(sub_chapter_count), fg="green")
    click.secho("Chapters: " + str(chapter_count), fg="green")
    click.secho("Sections: " + str(section_count), fg="green")

@main.command()
def sequence():
    """Resets indices in folders and files and resolves duplicates.

    Usage:
      >>> draft sequence

    """

    settings = get_settings()
    present_warning = settings["warnings"]["sequence"]

    answer = False
    if present_warning:
        answer = click.confirm(click.style("Highly recommend changes are COMMITed before proceeding. Continue?", fg="red", bold=True))

    if answer or not present_warning:
        generator = Generator()
        generator.confirm_project_layout()

        outliner = Outliner()
        outliner.update_file_sequence()

        click.secho("Files resequenced.", fg="green")

@main.command()
@click.argument("filename")
def parse(filename):
    """Generates a project tree based on a Markdown formatted file.
    Useful for generating project trees based on legacy projects or an outline file.

    Will automatically strip punctuation out of Markdown headers for folder names, but will preserve them in the 'overrides' section of settings.yml for use in compiling.

    :param str filename: Filename (i.e., not the full path) to be parsed (must include extension).
    :return: None

    Usage:
      >>> draft parse mobydick.md
    """
    settings = get_settings()
    present_warning = settings["warnings"]["parse"]

    answer = False
    if present_warning:
        answer = click.confirm(click.style("Highly recommend changes are COMMITed before proceeding. Continue?", fg="red", bold=True))

    if answer or not present_warning:
        generator = Generator()
        generator.confirm_project_layout()

        outliner = Outliner()
        filepath = _get_filepath(filename)
        outliner.generate_file_tree(filepath)

        click.secho("Tree generated.", fg="green")

@main.command()
@click.argument("filename", required=False)
def split(filename=None):
    """Splits multi-line sentences into separate lines.
    Affects all project files unless filepath is passed as an argument.

    :param str filename: (optional) Filename (i.e., not the full path) to be parsed (must include extension).
    :return: None

    Usage:
      >>> draft split '01-Meeting Ishmael.md'
    """
    settings = get_settings()
    present_warning = settings["warnings"]["split"]

    answer = False
    if present_warning:
        if not filename:
            click.secho("WARNING: You are about to split sentences across the " + "entire project tree.", fg="red", bold=True)
        answer = click.confirm(click.style("Highly recommend changes are COMMITed before proceeding. Continue?", fg="red", bold=True))

    if answer or not present_warning:
        if filename:
            filename = _get_filepath(filename)
        formatter = Formatter(filename)
        formatter.split_sentences()

        click.secho("Sentence split complete.", fg="green")

@main.command()
@click.argument("filename", required=False)
def trim(filename=None):
    """Removes all duplicate spaces from text.
    Acts on every file in project unless filepath argument passed.

    :param str filepath: (optional) Filename (i.e., not the full path) to be parsed (must include extension).
    :return: None

    Usage:
      >>> draft trim '01-Meeting Ishmael.md'

    """
    settings = get_settings()
    present_warning = settings["warnings"]["trim"]

    answer = False
    if present_warning:
        answer = click.confirm(click.style("Highly recommend changes are COMMITed before proceeding. Continue?", fg="red", bold=True))

    if answer or not present_warning:
        generator = Generator()
        generator.confirm_project_layout()

        if filename:
            filename = _get_filepath(filename)
        formatter = Formatter(filename)
        formatter.remove_duplicate_spaces()

    click.secho("Duplicate spaces removed.", fg="green")

@main.command()
@click.argument("title", type=click.STRING)
def create_project(title):
    """Generates a project structure.
    The root file name will be the title but: lower case, spaces replaced with dashes, and only the first two words (minus articles like 'and', 'of', etc.)

    :param str title: Title for the project.
    :return: None

    Usage:
      >>> draft generate-project 'Catcher In The Rye'

    """

    generator = Generator()
    generator.generate_project(title)

    click.secho("Project " + title + " created.", fg="green")

@main.command()
def outline():
    """Generates a new project outline.

    Usage:
      >>> draft outline

    """
    generator = Generator()
    generator.confirm_project_layout()

    outliner = Outliner()
    filename = outliner.compile_project()

    click.secho("Project outlined at " + filename + ".", fg="green")

@main.command()
def compile():
    """Compiles the project into markdown and HTML documents.

    Usage:
      >>> draft compile

    """
    generator = Generator()
    generator.confirm_project_layout()

    outliner = Outliner()
    filename = outliner.compile_project(draft=True)

    click.secho("Project compiled at " + filename + ".", fg="green")
