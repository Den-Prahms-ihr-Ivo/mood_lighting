class Mood_Light(object):
    """ """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Mood_Light, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def turn_on(self) -> None:
        """"""
        # TODO: implement
        print(f"Turning Mood Lighting ON")

    def turn_off(self) -> None:
        """"""
        # TODO: implement
        print(f"Turning Mood Lighting OFF")
