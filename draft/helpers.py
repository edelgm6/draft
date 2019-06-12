import re
import string

def clean_filename(filename):
    less_punctuation = filename.translate(str.maketrans('', '', string.punctuation)).strip()

    return re.sub(' +', ' ',less_punctuation)
