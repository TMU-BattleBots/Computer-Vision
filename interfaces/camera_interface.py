"""
Lightweight camera interface used by the ArUco MVP vertical slice.
"""

from abc import ABC, abstractmethod
from typing import Optional

import numpy as np


class CameraInterface(ABC):
    """Abstract camera contract for frame capture and cleanup."""

    @abstractmethod
    def open(self) -> None:
        """Open and initialize the camera device."""

    @abstractmethod
    def read(self) -> Optional[np.ndarray]:
        """Return the latest BGR frame or ``None`` if unavailable."""

    @abstractmethod
    def release(self) -> None:
        """Release all camera resources."""
