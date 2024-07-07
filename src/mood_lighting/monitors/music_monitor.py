from src.helper.monitor import Monitor
from src.helper.state_types import MusicStateType
from src.helper.state_types import BASIS_STATES


class MusicMonitor(Monitor):
    """
    Ein Monitor hat 2 Schnittstellen:
      - Einen Eingang um den 'Soll'-Zustand zu ändern.
      - Einen Eingang um eine 'Call-Back'-Funktion zu setzen, die vom Monitor
      aufgerufen wird, wenn sich die "Situation" (um das Wort "Zustand" zu vermeiden)
      der Nutzkomponente verändert.
    """

    current_music_state = {}

    def __init__(self, display) -> None:
        super().__init__(display)
        self.actual_state_callbacks = []
        self.target_state_callbacks = []
        self.current_music_state = {
            "state": BASIS_STATES.UNDEFINED,
            "playlist": None,
            "volume": None,
            "current_song": None,
            "refresh": None,
            "next_pressed": None,
        }

    def get_current_state(self) -> BASIS_STATES:
        return self.current_music_state

    def actual_state_callback(self, actual_state: MusicStateType):
        for key, value in actual_state.items():
            self.current_music_state[key] = value

        # TODO: möglicherweise anpassen des current State

        # TODO: display aufrufen bei speziellen State changes.
        for cb in self.actual_state_callbacks:
            cb(actual_state)
