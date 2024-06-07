from threading import Timer
from src.mood_lighting.config import CONFIG, CONTROLLER


class Display(object):
    """ """

    _instance = None
    timer = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Display, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def turn_off_display(self):
        print("TURN DISPLAY OFF")
        # TODO: Wirklich implementieren
        pass

    def turn_on_display(self):
        # TODO:  Eigentliches Anschalten implementieren.
        print("TURN DISPLAY ON")

        if self.timer is not None:
            self.timer.cancel()

        self.timer = Timer(
            float(CONFIG["DEFAULT"].get("display_wait_time", 5)),
            self.turn_off_display,
        )
        self.timer.start()

    def display(self, text):
        self.turn_on_display()
        # TODO: richtig implementieren.
        print(f"DISPLAY TEXT: {text}")
