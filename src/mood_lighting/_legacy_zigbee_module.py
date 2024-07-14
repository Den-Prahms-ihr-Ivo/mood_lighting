from threading import Timer

from config import CONFIG, CONTROLLER

# from src.mood_lighting import CONTROLLER


class Zigbee(object):
    """ """

    _instance = None
    speaker_timer = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Zigbee, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def turn_on_speaker(self) -> None:
        """"""
        # TODO: implement
        print(f"Turning Speakers ON")

    def turn_off_speaker(self) -> None:
        """"""
        # TODO: implement
        CONTROLLER["speaker_is_powered_on"] = False
        print(f"Turning Speakers OFF")

    def turn_on_ceiling(self, value=100) -> None:
        """
        Value gibt an, mit wie viel Prozent die Leuchte
        nach beenden des Mood-Modus, angeht.
        """
        # TODO: implement

        print(f"Turning Ceilings ON")

    def turn_off_ceiling(self) -> None:
        """"""
        # TODO: implement
        print(f"Turning Ceiling OFF")

    def cancel_speaker_idle_timer(self) -> None:
        if self.speaker_timer is not None:
            self.speaker_timer.cancel()

    def reset_speaker_idle_timer(self) -> None:
        if self.speaker_timer is not None:
            self.speaker_timer.cancel()

        self.speaker_timer = Timer(
            float(CONFIG["DEFAULT"].get("speaker_idle_time_out", 5)),
            self.turn_off_speaker,
        )
        self.speaker_timer.start()
