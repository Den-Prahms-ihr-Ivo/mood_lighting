from src.config import CONFIG

import RPi.GPIO as GPIO

import json
from pathlib import Path
from random import randrange
from threading import Timer
from subprocess import check_call

from src import new_usic_player as MUSIC_PLAYER
from src import new_candle as CANDLE
from src import new_ceiling as CEILING
from src import new_display as DISPLAY
from src import new_outlet as OUTLET
from src import new_mood_light as MOOD_LIGHT


music_playing = False
current_playlist_idx = 0
playlists = {}
snooze_timer = None
music_timer = None
sleep_mode_snooze = False
display_timer = None


def init_playlists():
    global playlists, current_playlist_idx
    playlist_path = Path(CONFIG["DEFAULT"]["playlist_json_path"])
    if not playlist_path.is_file():
        raise ValueError("Playlistpath doesn't exist :(")

    # print(t.is)
    with open(playlist_path, "r", encoding="UTF8") as f:
        playlists = json.load(f)

        current_playlist_idx = randrange(len(playlists.keys()))

    MUSIC_PLAYER.set_playlist(playlists.keys()[current_playlist_idx])


def get_next_playlist():
    global current_playlist_idx, playlists
    current_playlist_idx = (current_playlist_idx + 1) % len(playlists.keys())
    return playlists.keys()[current_playlist_idx]


def init():
    # Initialize Playlists:
    init_playlists()


def button_next_pressed():
    global music_playing, playlists
    if music_playing:
        MUSIC_PLAYER.next_song()
    else:
        next_playlist = get_next_playlist()
        show(playlists[next_playlist]["display_name"])
        MUSIC_PLAYER.set_playlist(next_playlist)


def button_start_stop_pressed():
    global music_playing
    if music_playing:
        MUSIC_PLAYER.set_state(False)
        mood_light_mode()
        music_playing = False
    else:
        MUSIC_PLAYER.set_state(True)
        stop_mood_light_mode()
        music_playing = True


def mood_light_mode():
    CEILING.set_state(False)
    DISPLAY.set_state(False)
    CANDLE.set_state(True)
    OUTLET.set_state(True)
    MOOD_LIGHT.set_state(True)


def stop_mood_light_mode():
    CEILING.set_intensity(CONFIG["DEFAULT"].get("stop_light_intensity", 255))
    CEILING.set_state(True)
    CANDLE.set_state(False)
    OUTLET.set_state(False)
    MOOD_LIGHT.set_state(False)
    MUSIC_PLAYER.set_state(False)


def turn_off_everything():
    CANDLE.set_state(False)
    CEILING.set_state(False)
    OUTLET.set_state(False)
    MOOD_LIGHT.set_state(False)
    MUSIC_PLAYER.set_state(False)
    DISPLAY.set_state(False)


def power_off():
    turn_off_everything()
    MOOD_LIGHT.shut_down()
    GPIO.cleanup()
    print("\n\nTschöö, gä!")
    check_call(["sudo", "poweroff"])


def snooze_mode():
    global sleep_mode_snooze, snooze_timer, music_playing
    sleep_mode_snooze = True
    music_playing = False

    if snooze_timer is not None:
        snooze_timer.cancel()

    snooze_timer = Timer(
        float(CONFIG["DEFAULT"].get("music_sleep_time", 300)),
        power_off,
    )
    snooze_timer.start()


def button_sleep_pressed():
    global snooze_timer, music_timer, music_playing

    CEILING.set_state(False)
    OUTLET.set_state(True)
    MOOD_LIGHT.set_state(False)
    DISPLAY.set_state(False)
    MUSIC_PLAYER.set_playlist("sleep")
    MUSIC_PLAYER.set_state(True)
    music_playing = True

    if snooze_timer is not None:
        snooze_timer.cancel()

    if music_timer is not None:
        music_timer.cancel()

    music_timer = Timer(
        float(CONFIG["DEFAULT"].get("music_sleep_time", 300)),
        snooze_mode,
    )
    music_timer.start()


def button_light1_pressed():
    CANDLE.toggle()


def button_light2_pressed():
    MOOD_LIGHT.toggle()


def show(text):
    global display_timer
    if display_timer is not None:
        display_timer.cancel()

    display_timer = Timer(
        int(CONFIG["DEFAULT"].get("display_wait_time", 10)),
        lambda: DISPLAY.set_state(False),
    )
    display_timer.start()

    DISPLAY.set_state(True)
    DISPLAY.show(text)
