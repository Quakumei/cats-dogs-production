"""Module for applying denoise_image methods to videos image per image"""

import hashlib
import random

import os
import cv2

from src.denoise_image import AVAILABLE_NOISES, apply_noise, denoise_cv2, denoise_median_blur


VIDEO_METHODS = [
    "echo",
    "cv2.fastNlMeansDenoisingColored",
    "cv2.medianBlur",
] + AVAILABLE_NOISES

# Use cv2 capabilities to read video frame by frame and
# write filtered frames to output video
# don't use filesystem to store video,
# use bytes in memory instead
def apply_denoise_func_video(video, method: str) -> bytes:
    """Apply denoise_image method to video"""
    # Create video reader and writer
    video_reader = cv2.VideoCapture(video, cv2.CAP_ANY)
    fps = video_reader.get(cv2.CAP_PROP_FPS)
    frame_size = (
        int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    )
    # hash_name = hashlib.sha256(video_reader).hexdigest()[:120]

    output_filename = f"{str(random.randint(0, 100000000))}.avi"
    video_writer = cv2.VideoWriter(
        output_filename,
        cv2.VideoWriter_fourcc(*"MJPG"),
        fps,
        frame_size,
    )

    # Read video frame by frame, apply denoise_image method to each frame
    # and write filtered frame to output video
    while True:
        success, frame = video_reader.read()
        if not success:
            break
        if method in AVAILABLE_NOISES:
            frame = apply_noise(frame, method)
        elif method == "cv2.fastNlMeansDenoisingColored":
            frame = denoise_cv2(frame)
        elif method == "cv2.medianBlur":
            frame = denoise_median_blur(frame)
        elif method == "echo":
            pass
        else:
            raise ValueError("Unknown denoise_image method")
        video_writer.write(frame)

    # Clean up
    return output_filename
