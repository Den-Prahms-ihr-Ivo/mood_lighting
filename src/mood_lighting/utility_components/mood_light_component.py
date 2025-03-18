from rpi_ws281x import PixelStrip, ws, Color

from typing import Optional, Callable

from src.helper.utility_component import Utility_Component
from src.helper.state_types import BINARY_STATES, SHUTDOWN_STATE
from threading import Thread
from enum import Enum
import time 
from queue import Queue

class LED_Mode(Enum):
    (off, animate, shutdown) = range(3)


LED_COUNT = 12
LED_COM = 13  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 1

LS = ws.WS2811_STRIP_GRB
LED_STRIP = PixelStrip(
    LED_COUNT,
    LED_COM,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL,
    LS,
)

def led_off(strip, wait_ms=50):
    for i in range(strip.numPixels(), strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
        
    strip.show()

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def led_animate(strip, wait_ms=100):

    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def led_consumer(queue: Queue):
  print("LED Consumer läuft...")

  while True:
    item = queue.get()

    if item is None:
      # LEDs auschhalten & Loop beenden
      break

    # item hat jetzt die Form (LED_Mode, LED_Strip Objekt, signal )
    mode, led_strip, signal = item 

    if mode == LED_Mode.animate:
        print("LED ANIMATE")
        led_animate(led_strip)

    elif mode == LED_Mode.off:
        print("LED OFF")
        led_off(led_strip)

    elif mode == LED_Mode.shutdown:
      #led_off(led_strip)
      led_off(led_strip)
      break

  print("LED Consumer ist fertig!")

led_queue = Queue()
led_thread = Thread(target=led_consumer, args=(led_queue,))
led_thread.start()

class MoodLightComponent(Utility_Component):
    """
    Nutzmodul für das Sportlight im Mood Light Modul.
    """

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)

        # Intialize the library (must be called once before other functions).
        LED_STRIP.begin()


    def target_state(self, desired_state: BINARY_STATES):
        # TODO: eigentliche Effekte...
        if desired_state == BINARY_STATES.ON:
            led_queue.put((LED_Mode.animate, LED_STRIP, None))

            self.actual_state(BINARY_STATES.ON)

        elif desired_state == SHUTDOWN_STATE.SHUTDOWN:
            led_queue.put((LED_Mode.shutdown, LED_STRIP, None))
            self.actual_state(BINARY_STATES.OFF)

        else:
            led_queue.put((LED_Mode.off, LED_STRIP, None))

            self.actual_state(BINARY_STATES.OFF)
