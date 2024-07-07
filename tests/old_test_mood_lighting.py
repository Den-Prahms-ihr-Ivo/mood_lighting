"""
High Level Tests, testing the desired state transitions
"""

import pytest
from time import sleep
from src.config import CONFIG, CONTROLLER
import src.mood_lighting as ML
from src.mood_lighting import (
    # CONTROLLER,
    PLAYLIST,
    DISPLAY,
    PLAYER,
    MOOD_LIGHT,
    ZIGBEE,
    next_button_pressed,
)


def test_next_playlist(mocker):
    """NEXT EVENT basic functionality

    Bei einem Druck auf den NEXT-Knopf soll die nächste Playlist ausgewählt werden
    und der entsprechende Name angezeigt werden.

    In diesem Test wird lediglich das Zusammenspiel getestet.
    """
    CONTROLLER["is_playing"] = False

    playlist_spy = mocker.spy(PLAYLIST, "next")
    player_spy = mocker.spy(PLAYER, "next")
    display_on_spy = mocker.spy(DISPLAY, "turn_on_display")
    display_off_spy = mocker.spy(DISPLAY, "turn_off_display")

    next_button_pressed()

    sleep(float(CONFIG["DEFAULT"].get("display_wait_time", 5)) + 1)

    assert playlist_spy.call_count == 1
    assert display_on_spy.call_count == 1
    assert display_off_spy.call_count == 1
    assert player_spy.call_count == 0

    CONTROLLER["is_playing"] = True

    next_button_pressed()

    assert player_spy.call_count == 1
    assert playlist_spy.call_count == 1
    assert display_on_spy.call_count == 2

    sleep(float(CONFIG["DEFAULT"].get("display_wait_time", 5)) + 1)

    assert display_off_spy.call_count == 2


@pytest.mark.parametrize(
    argnames="num_skips, expected_display_name",
    argvalues=[
        (1, "TECHNO"),
        (9, "CLASSICAL MUSIC"),
        (10, "TECHNO"),
        (2, "Stupid German Stuff"),
        (11, "Stupid German Stuff"),
    ],
)
def test_next_playlist_multiple(playlist, mocker, num_skips, expected_display_name):
    """ """
    CONTROLLER["is_playing"] = False

    playlist_spy = mocker.spy(PLAYLIST, "next")
    display_on_spy = mocker.spy(DISPLAY, "turn_on_display")
    display_off_spy = mocker.spy(DISPLAY, "turn_off_display")
    player_spy = mocker.spy(PLAYER, "next")

    for _ in range(0, num_skips):
        next_button_pressed()

    sleep(float(CONFIG["DEFAULT"].get("display_wait_time", 5)) + 0.25)

    assert playlist_spy.call_count == num_skips
    assert display_on_spy.call_count == num_skips
    assert display_off_spy.call_count == 1
    assert player_spy.call_count == 0
    assert playlist.current_playlist["display_name"] == expected_display_name

    CONTROLLER["is_playing"] = True

    for _ in range(0, num_skips):
        next_button_pressed()

    assert player_spy.call_count == num_skips
    assert playlist_spy.call_count == num_skips
    assert display_on_spy.call_count == 2 * num_skips

    sleep(float(CONFIG["DEFAULT"].get("display_wait_time", 5)) + 0.25)
    assert display_off_spy.call_count == 2


def test_start_stop_button_pressed():
    """
    SS active entire SYSTEM inactive => press SS => SS inactive, entire SYSTEM active => wait => SS active, entire SYSTEM active
    => press SS => SS inactive, entire SYSTEM inactive => wait => SS active, entire SYSTEM inactive
    """
    CONTROLLER["is_playing"] = False

    assert CONTROLLER["start_stop_button_is_active"]
    assert not CONTROLLER["is_playing"]

    ML.start_stop_button_pressed()
    sleep(0.01)

    assert not CONTROLLER["start_stop_button_is_active"]
    assert CONTROLLER["is_playing"]

    sleep(float(CONFIG["DEFAULT"].get("start_stop_button_wait_time", 5)) + 0.1)

    assert CONTROLLER["start_stop_button_is_active"]
    assert CONTROLLER["is_playing"]

    ML.start_stop_button_pressed()
    sleep(0.01)

    assert not CONTROLLER["start_stop_button_is_active"]
    assert not CONTROLLER["is_playing"]

    sleep(float(CONFIG["DEFAULT"].get("start_stop_button_wait_time", 5)) + 0.1)

    assert CONTROLLER["start_stop_button_is_active"]
    assert not CONTROLLER["is_playing"]


