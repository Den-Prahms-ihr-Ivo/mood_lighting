from threading import Timer

from src.mood_lighting.playlist_module import Playlist
from src.mood_lighting.display_module import Display
from src.mood_lighting.light_module import Mood_Light
from src.mood_lighting.zigbee_module import Zigbee
from src.mood_lighting.music_module import MusicPlayer
from src.mood_lighting.config import CONFIG, CONTROLLER

from time import sleep

# used sigletons
PLAYLIST = Playlist()
DISPLAY = Display()
PLAYER = MusicPlayer()
MOOD_LIGHT = Mood_Light()
ZIGBEE = Zigbee()


def system_power_on():
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
    PLAYER.set_shuffle_mode("ON")
    PLAYER.set_countinous_mode("ON")
    PLAYER.set_repeat_mode("ON")

    ZIGBEE.turn_on_speaker()
    ZIGBEE.turn_on_ceiling()
    ZIGBEE.reset_speaker_idle_timer()

    MOOD_LIGHT.turn_off()


def _enable_start_stop_button():
    CONTROLLER["start_stop_button_is_active"] = True


def start_stop_button_pressed():
    """
    What happens if the start/stop button is pressed, depends on the current state of the system.

    After toggling the current state, the button shall be disabled for START_STOP_BUTTON_WAIT_TIME amount of time.

    Desired States:
    IF ACTIVE
      => System becomes inactive
      => Button becomes inactive for an amount of time
    IF INACTIVE
      => System becomes active
      => Button becomes inactive for an amount of time
    """

    if CONTROLLER["start_stop_button_is_active"]:
        if CONTROLLER["is_playing"]:
            stop_event()
        else:
            start_event()

        CONTROLLER["start_stop_button_is_active"] = False
        timer = Timer(
            float(CONFIG["DEFAULT"].get("start_stop_button_wait_time", 5)),
            _enable_start_stop_button,
        )
        timer.start()


def start_event():
    """
    Desired States:
    => Mood Lights ON (all)
    => Ceiling Light OFF
    => Music START
    => Display current SONG
    => speaker_is_powered_on TRUE
    => is_playing = TURE
    IF ACTIVE SPEAKER = ON:
        CANCEL SPEAKER IDLE TIMER
    ELSE
        TURN SPEAKER ON
    """

    MOOD_LIGHT.turn_on()
    ZIGBEE.turn_off_ceiling()
    current_song = PLAYER.play()
    DISPLAY.display(current_song)
    if CONTROLLER["speaker_is_powered_on"]:
        ZIGBEE.cancel_speaker_idle_timer()
    else:
        ZIGBEE.turn_on_speaker()


def stop_event():
    """
    Desired States:
    => Mood Lights OFF (all)
    => Return Ceiling Light at "percentage_ceiling_light"
    => Music STOP
    => Activate SPEAKER IDLE TIMER
    => is_playing FALSE
    """
    MOOD_LIGHT.turn_off()
    ZIGBEE.turn_on_ceiling(
        value=CONFIG["DEFAULT"].get("start_stop_button_wait_time", 5)
    )
    ZIGBEE.reset_speaker_idle_timer()
    PLAYER.stop()


def next_button_pressed():
    """
    Desired States:
    ACTIVE MODE:
      => Skipped to the next Song
      => Current Song is displayed

    INACTIVE MODE:
      => Skipped to the next Playlist
      => Current Playlist is displayed
    """

    if CONTROLLER["is_playing"]:
        # If music is currently playing, the NEXT Button skips to the next song.
        PLAYER.next()

        DISPLAY.display(PLAYER.get_playing())
    else:
        # If music is not currently playing, the NEXT Button skips to the next Playlist.
        PLAYLIST.next()
        # TODO: DISPLAY NAME IS THE WRONG ATTRIBUTE!
        PLAYER.load(PLAYLIST.current_playlist["display_name"])

        DISPLAY.display(PLAYLIST.current_playlist["display_name"])


if __name__ == "__main__":
    system_power_on()

    # TODO: Musicplayer get current song.
    # ==> könntest du über diesen weg lösen:
    # Als system command
    # mpc idle player

    try:
        # TODO: Hinzufügen der ganzen Buttons
        MOOD_LIGHT.NEXT_BUTTON.when_released = next_button_pressed
        # GPIO.setwarnings(False)
        # GPIO.add_event_detect(PIR_SENSOR_GPIO, GPIO.RISING,  callback=detect_movement)

        # playlist_btn.when_released = playlist_callback
        # shutdown_btn.when_held = shutdown_callback
        # empty_btn.when_released = empty_callback
        while True:
            if CONTROLLER["is_playing"]:
                cs = PLAYER.get_playing()
                if not cs == PLAYER.current_song:
                    PLAYER.current_song = cs
                    DISPLAY.display(cs)
            sleep(0)

    except KeyboardInterrupt:
        # TODO Logging
        print("Keyboard interrupt")
    except Exception as e:
        # TODO: Logging
        print("Something went wrong")
    finally:
        # CLEAN UP
        DISPLAY.clean_up()
        PLAYER.clean_up()
        # TODO: LOGGING
