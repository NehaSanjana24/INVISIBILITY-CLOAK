"""Real-time invisibility cloak effect using OpenCV."""

import argparse
from datetime import datetime

import cv2
import numpy as np


COLOR_RANGES = {
    "red": (
        (np.array([0, 70, 35]), np.array([10, 255, 255])),
        (np.array([165, 70, 35]), np.array([179, 255, 255])),
    ),
    "green": (
        (np.array([30, 65, 35]), np.array([95, 255, 255])),
    ),
    "blue": (
        (np.array([85, 65, 35]), np.array([140, 255, 255])),
    ),
}

WINDOW_NAME = "Invisibility Cloak"
INSTRUCTIONS = "r=reset bg  s=save  m=mask  q=quit"


def capture_background(camera: cv2.VideoCapture, frame_count: int = 30) -> np.ndarray:
    """Capture and average several frames while the scene is empty."""
    captured_frames = []

    for frame_number in range(frame_count):
        success, frame = camera.read()
        if not success:
            raise RuntimeError("Could not read a frame while capturing the background.")

        captured_frames.append(frame.astype(np.float32))
        progress = f"Capturing background: {frame_number + 1}/{frame_count}"
        cv2.putText(
            frame,
            progress,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2,
            cv2.LINE_AA,
        )
        cv2.imshow(WINDOW_NAME, frame)
        cv2.waitKey(1)

    return np.mean(captured_frames, axis=0).astype(np.uint8)


def create_mask(frame: np.ndarray, color: str = "red") -> np.ndarray:
    """Build and clean a binary mask for the selected cloth color."""
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)

    for lower_bound, upper_bound in COLOR_RANGES[color]:
        mask |= cv2.inRange(hsv_frame, lower_bound, upper_bound)

    kernel = np.ones((9, 9), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    return mask


def apply_cloak_effect(frame: np.ndarray, background: np.ndarray, mask: np.ndarray) -> np.ndarray:
    """Replace masked cloth pixels with the corresponding background pixels."""
    background_pixels = cv2.bitwise_and(background, background, mask=mask)
    live_pixels = cv2.bitwise_and(frame, frame, mask=cv2.bitwise_not(mask))
    return cv2.bitwise_or(background_pixels, live_pixels)


def save_frame(frame: np.ndarray) -> str:
    """Save a frame with a timestamp and return its filename."""
    filename = f"output_{datetime.now():%Y%m%d_%H%M%S}.png"
    if not cv2.imwrite(filename, frame):
        raise IOError(f"Could not save frame to {filename}.")
    return filename


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an OpenCV invisibility cloak effect.")
    parser.add_argument(
        "--color",
        choices=tuple(COLOR_RANGES),
        default="red",
        help="cloth color to detect (default: red)",
    )
    args = parser.parse_args()

    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("Error: could not open webcam.")
        return

    background = None
    show_mask = False

    try:
        cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
        print("Step out of frame while the background is captured...")
        background = capture_background(camera)

        while True:
            success, frame = camera.read()
            if not success:
                print("Warning: could not read a webcam frame.")
                break

            mask = create_mask(frame, args.color)
            output = apply_cloak_effect(frame, background, mask)

            if show_mask:
                display_frame = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            else:
                display_frame = output

            cv2.putText(
                display_frame,
                INSTRUCTIONS,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.65,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            cv2.imshow(WINDOW_NAME, display_frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            if key == ord("r"):
                print("Re-capturing background; step out of frame...")
                background = capture_background(camera)
            elif key == ord("s"):
                filename = save_frame(output)
                print(f"Saved {filename}")
            elif key == ord("m"):
                show_mask = not show_mask
    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()