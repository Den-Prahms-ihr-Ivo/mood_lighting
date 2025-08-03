from typing import Optional, Callable
from subprocess import run
from src.helper.utility_component import Utility_Component
from enum import Enum
from threading import Timer
from src.config import CONFIG

import RPi.GPIO as GPIO


class TERTIARY_STATES(Enum):
    ON = 0
    OFF = 1
    IDLE_CNT_DWN = 2


current_state = TERTIARY_STATES.OFF
cnt_dwn_timer = None
audio_switch_timer = None


def set_state(desired_state):
    global current_state

    # Ist gerade an
    if current_state == TERTIARY_STATES.ON:
        if desired_state:
            # ist schon an und soll an... do nothing
            return
        else:
            _start_count_down()
            current_state = TERTIARY_STATES.IDLE_CNT_DWN

    elif current_state == TERTIARY_STATES.IDLE_CNT_DWN:
        if desired_state:
            _cancel_count_down()
            current_state = TERTIARY_STATES.ON
        else:
            return
    else:
        if desired_state:
            current_state = TERTIARY_STATES.ON
            _turn_on()


def _start_count_down():
    global cnt_dwn_timer
    if cnt_dwn_timer is not None:
        cnt_dwn_timer.cancel()

    cnt_dwn_timer = Timer(int(CONFIG["DEFAULT"].get("speaker_idle_time_out", 20)), _off)
    cnt_dwn_timer.start()


def _cancel_count_down():
    if cnt_dwn_timer is not None:
        cnt_dwn_timer.cancel()


def _off():
    global current_state
    current_state = TERTIARY_STATES.OFF
    _turn_off()


def _turn_off():
    run(
        [
            "mosquitto_pub",
            "-t",
            "zigbee2mqtt/Schlafzimmer_Steckdose_1/set",
            "-m",
            '{"state": "OFF"}',
        ]
    )


def _turn_on():
    global current_state
    run(
        [
            "mosquitto_pub",
            "-t",
            "zigbee2mqtt/Schlafzimmer_Steckdose_1/set",
            "-m",
            '{"state": "ON"}',
        ]
    )
    current_state = TERTIARY_STATES.ON

    get_out_of_standby_mode()


def get_out_of_standby_mode():
    global audio_switch_timer
    if audio_switch_timer is not None:
        audio_switch_timer.cancel()

    audio_switch_timer = Timer(
        float(CONFIG["DEFAULT"].get("turn_audio_delay", 1)), _set_standby_high
    )
    audio_switch_timer.start()


def _set_standby_low():
    GPIO.output(CONFIG["DEFAULT"].get("AUDIO_SWITCH", 5), GPIO.LOW)


def _set_standby_high():
    global audio_switch_timer

    GPIO.output(CONFIG["DEFAULT"].get("AUDIO_SWITCH", 5), GPIO.HIGH)

    audio_switch_timer = Timer(
        float(CONFIG["DEFAULT"].get("speaker_switch_timer", 0.6)),
        _set_standby_low,
    )
    audio_switch_timer.start()
