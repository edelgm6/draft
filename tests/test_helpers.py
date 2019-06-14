from unittest import TestCase
from draft.helpers import clean_filename

class TestCleanFilename(TestCase):

    def test_clean_filename(self):
        filenames = [
            ("The ! Great! G/atsby \\!","The Great Gatsby"),
            ("The ! Gr""eat! G/atsby \\!","The Great Gatsby"),
            ("The ! Gr**e''a't! G/at""s?by \\!","The Great Gatsby"),
            ("The ! Gre<a>t! G/atsby \\!","The Great Gatsby"),
            ("The ! Gr.e.at! G/at?sby \\!","The Great Gatsby"),
        ]

        for filename in filenames:
            cleaned_name = clean_filename(filename[0])
            self.assertEqual(cleaned_name, filename[1])
