from src.helper.utility_component import Utility_Component


class UtilityStub(Utility_Component):

    actual_state_callbacks = []

    def __init__(self, callback=None) -> None:
        if callback:
            self.actual_state_callbacks.append(callback)

    def target_state(self, desired_state):
        print("Utility Component recieved : ", desired_state)
        self.actual_state(desired_state)

    def actual_state(self, actual_state):
        # Im Sinne von:
        for cf in self.actual_state_callbacks:
            cf(actual_state)

    def add_callback_function(self, callback_function):
        self.actual_state_callbacks.append(callback_function)
