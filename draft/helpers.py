import re
import string
import yaml

def clean_filename(filename):
    less_punctuation = filename.translate(str.maketrans('', '', string.punctuation)).strip()

    return re.sub(' +', ' ',less_punctuation)

def get_settings():

    try:
        with open('settings.yml', 'r') as settings_file:
            settings = yaml.safe_load(settings_file)
    except FileNotFoundError:
        with open("static/settings.yml","r") as settings_file:
            settings = yaml.safe_load(settings_file)

    return settings
