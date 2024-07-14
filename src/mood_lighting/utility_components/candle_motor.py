import os

from typing import Optional, Callable
from src.helper.utility_component import Utility_Component
from src.helper.state_types import BINARY_STATES
from config import CONFIG

# Imports, die vom Betriebssystem abängen und die
# im Test Fall gemockt werden.
# if os.environ.get("TESTING_ENV", None) is None:
#    import GPIO
import GPIO


class CandleMotor(Utility_Component):

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)

    def target_state(self, desired_state: BINARY_STATES):
        if desired_state == BINARY_STATES.ON:
            GPIO.output(CONFIG["DEFAULT"].get("CANDLE_PIN", 20), GPIO.HIGH)
            self.actual_state(BINARY_STATES.ON)
        else:
            GPIO.output(CONFIG["DEFAULT"].get("CANDLE_PIN", 20), GPIO.LOW)
            self.actual_state(BINARY_STATES.OFF)
