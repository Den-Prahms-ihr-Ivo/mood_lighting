from threading import Timer
from RPLCD.I2C import Charlcd

from config import CONFIG


class Display(object):
    """ """

    _instance = None
    timer = None
    LCD = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Display, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self) -> None:
        self.LCD = CharLCD(
            i2c_expander="PCF8574", address=0x27, port=1, cols=16, rows=2, dotsize=8
        )
        self.LCD.lcd_clear()

    def turn_off_display(self):
        self.LCD.backlight_enabled = False
        self.timer = None  # TODO: bruache ich das?

    def turn_on_display(self):
        if self.timer is not None:
            self.timer.cancel()
        else:
            # TODO: ist das ausreichend hier?
            self.LCD.backlight_enabled = True

        self.timer = Timer(
            float(CONFIG["DEFAULT"].get("display_wait_time", 5)),
            self.turn_off_display,
        )
        self.timer.start()

    def display(self, text):
        self.turn_on_display()

        self.LCD.clear()
        self.LCD.write_string(text)

    def clean_up(self):
        self.LCD.clear()
        self.LCD.backlight_enabled = False
        self.LCD.close(clear=True)
