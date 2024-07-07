import pytest


def test_initialize_playlist(fresh_playlist):
    """Test if a random Playlist is selected in while initializing the Playlist class"""
    assert fresh_playlist.current_playlist is not None


@pytest.mark.parametrize(
    argnames="desired_playlist_key, expected_display_name",
    argvalues=[
        ("classic", "CLASSICAL MUSIC"),
        ("german", "Stupid German Stuff"),
        ("techno", "TECHNO"),
    ],
)
def test_explicit_playlist_switch(
    fresh_playlist, mocker, desired_playlist_key, expected_display_name
):
    """Changing to an explicit playlist"""
    # spy = mocker.spy(playlist_module, "display_playlist")
    # spy.assert_called_once_with(desired_playlist)
    fresh_playlist.set_playlist(desired_playlist_key)
    assert fresh_playlist.current_playlist["display_name"] == expected_display_name


@pytest.mark.parametrize(
    argnames="num_skips, expected_display_name",
    argvalues=[
        (1, "TECHNO"),
        (3, "CLASSICAL MUSIC"),
        (9, "CLASSICAL MUSIC"),
        (10, "TECHNO"),
        (2, "Stupid German Stuff"),
        (11, "Stupid German Stuff"),
    ],
)
def test_next_playlist(playlist, num_skips, expected_display_name):
    """pressing the next() event"""
    for _ in range(0, num_skips):
        playlist.next()

    assert playlist.current_playlist["display_name"] == expected_display_name
