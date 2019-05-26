import re
import os

class Outliner():

    def generate_file_tree(self, file, title):
        intervals = self._get_header_intervals(file)
        self._generate_folders(intervals, title, file)

    def _generate_folders(self, intervals, title, file):
        headers = list(intervals)

        try:
            os.mkdir(title)
        except FileExistsError:
            pass

        section = "^#{1} "
        chapter = "^#{2} "
        sub_chapter = "^#{3} "
        scene = "^#{4} "

        current_section = ''
        current_chapter = ''
        current_sub_chapter = ''

        section_count = '01'
        chapter_count = '01'
        sub_chapter_count = '01'
        scene_count = '01'

        for index, header in enumerate(headers):
            name = header.group(0)

            if re.match(section, header.group(0)):
                name = name.strip('#')
                name = name.strip()
                current_path = title + "/" + section_count + "-" + name + "/"

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

                fp = open(file, 'r')
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
