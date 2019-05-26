import os

class Generator():

    def generate_project(self, title):
        os.mkdir(title)
        os.mkdir(title + "/01-Section 1")
        os.mkdir(title + "/01-Section 1/01-Chapter 1")
        os.mkdir(title + "/01-Section 1/01-Chapter 1/01-Sub-Chapter 1")

        with open(title + "/01-Section 1/01-Chapter 1/01-Sub-Chapter 1/01-Scene 1.md", "w") as file:
            file.write('#### Scene 1\n')
            file.write('\n')
            file.write('Your genius awaits.')

        os.mkdir("legacy-project")
        with open("legacy-project/legacy.txt", "w") as file:
            file.write("If applicable, your legacy project goes here as a .txt file.")
            file.write('\n')
            file.write(
                "Separate out into Sections (e.g., # Section), Chapters \n"
                "(e.g., ## Chapter), Sub-chapters (e.g., ### Sub-chapter), and \n"
                "Scenes (e.g., ####) to take advantage of the Outliner \n"
                "functionality.")
