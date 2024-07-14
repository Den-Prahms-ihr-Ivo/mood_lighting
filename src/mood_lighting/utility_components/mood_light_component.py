from rpi_ws281x import PixelStrip, ws, Color

from typing import Optional, Callable

from src.helper.utility_component import Utility_Component
from src.helper.state_types import BINARY_STATES

LED_COUNT = 12
LED_COM = 13  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 1


class MoodLightComponent(Utility_Component):
    """
    Nutzmodul für das Sportlight im Mood Light Modul.
    """

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)

        LS = ws.WS2811_STRIP_GRB
        self.LED_STRIP = PixelStrip(
            LED_COUNT,
            LED_COM,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL,
            LS,
        )
        # Intialize the library (must be called once before other functions).
        self.LED_STRIP.begin()

    def target_state(self, desired_state: BINARY_STATES):
        # TODO: eigentliche Effekte...
        if desired_state == BINARY_STATES.ON:
            for i in range(0, LED_COUNT):
                self.LED_STRIP.setPixelColor(i, Color(255, 255, 255))

            self.LED_STRIP.show()
            self.actual_state(BINARY_STATES.ON)
        else:
            for i in range(0, LED_COUNT):
                self.LED_STRIP.setPixelColor(i, Color(0, 0, 0))

            self.LED_STRIP.show()
            self.actual_state(BINARY_STATES.OFF)
