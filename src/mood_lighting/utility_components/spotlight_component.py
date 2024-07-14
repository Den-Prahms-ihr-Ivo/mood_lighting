from typing import Optional, Callable

from src.helper.utility_component import Utility_Component
from src.helper.state_types import BINARY_STATES


class SpotlightComponent(Utility_Component):
    """
    Nutzmodul für das Sportlight im Mood Light Modul.
    """

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)

    def target_state(self, desired_state: BINARY_STATES):
        # TOOD: das ist für meinen Ansatz etwas zu over the top
        # Hier reicht es, den initialen INVALID state einfach wegzulassen
        # self.actual_state(BASIS_STATES.INVALID)
        if desired_state == BINARY_STATES.ON:
            # TODO: STECKDOSE ANSCHALTEN
            # ...
            self.actual_state(BINARY_STATES.ON)
        else:
            # TODO: STECKDOSE AUSSCHALTEN
            # ...
            self.actual_state(BINARY_STATES.OFF)
