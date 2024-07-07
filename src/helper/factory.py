from src.helper.input_component import Input_Component
from src.helper.monitor import Monitor
from src.helper.utility_component import Utility_Component
from typing import Tuple


def factory(
    mon: Monitor, inp: Input_Component, utl: Utility_Component
) -> Tuple[Input_Component, Monitor, Utility_Component]:
    m = mon()
    e = inp(m.target_state)
    m.add_actual_state_callback(e.actual_state_callback)
    u = utl(callback=m.actual_state_callback)
    m.add_target_state_callback(u.target_state)
    return (e, m, u)


def monitor_and_utility_factory(
    mon: Monitor, utl: Utility_Component, display_module=None
) -> Tuple[Monitor, Utility_Component]:
    if display_module is None:
        m = mon()
    else:
        m = mon(display_module)

    u = utl(callback=m.actual_state_callback)
    m.add_target_state_callback(u.target_state)
    return (m, u)
