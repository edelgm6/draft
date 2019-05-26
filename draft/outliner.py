import re

class Outliner():

    def generate_file_tree(file):

        section = "(\\n|\s|^)# .*?\\n"
        chapter = "(\\n|\s)#{2} .*?\\n"
        sub_chapter = "(\\n|\s)#{3} .*?\\n"
        scene = "(\\n|\s)#{4} .*?\\n"

        with open(file, 'r') as file:
            text = file.read()

            print(repr(text))

            headers = re.finditer(section, text)
            chapters = re.finditer(chapter, text)
            sub_chapters = re.finditer(sub_chapter, text)
            scenes = re.finditer(scene, text)

            demarcations = [headers, chapters, sub_chapters, scenes]

            for group in demarcations:
                for item in group:
                    print(item)
