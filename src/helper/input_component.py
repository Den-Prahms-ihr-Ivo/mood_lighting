from abc import ABC, abstractmethod
from typing import List, Callable
from enum import Enum


class Input_Component(ABC):

    monitor_callback: Callable = None

    def __init__(self, callback: Callable) -> None:
        self.monitor_callback = callback

    def set_target_state(self, desired_state: List[Enum]):
        self.monitor_callback(desired_state=desired_state)

    @abstractmethod
    def actual_state_callback(self, actual_state):
        pass
