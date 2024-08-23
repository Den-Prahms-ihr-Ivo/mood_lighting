import os
from mpd import MPDClient
from typing import Optional, Callable

from src.helper.utility_component import Utility_Component
from src.helper.state_types import BASIS_STATES, BINARY_STATES
from src.config import CONFIG
from src.helper.mailer import send_mail
import json
from random import randrange
from threading import Timer

from pathlib import Path

import logging

logger = logging.getLogger("moodlight")

# from mpd import MPDClient


class MusicComponent(Utility_Component):

    current_music_state = {}
    _currently_playing = False
    _currently_paused = False
    _current_playlist = None
    client = None

    _cnt_dwn_timer = None

    HOST = "localhost"
    PORT = 6600

    _connected = False

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
        self._currently_paused = False
        self._cnt_dwn_timer = None

        self._connected = False

        self.target_state(self.current_music_state)

        self.client = MPDClient()
        self.client.timeout = 10
        self.client.idletimeout = None

        self._connect()
        self.client.random(1)
        self.client.single(0)
        self.client.repeat(0)

        self.update_playlists()

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
            elif key == "volumne":
                self.current_music_state[key] = value
                self.set_volumne(value)

            else:
                self.current_music_state[key] = value

        self.actual_state(self.current_music_state)

    def update_playlists(self):
        self._connect()
        self.client.update()

    def playlist_change(self, state):
        self._connect()
        idx, _ = state
        self.client.clear()
        self.client.load(idx)
        self._current_playlist = idx

    def _play(self):
        self._currently_playing = True
        self._connect()
        if self._currently_paused:
            self._currently_paused = False
            self.client.pause(1)
        else:
            self.client.play()

    def _pause(self):
        self._currently_playing = False
        self._currently_paused = True
        self._connect()
        self.client.pause(0)

    def _stop(self):
        self._currently_playing = False
        self._connect()
        if self._current_playlist == "sleep":
            self.client.pause()
        else:
            self.client.stop()

    def _next(self):
        self._connect()
        try:
            self.client.next()
        except Exception as e:
            send_mail("Failure pressing next")
            logger.warn("Failure pressing next")
            logger.warn(e)

    def _get_current_song(self):
        self._connect()
        return self.client.playlist()

    def set_volumne(self, vol):
        self._connect()
        vol = max(int(vol), 0)
        vol = min(int(vol), 100)

        self.client.setvol(vol)

    def quit(self):
        self.client.close()
        self.client.disconnect()

    def _connect(self):
        if not self._connected:
            self.client.connect(self.HOST, self.PORT)
            self._connected = True
            self.cnt_dwn_timer = Timer(5, self.disconnect)
            self.cnt_dwn_timer.start()

    def disconnect(self):
        self._connected = False
        self.client.disconnect()
