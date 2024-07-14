import pytest
from src.helper.state_types import BINARY_STATES, TERTIARY_STATES
from src.mood_lighting.input_components.button_panel import ButtonPanel
from src.config import CONFIG
from time import sleep


def test_OFF_2_OFF(initialised_button_panel: ButtonPanel):
    """
    OFF -> OFF
    """
    IBP = initialised_button_panel

    IBP.outlet_monitor.set_target_state(BINARY_STATES.OFF)

    assert not IBP.outlet_component._turn_off.called
    assert not IBP.outlet_component._turn_on.called

    assert IBP.outlet_monitor.current_state == BINARY_STATES.OFF
    assert IBP.outlet_component.current_state == TERTIARY_STATES.OFF

    IBP.outlet_monitor.set_target_state(BINARY_STATES.OFF)

    assert not IBP.outlet_component._turn_off.called
    assert not IBP.outlet_component._turn_on.called

    assert IBP.outlet_monitor.current_state == BINARY_STATES.OFF
    assert IBP.outlet_component.current_state == TERTIARY_STATES.OFF


def test_OFF_2_ON(initialised_button_panel: ButtonPanel):
    """
    OFF -> ON
    """
    IBP = initialised_button_panel

    IBP.outlet_monitor.set_target_state(BINARY_STATES.OFF)

    assert not IBP.outlet_component._turn_off.called
    assert not IBP.outlet_component._turn_on.called

    assert IBP.outlet_monitor.current_state == BINARY_STATES.OFF
    assert IBP.outlet_component.current_state == TERTIARY_STATES.OFF

    IBP.outlet_monitor.set_target_state(BINARY_STATES.ON)

    assert not IBP.outlet_component._turn_off.called
    assert IBP.outlet_component._turn_on.called

    assert IBP.outlet_monitor.current_state == BINARY_STATES.ON
    assert IBP.outlet_component.current_state == TERTIARY_STATES.ON


def test_ON_2_ON(initialised_button_panel: ButtonPanel):
    """
    ON -> ON
    """
    IBP = initialised_button_panel

    IBP.outlet_monitor.set_target_state(BINARY_STATES.ON)

    assert not IBP.outlet_component._turn_off.called
    assert IBP.outlet_component._turn_on.called

    assert IBP.outlet_monitor.current_state == BINARY_STATES.ON
    assert IBP.outlet_component.current_state == TERTIARY_STATES.ON

    IBP.outlet_component._turn_on.reset_mock()

    IBP.outlet_monitor.set_target_state(BINARY_STATES.ON)

    assert not IBP.outlet_component._turn_off.called
    assert not IBP.outlet_component._turn_on.called

    assert IBP.outlet_monitor.current_state == BINARY_STATES.ON
    assert IBP.outlet_component.current_state == TERTIARY_STATES.ON


def test_ON_2_OFF(initialised_button_panel: ButtonPanel):
    """
    ON -> OFF
    """
    IBP = initialised_button_panel

    IBP.outlet_monitor.set_target_state(BINARY_STATES.ON)

    IBP.outlet_component._turn_on.reset_mock()
    IBP.outlet_component._turn_off.reset_mock()

    IBP.outlet_monitor.set_target_state(BINARY_STATES.OFF)

    assert not IBP.outlet_component._turn_off.called
    assert not IBP.outlet_component._turn_on.called

    assert IBP.outlet_monitor.current_state == BINARY_STATES.OFF
    assert IBP.outlet_component.current_state == TERTIARY_STATES.IDLE_CNT_DWN

    sleep(int(CONFIG["DEFAULT"].get("speaker_idle_time_out", 20)) + 0.01)

    assert IBP.outlet_component._turn_off.called
    assert IBP.outlet_monitor.current_state == BINARY_STATES.OFF
    assert IBP.outlet_component.current_state == TERTIARY_STATES.OFF


def test_IDLE_2_ON(initialised_button_panel: ButtonPanel):
    """
    ON -> OFF
    """
    IBP = initialised_button_panel

    IBP.outlet_monitor.set_target_state(BINARY_STATES.ON)
    IBP.outlet_monitor.set_target_state(BINARY_STATES.OFF)

    assert IBP.outlet_monitor.current_state == BINARY_STATES.OFF
    assert IBP.outlet_component.current_state == TERTIARY_STATES.IDLE_CNT_DWN

    IBP.outlet_component._turn_on.reset_mock()
    IBP.outlet_component._turn_off.reset_mock()

    IBP.outlet_monitor.set_target_state(BINARY_STATES.ON)

    assert IBP.outlet_monitor.current_state == BINARY_STATES.ON
    assert IBP.outlet_component.current_state == TERTIARY_STATES.ON

    assert not IBP.outlet_component._turn_off.called
    assert not IBP.outlet_component._turn_on.called

    sleep(int(CONFIG["DEFAULT"].get("speaker_idle_time_out", 20)) + 0.01)

    assert not IBP.outlet_component._turn_off.called
    assert IBP.outlet_monitor.current_state == BINARY_STATES.ON
    assert IBP.outlet_component.current_state == TERTIARY_STATES.ON


def test_IDLE_2_OFF(initialised_button_panel: ButtonPanel):
    """
    ON -> OFF
    """
    IBP = initialised_button_panel

    IBP.outlet_monitor.set_target_state(BINARY_STATES.ON)
    IBP.outlet_monitor.set_target_state(BINARY_STATES.OFF)

    assert IBP.outlet_monitor.current_state == BINARY_STATES.OFF
    assert IBP.outlet_component.current_state == TERTIARY_STATES.IDLE_CNT_DWN

    IBP.outlet_component._turn_on.reset_mock()
    IBP.outlet_component._turn_off.reset_mock()

    IBP.outlet_monitor.set_target_state(BINARY_STATES.OFF)

    assert IBP.outlet_monitor.current_state == BINARY_STATES.OFF
    assert IBP.outlet_component.current_state == TERTIARY_STATES.IDLE_CNT_DWN

    assert not IBP.outlet_component._turn_off.called
    assert not IBP.outlet_component._turn_on.called

    sleep(int(CONFIG["DEFAULT"].get("speaker_idle_time_out", 20)) + 0.01)

    assert IBP.outlet_component._turn_off.called
    assert IBP.outlet_monitor.current_state == BINARY_STATES.OFF
    assert IBP.outlet_component.current_state == TERTIARY_STATES.OFF
