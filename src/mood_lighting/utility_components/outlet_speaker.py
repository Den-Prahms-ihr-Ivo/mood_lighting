from typing import Optional, Callable

from src.helper.utility_component import Utility_Component
from src.helper.state_types import BASIS_STATES, BINARY_STATES, TERTIARY_STATES


class OutletSpeaker(Utility_Component):
    """
    Nutzmodul für die Steckdose für die Steckdose, die den Lautsprecher mit
    Strom versorgt.
    """

    # TODO: IVOOOOO
    """
    Bei State Change auf OFF ==> denk dran, auf einen dritten 
    State "IDLE_CNTDWN_RUNNING" zu setzen und erst wenn abgelaufen. tatsächlich auszuschalfen

    TODO: Die Eingabe Komponente kümmert sich um die TIMER soll sich um das Ausschalten kümmern.
    NEIN!! In diesem Fall macht es mehr Sinn den Kram zu abstrahieren und diese Komponente sich um den Time Out zu kümmern.
    """

    current_state = BASIS_STATES.UNDEFINED

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)
        self.current_state = BASIS_STATES.UNDEFINED

    def target_state(self, desired_state: BINARY_STATES):
        # TOOD: das ist für meinen Ansatz etwas zu over the top
        # Hier reicht es, den initialen INVALID state einfach wegzulassen
        # self.actual_state(BASIS_STATES.INVALID)
        if desired_state == BINARY_STATES.ON:
            self.current_state = TERTIARY_STATES.ON
        else:
            self.current_state = TERTIARY_STATES.OFF

        if desired_state == BINARY_STATES.ON:
            # TODO: STECKDOSE ANSCHALTEN
            # ...
            self.actual_state(BINARY_STATES.ON)
        else:
            # TODO: STECKDOSE AUSSCHALTEN
            # ...
            self.actual_state(BINARY_STATES.OFF)
