import sys
import os
import configparser


CONFIG_FILE = "config.ini"
CONFIG_FOLDER = os.path.abspath("")
CONFIG_PATH = os.path.join(CONFIG_FOLDER, CONFIG_FILE)

config = configparser.ConfigParser()

def load():
    if os.path.isfile(CONFIG_PATH):
        try:
            config.read(CONFIG_PATH)
        except Exception:
            print("Error: wrong 'config.ini' file")
    else:
        print("Error: use a 'config.ini' file")

def get(section, parameter):
    if config.has_option(section, parameter):
        value = config.get(section, parameter)
    else:
        value = os.getenv("_".join([section.upper(), parameter.upper()]))
    return value
