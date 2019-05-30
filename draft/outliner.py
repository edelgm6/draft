import re
import os
import shutil
import click
from draft.archiver import Archiver
from draft.generator import Generator

class Outliner():

    def _get_file_tree(self):

        outline = []
        for path, subdirs, files in os.walk('project/'):
            for dir in subdirs:
                outline.append(os.path.join(path, dir))
            for name in files:
                outline.append(os.path.join(path, name))

        outline.sort()
        return outline

    def get_statistics(self):

        outline = self._get_file_tree()
        files = []
        dirs = []

        for branch in outline:
            if os.path.isfile(branch) and branch[-3:] == ".md":
                files.append(branch)
            elif os.path.isdir(branch):
                dirs.append(branch)

        section_count = 0
        chapter_count = 0
        sub_chapter_count = 0

        for dir in dirs:
            split_branch = dir.split("/")
            print(split_branch)
            print(len(split_branch))
            levels = len(split_branch)
            if levels == 3:
                section_count += 1
            elif levels == 4:
                chapter_count += 1
            elif levels == 5:
                sub_chapter_count += 1

        scene_count = len(files)
        word_count = 0
        for file in files:
            with open(file, 'r') as fp:
                content = fp.read()
                text = self._get_text_element(content, draft=True)
                word_count += len(text.split())

        return word_count, scene_count, sub_chapter_count, chapter_count, section_count

    # Get the text in a file that is after the outline
    def _get_text_element(self, text, draft=False):
        outline_tag = '(?<=\*{3}\n).*(?=\n\*{3})'
        text = text.strip()
        scene_detail = re.search(outline_tag, text)
        if scene_detail:
            outline = scene_detail.group(0)
            outline_span = scene_detail.span()
            text = text[outline_span[1] + 4:]

        if draft:
            return text.strip()
        else:
            return outline.strip()

    def compile_project(self, draft=False):
        title = os.listdir('project')[0]
        outline_tag = '(?<=\*{3}\n).*(?=\n\*{3})'
        outline = self._get_file_tree()

        page = ""
        for branch in outline:
            if os.path.isfile(branch):
                with open(branch, 'r') as sc:
                    text = sc.read().strip()
                    text = self._get_text_element(text, draft)
                    if draft:
                        page = page + text.strip() + "\n\n"
                    else:
                        split_branch = branch.split("/")
                        branch_end = split_branch[-1]
                        extension_index = branch_end.rindex(".")
                        scene_name = "**" + branch_end[3:extension_index] + "**"

                        page = page + scene_name + ": " + text + "\n\n"

            elif os.path.isdir(branch):
                split_branch = branch.split("/")
                branch_end = split_branch[-1]
                if len(split_branch) == 2:
                    section = branch_end
                    page = page + "# " + section + "\n\n"

                elif len(split_branch) == 3:
                    chapter = branch_end[3:]
                    page = page + "## " + chapter + "\n\n"

                elif len(split_branch) == 4:
                    sub_chapter = branch_end[3:]
                    page = page + "### " + sub_chapter + "\n\n"

        if draft:
            file_name = title + '.md'
        else:
            file_name = 'outline.md'
        with open(file_name, 'w') as fp:
            fp.write(page)


    def update_file_sequence(self):
        """
        TODO: Add in something that checks that all files
        are named correctly.
        TODO: Add in something that checks to make sure there are not
        more than 99 files
        TODO: Add a method to more cleanly change the name of a directory (gets repeated a lot)
        TODO: Test with markdown files
        """

        archiver = Archiver()
        archiver.archive_directory()

        # Get outline of all files in tree
        outline = self._get_file_tree()

        # Build up base of all files in first level directory
        title = os.listdir('project')[0]
        base_dir = 'project/' + title + '/'

        leveled_branches = []
        for branch in outline:
            leveled_branch = branch.split('/')
            leveled_branches.append((len(leveled_branch), branch))

        leveled_branches.sort(reverse=True)

        levels = list(set([branch[0] for branch in leveled_branches]))
        levels.sort(reverse=True)

        outline = []
        for level in levels:
            level_list = [branch[1] for branch in leveled_branches if branch[0] == level]
            level_list.sort()
            outline += level_list

        for branch in outline:
            if os.path.isfile(branch):
                continue
            if len(os.listdir(branch)) == 0:
                continue

            no_duplicates = False
            while not no_duplicates:
                no_duplicates = True
                try:
                    files = os.listdir(branch)
                except NotADirectoryError:
                    files = []
                    break
                files.sort()

                # Find if there are any duplicates
                first_file = files[0]
                sequence = first_file[:2]
                for file in files[1:]:
                    if file[:2] == sequence:
                        no_duplicates = False
                        break
                    else:
                        sequence = file[:2]
                if no_duplicates:
                    break

                # If there are duplicates, find all of the duplicates
                duplicates = []
                for file in files:
                    if file[:2] == sequence:
                        duplicates.append((file, branch + "/" + file))

                for file in files:
                    if int(file[:2]) > int(sequence):
                        rank = str(int(file[:2]) + len(duplicates)).zfill(len(sequence))
                        new_file_name = rank + file[2:]
                        os.rename(branch + "/" + file, branch + "/" + new_file_name)


                self._resolve_duplicates(duplicates, sequence)

            sequence = '01'
            for file in files:
                if file[:2] != sequence:
                    new_file_name = sequence + file[2:]
                    os.rename(branch + "/" + file, branch + "/" + new_file_name)
                sequence = str(int(sequence) + 1).zfill(len(sequence))

    def _resolve_duplicates(self, duplicates, sequence):
        counter = 1
        click.echo("There are " + str(len(duplicates)) + " files with a duplicate sequence:")
        for duplicate in duplicates:
            click.echo(str(counter) + ") " + duplicate[0][3:])
            counter += 1
        click.echo("\n")

        """
        TODO: Validate the input here
        """
        choices = list(range(1,len(duplicates) + 1))
        for duplicate in duplicates:
            if len(choices) == 1:
                value = choices[0]
            else:
                click.echo("Of the " + str(len(duplicates)) + " duplicates, choose the order for " + duplicate[0][3:])
                value = click.prompt("Select any of " + str(choices), type=int)

            rank = str(int(sequence) + value - 1).zfill(len(sequence))

            directory_split = duplicate[1].split('/')
            new_file_name = rank + duplicate[0][2:]
            directory_split[-1] = new_file_name
            new_directory = "/".join(directory_split)
            os.rename(duplicate[1], new_directory)
            choices.remove(value)

    def generate_file_tree(self, filepath):

        archiver = Archiver()
        archiver.archive_directory()

        if not os.path.isfile(filepath):
            raise ValueError(filepath + " does not exist.")

        source_file, extension = os.path.splitext(filepath)
        if extension not in ['.txt','.md']:
            raise Exception('File must be .txt or .md, got ' + extension + '.')

        intervals = self._get_header_intervals(filepath)
        self._generate_folders(intervals, filepath)

    def _generate_folders(self, intervals, file):
        headers = list(intervals)
        current_path = 'project'

        shutil.rmtree('project/')
        os.mkdir('project/')

        title = "^#{1} "
        section = "^#{2} "
        chapter = "^#{3} "
        sub_chapter = "^#{4} "
        scene = "^#{5} "

        section_count = '01'
        chapter_count = '01'
        sub_chapter_count = '01'
        scene_count = '01'

        title_path = ''
        for header in headers:
            if re.match(title, header.group(0)):
                title = header.group(0)
                title = title.strip('#')
                title = title.strip()
                title_path = current_path + "/" + title

        if not title_path:
            raise StructureError("Must be a title (e.g., # The Great Gatsby) in the source file.")
        try:
            os.mkdir(title_path)
        except FileExistsError:
            pass

        for index, header in enumerate(headers):
            name = header.group(0)

            if re.match(section, header.group(0)):
                name = name.strip('#')
                name = name.strip()
                section_path = title_path + "/" + section_count + "-" + name + "/"
                chapter_path, sub_chapter_path, scene_path = section_path, section_path, section_path
                try:
                    os.mkdir(section_path)
                except FileExistsError:
                    pass

                section_count = str(int(section_count) + 1).zfill(len(section_count))

            elif re.match(chapter, header.group(0)):
                name = name.strip('#')
                name = name.strip()
                chapter_path = section_path + chapter_count + "-" + name + "/"
                sub_chapter_path, scene_path = chapter_path, chapter_path
                try:
                    os.mkdir(chapter_path)
                except FileExistsError:
                    pass

                chapter_count = str(int(chapter_count) + 1).zfill(len(chapter_count))

            elif re.match(sub_chapter, header.group(0)):
                name = name.strip('#')
                name = name.strip()
                sub_chapter_path = chapter_path + sub_chapter_count + "-" + name + "/"
                scene_path = sub_chapter_path
                try:
                    os.mkdir(sub_chapter_path)
                except FileExistsError:
                    pass

                sub_chapter_count = str(int(sub_chapter_count) + 1).zfill(len(sub_chapter_count))

            elif re.match(scene, header.group(0)):
                name = name.strip('#')
                name = name.strip()
                scene_path = sub_chapter_path + scene_count + "-" + name + ".md"

                start_scene = header.end(0) + 1
                try:
                    end_scene = headers[index + 1].start(0)
                except IndexError:
                    end_scene = None

                with open(file, 'r') as fp:
                    text = fp.read()

                scene_text = text[start_scene:end_scene]
                try:
                    with open(scene_path, 'w') as scene_file:
                        scene_file.write(scene_text)
                except FileExistsError:
                    pass

                scene_count = str(int(scene_count) + 1).zfill(len(scene_count))


    def _get_header_intervals(self, file):

        section = "((?<=[\\n\s])|^)#{1,5} .*?\\n"

        with open(file, 'r') as file:
            text = file.read()

            headers = re.finditer(section, text)

            return headers
