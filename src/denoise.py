"""Модуль для удаления шума из изображений"""

import io

import cv2
import numpy as np
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim


def telegram_to_pil(image) -> Image.Image:
    """Convert telegram image to PIL image"""
    image = Image.open(io.BytesIO(image))
    return image


def pil_to_telegram(image: Image.Image) -> bytes:
    """Convert PIL image to telegram image"""
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format="PNG")
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


def denoise_cv2(image: Image.Image) -> Image.Image:
    """Denoise image with cv2.fastNlMeansDenoisingColored"""
    image = np.array(image)
    image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    image = Image.fromarray(image)
    return image


def denoise_neural(image: Image.Image) -> Image.Image:
    """Denoise image with neural network"""

    # TODO: Add neural network

    return image


def denoise(image: Image.Image, method: str) -> Image.Image:
    """Denoise image"""
    if method == "cv2.fastNlMeansDenoisingColored":
        return denoise_cv2(image)
    elif method == "Нейронная сеть":
        return denoise_neural(image)
    else:
        raise ValueError("Unknown denoise method")


def calc_psnr(image_gt: Image.Image, image_denoised: Image.Image) -> float:
    """PSNR for denoise image
    inf if good
    0 if bad
    """
    return psnr(image_gt, image_denoised)


def calc_ssim(image_gt: Image.Image, image_denoised: Image.Image) -> float:
    """SSIM for denoise image
    1 if good
    0 if bad
    """
    return ssim(image_gt, image_denoised, multichannel=True)
