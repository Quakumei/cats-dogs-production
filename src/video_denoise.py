"""Модуль для очистки видео от шума"""

import io

import cv2
import moviepy
import numpy as np
# from moviepy.editor import *
from PIL import Image

from denoise import apply_noise

# # Load the video clip
# clip = VideoFileClip('input_video.mp4')

# # Define a function to convert a frame to grayscale
# def to_grayscale(frame):
#     return frame.convert('L')

# # Apply the function to every frame of the video clip
# gray_clip = clip.fl_image(to_grayscale)

# Use fl_image to apply noise to every frame of the video clip


def telegram_to_moviepy(tg_video_clip: io.BytesIO) -> moviepy.video.VideoClip:
    """Convert Telegram video clip to MoviePy video clip"""
    tg_video_clip.seek(0)
    tg_video_clip = np.frombuffer(tg_video_clip.read(), np.uint8)
    tg_video_clip = cv2.imdecode(tg_video_clip, cv2.IMREAD_COLOR)
    tg_video_clip = cv2.cvtColor(tg_video_clip, cv2.COLOR_BGR2RGB)
    tg_video_clip = Image.fromarray(tg_video_clip)
    return moviepy.video.VideoClip.ImageClip(tg_video_clip)


def moviepy_to_telegram(mp_video_clip: moviepy.video.VideoClip) -> io.BytesIO:
    """Convert MoviePy video clip to Telegram video clip"""
    mp_video_clip = mp_video_clip.to_ImageClip()
    mp_video_clip = np.array(mp_video_clip)
    mp_video_clip = cv2.cvtColor(mp_video_clip, cv2.COLOR_RGB2BGR)
    mp_video_clip = cv2.imencode(".jpg", mp_video_clip)[1]
    mp_video_clip = io.BytesIO(mp_video_clip)
    return mp_video_clip


def apply_noise_videoclip(
    clip: moviepy.video.VideoClip, noise_type
) -> moviepy.video.VideoClip:
    """Apply noise to every frame of the video clip"""

    def apply_noise_frame(frame):
        """Apply noise to a single frame"""
        frame = Image.fromarray(frame)
        frame = apply_noise(frame, noise_type)
        frame = np.array(frame)
        return frame

    return clip.fl_image(apply_noise_frame)
