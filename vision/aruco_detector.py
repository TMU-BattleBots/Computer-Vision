"""
ArUco marker detector for the first MVP vertical slice.

This implementation focuses only on:
- target visibility
- marker center (cx, cy)
- marker pixel area
- marker id (when available)
"""

from typing import Optional, Tuple

import cv2
import numpy as np

from config.aruco_config import ArucoConfig, DEFAULT_ARUCO_CONFIG
from interfaces.detector_interface import DetectionResult, DetectorInterface


def _resolve_dictionary(dictionary_name: str) -> cv2.aruco.Dictionary:
    """Resolve a dictionary constant name to a cv2.aruco dictionary object."""
    dict_id = getattr(cv2.aruco, dictionary_name, None)
    if dict_id is None:
        raise ValueError(f"Unknown ArUco dictionary: {dictionary_name}")
    return cv2.aruco.getPredefinedDictionary(dict_id)


def _marker_center(corners: np.ndarray) -> Tuple[int, int]:
    """Compute integer center of one marker from its 4 corner points."""
    points = corners.reshape(4, 2)
    center = points.mean(axis=0)
    return int(center[0]), int(center[1])


def _marker_area(corners: np.ndarray) -> float:
    """Compute marker area in pixels from 4-corner polygon."""
    points = corners.reshape(4, 2).astype(np.float32)
    return float(cv2.contourArea(points))


class ArucoDetector(DetectorInterface):
    """OpenCV ArUco detector returning MVP-ready detection output."""

    def __init__(self, config: ArucoConfig = DEFAULT_ARUCO_CONFIG) -> None:
        self._config = config
        dictionary = _resolve_dictionary(config.dictionary_name)
        self._dictionary = dictionary
        self._parameters = self._build_parameters()
        self._aruco_detector = self._build_detector(dictionary, self._parameters)

    def detect(self, frame: np.ndarray) -> DetectionResult:
        """Detect markers in a BGR frame and return the best candidate."""
        if self._aruco_detector is not None:
            corners, ids, _rejected = self._aruco_detector.detectMarkers(frame)
        else:
            corners, ids, _rejected = cv2.aruco.detectMarkers(
                frame, self._dictionary, parameters=self._parameters
            )
        if ids is None or len(corners) == 0:
            return DetectionResult(target_visible=False)

        best_index = self._select_marker_index(ids)
        if best_index is None:
            return DetectionResult(target_visible=False)

        selected_corners = corners[best_index]
        marker_id = int(ids[best_index][0])
        center = _marker_center(selected_corners)
        area = _marker_area(selected_corners)
        return DetectionResult(
            target_visible=True,
            center=center,
            marker_area=area,
            marker_id=marker_id,
        )

    def _select_marker_index(self, ids: np.ndarray) -> Optional[int]:
        """Choose marker index using optional target id filtering."""
        target_id = self._config.target_marker_id
        if target_id is None:
            return 0

        for i, marker_id_array in enumerate(ids):
            if int(marker_id_array[0]) == target_id:
                return i
        return None

    @staticmethod
    def _build_parameters() -> object:
        """Build detector parameters for OpenCV old/new APIs."""
        if hasattr(cv2.aruco, "DetectorParameters"):
            return cv2.aruco.DetectorParameters()
        if hasattr(cv2.aruco, "DetectorParameters_create"):
            return cv2.aruco.DetectorParameters_create()
        raise RuntimeError("OpenCV ArUco detector parameters API not available.")

    @staticmethod
    def _build_detector(dictionary: cv2.aruco.Dictionary, parameters: object) -> Optional[object]:
        """Return ArucoDetector when available, else use legacy detectMarkers."""
        if hasattr(cv2.aruco, "ArucoDetector"):
            return cv2.aruco.ArucoDetector(dictionary, parameters)
        return None
