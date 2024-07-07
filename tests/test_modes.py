import pytest
from src.helper.state_types import BINARY_STATES
from src.mood_lighting.input_components.button_panel import ButtonPanel
from src.config import CONFIG
from time import sleep


def test_init(initialised_button_panel: ButtonPanel):
    """
    Testing the initial states of the System
    """
    IBP = initialised_button_panel

    # CANDLE AND MOTOR CHECK
    assert IBP.candle_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.candle_state == BINARY_STATES.OFF

    # POWER OUTLET CHECK
    assert IBP.outlet_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.outlet_state == BINARY_STATES.OFF

    # MOOD LIGHT CHECK
    assert IBP.mood_light_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.mood_light_state == BINARY_STATES.OFF

    # SPOT LIGHT CHECK
    assert IBP.spotlight_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.spotlight_state == BINARY_STATES.OFF

    # AUDIO MONITOR CHECK
    assert IBP.audio_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.audio_state == BINARY_STATES.OFF

    # DISPLAY CHECK
    IBP.display.set_target_state.assert_called_with(BINARY_STATES.OFF)

    # MUSIC CHECK
    assert IBP.music_monitor.get_current_state().get("state", None) == BINARY_STATES.OFF
    assert IBP.music_component._currently_playing == False
    assert IBP.music_state.get("state", None) == BINARY_STATES.OFF

    # TEST IF PLAYLIST IS INITIALISED AND NOT NONE


def test_sleep_mode(initialised_button_panel: ButtonPanel):
    """
    Testing the sleep mode.
    This Test includes a few time-out tests

    MUSIK AN
    LICHT AUS
    KERZE AN (für 5 min)
    MUSIK AUS (nach 30 min)

    """
    IBP = initialised_button_panel
    IBP.music_component._stop.reset_mock()
    IBP.music_component._play.reset_mock()
    IBP.display.set_target_state.reset_mock()
    IBP.sleep_mode()

    # ################################################
    # PRE TIMEOUT STATES
    # ################################################
    assert IBP.ceiling_monitor.get_current_state()[0] == BINARY_STATES.OFF
    assert IBP.ceiling_state[0] == BINARY_STATES.OFF
    assert IBP.ceiling_state[1] == 100

    assert IBP.outlet_monitor.get_current_state() == BINARY_STATES.ON
    assert IBP.outlet_state == BINARY_STATES.ON

    assert IBP.audio_monitor.get_current_state() == BINARY_STATES.ON
    assert IBP.audio_state == BINARY_STATES.ON

    assert IBP.mood_light_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.mood_light_state == BINARY_STATES.OFF

    assert IBP.spotlight_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.spotlight_state == BINARY_STATES.OFF

    IBP.display.set_target_state.assert_called_with(BINARY_STATES.OFF)

    assert IBP.music_state.get("state", None) == BINARY_STATES.ON
    assert IBP.music_component._currently_playing == True
    assert IBP.playlist_state[1] == "Schlafmodus"
    assert IBP.music_state.get("volume", None) == CONFIG["DEFAULT"].get("sleep_volumne")

    assert IBP.candle_monitor.get_current_state() == BINARY_STATES.ON
    assert IBP.candle_state == BINARY_STATES.ON

    # assert IBP.music_component._play.assert()
    assert not IBP.music_component._stop.called
    IBP.music_component._play.assert_called()

    # ################################################
    # FIRST TIME OUT
    # ################################################
    # Wait for the shortend Time-Out
    sleep(float(CONFIG["DEFAULT"].get("candle_sleep_time", 10)) + 0.01)

    # CANDLE AND MOTOR CHECK
    assert IBP.candle_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.candle_state == BINARY_STATES.OFF

    # ################################################
    # SECOND TIME OUT
    # ################################################
    # Wait for the shortend Time-Out
    sleep(float(CONFIG["DEFAULT"].get("music_sleep_time", 10)) + 0.01)

    assert IBP.music_state.get("state", None) == BINARY_STATES.OFF
    assert IBP.music_component._currently_playing == False
    # IBP.display.set_target_state.assert_called_with(BINARY_STATES.OFF)

    assert IBP.candle_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.candle_state == BINARY_STATES.OFF

    assert IBP.ceiling_monitor.get_current_state()[0] == BINARY_STATES.OFF
    assert IBP.ceiling_state[0] == BINARY_STATES.OFF
    assert IBP.ceiling_state[1] == 100

    assert IBP.outlet_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.outlet_state == BINARY_STATES.OFF

    assert IBP.audio_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.audio_state == BINARY_STATES.OFF

    assert IBP.mood_light_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.mood_light_state == BINARY_STATES.OFF

    assert IBP.spotlight_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.spotlight_state == BINARY_STATES.OFF

    IBP.music_component._stop.assert_called()
