import re
import os
import shutil
import click
import yaml
from collections import Counter
from draft.generator import Generator, StructureError
from draft.helpers import clean_filename, get_settings

class Outliner():


    def _create_next_filename(self, filename):

        root_files = os.listdir(".")

        duplicates = [file for file in root_files if filename in file]

        sequence = str(len(duplicates) + 1).zfill(2)
        while os.path.exists(sequence + "-" + filename):
            sequence = str(int(sequence) + 1).zfill(len(sequence))

        return sequence + "-" + filename

    def _get_file_tree(self):

        outline = []
        for path, subdirs, files in os.walk("project/"):
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
            with open(file, "r") as fp:
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
        outline = self._get_file_tree()
        settings = get_settings()["headers"]
        overrides = get_settings()["overrides"]

        title = os.listdir("project")[0]
        try:
            override = overrides[title]
            title = override
        except (KeyError, TypeError):
            pass

        page = "# " + title + "\n\n"
        for branch in outline:
            if os.path.isfile(branch):
                with open(branch, "r") as sc:
                    text = sc.read().strip()
                    text = self._get_text_element(text, draft)
                    if draft:
                        page = page + text.strip() + "\n\n</br>\n\n"
                    else:
                        split_branch = branch.split("/")
                        branch_end = split_branch[-1]
                        extension_index = branch_end.rindex(".")
                        scene_name = "**" + branch_end[3:extension_index] + "**"

                        page = page + scene_name + ": " + text + "\n\n"

            elif os.path.isdir(branch):
                split_branch = branch.split("/")
                branch_end = split_branch[-1]

                try:
                    title = overrides[branch_end[3:]]
                except (KeyError, TypeError):
                    title = branch_end[3:]

                if len(split_branch) == 3:
                    if settings["section"] or not draft:
                        section = "## " + title + "\n\n"
                    else:
                        section = "\n\n</br>\n\n"

                elif len(split_branch) == 4:
                    if settings["chapter"] or not draft:
                        section = "### " + title + "\n\n"
                    else:
                        section = "\n\n</br>\n\n"

                elif len(split_branch) == 5:
                    if settings["sub_chapter"] or not draft:
                        section = "#### " + title + "\n\n"
                    else:
                        section = "\n\n</br>\n\n"
                elif len(split_branch) == 2:
                    continue

                page = page + section

        if draft:
            title = os.listdir("project")[0]
            file_name = title + ".md"
        else:
            file_name = "outline.md"

        file_name = self._create_next_filename(file_name)
        with open(file_name, "w") as fp:
            page = re.sub("\\n{3,}","\\n\\n", page)
            fp.write(page)

        return file_name


    def update_file_sequence(self):

        # Get outline of all files in tree
        outline = self._get_file_tree()

        files = [branch for branch in outline if branch[-3:] == ".md"]
        if len(files) > 99:
            sequence_base = "001" # pragma: no cover
        else:
            sequence_base = "01"

        sequences = {
            1: sequence_base,
            2: sequence_base,
            3: sequence_base,
            4: sequence_base,
            5: sequence_base,
            "file": sequence_base
        }

        leveled_branches = []
        for branch in outline:
            leveled_branch = branch.split("/")
            leveled_branches.append((len(leveled_branch), branch))

        leveled_branches.sort(reverse=True)

        levels = list(set([branch[0] for branch in leveled_branches]))
        levels.sort(reverse=True)

        outline = []
        for level in levels:
            level_list = [branch[1] for branch in leveled_branches if branch[0] == level]
            level_list.sort()
            outline += level_list

        rename_dict = {}

        branches = [branch for branch in outline if os.path.isdir(branch)]
        branches = [branch for branch in branches if len(os.listdir(branch)) > 0]

        for branch in branches:
            files = os.listdir(branch)
            files.sort()
            sequence_list = [file[:2] for file in files]

            #duplicates = [file for file in files if file[:2] in sequence_list]
            file_dict = {}
            for sequence in sequence_list:
                file_dict[sequence] = [file for file in files if file[:2] == sequence]

            for sequence, objs in file_dict.items():
                if len(objs) > 1:
                    file_dict[sequence] = self._resolve_duplicates(objs)

            ordered_files = []
            for key, objs in file_dict.items():
                for file in objs:
                    ordered_files.append(file)

            # Once all files are de-duped, re-base at 01 for each tree level and sequence
            rename_dict = {}
            for file in ordered_files:
                if file[-3:] == ".md":
                    levels = "file"
                else:
                    split_branch = branch.split("/")
                    levels = len(split_branch)
                level_sequence = sequences[levels]
                if file[:2] != level_sequence:
                    new_file_name = level_sequence + file[2:]
                    rename_dict[branch + "/" + file] = branch + "/" + new_file_name
                sequences[levels] = str(int(level_sequence) + 1).zfill(len(level_sequence))

            for old, new in rename_dict.items():
                if os.path.isfile(new) or os.path.isdir(new):
                    click.secho("Duplicate file or directory names: \n" +
                        "Want to change: " + old + " \n" +
                        "to: " + new + "\n" +
                        "but 'to' already exists.", fg="red")
                    raise click.Abort()
                else:
                    os.rename(old, new)

    def _resolve_duplicates(self, duplicates):
        rename_list = []
        counter = 1
        click.secho("There are " + str(len(duplicates)) + " files with a duplicate sequence:", fg="green")
        for duplicate in duplicates:
            click.secho(str(counter) + ") " + duplicate[3:], fg="green")
            counter += 1
        click.echo("\n")

        """
        TODO: Validate the input here
        """
        choices = list(range(1,len(duplicates) + 1))
        for duplicate in duplicates:
            value = 0
            if len(choices) == 1:
                value = choices[0]
            else:
                click.echo("Of the " + str(len(duplicates)) + " duplicates, choose the order for " + duplicate[3:])
                while value not in choices:
                    value = click.prompt("Select any of " + str(choices), type=int)

            rename_list.append((value, duplicate))
            choices.remove(value)

        rename_list.sort()
        rename_list = [rename[1] for rename in rename_list]
        return rename_list

    def generate_file_tree(self, filepath):

        source_file, extension = os.path.splitext(filepath)
        if extension not in [".txt",".md"]:
            raise Exception("File must be .txt or .md, got " + extension + ".")

        intervals = self._get_header_intervals(filepath)
        self._generate_folders(intervals, filepath)

    def _generate_folders(self, intervals, file):
        headers = list(intervals)
        current_path = "project"

        shutil.rmtree("project/")
        os.mkdir("project/")

        title = "^#{1} "
        section = "^#{2} "
        chapter = "^#{3} "
        sub_chapter = "^#{4} "
        scene = "^#{5} "

        section_count = "01"
        chapter_count = "01"
        sub_chapter_count = "01"
        scene_count = "01"

        title_path = ""
        for header in headers:
            if re.match(title, header.group(0)):
                title = header.group(0)
                title = title.strip("#")
                title = clean_filename(title)
                title_path = current_path + "/" + title

        if not title_path:
            raise StructureError("Must be a title (e.g., # The Great Gatsby) in the source file.")
        os.mkdir(title_path)

        overrides = {}

        for index, header in enumerate(headers):
            name = header.group(0)
            original_name = name.strip("#").strip()
            name = clean_filename(original_name)
            if original_name != name:
                overrides[name] = original_name

            if re.match(section, header.group(0)):
                section_path = title_path + "/" + section_count + "-" + name + "/"
                chapter_path, sub_chapter_path, scene_path = section_path, section_path, section_path

                os.mkdir(section_path)

                section_count = str(int(section_count) + 1).zfill(len(section_count))

            elif re.match(chapter, header.group(0)):
                chapter_path = section_path + chapter_count + "-" + name + "/"
                sub_chapter_path, scene_path = chapter_path, chapter_path
                os.mkdir(chapter_path)

                chapter_count = str(int(chapter_count) + 1).zfill(len(chapter_count))

            elif re.match(sub_chapter, header.group(0)):
                sub_chapter_path = chapter_path + sub_chapter_count + "-" + name + "/"
                scene_path = sub_chapter_path
                os.mkdir(sub_chapter_path)

                sub_chapter_count = str(int(sub_chapter_count) + 1).zfill(len(sub_chapter_count))

            elif re.match(scene, header.group(0)):
                scene_path = sub_chapter_path + scene_count + "-" + name + ".md"

                start_scene = header.end(0) + 1
                try:
                    end_scene = headers[index + 1].start(0)
                except IndexError:
                    end_scene = None

                with open(file, "r") as fp:
                    text = fp.read()

                scene_text = text[start_scene:end_scene]
                with open(scene_path, "w") as scene_file:
                    scene_file.write(scene_text)

                scene_count = str(int(scene_count) + 1).zfill(len(scene_count))

            try:
                with open("settings.yml", "r") as settings_file:
                    settings = yaml.safe_load(settings_file)

            except FileNotFoundError:
                settings = {}

            settings["overrides"] = overrides

            new_settings = yaml.dump(settings)
            with open("settings.yml", "w") as settings_file:
                settings_file.write(new_settings)

    def _get_header_intervals(self, file):

        section = "((?<=[\\n\s])|^)#{1,5} .*?\\n"

        with open(file, "r") as file:
            text = file.read()

            headers = re.finditer(section, text)

            return headers
