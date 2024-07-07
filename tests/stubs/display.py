from src.helper.abstract_display import AbstractDisplay
from unittest.mock import MagicMock


class Display(AbstractDisplay):

    set_target_state = MagicMock()
    show = MagicMock()
