import pytest
from src.mood_lighting.playlist_module import Playlist
from src.mood_lighting.config import CONFIG
import src.mood_lighting as ML


def pytest_configure(config):
    # def pytest_configure(session):
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """
    # Updating the DEFAULT config with the test config values
    for key, value in list(CONFIG["TEST"].items()):
        CONFIG.set("DEFAULT", key, value)

    ML.PLAYLIST.read_playlist()



@pytest.fixture
def fresh_playlist() -> Playlist:
    """Return an freshly initialized Playlist class"""
    return Playlist()


@pytest.fixture
def playlist() -> Playlist:
    """Returns a Playlist Class set to classic"""
    p = Playlist()
    p.set_playlist("classic")
    return p
