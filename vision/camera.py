"""
OpenCV camera implementation for Raspberry Pi MVP testing.
"""

from typing import Optional

import cv2
import numpy as np

from config.aruco_config import CameraConfig, DEFAULT_CAMERA_CONFIG
from interfaces.camera_interface import CameraInterface


class OpenCVCamera(CameraInterface):
    """Thin OpenCV camera wrapper implementing the MVP camera contract."""

    def __init__(self, config: CameraConfig = DEFAULT_CAMERA_CONFIG) -> None:
        self._config = config
        self._capture: Optional[cv2.VideoCapture] = None

    def open(self) -> None:
        """Open the configured camera and apply basic frame settings."""
        capture = cv2.VideoCapture(self._config.device_index)
        if not capture.isOpened():
            raise RuntimeError(
                f"Failed to open camera device {self._config.device_index}."
            )

        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self._config.frame_width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self._config.frame_height)
        self._capture = capture

    def read(self) -> Optional[np.ndarray]:
        """Read and return a BGR frame or ``None`` when read fails."""
        if self._capture is None:
            raise RuntimeError("Camera must be opened before reading frames.")

        ok, frame = self._capture.read()
        if not ok:
            return None
        return frame

    def release(self) -> None:
        """Release the camera handle if it is open."""
        if self._capture is not None:
            self._capture.release()
            self._capture = None
