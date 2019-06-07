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

    click.secho("Words: " + str(word_count), fg="green")
    click.secho("Scenes: " + str(scene_count), fg="green")
    click.secho("Sub-Chapters: " + str(sub_chapter_count), fg="green")
    click.secho("Chapters: " + str(chapter_count), fg="green")
    click.secho("Sections: " + str(section_count), fg="green")

@main.command()
def sequence():
    """
    Resets indices in folders and files and resolves duplicates.
    """
    answer = click.confirm(click.style("Highly recommend changes are COMMITed before proceeding. Continue?", fg="red", bold=True))

    if answer:
        generator = Generator()
        generator.confirm_project_layout()

        outliner = Outliner()
        outliner.update_file_sequence()

        click.secho("Files resequenced.", fg="green")

@main.command()
@click.argument('filepath', type=click.Path(exists=True, dir_okay=False))
def parse(filepath):
    """
    Generates a project tree based on a Markdown formatted .md or .txt file.

    Useful for generating project trees based on legacy projects or an
    outline file.
    """
    answer = click.confirm(click.style("Highly recommend changes are COMMITed before proceeding. Continue?", fg="red", bold=True))

    if answer:
        generator = Generator()
        generator.confirm_project_layout()

        outliner = Outliner()
        outliner.generate_file_tree(filepath)

        click.secho("Tree generated.", fg="green")

@main.command()
@click.argument('filename', type=click.Path(exists=True), required=False)
def split(filename=None):
    """
    Splits multi-line sentences into separate lines.

    Takes a FILENAME as the argument.
    """
    if not filename:
        click.secho("WARNING: You are about to split-sentences across the " +
            "entire project tree.", fg="red", bold=True)
    answer = click.confirm(click.style("Highly recommend changes are COMMITed before proceeding. Continue?", fg="red", bold=True))

    if answer:
        formatter = Formatter(filename)
        formatter.split_sentences()

        click.secho("Sentence split complete.", fg="green")

@main.command()
@click.argument('filename', type=click.Path(exists=True), required=False)
def trim(filename=None):
    """
    Removes all duplicate spaces from text file.

    Takes a FILENAME as the argument. File must be in the to-process folder.
    """
    answer = click.confirm(click.style("Highly recommend changes are COMMITed before proceeding. Continue?", fg="red", bold=True))

    if answer:
        generator = Generator()
        generator.confirm_project_layout()

        formatter = Formatter(filename)
        formatter.remove_duplicate_spaces()

    click.secho("Duplicate spaces removed.", fg="green")

@main.command()
@click.argument('title', type=click.STRING)
def create_project(title):
    """
    Generates a project structure.

    Takes a TITLE as the argument.
    """
    generator = Generator()
    generator.generate_project(title)

    click.secho("Project " + title + " created.", fg="green")

@main.command()
def outline():
    """
    Generates or updates a project outline.
    """
    generator = Generator()
    generator.confirm_project_layout()

    outliner = Outliner()
    outliner.compile_project()

    click.secho("Project outlined.")

@main.command()
def compile():
    """
    Generates or updates a project outline.
    """
    generator = Generator()
    generator.confirm_project_layout()

    outliner = Outliner()
    outliner.compile_project(draft=True)

    click.secho("Project compiled.", fg="green")
