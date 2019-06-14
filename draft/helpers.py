import re
import string
import yaml

def clean_filename(filename):
    filename = filename.replace("-", " ")
    less_punctuation = filename.translate(str.maketrans('', '', string.punctuation)).strip()

    return re.sub(' +', ' ',less_punctuation)

def get_settings():

    DEFAULT_SETTINGS = {
        'headers': {
            'section': True,
            'chapter': True,
            'sub_chapter': True
        },
        'warnings': {
            'parse': True,
            'split': True,
            'sequence': True,
            'trim': True
        },
        'overrides': None
        }

    settings = DEFAULT_SETTINGS

    try:
        with open('settings.yml', 'r') as user_settings_file:
            user_settings = yaml.safe_load(user_settings_file)
            for key, value in settings.items():
                try:
                    override = user_settings[key]
                    settings[key] = override
                except (KeyError, TypeError):
                    continue
    except FileNotFoundError:
        pass

    return settings
