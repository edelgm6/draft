import re
import os
import mistune

class Outliner():

    def update_outline(self):
        title = os.listdir('project')

        assert len(title) == 1, "Project folder has more than one directory."

        outline = []
        for path, subdirs, files in os.walk('project/' + title[0]):
            for dir in subdirs:
                outline.append(os.path.join(path, dir))
            for name in files:
                outline.append(os.path.join(path, name))

        outline.sort()

        clean_outline = []
        for entry in outline:
            entry = entry.split('/')
            clean_outline.append(entry[2:])

        section = ''
        chapter = ''
        sub_chapter = ''
        scene = ''

        outline_tag = '(?<=======\\n).*(?=\\n======)'

        markdown = mistune.Markdown()
        page = ''

        for entry in clean_outline:
            if len(entry) == 1:
                section = entry[0]
                page = markdown("# " + section + "\n\n")

            elif len(entry) == 2:
                chapter = entry[-1]
                page = page + markdown("## " + chapter + "\n\n")

            elif len(entry) == 3:
                sub_chapter = entry[-1]
                page = page + markdown("### " + sub_chapter + "\n\n")

            elif len(entry) == 4:
                dir = 'project/' + os.listdir('project')[0] + '/' + '/'.join(entry)
                scene = entry[-1]
                scene_entry = scene

                with open(dir, 'r') as sc:
                    text = sc.read().strip()
                    scene_detail = re.search(outline_tag, text)
                    scene_entry = scene_entry + ": " + scene_detail.group(0)
                    page = page + markdown(scene_entry)

        with open('outline.md', 'w') as outline:
            outline.write(page)

    def generate_file_tree(self):

        project = os.listdir('project')
        assert len(project) == 1, "Must have one file in top-level project/ directory."
        project = project[0]

        legacy_project = os.listdir('legacy-project')
        assert len(legacy_project) == 1, "Must have one file in top-level legacy-project/ directory."
        legacy_project = legacy_project[0]
        legacy_file, extension = os.path.splitext('legacy-project/' + legacy_project)
        assert extension == ".txt", "Legacy project must be a .txt file."

        file = 'legacy-project/' + legacy_project
        intervals = self._get_header_intervals(file)
        self._generate_folders(intervals, file, project)

    def _generate_folders(self, intervals, file, title):
        headers = list(intervals)
        base_path = 'project/' + title

        try:
            os.mkdir('project/' + title)
        except FileExistsError:
            pass

        section = "^#{1} "
        chapter = "^#{2} "
        sub_chapter = "^#{3} "
        scene = "^#{4} "

        current_section = ""
        current_chapter = ""
        current_sub_chapter = ""

        section_count = '01'
        chapter_count = '01'
        sub_chapter_count = '01'
        scene_count = '01'

        for index, header in enumerate(headers):
            name = header.group(0)

            if re.match(section, header.group(0)):
                name = name.strip('#')
                name = name.strip()
                current_path = base_path + "/" + section_count + "-" + name + "/"

                try:
                    os.mkdir(current_path)
                except FileExistsError:
                    pass

                section_count = str(int(section_count) + 1).zfill(len(section_count))

            elif re.match(chapter, header.group(0)):
                name = name.strip('#')
                name = name.strip()
                current_path = current_path + chapter_count + "-" + name + "/"
                try:
                    os.mkdir(current_path)
                except FileExistsError:
                    pass

                chapter_count = str(int(chapter_count) + 1).zfill(len(chapter_count))

            elif re.match(sub_chapter, header.group(0)):
                name = name.strip('#')
                name = name.strip()
                current_path = current_path + sub_chapter_count + "-" + name + "/"
                try:
                    os.mkdir(current_path)
                except FileExistsError:
                    pass

                sub_chapter_count = str(int(sub_chapter_count) + 1).zfill(len(sub_chapter_count))

            elif re.match(scene, header.group(0)):
                name = name.strip('#')
                name = name.strip()
                current_path = current_path + scene_count + "-" + name + ".md"

                start_scene = header.end(0) + 1
                try:
                    end_scene = headers[index + 1].start(0)
                except IndexError:
                    end_scene = None

                with open(file, 'r') as fp:
                    text = fp.read()

                scene_text = text[start_scene:end_scene]
                try:
                    with open(current_path, 'w') as scene_file:
                        scene_file.write(scene_text)
                except FileExistsError:
                    pass

                scene_count = str(int(scene_count) + 1).zfill(len(scene_count))


    def _get_header_intervals(self, file):

        section = "((?<=[\\n\s])|^)#{1,4} .*?\\n"

        with open(file, 'r') as file:
            text = file.read()

            headers = re.finditer(section, text)

            return headers
