from typing import Optional, Callable
from src.helper.utility_component import Utility_Component
from src.helper.state_types import BASIS_STATES, BINARY_STATES
from math import ceil


class CeilingLight(Utility_Component):

    light_intensity_percentage = 0
    light_intensity_absolute = 0
    current_state = BASIS_STATES.UNDEFINED

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)
        self.light_intensity_percentage = 100
        self.light_intensity_absolute = 255
        self.current_state = BASIS_STATES.UNDEFINED

    def convert_percent_to_absolute(self, percent):
        percent = max(percent, 0)
        percent = min(percent, 100)

        return ceil(255 * percent / 100)

    def target_state(self, desired_state: BINARY_STATES):

        if type(desired_state) == BINARY_STATES:
            self.current_state = desired_state
        else:
            self.current_state, percentage = desired_state
            if int(percentage) > 0:
                self.light_intensity_percentage = percentage

        self.actual_state((self.current_state, self.light_intensity_percentage))
