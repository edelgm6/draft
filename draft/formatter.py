import os
import re

class Formatter():

    def clean_duplicate_spaces(file):

        pattern = ' {2,}'

        with open(file, 'r+') as file:
            text = file.read()
            text = re.sub(pattern, ' ', text)

            file.truncate(0)
            file.seek(0)
            file.write(text)

    def split_sentences(file):

        pattern = '([\"\“]?[A-Z][^\.!?]*[\.!?][\"\”]?) '
        abbreviations = ['etc.', 'Mrs.', 'Mr.', 'Dr.']

        with open(file, 'r+') as file:

            text = file.read()
            lines = re.split(pattern, text)
            lines = [line.strip() for line in lines if line not in ['',' ']]

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

            file.truncate(0)
            file.seek(0)
            file.write(text)
