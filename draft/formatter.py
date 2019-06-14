import os
import re
import click
import string
from draft.generator import Generator
from draft.outliner import Outliner

class Formatter():

    def __init__(self, filepath):
        self.filepath = filepath

    def remove_duplicate_spaces(self):
        pattern = " {2,}"

        if self.filepath:
            paths = [self.filepath]
        else:
            outliner = Outliner()
            files = outliner._get_file_tree()
            paths = [file for file in files if os.path.isfile(file) and file[-3:] == ".md"]

        for path in paths:
            with open(path, "r+") as file:

                text = file.read()
                text = re.sub(pattern, " ", text)

                file.truncate(0)
                file.seek(0)
                file.write(text)

    def _get_split_ratio(self, text):

        split_pattern = '[\.|\\”|\"] {0,2}\\n'
        unsplit_pattern = '[\.|?|!]\"?”? [A-Z|\"|“]'

        split_lines = len(re.findall(split_pattern, text))
        unsplit_lines = len(re.findall(unsplit_pattern, text))

        return split_lines / (split_lines + unsplit_lines)

    def split_sentences(self):

        pattern = '([\"\“]?[A-Z][^\.!?]*[\.!?][\"\”]?) {1,2}'
        abbreviations = ["etc.", "Mrs.", "Mr.", "Dr.", "Ms."]

        if self.filepath:
            paths = [self.filepath]
        else:
            outliner = Outliner()
            files = outliner._get_file_tree()
            paths = [file for file in files if os.path.isfile(file) and file[-3:] == ".md"]

        skipped_files = []

        for path in paths:
            with open(path, "r+") as file:
                text = file.read()

                # If more than half of the lines in a file is already on new lines
                # then skip it unless it was explicitly called on that file
                if self._get_split_ratio(text) > .5 and not self.filepath:
                    split_path = path.split("/")
                    name = split_path[-1]
                    skipped_files.append(name)
                    continue

                text = text.replace("\t", "")
                text = text.replace("\n", "\n\n")
                lines = re.split(pattern, text)
                lines = [line for line in lines if line]

                skip = False
                kill_index = []
                for index, line in enumerate(lines):
                    if skip:
                        skip = False
                        kill_index.append(index)
                        continue

                    for abbreviation in abbreviations:
                        if line.endswith(abbreviation):
                            line = line + " " + lines[index + 1]
                            lines[index] = line
                            skip = True
                            break

                    try:
                        if lines[index + 1][0].islower():
                            line = line + " " + lines[index + 1]
                            lines[index] = line
                            skip = True
                    except IndexError:
                        pass

                lines = [line for index, line in enumerate(lines) if index not in kill_index]
                text = "\n".join(lines)
                text = re.sub("\\n{3,}","\\n\\n", text)
                text = text.replace(" \n","\n")

                file.truncate(0)
                file.seek(0)
                file.write(text)

        for file in skipped_files:
            click.secho(file, fg="red")

        if skipped_files:
            click.secho("Above files skipped since >50% of lines are already separated", fg="red")
            click.secho("You can force by running `draft trim filepath`", fg="red")
