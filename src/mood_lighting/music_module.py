from musicpd import MPDClient
from src.mood_lighting.config import CONFIG, CONTROLLER

# from src.mood_lighting import CONTROLLER

from unittest.mock import MagicMock
from typing import Literal


class MusicPlayer:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MusicPlayer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.client = MPDClient()
        self.client = MagicMock()  # TODO: in der Raspberry version entfernen. :)
        self.connect()

        # self.client.timeout = 10
        # TODO: HIER MAL ausprobieren, ob du nicht jeeeeedes mal ne neue Instanz erstellen musst.
        # Sondern einfach mit einem None idle timeout das Ding ewig stehen lassen kannst. (2h sollten zum test mal reichen.)
        self.client.idletimeout = None

    def connect(self):
        self.client.connect(
            CONFIG["DEFAULT"].get("HOST", "localhost"),
            int(CONFIG["DEFAULT"].get("PORT", 6600)),
        )

    def disconnect(self):
        self.client.disconnect()

    def quit(self):
        self.client.close()
        self.client.disconnect()

    def get_playlists(self):
        val = self.client.listplaylists()
        return val

    def get_playing(self) -> str:
        name = "unknown"
        val = self.client.currentsong()

        if "title" in val:
            name = val["title"]
        elif "file" in val:
            name = val["file"]
        else:
            name = "unknown"

        return name

    def load(self, playlist):
        self.connect()
        print(f"Loading Playlist: {playlist}")
        self.client.clear()
        self.client.load(playlist)
        self.disconnect()

    def next(self):
        print("PLAYING NEXT SONG")
        # TODO: implement

    def play(self) -> str:
        # TODO: check, if necessary
        CONTROLLER["is_playing"] = True

        self.connect()
        self.client.play()
        current_song = self.get_playing()
        self.disconnect()
        return current_song

    def stop(self):
        # TODO: check, if necessary
        CONTROLLER["is_playing"] = False

        self.connect()
        self.client.play()
        self.disconnect()

    def set_shuffle_mode(self, mode: Literal["ON", "OFF"]) -> None:
        """"""
        # TODO: implement
        print(f"Setting Shuffle Mode {mode}")

    def set_countinous_mode(self, mode: Literal["ON", "OFF"]) -> None:
        """"""
        # TODO: implement
        print(f"Setting Continous Mode {mode}")

    def set_repeat_mode(self, mode: Literal["ON", "OFF"]) -> None:
        """"""
        # TODO: implement
        print(f"Setting Repeat Mode {mode}")
