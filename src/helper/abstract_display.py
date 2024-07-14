from abc import ABC, abstractmethod
from src.helper.state_types import DisplayStateType


class AbstractDisplay(ABC):
    """
    Display Singleton Steuerklasse mit einem "öffentlichen" Callback
    für das Anzeigen auf dem Display.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(AbstractDisplay, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    @abstractmethod
    def set_target_state(self, state: DisplayStateType):
        pass

    @abstractmethod
    def show(self, text):
        pass
