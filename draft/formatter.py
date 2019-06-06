import os
import re
from draft.archiver import Archiver
from draft.generator import Generator
from draft.outliner import Outliner

class Formatter():

    def __init__(self, filename):
        self.filename = filename

    def remove_duplicate_spaces(self):
        pattern = ' {2,}'

        with open(self.filename, 'r+') as file:

            text = file.read()
            text = re.sub(pattern, ' ', text)

            file.truncate(0)
            file.seek(0)
            file.write(text)

    def split_sentences(self):

        pattern = '([\"\“]?[A-Z][^\.!?]*[\.!?][\"\”]?) {1,2}'
        abbreviations = ['etc.', 'Mrs.', 'Mr.', 'Dr.']

        if self.filename:
            paths = [self.filename]
        else:
            outliner = Outliner()
            files = outliner._get_file_tree()
            paths = [file for file in files if os.path.isfile(file) and file[-3:] == ".md"]

        for path in paths:
            with open(path, 'r+') as file:
                text = file.read()

                text = text.replace('\t', '')
                text = text.replace('\n', '\n\n')
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
                            line = line + ' ' + lines[index + 1]
                            lines[index] = line
                            skip = True
                            break

                    try:
                        if lines[index + 1][0].islower():
                            line = line + ' ' + lines[index + 1]
                            lines[index] = line
                            skip = True
                    except IndexError:
                        pass

                lines = [line for index, line in enumerate(lines) if index not in kill_index]
                text = "\n".join(lines)
                text = text.replace('\n\n\n', '\n\n')
                text = text.replace(' \n','\n')

                file.truncate(0)
                file.seek(0)
                file.write(text)
