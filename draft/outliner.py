import re
import os
import shutil
import click
import yaml
import mistune
from collections import Counter
from draft.generator import Generator, StructureError
from draft.helpers import clean_filename, get_settings

class Outliner():


    def _create_next_filename(self, filename):

        root_files = os.listdir(".")

        duplicates = [file for file in root_files if filename in file]
        if len(duplicates) == 0:
            return filename
        else:
            sequence = str(len(duplicates))
            while os.path.exists(sequence + "-" + filename):
                sequence = str(int(sequence) + 1)

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
            outline = scene_detail.group(0).strip()
            outline_span = scene_detail.span()
            text = text[outline_span[1] + 4:]
        else:
            outline = ""

        if draft:
            return text.strip()
        else:
            return outline

    def compile_project(self, draft=False):
        outline = self._get_file_tree()
        settings = get_settings()
        headers = settings["headers"]
        overrides = settings["overrides"]
        author = settings["author"]
        SECTION_BREAK = "\n\n<br>\n\n"

        title = os.listdir("project")[0]
        try:
            override = overrides[title]
            title = override
        except (KeyError, TypeError):
            pass

        page = "# " + title + "\n\n"
        if author:
            page = page + "##### " + author + "\n\n"
        for branch in outline:
            if os.path.isfile(branch):
                with open(branch, "r") as sc:
                    text = sc.read().strip()
                    text = self._get_text_element(text, draft)

                    # i.e., if we're making an outline and there is some outline text
                    if text and not draft:
                        text = ": " + text
                    if draft:
                        page = page + text.strip() + SECTION_BREAK
                    else:
                        split_branch = branch.split("/")
                        branch_end = split_branch[-1]
                        extension_index = branch_end.rindex(".")
                        _, sequence_index = self._get_sequence_index(branch_end)
                        scene_name = "**" + branch_end[sequence_index + 1:extension_index] + "**"

                        page = page + scene_name + text + "\n\n"

            elif os.path.isdir(branch):
                split_branch = branch.split("/")
                branch_end = split_branch[-1]

                _, sequence_index = self._get_sequence_index(branch_end)
                try:
                    title = overrides[branch_end[sequence_index + 1:]]
                except (KeyError, TypeError):
                    title = branch_end[sequence_index + 1:]

                if len(split_branch) == 3:
                    if headers["section"] or not draft:
                        section = "## " + title + "\n\n"
                    else:
                        section = SECTION_BREAK

                elif len(split_branch) == 4:
                    if headers["chapter"] or not draft:
                        section = "### " + title + "\n\n"
                    else:
                        section = SECTION_BREAK

                elif len(split_branch) == 5:
                    if headers["sub_chapter"] or not draft:
                        section = "#### " + title + "\n\n"
                    else:
                        section = SECTION_BREAK
                elif len(split_branch) == 2:
                    continue

                page = page + section

        if draft:
            title = os.listdir("project")[0]
            file_name = title + ".md"
            html_name = title + ".html"
        else:
            file_name = "outline.md"
            html_name = "outline.html"

        file_name = self._create_next_filename(file_name)
        with open(file_name, "w") as fp:
            page = re.sub("\\n{3,}","\\n\\n", page)
            fp.write(page)

            with open(html_name, "w") as ht:
                renderer = mistune.Renderer(escape=False, hard_wrap=False)
                # use this renderer instance
                markdown = mistune.Markdown(renderer=renderer)
                html = markdown(page)
                ht.write(html)

        return file_name

    """
    TODO: split the below into methods
    1) Get dict of levels and order
    2) Sequence all of the files
    Then #2 can be re-used when you're generating the tree in the first place
    """

    def update_file_sequence(self):

        # Get outline of all files in tree
        outline = self._get_file_tree()

        files = [branch for branch in outline if branch[-3:] == ".md"]

        sequences = {
            2: 0,
            3: 0,
            4: 0,
            "file": 0
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

        branches = [branch for branch in outline if os.path.isdir(branch)]

        rename_dict = {}
        rename_tuples = []
        for branch in branches:
            files = os.listdir(branch)
            files.sort()
            #sequence_list = [file[:2] for file in files]
            sequence_list = [self._get_sequence_index(file) for file in files]

            # Build dictionary of every existing sequence and a list of every file with that sequence
            file_dict = {}
            for sequence in sequence_list:
                file_dict[sequence] = [file for file in files if self._get_sequence_index(file) == sequence]

            # For every sequence with more than one file, get back the correct order from the user
            for sequence, objs in file_dict.items():
                if len(objs) > 1:
                    file_dict[sequence] = self._resolve_duplicates(objs)

            ordered_files = []
            for key, objs in file_dict.items():
                for file in objs:
                    ordered_files.append(file)

            # Once all files are de-duped, re-base at 01 for each tree level and sequence
            for file in ordered_files:

                if file[-3:] == ".md":
                    levels = "file"
                else:
                    split_branch = branch.split("/")
                    levels = len(split_branch)
                level_sequence = sequences[levels] + 1
                if self._get_sequence_index(file)[0] != level_sequence:
                    rename_tuples.append((level_sequence, branch + "/" + file, levels))
                sequences[levels] += 1

        self._rename_files(rename_tuples, sequences)

    def _get_sequence_index(self, path):
        try:
            sequence_index = path.index("-")
            sequence = path[:sequence_index]
            sequence_integer = int(sequence)
        except ValueError:
            sequence = None
            sequence_index = -1

        return sequence, sequence_index

    def _rename_files(self, rename_tuples, sequence_dict):

        index_digits = {}
        for key, _ in sequence_dict.items():
            indices = [tuple[0] for tuple in rename_tuples if tuple[2] == key]
            try:
                index_digits[key] = len(str(max(indices)))
            except ValueError:
                pass

        for tuple in rename_tuples:
            index = str(tuple[0]).zfill(index_digits[tuple[2]])
            path = tuple[1]

            split_path = path.split("/")
            #Remove empty strings
            split_path = [node for node in split_path if node]
            terminal = split_path[-1]

            sequence, sequence_index = self._get_sequence_index(terminal)

            # If file/path already has the right index, skip
            if sequence == index:
                continue
            filename = index + "-" + terminal[sequence_index + 1:]

            split_path[-1] = filename
            new = "/".join(split_path)

            if os.path.isfile(new) or os.path.isdir(new):
                click.secho("Duplicate file or directory names: \n" +
                    "Want to change: " + path + " \n" +
                    "to: " + new + "\n" +
                    "but 'to' already exists.", fg="red")
                raise click.Abort()
            else:
                os.rename(path, new)

    def _resolve_duplicates(self, duplicates):
        rename_list = []
        counter = 1
        click.secho("There are " + str(len(duplicates)) + " files with a duplicate sequence:", fg="green")
        for duplicate in duplicates:
            sequence, _ = self._get_sequence_index(duplicate)
            sequence_length = len(sequence) + 1
            click.secho(str(counter) + ") " + duplicate[sequence_length:], fg="green")
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
                click.echo("Of the " + str(len(duplicates)) + " duplicates, choose which is first.")
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
        shutil.rmtree("project/")
        os.mkdir("project/")

        title = "^#{1} "
        section = "^#{2} "
        chapter = "^#{3} "
        sub_chapter = "^#{4} "
        scene = "^#{5} "

        sequences = {
            "section": 1,
            "chapter": 1,
            "sub_chapter": 1,
            "scene": 1
        }

        title_path = ""
        for header in headers:
            if re.match(title, header.group(0)):
                title = header.group(0)
                title = title.strip("#")
                title = clean_filename(title)
                title_path = "project/" + title
                break

        if not title_path:
            raise StructureError("Must be a title (e.g., # The Great Gatsby) in the source file.")
        os.mkdir(title_path)

        with open(file, "r") as fp:
            text = fp.read()

        overrides = {}
        rename_tuples = []
        for index, header in enumerate(headers):
            name = header.group(0)
            original_name = name.strip("#").strip()
            name = clean_filename(original_name)
            if original_name != name:
                overrides[name] = original_name

            if re.match(section, header.group(0)):
                section_path = title_path + "/" + name + "/"
                chapter_path, sub_chapter_path, scene_path = section_path, section_path, section_path

                os.mkdir(section_path)
                rename_tuples.append((sequences["section"],section_path, "section"))

                sequences["section"] += 1

            elif re.match(chapter, header.group(0)):
                chapter_path = section_path + name + "/"
                sub_chapter_path, scene_path = chapter_path, chapter_path
                os.mkdir(chapter_path)
                rename_tuples.append((sequences["chapter"],chapter_path, "chapter"))

                sequences["chapter"] += 1

            elif re.match(sub_chapter, header.group(0)):
                sub_chapter_path = chapter_path + name + "/"
                scene_path = sub_chapter_path
                os.mkdir(sub_chapter_path)
                rename_tuples.append((sequences["sub_chapter"],sub_chapter_path, "sub_chapter"))

                sequences["sub_chapter"] += 1

            elif re.match(scene, header.group(0)):
                scene_path = sub_chapter_path + name + ".md"

                start_scene = header.end(0) + 1
                try:
                    end_scene = headers[index + 1].start(0)
                except IndexError:
                    end_scene = None

                scene_text = text[start_scene:end_scene]
                with open(scene_path, "w") as scene_file:
                    scene_file.write(scene_text)
                rename_tuples.append((sequences["scene"],scene_path, "scene"))

                sequences["scene"] += 1

        clean_tuples = []
        for tuple in rename_tuples:
            path = tuple[1]
            if path[-1] == "/":
                path = path[:-1]

            path_length = len(path.split("/"))

            clean_tuples.append((path_length, tuple[0], tuple[1], tuple[2]))

        clean_tuples.sort(reverse=True)
        clean_tuples = [(tuple[1], tuple[2], tuple[3]) for tuple in clean_tuples]
        self._rename_files(clean_tuples, sequences)

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
