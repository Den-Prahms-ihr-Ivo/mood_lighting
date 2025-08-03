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

BUTTON_DISABLE_TIME = 1

music_playing = False
current_playlist_idx = 0
playlists = {}
snooze_timer = None
music_timer = None
sleep_mode_snooze = False
display_timer = None
buttons_enabled = True


def init_playlists():
    global playlists, current_playlist_idx
    playlist_path = Path(CONFIG["DEFAULT"]["playlist_json_path"])
    if not playlist_path.is_file():
        raise ValueError("Playlistpath doesn't exist :(")

    # print(t.is)
    with open(playlist_path, "r", encoding="UTF8") as f:
        playlists = json.load(f)

        current_playlist_idx = randrange(len(playlists.keys()))

    MUSIC_PLAYER.set_playlist(list(playlists.keys())[current_playlist_idx])
    print(playlists.keys())
    print(len(playlists.keys()))


def get_next_playlist():
    global current_playlist_idx, playlists
    current_playlist_idx = (current_playlist_idx + 1) % len(playlists.keys())
    return list(playlists.keys())[current_playlist_idx]


def init():
    # Initialize Playlists:
    init_playlists()
    turn_off_everything()


def button_next_pressed():
    global music_playing, playlists, buttons_enabled

    if not buttons_enabled:
        return
    buttons_enabled = False
    button_start_stop_timer = Timer(BUTTON_DISABLE_TIME, enable_buttons)
    button_start_stop_timer.start()

    print("BUTTON NEXT PRESSED")

    if music_playing:
        MUSIC_PLAYER.next_song()
    else:
        next_playlist = get_next_playlist()
        show(playlists[next_playlist]["display_name"])
        MUSIC_PLAYER.set_playlist(next_playlist)


def button_start_stop_pressed():
    global music_playing, buttons_enabled

    if not buttons_enabled:
        return
    buttons_enabled = False
    button_start_stop_timer = Timer(BUTTON_DISABLE_TIME, enable_buttons)
    button_start_stop_timer.start()

    print("BUTTON START STOP PRESSED")

    if music_playing:
        MUSIC_PLAYER.set_state(False)
        stop_mood_light_mode()
        music_playing = False
    else:
        MUSIC_PLAYER.set_state(True)
        mood_light_mode()
        music_playing = True


def mood_light_mode():
    print("start mood ligth")
    CEILING.set_state(False)
    DISPLAY.set_state(False)
    CANDLE.set_state(True)
    OUTLET.set_state(True)
    MOOD_LIGHT.set_state(True)


def stop_mood_light_mode():
    print("stop mood light")
    CEILING.set_intensity(int(CONFIG["DEFAULT"].get("stop_light_intensity", 255)))
    CEILING.set_state(True)
    CANDLE.set_state(False)
    OUTLET.set_state(False)
    MOOD_LIGHT.set_state(False)
    MUSIC_PLAYER.set_state(False)


def turn_off_everything():
    global music_playing

    music_playing = False
    print("turn off everything")
    CANDLE.set_state(False)
    CEILING.set_state(False)
    OUTLET.set_state(False)
    MOOD_LIGHT.set_state(False)
    MUSIC_PLAYER.set_state(False)
    DISPLAY.set_state(False)


def power_off():
    print("Power off")
    turn_off_everything()
    MOOD_LIGHT.shut_down()
    GPIO.cleanup()
    print("\n\nTschöö, gä!")
    check_call(["sudo", "poweroff"])


def snooze_mode():
    print("SNOOZE MODE")
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
    global snooze_timer, music_timer, music_playing, buttons_enabled

    if not buttons_enabled:
        return
    buttons_enabled = False
    button_start_stop_timer = Timer(BUTTON_DISABLE_TIME, enable_buttons)
    button_start_stop_timer.start()

    print("BUTTON SLEEP PRESSED")

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
    global buttons_enabled

    if not buttons_enabled:
        return
    buttons_enabled = False
    button_start_stop_timer = Timer(BUTTON_DISABLE_TIME, enable_buttons)
    button_start_stop_timer.start()

    print("BUTTON LIGHT 1 PRESSED")
    CANDLE.toggle()


def button_light2_pressed():
    global buttons_enabled

    if not buttons_enabled:
        return
    buttons_enabled = False
    button_start_stop_timer = Timer(BUTTON_DISABLE_TIME, enable_buttons)
    button_start_stop_timer.start()

    print("BUTTON LIGHT 2 PRESSED")
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


def enable_buttons():
    global buttons_enabled
    buttons_enabled = True
