import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read("./tools.ini")

CONTROLLER = {
    "start_stop_button_is_active": True,
    "is_playing": False,
    "speaker_is_powered_on": False,
}
