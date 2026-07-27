"""
State definitions for the battlebot state machine.

This module declares all behavioral states (e.g., IDLE, SEEK_OPPONENT,
ENGAGE, EVADE, SCAN_ARENA) and their associated transitions.
Each state defines entry, update, and exit behaviors.
"""

from enum import Enum, auto


class RobotState(Enum):
    """
   Robot behavior states.
    """

    INIT = auto()
    SEARCH = auto()
    TRACK = auto()
    CHASE = auto()
    LOST = auto() 
    