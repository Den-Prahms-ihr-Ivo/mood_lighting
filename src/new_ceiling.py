from src.helper.utility_component import Utility_Component
from src.helper.state_types import BINARY_STATES, CeilingSateType
from subprocess import run
from src.config import CONFIG

intensity = 255


def set_intensity(i):
    global intensity
    intensity = i


def set_state(state):
    global intensity

    if state:
        payload = f'{{"state": "ON", "brightness": {intensity}}}'

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
    else:
        payload = f'{{"state": "OFF", "brightness": {max(0,intensity)}}}'

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
