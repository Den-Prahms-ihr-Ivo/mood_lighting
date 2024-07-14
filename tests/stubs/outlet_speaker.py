from typing import Optional, Callable
from src.helper.utility_component import Utility_Component
from src.helper.state_types import BINARY_STATES


class OutletSpeaker(Utility_Component):

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)

    def target_state(self, desired_state: BINARY_STATES):
        if desired_state == BINARY_STATES.ON:
            self.actual_state(BINARY_STATES.ON)
        else:
            self.actual_state(BINARY_STATES.OFF)
