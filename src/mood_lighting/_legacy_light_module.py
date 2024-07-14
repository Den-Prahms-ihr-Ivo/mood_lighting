import RPi.GPIO as GPIO

from typing import Optional
from gpiozero import LED, Button
from threading import Thread
from queue import Queue

# pip install rpi-ws281x
# Muss leider als sudo ausgeführt werden
from rpi_ws281x import PixelStrip, ws, Color

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
    NEXT_BUTTON: Optional[Button] = None
    _LED_STRIP = None
    _LED_THREAD = None
    _LED_QUEUE = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Mood_Light, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        # GPIOs mit GPIO-Nummer ansprechen
        GPIO.setmode(GPIO.BCM)

        # Geteilte Warteschlange
        self._LED_QUEUE = Queue()

        # Consumer definieren
        self._LED_THREAD = Thread(
            target=self.led_consumer, args=(self._LED_QUEUE, self._LED_STRIP)
        )

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
        led_strip = ws.WS2811_STRIP_GRB

        self._LED_STRIP = PixelStrip(
            LED_COUNT,
            LED_COM,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL,
            led_strip,
        )
        # Intialize the library (must be called once before other functions).
        self._LED_STRIP.begin()
        self._LED_THREAD.start()

    def turn_on(self) -> None:
        """"""
        # TODO: implement
        print(f"Turning Mood Lighting ON")
        self._LED_QUEUE.put()

    def turn_off(self) -> None:
        """"""
        # TODO: implement
        print(f"Turning Mood Lighting OFF")
        # SET LOW!!!!
        # TODO: das zum initialisieren machen

    # ###########################################
    # Consumer Definition
    # ###########################################
    #
    # TODO: Consumer bearbeiten und entsprechend die Funktionsaufrufe
    # anpassen.
    # ==> keine direkten aufrufe, sondern PUTs into queue
    def led_consumer(self, queue: Queue, led_strip):
        print("LED Consumer läuft...")
        while True:
            item = queue.get()

            if item is None:
                # LEDs auschhalten & Loop beenden
                break

            # item hat jetzt die Form (LED_Mode, LED_Strip Objekt, signal )
            mode, led_strip, signal = item  # TODO: Mode shutdpwn

            if mode == LED_Mode.playlist:
                process_playlist_change(led_strip, signal)

            elif mode == LED_Mode.song:
                process_song_change(led_strip, signal)

            elif mode == LED_Mode.startup:
                animate_startup(led_strip)

            elif mode == LED_Mode.ready:
                animate_ready(led_strip, signal)

            elif mode == LED_Mode.shutdown:
                animate_shutdown(led_strip)
                break

        print("LED Consumer ist fertig!")
