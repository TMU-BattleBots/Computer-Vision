"""
Detector contract and data model for the ArUco MVP.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np


@dataclass(frozen=True)
class DetectionResult:
    """Single-frame marker detection result used by the MVP runner."""

    target_visible: bool
    center: Optional[Tuple[int, int]] = None
    marker_area: float = 0.0
    marker_id: Optional[int] = None


class DetectorInterface(ABC):
    """Abstract detector API for BGR frame inference."""

    @abstractmethod
    def detect(self, frame: np.ndarray) -> DetectionResult:
        """Run detection on one frame and return MVP fields."""
