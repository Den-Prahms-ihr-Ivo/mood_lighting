"""
Ein Monitor hat 2 Schnittstellen:
  - Einen Eingang um den 'Soll'-Zustand zu ändern.
  - Einen Eingang um eine 'Call-Back'-Funktion zu setzen, die vom Monitor
  aufgerufen wird, wenn sich die "Situation" (um das Wort "Zustand" zu vermeiden)
  der Nutzkomponente verändert.
"""

from typing import Callable, Union, Optional, Tuple, Any
from enum import Enum
from src.helper.abstract_display import AbstractDisplay
from src.helper.state_types import BASIS_STATES, BINARY_STATES, TERTIARY_STATES

# TODO: Type for State declarieren?
# Wie will ich das genau anstellen?
# ==> Über List of Enums declared as a new Type!
# ==> Oder doch lieber über ein Dict aus Enums? Ist für den Zugriff sicher einfacher?


class Monitor:

    display_monitor = None
    current_state: Union[BASIS_STATES, BINARY_STATES, TERTIARY_STATES] = (
        BASIS_STATES.UNDEFINED
    )

    def __init__(self, display_monitor: Optional[AbstractDisplay] = None) -> None:
        self.display_monitor = display_monitor
        self.actual_state_callbacks = []
        self.target_state_callbacks = []
        self.display_monitor = None
        self.current_state = BASIS_STATES.UNDEFINED

    # TODO: muss das abstract sein?
    def set_target_state(self, desired_state: Tuple[Any]):
        for cb in self.target_state_callbacks:
            cb(desired_state)

    def actual_state_callback(self, actual_state: Tuple[Any]):
        self.current_state = actual_state
        # Für einen Monitor, der den State anpasst,
        # müsste man diese Funktion überschreiben
        for cb in self.actual_state_callbacks:
            cb(actual_state)

    def add_actual_state_callback(self, callback_function: Callable[[Enum], None]):
        self.actual_state_callbacks.append(callback_function)

    def add_target_state_callback(self, callback_function: Callable):
        self.target_state_callbacks.append(callback_function)

    def get_current_state(self) -> BASIS_STATES:
        return self.current_state
