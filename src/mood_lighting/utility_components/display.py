import os

from src.helper.state_types import BINARY_STATES, DisplayStateType
from src.helper.abstract_display import AbstractDisplay

from RPLCD.i2c import CharLCD


class Display(AbstractDisplay):
    """
    Display Singleton Steuerklasse mit einem "öffentlichen" Callback
    für das Anzeigen auf dem Display.
    """

    def __init__(self) -> None:
        super().__init__()
        self.lcd = CharLCD(
            i2c_expander="PCF8574", address=0x27, port=1, cols=16, rows=2, dotsize=8
        )
        self.lcd.clear()

    def set_target_state(self, state: BINARY_STATES):
        if state == BINARY_STATES.ON:
            self.lcd.backlight_enabled = True
        else:
            self.lcd.backlight_enabled = False
            self.lcd.clear()

    def show(self, text):
        self.lcd.clear()
        self.lcd.write_string(text)
