from typing import Optional, Callable
from subprocess import run
from src.helper.utility_component import Utility_Component
from src.helper.state_types import BASIS_STATES, BINARY_STATES, TERTIARY_STATES
from threading import Timer
from src.config import CONFIG


class OutletSpeaker(Utility_Component):
    """
    Nutzmodul für die Steckdose für die Steckdose, die den Lautsprecher mit
    Strom versorgt.
    """

    current_state = BASIS_STATES.UNDEFINED
    cnt_dwn_timer = None

    def __init__(self, callback: Optional[Callable] = None) -> None:
        super().__init__(callback=callback)
        self.current_state = BASIS_STATES.UNDEFINED

        self.cnt_dwn_timer = None

    def target_state(self, desired_state: BINARY_STATES):
        # TOOD: das ist für meinen Ansatz etwas zu over the top
        # Hier reicht es, den initialen INVALID state einfach wegzulassen
        # self.actual_state(BASIS_STATES.INVALID)
        if self.current_state == TERTIARY_STATES.ON:
            if desired_state == BINARY_STATES.ON:
                self.current_state = TERTIARY_STATES.ON
                self.actual_state(BINARY_STATES.ON)
            else:
                self._start_count_down()
                self.current_state = TERTIARY_STATES.IDLE_CNT_DWN
                self.actual_state(BINARY_STATES.OFF)

        elif self.current_state == TERTIARY_STATES.IDLE_CNT_DWN:
            if desired_state == BINARY_STATES.ON:
                self._cancel_count_cown()
                self.current_state = TERTIARY_STATES.ON
                self.actual_state(BINARY_STATES.ON)
            else:
                self.current_state = TERTIARY_STATES.IDLE_CNT_DWN
                self.actual_state(BINARY_STATES.OFF)

        else:
            if desired_state == BINARY_STATES.ON:
                self.current_state = TERTIARY_STATES.ON
                self.actual_state(BINARY_STATES.ON)
                self._turn_on()
            else:
                self.current_state = TERTIARY_STATES.OFF
                self.actual_state(BINARY_STATES.OFF)

    def _start_count_down(self):
        if self.cnt_dwn_timer is not None:
            self.cnt_dwn_timer.cancel()

        self.cnt_dwn_timer = Timer(
            int(CONFIG["DEFAULT"].get("speaker_idle_time_out", 20)), self._off
        )
        self.cnt_dwn_timer.start()

    def _cancel_count_cown(self):
        if self.cnt_dwn_timer is not None:
            self.cnt_dwn_timer.cancel()

    def _off(self):
        self.current_state = TERTIARY_STATES.OFF
        self.actual_state(BINARY_STATES.OFF)
        self._turn_off()

    def _turn_off(self):
        run(
            [
                "mosquitto_pub",
                "-t",
                "zigbee2mqtt/Schlafzimmer_Steckdose_1/set",
                "-m",
                '{"state": "OFF"}',
            ]
        )

    def _turn_on(self):
        run(
            [
                "mosquitto_pub",
                "-t",
                "zigbee2mqtt/Schlafzimmer_Steckdose_1/set",
                "-m",
                '{"state": "ON"}',
            ]
        )
        self.current_state = TERTIARY_STATES.ON
