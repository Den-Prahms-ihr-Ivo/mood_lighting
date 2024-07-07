from typing import NewType, Tuple, Optional, TypedDict, Union
from enum import Enum


class MUSIC_STATES(Enum):
    PLAY = "ON"
    STOP = "OFF"


# class syntax
class BASIS_STATES(Enum):
    UNDEFINED = 0
    VALID = 1
    INVALID = 2


class BINARY_STATES(Enum):
    ON = 0
    OFF = 1


class TERTIARY_STATES(Enum):
    ON = 0
    OFF = 1
    IDLE_CNT_DWN = 2



class MusicStateType(TypedDict):
    state: BINARY_STATES
    playlist: Optional[Union[str, int]]
    volume: Optional[int]
    current_song: Optional[str]
    next_pressed: Optional[BINARY_STATES]
    refresh: Optional[BINARY_STATES]


UserId = NewType("UserId", int)

CeilingSateType = NewType("CeilingSateType", Tuple[BINARY_STATES, int])
DisplayStateType = NewType(
    "DisplayStateType", Union[BINARY_STATES, Tuple[BINARY_STATES, str]]
)

# lade String und display string
PLAYLIST_STATE_TYPE = NewType("PLAYLIST_STATE_TYPE", Tuple[str, str])

"""
MusicStateType = NewType(
    "MusicStateType",
    Unpack[_MusicType],
)
"""
