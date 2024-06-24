# import RPi.GPIO as GPIO

from typing import Optional
from threading import Thread
from queue import Queue


# TODO: LED COntroller sollte in nem eigenen Thread laufen!!!!!
# Und dementsprechend auch gecancelt werden

# TODO: color und animation müssen noch ausgeklügelt werden

"""
    for i in range(0, LED_COUNT_HALF):
      led_strip.setPixelColor(i, Color(right_r, right_g, right_b))
    
    for i in range(LED_COUNT_HALF, led_strip.numPixels() - 3):
      led_strip.setPixelColor(i, Color(left_r, left_g, left_b))

      
    led_strip.show()
"""


class Mood_Light(object):
    """ """

    _instance = None
    # NEXT_BUTTON: Optional[Button] = None
    LED_STRIP = None
    LED_THREAD = None
    LED_QUEUE = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Mood_Light, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        # GPIOs mit GPIO-Nummer ansprechen
        # GPIO.setmode(GPIO.BCM)

        # Geteilte Warteschlange
        self.LED_QUEUE = Queue()

        # Consumer definieren
        self.LED_THREAD = Thread(target=self.led_consumer, args=(self.LED_QUEUE,))

        # Ein- und Ausgaenge definieren
        # GPIOs 18-21 Sind Tabu, die werden vom Audio Schild benutzt.
        # TODO: anpassen
        # GPIO.setup(PIR_SENSOR_GPIO, GPIO.IN)
        # movement_led       = LED(MOVEMENT_LED) # Konstanten 24
        # movement_spotlight = LED(MOVEMENT_SPOTLIGHT)

        # playlist_btn = Button(PLAYLIST_BUTTON)
        # shutdown_btn = Button(SHUTDOWN_BUTTON, hold_time=2)
        # empty_btn    = Button(EMPTY_BUTTON)

        # NeoPixel Definition
        # Intialize the library (must be called once before other functions).
        # self.LED_STRIP.begin()

        self.LED_THREAD.start()

    def turn_on(self) -> None:
        """"""
        # TODO: implement
        print(f"Turning Mood Lighting ON")
        self.LED_QUEUE.put("01")

    def turn_off(self) -> None:
        """"""
        # TODO: implement
        print(f"Turning Mood Lighting OFF")
        self.LED_QUEUE.put("BREAK")

    # ###########################################
    # Consumer Definition
    # ###########################################
    #
    # TODO: Consumer bearbeiten und entsprechend die Funktionsaufrufe
    # anpassen.
    # ==> keine direkten aufrufe, sondern PUTs into queue
    def led_consumer(cls, queue: Queue):
        print("LED Consumer läuft...")
        while True:
            item = queue.get()

            if item is None:
                # LEDs auschhalten & Loop beenden
                break

            # item hat jetzt die Form (LED_Mode, LED_Strip Objekt, signal )
            mode = item  # TODO: Mode shutdpwn

            if mode == "01":
                print("-- 01")

            elif mode == "02":
                print("-- 02")

            elif mode == "BREAK":
                print("-- BREAK")
                break

        print("LED Consumer ist fertig!")
