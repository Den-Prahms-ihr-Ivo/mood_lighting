from src.helper.monitor import Monitor
from src.helper.factory import monitor_and_utility_factory
from src.mood_lighting.utility_components.candle_motor import CandleMotor
from src.mood_lighting.utility_components.outlet_speaker import OutletSpeaker
from src.mood_lighting.utility_components.audio_component import AudioComponent
from src.mood_lighting.utility_components.mood_light_component import MoodLightComponent
from src.mood_lighting.utility_components.spotlight_component import SpotlightComponent
from src.mood_lighting.utility_components.ceiling_light import CeilingLight
from src.mood_lighting.utility_components.music_component import MusicComponent
from src.mood_lighting.utility_components.playlist_component import PlaylistComponent
from src.mood_lighting.monitors.music_monitor import MusicMonitor
from src.mood_lighting.utility_components.display import Display
from src.mood_lighting.input_components.button_panel import ButtonPanel

import os
import logging

logger = logging.getLogger("moodlight")
logging.basicConfig(filename="moodlight.log", encoding="utf-8", level=logging.DEBUG)


def initialise_button_panel() -> ButtonPanel:
    # Initialisation.
    # Theoretisch brauche ich keinen eigenen Zugriff auf die Nutzkomponenten, oder?

    candle_monitor, _ = monitor_and_utility_factory(mon=Monitor, utl=CandleMotor)
    outlet_monitor, _ = monitor_and_utility_factory(mon=Monitor, utl=OutletSpeaker)
    audio_monitor, _ = monitor_and_utility_factory(mon=Monitor, utl=AudioComponent)
    mood_light_monitor, _ = monitor_and_utility_factory(
        mon=Monitor, utl=MoodLightComponent
    )
    spotlight_monitor, _ = monitor_and_utility_factory(
        mon=Monitor, utl=SpotlightComponent
    )
    ceiling_monitor, _ = monitor_and_utility_factory(mon=Monitor, utl=CeilingLight)
    display = Display()

    music_monitor, music_component = monitor_and_utility_factory(
        mon=MusicMonitor, utl=MusicComponent, display_module=display
    )
    playlist_monitor, _ = monitor_and_utility_factory(
        mon=Monitor, utl=PlaylistComponent
    )
    playlist_monitor.add_actual_state_callback(music_component.playlist_change)

    if os.environ.get("TESTING_ENV", None) is None:
        music_component = None

    return ButtonPanel(
        candle_monitor=candle_monitor,
        outlet_monitor=outlet_monitor,
        audio_monitor=audio_monitor,
        mood_light_monitor=mood_light_monitor,
        spotlight_monitor=spotlight_monitor,
        ceiling_monitor=ceiling_monitor,
        music_monitor=music_monitor,
        display=display,
        playlist_monitor=playlist_monitor,
        music_component=music_component,
    )


if __name__ == "__main__":
    raise NotImplementedError
    # TODO: Main Loop
    # while True:
    #  pass
