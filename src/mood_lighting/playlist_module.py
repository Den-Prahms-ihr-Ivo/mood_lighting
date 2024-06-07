""" """

import json

from typing import Optional, Dict
from random import randrange
from pathlib import Path
from src.mood_lighting.config import CONFIG, CONTROLLER


class Playlist(object):
    """ """

    _instance = None

    _current_playlist: Optional[int] = None
    _playlists: Optional[Dict[str, Dict[str, str]]] = None
    _playlist_keys: Optional[str] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Playlist, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.read_playlist()

    def read_playlist(self) -> None:
        # read the initialization json file.
        playlist_path = Path(CONFIG["DEFAULT"]["playlist_json_path"])
        if not playlist_path.is_file():
            # TODO: RAISE ERROR & LOGGING
            print(playlist_path)
            raise ValueError("Playlistpath doesn't exist :(")

        # print(t.is)
        with open(playlist_path, "r", encoding="UTF8") as f:
            d = json.load(f)
            self._playlists = d
            self._playlist_keys = list(d.keys())

            self._current_playlist = randrange(len(d.keys()))

    @property
    def current_playlist(self) -> Dict[str, str]:
        if self._current_playlist is None:
            raise ValueError(
                "Something went wrong retrieving the getter for current_playlist"
            )

        return self._playlists[self._playlist_keys[self._current_playlist]]

    def instance(self):
        pass

    def set_playlist(self, playlist_key) -> None:
        """Updates the current playlist"""
        if playlist_key not in self._playlists.keys():
            # TODO: raise ERROR & LOGGING
            raise ValueError("Playlist key not in current playlists")

        # self.current_playlist = self._playlists[playlist_key]
        self._current_playlist = self._playlist_keys.index(playlist_key)

    def next(self) -> None:
        self._current_playlist = (self._current_playlist + 1) % len(self._playlist_keys)
