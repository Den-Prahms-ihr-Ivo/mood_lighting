from typing import Optional, Callable

from src.helper.utility_component import Utility_Component
from src.helper.state_types import BINARY_STATES


class AudioComponent(Utility_Component):
    """
    Nutzmodul für das Anschalten des Speakers.
    Leider muss erst ein Knopf gedrückt werden, nachdem der Lautsprecher
    komplett vom Strom getrennt wurde.
    """

    # TODO: IVOOOOO
    """
    Bei State Change auf OFF ==> denk dran, auf einen dritten 
    State "IDLE_CNTDWN_RUNNING" zu setzen und erst wenn abgelaufen. tatsächlich auszuschalfen
    """

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)

    def target_state(self, desired_state: BINARY_STATES):
        # TOOD: das ist für meinen Ansatz etwas zu over the top
        # Hier reicht es, den initialen INVALID state einfach wegzulassen
        # self.actual_state(BASIS_STATES.INVALID)
        if desired_state == BINARY_STATES.ON:
            # TODO: KERZE ANSCHALTEN
            # ...
            self.actual_state(BINARY_STATES.ON)
        else:
            # TODO: KERZE AUSSCHALTEN
            # ...
            self.actual_state(BINARY_STATES.OFF)
