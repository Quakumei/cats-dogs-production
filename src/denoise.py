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


def apply_noise(image: Image.Image, noise_type: str) -> Image.Image:
    def noisy(noise_typ, image):
        return image
        # if noise_typ == "gauss":
        #     row,col,ch= image.shape
        #     mean = 0
        #     var = 0.1
        #     sigma = var**0.5
        #     gauss = np.random.normal(mean,sigma,(row,col,ch))
        #     gauss = gauss.reshape(row,col,ch)
        #     noisy = image + gauss
        #     return noisy
        # elif noise_typ == "s&p":
        #     row,col,ch = image.shape
        #     s_vs_p = 0.5
        #     amount = 0.004
        #     out = np.copy(image)
        #     # Salt mode
        #     num_salt = np.ceil(amount * image.size * s_vs_p)
        #     coords = [np.random.randint(0, i - 1, int(num_salt))
        #             for i in image.shape]
        #     out[coords] = 1

        #     # Pepper mode
        #     num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
        #     coords = [np.random.randint(0, i - 1, int(num_pepper))
        #             for i in image.shape]
        #     out[coords] = 0
        #     return out
        # elif noise_typ == "poisson":
        #     vals = len(np.unique(image))
        #     vals = 2 ** np.ceil(np.log2(vals))
        #     noisy = np.random.poisson(image * vals) / float(vals)
        #     return noisy
        # elif noise_typ =="speckle":
        #     row,col,ch = image.shape
        #     gauss = np.random.randn(row,col,ch)
        #     gauss = gauss.reshape(row,col,ch)
        #     noisy = image + image * gauss
        #     return noisy
        # else:
        #     return image

    image = np.array(image)
    image = noisy(noise_type, image)
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
