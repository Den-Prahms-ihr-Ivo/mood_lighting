from src import new_button_panel as BP
from src.config import CONFIG
from src.helper.mailer import send_mail
from src import new_outlet as OUTLET

import time


import RPi.GPIO as GPIO

from gpiozero import LED, Button


GPIO.setmode(GPIO.BCM)

START_STOP_PIN = int(CONFIG["DEFAULT"].get("SS_BUTTON_PIN", 16))
NEXT_PIN = int(CONFIG["DEFAULT"].get("NEXT_BUTTON_PIN", 25))
# START_STOP_PIN = int(CONFIG["DEFAULT"].get("SS_BUTTON_PIN", 16))
SLEEP_PIN = int(CONFIG["DEFAULT"].get("SLEEP_PIN", 22))
EMPTY_PIN = int(CONFIG["DEFAULT"].get("EMPTY_PIN", 25))
POWEROFF_BUTTON_PIN = int(CONFIG["DEFAULT"].get("POWEROFF_BUTTON_PIN", 12))

AUDIO_SWITCH_PIN = int(CONFIG["DEFAULT"].get("AUDIO_SWITCH", 5))
CANDLE_PIN = int(CONFIG["DEFAULT"].get("CANDLE_PIN", 20))


# GPIO.setup(NEXT_PIN, GPIO.IN)
# GPIO.setup(START_STOP_PIN, GPIO.IN)
# GPIO.setup(SLEEP_PIN, GPIO.IN)
# GPIO.setup(EMPTY_PIN, GPIO.IN)
# GPIO.setup(POWEROFF_BUTTON_PIN, GPIO.IN)

GPIO.setup(AUDIO_SWITCH_PIN, GPIO.OUT, initial=0)
GPIO.setup(CANDLE_PIN, GPIO.OUT, initial=0)
GPIO.setup(20, GPIO.OUT, initial=1)

next_btn = Button(NEXT_PIN)
start_stop_btn = Button(START_STOP_PIN)
sleep_btn = Button(SLEEP_PIN)
shutdown_btn = Button(POWEROFF_BUTTON_PIN, hold_time=2)
empty_btn = Button(EMPTY_PIN)

# audio_switch = LED(AUDIO_SWITCH_PIN)
# candle_pin = LED(CANDLE_PIN)

try:
    BP.init()
    OUTLET._turn_off()

except ConnectionRefusedError as e:
    send_mail(
        text="[Errno 111] Connection refused.\nTried to Initialize Button Panel and Connect to the MPD",
        title="MoodLight Connection Refused :(",
    )

    # TODO: SAFE SHUTDOWN
    GPIO.cleanup()
    print("\n\nTschöö, gä!")


if __name__ == "__main__":

    try:
        GPIO.setwarnings(False)

        next_btn.when_released = BP.button_next_pressed
        sleep_btn.when_released = BP.button_sleep_pressed
        start_stop_btn.when_released = BP.button_start_stop_pressed
        shutdown_btn.when_held = BP.button_light1_pressed
        empty_btn.when_released = BP.button_light2_pressed

        while True:
            time.sleep(0)

    except KeyboardInterrupt:
        # TODO: aufräumen

        # clean up
        GPIO.cleanup()

        print("\n\nTschöö, gä!")
