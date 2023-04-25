"""Модуль для удаления шума из изображений"""

import io

import cv2
import numpy as np
from PIL import Image
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from skimage.util import img_as_float, random_noise


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


def denoise_median_blur(image: Image.Image, ks: int = 3) -> Image.Image:
    """Denoise image with cv2.medianBlur"""
    image = np.array(image)
    image = cv2.medianBlur(image, ks)
    image = Image.fromarray(image)
    return image


AVAILABLE_NOISES = ["gaussian", "s&p", "poisson", "speckle"]


def apply_noise(image: Image.Image, noise_type: str) -> Image.Image:
    """Apply noise to image using skimage.util.random_noise"""
    # Convert image to numpy array with a compatible data type
    image = np.array(image)
    if image.dtype != np.uint8:
        image = np.uint8(image * 255)

    # Apply noise
    image = img_as_float(image)
    image = random_noise(image, mode=noise_type)

    # Convert image to PIL format
    image = Image.fromarray(np.uint8(image * 255))
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
    elif method == "cv2.medianBlur":
        return denoise_median_blur(image)
    else:
        raise ValueError("Unknown denoise method")


def calc_psnr(image_gt: Image.Image, image_denoised: Image.Image) -> float:
    """PSNR for denoise image
    inf if good
    0 if bad
    """
    image_gt = np.array(image_gt)
    image_denoised = np.array(image_denoised)
    return psnr(image_gt, image_denoised)


def calc_ssim(image_gt: Image.Image, image_denoised: Image.Image) -> float:
    """SSIM for denoise image
    1 if good
    0 if bad
    """
    image_gt = np.array(image_gt)
    image_denoised = np.array(image_denoised)
    return ssim(image_gt, image_denoised, multichannel=True, channel_axis=2)
