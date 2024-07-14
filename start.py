from src.mood_lighting import initialise_button_panel as INITIALISE_BP
from src.config import CONFIG
import time

import RPi.GPIO as GPIO

from gpiozero import LED, Button


GPIO.setmode(GPIO.BCM)

NEXT_PIN = CONFIG["DEFAULT"].get("NEXT_BUTTON_PIN", 25)
START_STOP_PIN = CONFIG["DEFAULT"].get("SS_BUTTON_PIN", 16)
SLEEP_PIN = CONFIG["DEFAULT"].get("SLEEP_PIN", 22)
EMPTY_PIN = CONFIG["DEFAULT"].get("EMPTY_PIN", 23)
POWEROFF_BUTTON_PIN = CONFIG["DEFAULT"].get("POWEROFF_BUTTON_PIN", 12)

AUDIO_SWITCH_PIN = CONFIG["DEFAULT"].get("AUDIO_SWITCH", 5)
CANDLE_PIN = CONFIG["DEFAULT"].get("CANDLE_PIN", 20)

GPIO.setup(NEXT_PIN, GPIO.IN)
GPIO.setup(START_STOP_PIN, GPIO.IN)
GPIO.setup(SLEEP_PIN, GPIO.IN)
GPIO.setup(EMPTY_PIN, GPIO.IN)
GPIO.setup(POWEROFF_BUTTON_PIN, GPIO.IN)

GPIO.setup(AUDIO_SWITCH_PIN, GPIO.OUT)
GPIO.setup(CANDLE_PIN, GPIO.OUT)

next_btn = Button(NEXT_PIN)
start_stop_btn = Button(START_STOP_PIN)
sleep_btn = Button(SLEEP_PIN)
shutdown_btn = Button(POWEROFF_BUTTON_PIN, hold_time=2)
empty_btn = Button(EMPTY_PIN)

audio_switch = LED(AUDIO_SWITCH_PIN)
candle_pin = LED(CANDLE_PIN)

bp = INITIALISE_BP()
bp.initialise_states()


if __name__ == "__main__":

    try:
        GPIO.setwarnings(False)

        next_btn.when_released = bp.button_next_pressed
        start_stop_btn.when_released = bp.button_start_stop_pressed
        sleep_btn.when_released = bp.button_sleep_pressed
        empty_btn.when_released = bp.button_mood_pressed
        shutdown_btn.when_held = bp.button_shutdown_pressed

        while True:
            time.sleep(0)

    except KeyboardInterrupt:
        # Sentinel Value in die Schlange hinzufügen und auf beenden des Threads warten
        # TODO: aufräumen

        # clean up
        GPIO.cleanup()

        print("\n\nTschöö, gä!")
