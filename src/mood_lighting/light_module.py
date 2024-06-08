import RPi.GPIO as GPIO

from typing import Optional
from gpiozero import LED, Button


class Mood_Light(object):
    """ """

    _instance = None
    NEXT_BUTTON: Optional[Button] = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Mood_Light, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        # GPIOs mit GPIO-Nummer ansprechen
        GPIO.setmode(GPIO.BCM)

        # Ein- und Ausgaenge definieren
        # GPIOs 18-21 Sind Tabu, die werden vom Audio Schild benutzt.
        # TODO: anpassen
        # GPIO.setup(PIR_SENSOR_GPIO, GPIO.IN)
        # movement_led       = LED(MOVEMENT_LED) # Konstanten 24
        # movement_spotlight = LED(MOVEMENT_SPOTLIGHT)

        # playlist_btn = Button(PLAYLIST_BUTTON)
        # shutdown_btn = Button(SHUTDOWN_BUTTON, hold_time=2)
        # empty_btn    = Button(EMPTY_BUTTON)

    def turn_on(self) -> None:
        """"""
        # TODO: implement
        print(f"Turning Mood Lighting ON")

    def turn_off(self) -> None:
        """"""
        # TODO: implement
        print(f"Turning Mood Lighting OFF")
