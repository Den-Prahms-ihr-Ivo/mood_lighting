import pytest
from src.helper.state_types import BINARY_STATES, TERTIARY_STATES
from src.mood_lighting.input_components.button_panel import ButtonPanel
from src.config import CONFIG
from time import sleep


def test_playlist_init(initialised_button_panel: ButtonPanel):
    """
    Testing the initial states of the System
    """
    IBP = initialised_button_panel

    assert IBP.playlist_state is not None


@pytest.mark.parametrize(
    argnames="desired_playlist_key, expected_display_name",
    argvalues=[
        ("classic", "CLASSICAL MUSIC"),
        ("german", "Stupid German Stuff"),
        ("techno", "TECHNO"),
    ],
)
def test_explicit_playlist_switch(
    initialised_button_panel: ButtonPanel, desired_playlist_key, expected_display_name
):
    """Changing to an explicit playlist"""
    # spy = mocker.spy(playlist_module, "display_playlist")
    # spy.assert_called_once_with(desired_playlist)
    IBP = initialised_button_panel

    IBP.playlist_monitor.set_target_state(desired_playlist_key)
    assert IBP.playlist_state[1] == expected_display_name
