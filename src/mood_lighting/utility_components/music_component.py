import os
from typing import Optional, Callable

from src.helper.utility_component import Utility_Component
from src.helper.state_types import BASIS_STATES, BINARY_STATES
from src.config import CONFIG
import json
from random import randrange

from pathlib import Path


class MusicComponent(Utility_Component):

    current_music_state = {}
    _currently_playing = False
    _current_playlist = None

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)
        self.current_music_state = {
            "state": BASIS_STATES.UNDEFINED,
            "volume": None,
            "current_song": None,
            "refresh": None,
            "next_pressed": None,
        }

        self._playlists = None
        self._playlist_keys = None
        self._current_playlist = None
        self._currently_playing = False

        self.target_state(self.current_music_state)

    def target_state(self, desired_state):
        # resetting values
        reset_values = ["current_song", "next_pressed"]
        for key in reset_values:
            if key not in desired_state.keys():
                self.current_music_state[key] = None

        for key, value in desired_state.items():
            # ##################
            # Update Playlist
            # ##################
            if key == "state":
                if value == BINARY_STATES.ON and not self._currently_playing:
                    self._play()
                    self._currently_playing = True
                elif value == BINARY_STATES.OFF and self._currently_playing:
                    self._stop()
                    self._currently_playing = False

                self.current_music_state[key] = value
            elif key == "next_pressed":
                self.current_music_state[key] = value
                if (
                    desired_state["state"] == BINARY_STATES.ON
                    and desired_state["next_pressed"] == BINARY_STATES.ON
                ):
                    self._next()
                    self.current_music_state["current_song"] = self._get_current_song()

            else:
                self.current_music_state[key] = value

        self.actual_state(self.current_music_state)

    def playlist_change(self, state):
        # TODO: mpc load playlist
        pass
        # print(state)

    def _load_playlist(self):
        raise NotImplementedError

    def _play(self):
        self._currently_playing = True
        raise NotImplementedError

    def _stop(self):
        self._currently_playing = False
        raise NotImplementedError

    def _next(self):
        raise NotImplementedError

    def _get_current_song(self):
        raise NotImplementedError
