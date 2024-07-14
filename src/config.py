import os
import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read("./tools.ini")


if os.environ.get("TESTING_ENV", None) is None:
    CONFIG.read("/home/ivo/mood_light/mood_lighting/tools.ini")
else:
    CONFIG.read("./tools.ini")
