""" Convert Robot States to Arduino Motor PWM Commands

Arduino: left_pwm, right_pwm

Stop -> 1500,1500
Search by moving left or right -> 1450,1550
"""

from state_machine.states import RobotState
from interfaces.detector_interface import DetectionResult

from config.motor_config import (
    STOP_PWM,
    FORWARD_PWM,
    SEARCH_LEFT_PWM,
    SEARCH_RIGHT_PWM,
    MIN_PWM,
    MAX_PWM,
)


# PWM values within Arduino limits
def clamp_pwm(value: int) -> int:
    return max(MIN_PWM, min(MAX_PWM, value))


# Left and right motor values
def get_motor_command(
    state: RobotState,
    detection: DetectionResult
) -> tuple[int, int]:

    # Stop
    left_pwm = STOP_PWM
    right_pwm = STOP_PWM

    # Search left and right for markers
    if state == RobotState.SEARCH:
        left_pwm = SEARCH_LEFT_PWM
        right_pwm = SEARCH_RIGHT_PWM

    # Stop temporarily when marker is found
    elif state == RobotState.TRACK:
        left_pwm = STOP_PWM
        right_pwm = STOP_PWM

    # Move towards marker
    elif state == RobotState.CHASE:
        left_pwm = FORWARD_PWM
        right_pwm = FORWARD_PWM

    # Search for marker when lost
    elif state == RobotState.LOST:
        left_pwm = SEARCH_LEFT_PWM
        right_pwm = SEARCH_RIGHT_PWM

    return (
        clamp_pwm(left_pwm),
        clamp_pwm(right_pwm)
    )
