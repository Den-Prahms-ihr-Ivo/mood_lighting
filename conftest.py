import pytest
import os

# Setzen der Testumgebung
os.environ["TESTING_ENV"] = "testing"

from typing import Tuple
import sys
from unittest.mock import MagicMock

from tests.stubs import (
    display,
    audio_component,
    candle_motor,
    outlet_speaker,
    spotlight_component,
    ceiling_light,
    mood_light_component,
)


# Stubbing der verschiedenen Imports
sys.modules["src.mood_lighting.utility_components.display"] = display
sys.modules["src.mood_lighting.utility_components.candle_motor"] = candle_motor
sys.modules["src.mood_lighting.utility_components.outlet_speaker"] = outlet_speaker
sys.modules["src.mood_lighting.utility_components.audio_component"] = audio_component
sys.modules["src.mood_lighting.utility_components.mood_light_component"] = (
    mood_light_component
)
# sys.modules["src.mood_lighting.utility_components.music_component"] = music_component
sys.modules["src.mood_lighting.utility_components.ceiling_light"] = ceiling_light
sys.modules["src.mood_lighting.utility_components.spotlight_component"] = (
    spotlight_component
)


# Darf erst nach dem Setzen der Testumgebung importiert werden
from src.config import CONFIG
from src.mood_lighting import initialise_button_panel as INITIALISE_BP


def pytest_configure(config):
    # def pytest_configure(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    os.environ["TESTING_ENV"] = "testing"

    # Updating the DEFAULT config with the test config values
    for key, value in list(CONFIG["TEST"].items()):
        CONFIG.set("DEFAULT", key, value)

    # TODO:
    # ML.PLAYLIST.read_playlist()

    # Aufbauen


@pytest.fixture
def initialised_button_panel() -> Tuple[str]:
    """
    candle_monitor: Monitor,
    outlet_monitor: Monitor,
    audio_monitor: Monitor,
    mood_light_monitor: Monitor,
    music_monitor: MusicMonitor,
    display: Display,
    spotlight_monitor: Monitor,
    ceiling_monitor: Monitor,
    """
    bp = INITIALISE_BP()
    bp.music_component._load_playlist = MagicMock()
    bp.music_component._play = MagicMock()
    bp.music_component._stop = MagicMock()
    bp.music_component._next = MagicMock()
    bp.music_component._get_current_song = MagicMock()
    bp.music_component._get_current_song.return_value = "BITCHES"

    bp.initialise_states()
    return bp


"""

@pytest.fixture
def playlist() -> Playlist:
    
    p = Playlist()
    p.set_playlist("classic")
    return p
"""
