import re
import os
import mistune
import shutil
import click
from draft.archiver import Archiver
from draft.generator import Generator

class Outliner():

    def _get_file_tree(self):
        title = os.listdir('project')

        outline = []
        for path, subdirs, files in os.walk('project/' + title[0]):
            for dir in subdirs:
                outline.append(os.path.join(path, dir))
            for name in files:
                outline.append(os.path.join(path, name))

        outline.sort()
        return outline

    def update_file_sequence(self):
        """
        TODO: Add in something that checks that all files
        are named correctly.
        """

        archiver = Archiver()
        archiver.archive_directory()

        outline = self._get_file_tree()

        for item in outline:
            print(item)

        title = os.listdir('project')[0]
        base_dir = 'project/' + title + '/'
        files = os.listdir(base_dir)
        files.sort()

        previous_file = files[0]
        sequence = previous_file[:2]
        duplicates = [(previous_file, base_dir + previous_file)]
        for file in files[1:]:
            if file[:2] == sequence:
                duplicates.append((file, base_dir + file))
            else:
                break

        click.echo("There are " + str(len(duplicates)) + " files with the " + sequence + " sequence:")
        for duplicate in duplicates:
            click.echo(duplicate[0])
        click.echo("\n")

        """
        TODO: Validate the input here
        """
        for duplicate in duplicates:
            value = click.prompt("What sequence should " + duplicate[0] + " have? \nMust be a two digit number (e.g., 01, 02, 10, 11, etc.)")
            print(value)
            directory_split = duplicate[1].split('/')
            new_file_name = value + duplicate[0][2:]
            directory_split[-1] = new_file_name
            new_directory = "/".join(directory_split)
            os.rename(duplicate[1], new_directory)

    def update_outline(self):
        title = os.listdir('project')
        outline = self._get_file_tree()

        clean_outline = []
        for entry in outline:
            entry = entry.split('/')
            clean_outline.append(entry[2:])

        outline_tag = '(?<=======\\n).*(?=\\n======)'

        markdown = mistune.Markdown()
        page = markdown("# " + title[0] + "\n\n")

        for entry in clean_outline:
            if len(entry) == 1:
                section = entry[0]
                page = page + markdown("## " + section + "\n\n")

            elif len(entry) == 2:
                chapter = entry[-1]
                page = page + markdown("### " + chapter + "\n\n")

            elif len(entry) == 3:
                sub_chapter = entry[-1]
                page = page + markdown("#### " + sub_chapter + "\n\n")

            elif len(entry) == 4:
                dir = 'project/' + os.listdir('project')[0] + '/' + '/'.join(entry)
                #scene = entry[-1]
                scene = os.path.splitext(dir)[0]
                scene_entry = scene

                with open(dir, 'r') as sc:
                    text = sc.read().strip()
                    scene_detail = re.search(outline_tag, text)
                    scene_entry = scene_entry + ": " + scene_detail.group(0)
                    page = page + markdown(scene_entry)

        with open('outline.md', 'w') as outline:
            outline.write(page)

    def generate_file_tree(self, filepath):

        archiver = Archiver()
        archiver.archive_directory()

        project = os.listdir('project')
        project = project[0]

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
