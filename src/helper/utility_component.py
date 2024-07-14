from abc import ABC, abstractmethod
from typing import Callable, Optional
from enum import Enum


class Utility_Component(ABC):

    actual_state_callbacks = []
    display = None

    def __init__(self, callback: Optional[Callable] = None, display=None) -> None:
        self.actual_state_callbacks = []
        self.display = None

        if callback:
            self.actual_state_callbacks.append(callback)
        else:
            self.actual_state_callbacks = []
        if display:
            self.display = display
        else:
            self.display = None

    @abstractmethod
    def target_state(self, desired_state: Enum):
        pass

    def actual_state(self, actual_state):
        # Im Sinne von:
        for cf in self.actual_state_callbacks:
            cf(actual_state)

    def add_callback_function(self, callback_function):
        self.actual_state_callbacks.append(callback_function)
