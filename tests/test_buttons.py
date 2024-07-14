import pytest
from src.helper.state_types import BINARY_STATES, TERTIARY_STATES
from src.mood_lighting.input_components.button_panel import ButtonPanel
from src.config import CONFIG
from time import sleep


@pytest.mark.parametrize(
    argnames="num_skips, expected_display_name",
    argvalues=[
        (1, "TECHNO"),
        (4, "CLASSICAL MUSIC"),
        (12, "CLASSICAL MUSIC"),
        (9, "TECHNO"),
        (3, "Stupid German Stuff"),
        (7, "Stupid German Stuff"),
    ],
)
def test_next_playlist(
    initialised_button_panel: ButtonPanel, num_skips, expected_display_name
):
    """Pressing the next-Button"""
    IBP = initialised_button_panel
    IBP.music_component._next.reset_mock()

    IBP.music_monitor.set_target_state({"state": BINARY_STATES.OFF})
    IBP.playlist_monitor.set_target_state("classic")

    assert IBP.music_monitor.get_current_state().get("state", None) == BINARY_STATES.OFF
    assert IBP.music_component._currently_playing == False

    for _ in range(0, num_skips):
        IBP.button_next_pressed()

    assert IBP.playlist_state[1] == expected_display_name
    assert not IBP.music_component._next.called


def test_next_song(initialised_button_panel: ButtonPanel):
    """Pressing the next-Button"""
    IBP = initialised_button_panel
    IBP.music_component._next.reset_mock()

    IBP.music_monitor.set_target_state(
        {"state": BINARY_STATES.ON, "next_pressed": BINARY_STATES.OFF}
    )
    IBP.playlist_monitor.set_target_state("classic")

    assert not IBP.music_component._next.called

    assert IBP.music_monitor.get_current_state().get("state", None) == BINARY_STATES.ON
    assert IBP.music_component._currently_playing == True

    IBP.button_next_pressed()

    assert IBP.music_component._next.called
    IBP.display.show.assert_called_with("BITCHES")
    sleep(float(CONFIG["DEFAULT"].get("display_wait_time", 10)) + 0.01)
    IBP.display.set_target_state.assert_called_with(BINARY_STATES.OFF)


def test_start_stop_button(initialised_button_panel: ButtonPanel):
    """
    Music läuft ==> Danach nicht mehr
    """
    IBP = initialised_button_panel
    IBP.music_component._next.reset_mock()

    IBP.music_monitor.set_target_state({"state": BINARY_STATES.OFF})
    assert IBP.music_component._currently_playing == False

    IBP.button_start_stop_pressed()

    IBP.music_monitor.set_target_state({"state": BINARY_STATES.ON})
    assert IBP.music_component._currently_playing == True

    IBP.button_start_stop_pressed()

    IBP.music_monitor.set_target_state({"state": BINARY_STATES.OFF})
    assert IBP.music_component._currently_playing == False


def test_start_stop_button_side_effects(initialised_button_panel: ButtonPanel):
    """
    MUSIK SPIELT
        DECKE OFF
        CANDLE ON
        MOODLIGHT ON
        STECKDOSE ON
        AUDIO ON
        SPOTLIGHT ON
        MUSIK ON

    MUSIK AUS:
        DECKE ON gedimmt
        CANDLE OFF
        MOOD LIGHT OFF
        STECKDOSE OFF
        AUDIO OFF
        SPOTLIGHT OFF
        MUSIC OFF

    """
    IBP = initialised_button_panel

    IBP.music_monitor.set_target_state({"state": BINARY_STATES.OFF})
    assert IBP.music_component._currently_playing == False

    IBP.playlist_monitor.set_target_state("classic")

    IBP.button_start_stop_pressed()

    IBP.music_monitor.set_target_state({"state": BINARY_STATES.ON})
    assert IBP.music_component._currently_playing == True

    # CEILING CHECK
    assert IBP.ceiling_monitor.get_current_state()[0] == BINARY_STATES.OFF
    assert IBP.ceiling_state[0] == BINARY_STATES.OFF
    assert IBP.ceiling_state[1] == 100

    # CANDLE
    assert IBP.candle_monitor.get_current_state() == BINARY_STATES.ON
    assert IBP.candle_state == BINARY_STATES.ON
    # MOOD LIGHT
    assert IBP.mood_light_monitor.get_current_state() == BINARY_STATES.ON
    assert IBP.mood_light_state == BINARY_STATES.ON
    # OUTLET
    assert IBP.outlet_monitor.get_current_state() == BINARY_STATES.ON
    assert IBP.outlet_state == BINARY_STATES.ON
    # AUDIO
    assert IBP.audio_monitor.get_current_state() == BINARY_STATES.ON
    assert IBP.audio_state == BINARY_STATES.ON
    # SPOTLIGHT
    assert IBP.spotlight_monitor.get_current_state() == BINARY_STATES.ON
    assert IBP.spotlight_state == BINARY_STATES.ON

    IBP.display.set_target_state.assert_called_with(BINARY_STATES.ON)
    assert IBP.display.show.called

    IBP.button_start_stop_pressed()

    IBP.music_monitor.set_target_state({"state": BINARY_STATES.OFF})
    assert IBP.music_component._currently_playing == False

    # CEILING CHECK
    assert IBP.ceiling_monitor.get_current_state()[0] == BINARY_STATES.ON
    assert IBP.ceiling_state[0] == BINARY_STATES.ON
    assert IBP.ceiling_state[1] == CONFIG["DEFAULT"].get("stop_light_intensity", 255)

    # CANDLE
    assert IBP.candle_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.candle_state == BINARY_STATES.OFF
    # MOOD LIGHT
    assert IBP.mood_light_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.mood_light_state == BINARY_STATES.OFF
    # OUTLET
    assert IBP.outlet_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.outlet_state == BINARY_STATES.OFF
    # AUDIO
    assert IBP.audio_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.audio_state == BINARY_STATES.OFF
    # SPOTLIGHT
    assert IBP.spotlight_monitor.get_current_state() == BINARY_STATES.OFF
    assert IBP.spotlight_state == BINARY_STATES.OFF

    sleep(float(CONFIG["DEFAULT"].get("display_wait_time", 10)) + 0.01)
    IBP.display.set_target_state.assert_called_with(BINARY_STATES.OFF)


def test_shut_down(initialised_button_panel: ButtonPanel):
    """
    popo
    """
    IBP = initialised_button_panel
    # TODO: Das fehlt, glaube ich noch
    # Sowie die eigentlich implementierung.
