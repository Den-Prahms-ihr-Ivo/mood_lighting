from typing import Optional, Callable, Tuple

from src.helper.utility_component import Utility_Component
from src.helper.state_types import BINARY_STATES, CeilingSateType
from subprocess import run
from src.config import CONFIG


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
            payload = f'"state": "ON", "brightness": {intensity}'

            for i in range(1, int(CONFIG["DEFAULT"].get("CEILING_LIGHT_COUNT", 2)) + 1):
                run(
                    [
                        "mosquitto_pub",
                        "-t",
                        f"zigbee2mqtt/Schlafzimmer_Decke_{i}/set",
                        "-m",
                        payload,
                    ]
                )

            self.actual_state((BINARY_STATES.ON, intensity))
        else:
            payload = f'"state": "OFF", "brightness": {min(0,intensity)}'

            for i in range(1, int(CONFIG["DEFAULT"].get("CEILING_LIGHT_COUNT", 2)) + 1):
                run(
                    [
                        "mosquitto_pub",
                        "-t",
                        f"zigbee2mqtt/Schlafzimmer_Decke_{i}/set",
                        "-m",
                        payload,
                    ]
                )

            self.actual_state((BINARY_STATES.OFF, 0))
