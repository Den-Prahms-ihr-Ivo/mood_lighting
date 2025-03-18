from typing import Optional
from src.helper.input_component import Input_Component
from src.helper.monitor import Monitor
from src.helper.state_types import (
    BINARY_STATES,
    SHUTDOWN_STATE,
    MUSIC_STATES,
    PLAYLIST_STATE_TYPE,
    BASIS_STATES,
)
from src.mood_lighting.monitors.music_monitor import MusicMonitor
from src.mood_lighting.utility_components.display import Display
from src.config import CONFIG
from threading import Timer

from src.helper.utility_component import Utility_Component

import logging

logger = logging.getLogger("moodlight")


class ButtonPanel(Input_Component):

    candle_state = BASIS_STATES.UNDEFINED
    outlet_state = BASIS_STATES.UNDEFINED
    mood_light_state = BASIS_STATES.UNDEFINED
    spotlight_state = BASIS_STATES.UNDEFINED
    ceiling_state = (BASIS_STATES.UNDEFINED, -1)
    playlist_state = BASIS_STATES.UNDEFINED
    music_component = None
    outlet_component = None
    music_state = {}

    BUTTON_DISABLE_TIME = 1

    def __init__(
        self,
        candle_monitor: Monitor,
        outlet_monitor: Monitor,
        mood_light_monitor: Monitor,
        music_monitor: MusicMonitor,
        display: Display,
        spotlight_monitor: Monitor,
        ceiling_monitor: Monitor,
        playlist_monitor: Monitor,
        music_component: Optional[Utility_Component] = None,
        outlet_component: Optional[Utility_Component] = None,
    ) -> None:
        self.candle_monitor = candle_monitor
        self.outlet_monitor = outlet_monitor
        self.music_monitor = music_monitor
        self.mood_light_monitor = mood_light_monitor
        self.display = display
        self.spotlight_monitor = spotlight_monitor
        self.ceiling_monitor = ceiling_monitor
        self.music_component = music_component
        self.outlet_component = outlet_component
        self.playlist_monitor = playlist_monitor
        #
        self.candle_timer = None
        self.music_timer = None
        self.display_timer = None
        self._button_next_timer = None
        self._button_start_stop_timer = None
        self._button_mood_timer = None
        self._button_sleep_timer = None
        self._snooze_timer = None

        self._button_next_enabled = True
        self._button_start_stop_enabled = True
        self._button_mood_enabled = True
        self._button_sleep_enabled = True
        self._sleep_mode_snooze = False
        #
        #
        self.candle_state = BASIS_STATES.UNDEFINED
        self.outlet_state = BASIS_STATES.UNDEFINED
        self.mood_light_state = BASIS_STATES.UNDEFINED
        self.spotlight_state = BASIS_STATES.UNDEFINED
        self.audio_state = BASIS_STATES.UNDEFINED
        self.ceiling_state = (BASIS_STATES.UNDEFINED, -1)
        self.music_state = {
            "state": BASIS_STATES.UNDEFINED,
            "volume": None,
            "current_song": None,
            "refresh": None,
            "currently_playing": None,
            "next_pressed": None,
        }
        #
        self.candle_monitor.add_actual_state_callback(self.update_candle_state)
        self.outlet_monitor.add_actual_state_callback(self.update_outlet_state)
        self.music_monitor.add_actual_state_callback(self.update_music_state)
        self.mood_light_monitor.add_actual_state_callback(self.update_mood_light_state)
        self.spotlight_monitor.add_actual_state_callback(self.update_spotlight_state)
        self.ceiling_monitor.add_actual_state_callback(self.update_ceiling_light_state)
        self.playlist_monitor.add_actual_state_callback(self.update_playlist_state)

    def actual_state_callback(self, actual_state):
        raise NotImplementedError

    def initialise_states(self):

        self.candle_monitor.set_target_state(BINARY_STATES.OFF)
        self.outlet_monitor.set_target_state(BINARY_STATES.OFF)
        self.mood_light_monitor.set_target_state(BINARY_STATES.OFF)
        self.spotlight_monitor.set_target_state(BINARY_STATES.OFF)
        self.music_monitor.set_target_state(
            {
                "state": BINARY_STATES.OFF,
                "refresh": BINARY_STATES.ON,
            }
        )
        self.display.set_target_state(BINARY_STATES.OFF)

    def sleep_mode(self):
        # IVO
        self.ceiling_monitor.set_target_state((BINARY_STATES.OFF, -1))
        self.outlet_monitor.set_target_state(BINARY_STATES.ON)

        self.mood_light_monitor.set_target_state(BINARY_STATES.OFF)
        self.spotlight_monitor.set_target_state(BINARY_STATES.OFF)
        self.display.set_target_state(BINARY_STATES.OFF)

        self.playlist_monitor.set_target_state("sleep")
        self.music_monitor.set_target_state(
            {
                "state": BINARY_STATES.ON,
                "volume": CONFIG["DEFAULT"].get("sleep_volumne", 50),
            }
        )

        if self._snooze_timer is not None:
            self._snooze_timer.cancel()

        if not self._sleep_mode_snooze:
            self.candle_monitor.set_target_state(BINARY_STATES.ON)
            # Turn Candle on for 5 min:
            if self.candle_timer is not None:
                self.candle_timer.cancel()

            self.candle_timer = Timer(
                float(CONFIG["DEFAULT"].get("candle_sleep_time", 300)),
                lambda: self.candle_monitor.set_target_state(BINARY_STATES.OFF),
            )
            self.candle_timer.start()

        if self.music_timer is not None:
            self.music_timer.cancel()

        self.music_timer = Timer(
            float(CONFIG["DEFAULT"].get("music_sleep_time", 300)),
            self.snooze_mode,
        )
        self.music_timer.start()

    def sleep_relax_mode(self):
        self.ceiling_monitor.set_target_state((BINARY_STATES.OFF, -1))
        self.outlet_monitor.set_target_state(BINARY_STATES.ON)

        self.mood_light_monitor.set_target_state(BINARY_STATES.OFF)
        self.spotlight_monitor.set_target_state(BINARY_STATES.OFF)
        self.display.set_target_state(BINARY_STATES.OFF)

        self.playlist_monitor.set_target_state("relax")
        self.music_monitor.set_target_state(
            {
                "state": BINARY_STATES.ON,
                "volume": CONFIG["DEFAULT"].get("sleep_volumne", 50),
            }
        )

        if self._snooze_timer is not None:
            self._snooze_timer.cancel()

        if not self._sleep_mode_snooze:
            self.candle_monitor.set_target_state(BINARY_STATES.ON)
            # Turn Candle on for 3 min:
            if self.candle_timer is not None:
                self.candle_timer.cancel()

            self.candle_timer = Timer(
                float(CONFIG["DEFAULT"].get("candle_sleep_time", 180)),
                lambda: self.candle_monitor.set_target_state(BINARY_STATES.OFF),
            )
            self.candle_timer.start()

        if self.music_timer is not None:
            self.music_timer.cancel()

        self.music_timer = Timer(
            float(CONFIG["DEFAULT"].get("music_sleep_time", 300)),
            self.snooze_mode,
        )
        self.music_timer.start()



    def snooze_mode(self):
        self._sleep_mode_snooze = True
        if self._snooze_timer is not None:
            self._snooze_timer.cancel()

        self._snooze_timer = Timer(
            float(CONFIG["DEFAULT"].get("music_sleep_time", 300)),
            self.turn_off_everything,
        )
        self._snooze_timer.start()

    def play_music(self):
        self.ceiling_monitor.set_target_state((BINARY_STATES.OFF, -1))
        self.candle_monitor.set_target_state(BINARY_STATES.ON)
        self.mood_light_monitor.set_target_state(BINARY_STATES.ON)
        self.outlet_monitor.set_target_state(BINARY_STATES.ON)
        self.spotlight_monitor.set_target_state(BINARY_STATES.ON)
        # Display wird von music Monitor im State Change bedient
        self.music_monitor.set_target_state(
            {"state": BINARY_STATES.ON, "next_pressed": BINARY_STATES.ON}
        )

    def stop_music(self):
        self.ceiling_monitor.set_target_state(
            (BINARY_STATES.ON, CONFIG["DEFAULT"].get("stop_light_intensity", 255))
        )
        self.candle_monitor.set_target_state(BINARY_STATES.OFF)
        self.mood_light_monitor.set_target_state(BINARY_STATES.OFF)
        self.outlet_monitor.set_target_state(BINARY_STATES.OFF)
        self.spotlight_monitor.set_target_state(BINARY_STATES.OFF)
        self.music_monitor.set_target_state({"state": BINARY_STATES.OFF})
        self._sleep_mode_snooze = False

    def turn_off_everything(self):
        self.candle_monitor.set_target_state(BINARY_STATES.OFF)
        self.ceiling_monitor.set_target_state((BINARY_STATES.OFF, -1))
        self.outlet_monitor.set_target_state(BINARY_STATES.OFF)
        self.mood_light_monitor.set_target_state(SHUTDOWN_STATE.SHUTDOWN)
        self.spotlight_monitor.set_target_state(BINARY_STATES.OFF)
        self.music_monitor.set_target_state(
            {
                "state": BINARY_STATES.OFF,
                "refresh": BINARY_STATES.ON,
            }
        )
        self.display.set_target_state(BINARY_STATES.OFF)
        

    def next_playlist(self):
        self.playlist_monitor.set_target_state(1)

    def next_song(self):
        self.music_monitor.set_target_state(
            {"state": BINARY_STATES.ON, "next_pressed": BINARY_STATES.ON}
        )
        self.show(self.music_state.get("current_song", "Frosch"))

    def mood_ligth_mode(self):
        self.candle_monitor.set_target_state(BINARY_STATES.ON)
        self.ceiling_monitor.set_target_state((BINARY_STATES.OFF, -1))
        self.outlet_monitor.set_target_state(BINARY_STATES.OFF)
        self.mood_light_monitor.set_target_state(BINARY_STATES.ON)
        self.spotlight_monitor.set_target_state(BINARY_STATES.ON)
        self.music_monitor.set_target_state({"state": BINARY_STATES.OFF})
        self.display.set_target_state(BINARY_STATES.OFF)

    def update_candle_state(self, state):
        self.candle_state = state
        logger.debug("Updated Candle State to: %s", state)

    def update_outlet_state(self, state):
        self.outlet_state = state
        logger.debug("Updated Outlet State to: %s", state)

    def update_music_state(self, state: MUSIC_STATES):
        for key, value in state.items():
            self.music_state[key] = value

        if self.music_state["next_pressed"] == BINARY_STATES.ON:
            text = None
            if self.music_state["state"] == BINARY_STATES.ON:
                text = self.music_state.get("current_song", None)
            elif self.music_state["state"] == BINARY_STATES.OFF:
                text = self.music_state.get("playlist", None)

            if text is not None and text != "sleep":
                self.show(text)

        logger.debug("Updated Outlet State to: %s", state.get("state", "None"))

    def update_mood_light_state(self, state):
        self.mood_light_state = state
        logger.debug("Updated Mood Light State to: %s", state)

    def update_playlist_state(self, state: PLAYLIST_STATE_TYPE):
        self.playlist_state = state
        self.show(state[1])
        logger.debug("Updated Playlist State to: %s", state[1])

    def update_spotlight_state(self, state):
        self.spotlight_state = state
        logger.debug("Updated Spotlight State to: %s", state)

    def update_ceiling_light_state(self, state):
        self.ceiling_state = state
        logger.debug("Updated Ceiling State to: %s", state[0])

    def update_audio_state(self, state):
        self.audio_state = state
        logger.debug("Updated Audio State to: %s", state)

    def _enable_next_button(self):
        self._button_next_enabled = True

    def button_next_pressed(self):
        if not self._button_next_enabled:
            return

        self._button_next_enabled = False
        self._button_next_timer = Timer(
            self.BUTTON_DISABLE_TIME, self._enable_next_button
        )
        self._button_next_timer.start()

        print("Button NEXT pressed")

        if self.music_state.get("state") == BINARY_STATES.ON:
            self.next_song()
        else:
            self.next_playlist()

    def _enable_start_stop_button(self):
        self._button_start_stop_enabled = True

    def button_start_stop_pressed(self):
        if not self._button_start_stop_enabled:
            return

        self._button_start_stop_enabled = False
        self._button_start_stop_timer = Timer(
            self.BUTTON_DISABLE_TIME, self._enable_start_stop_button
        )
        self._button_start_stop_timer.start()

        print("Button START STOP pressed")
        if self.music_state.get("state") == BINARY_STATES.ON:
            self.stop_music()
        else:
            self.play_music()

    def _enable_sleep_button(self):
        self._button_sleep_enabled = True

    def button_sleep_pressed(self):
        if not self._button_sleep_enabled:
            return

        self._button_sleep_enabled = False
        self._button_sleep_timer = Timer(
            self.BUTTON_DISABLE_TIME, self._enable_sleep_button
        )
        self._button_sleep_timer.start()
        print("Button SLEEP pressed")
        self.sleep_mode()

    def button_sleep_relax_pressed(self):
        if not self._button_sleep_enabled:
            return

        self._button_sleep_enabled = False
        self._button_sleep_timer = Timer(
            self.BUTTON_DISABLE_TIME, self._enable_sleep_button
        )
        self._button_sleep_timer.start()
        print("Button SLEEP RELAX pressed")
        self.sleep_relax_mode()

    def _enable_mood_button(self):
        self._button_mood_enabled = True

    def button_mood_pressed(self):
        if not self._button_mood_enabled:
            return

        self._button_mood_enabled = False
        self._button_mood_timer = Timer(
            self.BUTTON_DISABLE_TIME, self._enable_mood_button
        )
        self._button_mood_timer.start()
        print("Button MOOD pressed")
        self.mood_ligth_mode()

    def button_shutdown_pressed(self):
        print("Button SHUT DOWN pressed")
        self.shut_down()

    def shut_down(self):
        self.turn_off_everything()
        # TODO weiteres TURN OFF fertig machen

    def show(self, text):
        if (
            type(self.playlist_state) != BASIS_STATES
            and self.playlist_state[0] != "sleep"
        ):
            if self.display_timer is not None:
                self.display_timer.cancel()

            self.display_timer = Timer(
                int(CONFIG["DEFAULT"].get("display_wait_time", 10)),
                lambda: self.display.set_target_state(BINARY_STATES.OFF),
            )
            self.display_timer.start()

            self.display.set_target_state(BINARY_STATES.ON)
            self.display.show(text)
