import re
import string
import yaml

def clean_filename(filename):
    less_punctuation = filename.translate(str.maketrans('', '', string.punctuation)).strip()

    return re.sub(' +', ' ',less_punctuation)

def get_settings():

    with open("draft/settings.yml","r") as default_settings:
        settings = yaml.safe_load(default_settings)

    try:
        with open('settings.yml', 'r') as user_settings_file:
            user_settings = yaml.safe_load(user_settings_file)
            for key, value in settings.items():
                try:
                    override = user_settings[key]
                    settings[key] = override
                except KeyError:
                    continue
    except FileNotFoundError:
        pass

    return settings
