"""
Minimal ArUco MVP runner for Raspberry Pi camera testing.

Run this module to:
- open camera feed
- read frames continuously
- detect ArUco markers
- print FPS and marker status
- optionally show a debug preview window
"""

from __future__ import annotations

import argparse
import time

import cv2

from config.aruco_config import ArucoConfig, CameraConfig
from vision.aruco_detector import ArucoDetector
from vision.camera import OpenCVCamera


def parse_args() -> argparse.Namespace:
    """Parse command-line options for quick MVP tuning."""
    parser = argparse.ArgumentParser(description="Run ArUco MVP detector loop.")
    parser.add_argument("--camera-index", type=int, default=0, help="Camera device index.")
    parser.add_argument("--width", type=int, default=640, help="Capture width.")
    parser.add_argument("--height", type=int, default=480, help="Capture height.")
    parser.add_argument(
        "--dictionary",
        type=str,
        default="DICT_4X4_50",
        help="OpenCV ArUco dictionary name.",
    )
    parser.add_argument(
        "--target-id",
        type=int,
        default=None,
        help="Optional marker id to track. If omitted, first detected marker is used.",
    )
    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Disable OpenCV preview window for headless testing.",
    )
    return parser.parse_args()


def main() -> None:
    """Run camera capture + ArUco detection loop until interrupted."""
    args = parse_args()
    camera = OpenCVCamera(
        CameraConfig(
            device_index=args.camera_index,
            frame_width=args.width,
            frame_height=args.height,
        )
    )
    detector = ArucoDetector(
        ArucoConfig(
            dictionary_name=args.dictionary,
            target_marker_id=args.target_id,
        )
    )

    camera.open()
    frames = 0
    last_fps_time = time.perf_counter()
    fps = 0.0

    print("Starting ArUco MVP loop. Press 'q' in preview window to exit.")
    try:
        while True:
            frame = camera.read()
            if frame is None:
                print("Warning: camera read failed, retrying...")
                continue

            result = detector.detect(frame)
            frames += 1
            now = time.perf_counter()
            elapsed = now - last_fps_time
            if elapsed >= 1.0:
                fps = frames / elapsed
                frames = 0
                last_fps_time = now

            center_text = result.center if result.center is not None else "None"
            print(
                f"FPS={fps:5.1f} | visible={result.target_visible} | "
                f"id={result.marker_id} | center={center_text} | area={result.marker_area:.1f}",
                end="\r",
            )

            if not args.no_preview:
                overlay = frame.copy()
                status = (
                    f"FPS {fps:5.1f} | visible {result.target_visible} | "
                    f"id {result.marker_id} | center {center_text} | area {result.marker_area:.1f}"
                )
                cv2.putText(
                    overlay,
                    status,
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.55,
                    (0, 255, 0),
                    2,
                    cv2.LINE_AA,
                )

                if result.center is not None:
                    cv2.circle(overlay, result.center, 6, (0, 255, 255), thickness=-1)

                cv2.imshow("ArUco MVP Debug", overlay)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    except KeyboardInterrupt:
        pass
    finally:
        camera.release()
        cv2.destroyAllWindows()
        print("\nArUco MVP stopped.")


if __name__ == "__main__":
    main()
