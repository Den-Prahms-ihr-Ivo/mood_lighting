from enum import Enum
from typing import Optional, Callable

from src.helper.utility_component import Utility_Component
from src.config import CONFIG
import json
from random import randrange

from pathlib import Path


class PlaylistComponent(Utility_Component):

    _playlists = None
    _playlist_keys = None
    _current_playlist_idx = None
    _current_playlist_state = None

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)

        self._playlists = None
        self._playlist_keys = None
        self._current_playlist_idx = None
        self._current_playlist_state = None

        self.read_playlist()
        self.target_state(self._current_playlist_state)

    def target_state(self, desired_state: Enum):
        if isinstance(desired_state, str):
            if desired_state in self._playlists.keys():
                self._set_state_by_index(self._playlist_keys.index(desired_state))

        elif isinstance(desired_state, int):
            self._set_state_by_index(
                (self._current_playlist_idx + desired_state) % len(self._playlist_keys)
            )
        else:
            # TODO: logging
            pass

    def _set_state_by_index(self, index):
        self._current_playlist_idx = index

        display_name = self._playlists[self._playlist_keys[index]]["display_name"]

        idx = self._playlist_keys[index]
        self._current_playlist_state = (idx, display_name)

        self.actual_state((idx, display_name))

    def read_playlist(self) -> None:
        # read the initialization json file.
        playlist_path = Path(CONFIG["DEFAULT"]["playlist_json_path"])
        if not playlist_path.is_file():
            # TODO: RAISE ERROR & LOGGING
            raise ValueError("Playlistpath doesn't exist :(")

        # print(t.is)
        with open(playlist_path, "r", encoding="UTF8") as f:
            d = json.load(f)
            self._playlists = d
            self._playlist_keys = list(d.keys())

            self._current_playlist_idx = randrange(len(d.keys()))

        display_name = self._playlists[self._playlist_keys[self._current_playlist_idx]][
            "display_name"
        ]

        idx = self._playlist_keys[self._current_playlist_idx]
        self._current_playlist_state = (idx, display_name)