def test_system_power_on(mocker):
    """
    SYSTEM POWER ON
    Desired States:
    => Shuffle Mode: ON
    => Continous Mode: ON
    => Repeat Mode: ON
    => Active Speaker: ON
    => Start Active Speaker Idle Timer
    => Ceiling Lamp: ON
    => All other Lights: OFF
    """
    # SETUP
    shuffle_spy = mocker.spy(PLAYER, "set_shuffle_mode")
    cont_spy = mocker.spy(PLAYER, "set_countinous_mode")
    repeat_spy = mocker.spy(PLAYER, "set_repeat_mode")

    speaker_on_spy = mocker.spy(ZIGBEE, "turn_on_speaker")
    speaker_off_spy = mocker.spy(ZIGBEE, "turn_off_speaker")
    ceiling_lamp_spy = mocker.spy(ZIGBEE, "turn_on_ceiling")

    mood_spy = mocker.spy(MOOD_LIGHT, "turn_off")

    # ACTUAL CALL

    ML.system_power_on()
    sleep(0.01)

    # ASSERTIONS
    shuffle_spy.assert_called_once_with("ON")
    cont_spy.assert_called_once_with("ON")
    repeat_spy.assert_called_once_with("ON")
    assert speaker_on_spy.call_count == 1
    assert ceiling_lamp_spy.call_count == 1
    assert mood_spy.call_count == 1

    # Time Out Assertions
    sleep(float(CONFIG["DEFAULT"].get("speaker_idle_time_out", 5)) + 0.1)
    assert speaker_off_spy.call_count == 1


def test_start_event_active(mocker):
    """
    Desired States:
    => Mood Lights ON (all)
    => Ceiling Light OFF
    => Music START
    => Display current SONG
    ==> IF ACTIVE SPEAKER = ON:
          CANCEL SPEAKER IDLE TIMER
        ELSE
          TURN SPEAKER ON
    """
    # SETUP
    CONTROLLER["speaker_is_powered_on"] = True
    mood_light_on_spy = mocker.spy(MOOD_LIGHT, "turn_on")
    ceiling_off_spy = mocker.spy(ZIGBEE, "turn_off_ceiling")
    speaker_timer_spy = mocker.spy(ZIGBEE, "cancel_speaker_idle_timer")
    speaker_turn_on = mocker.spy(ZIGBEE, "turn_on_speaker")
    music_play_spy = mocker.spy(PLAYER, "play")
    display_spy = mocker.spy(DISPLAY, "display")

    # ACTUAL CALL
    ML.start_event()
    sleep(0.01)

    # ASSERTIONS
    assert mood_light_on_spy.call_count == 1
    assert ceiling_off_spy.call_count == 1
    assert speaker_timer_spy.call_count == 1
    assert speaker_turn_on.call_count == 0
    assert music_play_spy.call_count == 1
    assert display_spy.call_count == 1
    #
    assert CONTROLLER["is_playing"]


def test_start_event_inactive(mocker):
    """
    Desired States:
    => Mood Lights ON (all)
    => Ceiling Light OFF
    => Music START
        IF ACTIVE SPEAKER = ON:
          CANCEL SPEAKER IDLE TIMER
    ==> ELSE
          TURN SPEAKER ON
    """
    # SETUP
    CONTROLLER["speaker_is_powered_on"] = False

    mood_light_on_spy = mocker.spy(MOOD_LIGHT, "turn_on")
    ceiling_off_spy = mocker.spy(ZIGBEE, "turn_off_ceiling")
    speaker_timer_spy = mocker.spy(ZIGBEE, "cancel_speaker_idle_timer")
    speaker_turn_on = mocker.spy(ZIGBEE, "turn_on_speaker")
    music_play_spy = mocker.spy(PLAYER, "play")
    display_spy = mocker.spy(DISPLAY, "display")

    # ACTUAL CALL
    ML.start_event()
    sleep(0.01)

    # ASSERTIONS
    assert mood_light_on_spy.call_count == 1
    assert ceiling_off_spy.call_count == 1
    assert speaker_timer_spy.call_count == 0
    assert speaker_turn_on.call_count == 1
    assert music_play_spy.call_count == 1
    assert display_spy.call_count == 1
    #
    assert CONTROLLER["is_playing"]


def test_stop_event(mocker):
    """
    Desired States:
    => Mood Lights OFF (all)
    => Turn on Ceiling light at X Percent
    => Music STOP
    => Activate SPEAKER IDLE TIMER
    => is_playing FALSE
    """
    # SETUP
    CONTROLLER["is_playing"] = True

    mood_light_on_spy = mocker.spy(MOOD_LIGHT, "turn_off")
    speaker_timer_spy = mocker.spy(ZIGBEE, "reset_speaker_idle_timer")
    speaker_off_spy = mocker.spy(ZIGBEE, "turn_off_speaker")
    ceiling_on_spy = mocker.spy(ZIGBEE, "turn_on_ceiling")
    music_play_spy = mocker.spy(PLAYER, "stop")

    # ACTUAL CALL
    ML.stop_event()
    sleep(0.01)

    # ASSERTIONS
    assert mood_light_on_spy.call_count == 1
    assert speaker_timer_spy.call_count == 1
    assert music_play_spy.call_count == 1
    ceiling_on_spy.assert_called_once_with(
        CONFIG["DEFAULT"].get("start_stop_button_wait_time", 5)
    )
    #
    assert not CONTROLLER["is_playing"]

    # TIME OUTs
    sleep(float(CONFIG["DEFAULT"].get("speaker_idle_time_out", 5)) + 0.1)
    assert speaker_off_spy.call_count == 1
    assert not CONTROLLER["speaker_is_powered_on"]
