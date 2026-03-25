"""
ArUco-specific configuration values for the MVP detector pipeline.

The first MVP keeps configuration intentionally small and practical for
Raspberry Pi testing:
- camera device and frame size
- ArUco dictionary selection
- optional target marker id filter
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CameraConfig:
    """Runtime camera settings for OpenCV capture."""

    device_index: int = 0
    frame_width: int = 640
    frame_height: int = 480


@dataclass(frozen=True)
class ArucoConfig:
    """Runtime ArUco detector settings for MVP use."""

    dictionary_name: str = "DICT_4X4_50"
    target_marker_id: Optional[int] = None


DEFAULT_CAMERA_CONFIG = CameraConfig()
DEFAULT_ARUCO_CONFIG = ArucoConfig()
