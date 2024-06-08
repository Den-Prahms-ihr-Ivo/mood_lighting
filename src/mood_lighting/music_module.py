# https://pypi.org/project/python-mpd2/
from musicpd import MPDClient

from src.mood_lighting.config import CONFIG, CONTROLLER

# from src.mood_lighting import CONTROLLER

from typing import Literal


class MusicPlayer:

    _instance = None
    current_song = ""

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(MusicPlayer, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.client = MPDClient()
        # TODO: HIER MAL ausprobieren, ob du nicht jeeeeedes mal ne neue Instanz erstellen musst.
        # Sondern einfach mit einem None idle timeout das Ding ewig stehen lassen kannst. (2h sollten zum test mal reichen.)
        self.client.timeout = None
        self.client.idletimeout = None
        self.connect()

        self.set_volumne(int(CONFIG["DEFAULT"].get("initial_volume", 100)))
        self.set_repeat_mode("ON")
        self.set_countinous_mode("ON")
        self.set_repeat_mode("ON")

    def connect(self):
        self.client.connect(
            CONFIG["DEFAULT"].get("HOST", "localhost"),
            int(CONFIG["DEFAULT"].get("PORT", 6600)),
        )

    def disconnect(self):
        self.client.disconnect()

    def get_playlists(self):
        val = self.client.listplaylists()
        return val

    def get_playing(self) -> str:
        try:
            val = self.client.currentsong()
        except Exception as e:
            # TODO: LOGGING
            print(e)
            self.connect()
            val = self.client.currentsong()

        if "title" in val:
            name = val["title"]
        elif "file" in val:
            name = val["file"]
        else:
            name = "unknown"

        return name

    def load(self, playlist):
        try:
            self.client.clear()
            self.client.load(playlist)
        except Exception as e:
            # TODO: LOGGING
            print(e)
            self.connect()
            self.client.clear()
            self.client.load(playlist)

    def next(self):
        try:
            self.client.next()
        except Exception as e:
            # TODO: LOGGING
            print(e)
            self.connect()
            self.client.next()

    def play(self) -> str:
        CONTROLLER["is_playing"] = True

        try:
            self.client.play()
        except Exception as e:
            # TODO: LOGGING
            print(e)
            self.connect()
            self.client.play()

        cs = self.get_playing()
        return cs

    def stop(self):
        CONTROLLER["is_playing"] = False
        self.current_song = ""
        try:
            self.client.stop()
        except Exception as e:
            # TODO: LOGGING
            print(e)
            self.connect()
            self.client.stop()

    def set_volumne(self, vol=100) -> None:
        if vol < 0:
            vol = 0
        if 100 < vol:
            vol = 100

        self.client.setvol(vol=100)

    def set_shuffle_mode(self, mode: Literal["ON", "OFF"]) -> None:
        """"""
        if mode == "ON":
            self.client.random(state=1)
        else:
            self.client.random(state=0)

    def set_countinous_mode(self, mode: Literal["ON", "OFF"]) -> None:
        """
        Sets single state to STATE, STATE should be 0 or 1. When single is activated, playback is stopped after current song, or song is repeated if the ‘repeat’ mode is enabled.
        """
        if mode == "ON":
            self.client.single(state=1)
        else:
            self.client.single(state=0)

    def set_repeat_mode(self, mode: Literal["ON", "OFF"]) -> None:
        """"""
        if mode == "ON":
            self.client.repeat(state=1)
        else:
            self.client.repeat(state=0)

    def clean_up(self):
        self.client.close()
        self.client.disconnect()
