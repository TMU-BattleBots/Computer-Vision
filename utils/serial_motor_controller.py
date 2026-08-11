"""
Arduino motor controller implementation using USB serial.
"""

import serial

from interfaces.motor_interface import MotorInterface
from config.motor_config import STOP_PWM


class SerialMotorController(MotorInterface):
    """Send motor PWM commands to an Arduino over serial."""

    def __init__(
        self,
        port: str,
        baudrate: int = 9600,
        timeout: float = 1.0,
    ):
        self.serial = serial.Serial(
            port=port,
            baudrate=baudrate,
            timeout=timeout,
        )

    def send_command(self, left_pwm: int, right_pwm: int) -> None:
        """Send left and right PWM commands to the Arduino."""

        command = f"{left_pwm},{right_pwm}\n"
        self.serial.write(command.encode("ascii"))

    def stop(self) -> None:
        """Send the stop command to both motors."""

        self.send_command(STOP_PWM, STOP_PWM)

    def close(self) -> None:
        """Close the serial connection."""

        if self.serial.is_open:
            self.serial.close()
