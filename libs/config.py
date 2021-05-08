import sys
import os
import configparser


CONFIG_FILE = "config.ini"
CONFIG_FOLDER = os.path.abspath("")
CONFIG_PATH = os.path.join(CONFIG_FOLDER, CONFIG_FILE)

config = configparser.ConfigParser()

def load():
    if not os.path.isfile(CONFIG_PATH):
        CONFIG_FOLDER = os.path.dirname(os.path.abspath(""))
        CONFIG_PATH = os.path.join(CONFIG_FOLDER, CONFIG_FILE)
    try:
        config.read(CONFIG_PATH)
    except Exception:
        print("Error: wrong or missing 'config.ini' file")

def get(section, parameter):
    if config.has_option(section, parameter):
        value = config.get(section, parameter)
    else:
        value = os.getenv("_".join([section.upper(), parameter.upper()]))
    return value

