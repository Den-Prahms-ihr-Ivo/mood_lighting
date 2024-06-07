class Controller:

    _instance = None
    is_playing = False
    speaker_is_powered_on = False
    start_stop_button_is_active = True

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Controller, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.is_playing = False
        self.speaker_is_powered_on = False
        self.start_stop_button_is_active = True
