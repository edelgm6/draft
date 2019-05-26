import click
from draft.formatter import Formatter

@click.group()
def main():
    pass

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

if __name__ == "__main__":
    main()
