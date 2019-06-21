import re
import string
import yaml

GITIGNORE = '## Mac\n# General\n.DS_Store\n.AppleDouble\n.LSOverride\n\n# Icon must end with two \\r\nIcon\n\n# Thumbnails\n._*\n\n# Files that might appear in the root of a volume\n.DocumentRevisions-V100\n.fseventsd\n.Spotlight-V100\n.TemporaryItems\n.Trashes\n.VolumeIcon.icns\n.com.apple.timemachine.donotpresent\n\n# Directories potentially created on remote AFP share\n.AppleDB\n.AppleDesktop\nNetwork Trash Folder\nTemporary Items\n.apdisk\n\n## Windows\n# Windows thumbnail cache files\nThumbs.db\nThumbs.db:encryptable\nehthumbs.db\nehthumbs_vista.db\n\n# Dump file\n*.stackdump\n\n# Folder config file\n[Dd]esktop.ini\n\n# Recycle Bin used on file shares\n$RECYCLE.BIN/\n\n# Windows Installer files\n*.cab\n*.msi\n*.msix\n*.msm\n*.msp\n\n# Windows shortcuts\n*.lnk\n'


def clean_filename(filename):
    filename = filename.replace("-", " ")
    less_punctuation = filename.translate(str.maketrans("", "", string.punctuation)).strip()

    return re.sub(" +", " ",less_punctuation)

def get_settings():

    DEFAULT_SETTINGS = {
            "headers": {
                "section": True,
                "chapter": True,
                "sub_chapter": True
            },
            "warnings": {
                "parse": True,
                "split": True,
                "sequence": True,
                "trim": True
            },
            "overrides": None,
            "author": None
        }


    settings = DEFAULT_SETTINGS

    try:
        with open("settings.yml", "r") as user_settings_file:
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
