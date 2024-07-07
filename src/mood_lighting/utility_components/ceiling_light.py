from typing import Optional, Callable, Tuple

from src.helper.utility_component import Utility_Component
from src.helper.state_types import BINARY_STATES, CeilingSateType


class CeilingLight(Utility_Component):
    """
    Nutzmodul für das Deckenlicht.
    """

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)

    def target_state(self, desired_state: CeilingSateType):
        # TOOD: das ist für meinen Ansatz etwas zu over the top
        # Hier reicht es, den initialen INVALID state einfach wegzulassen
        # self.actual_state(BASIS_STATES.INVALID)
        state, intensity = desired_state

        if state == BINARY_STATES.ON:
            # TODO: STECKDOSE ANSCHALTEN
            # ...
            self.actual_state((BINARY_STATES.ON, intensity))
        else:
            # TODO: STECKDOSE AUSSCHALTEN
            # ...
            self.actual_state((BINARY_STATES.OFF, 0))
