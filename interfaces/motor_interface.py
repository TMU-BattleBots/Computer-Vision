"""
Motor controller contract for sending PWM commands to the Arduino.
"""

from abc import ABC, abstractmethod


class MotorInterface(ABC):
    """Abstract interface for sending motor commands."""

    @abstractmethod
    def send_command(self, left_pwm: int, right_pwm: int) -> None:
        """Send left and right motor PWM commands."""

    @abstractmethod
    def stop(self) -> None:
        """Stop both motors."""

    @abstractmethod
    def close(self) -> None:
        """Close the motor controller connection."""
