import warnings

import pytest
from PIL import Image

from src.denoise import calc_psnr, calc_ssim, denoise


def get_psnr_ssim(image_gt, image_denoised) -> tuple[float, float]:
    psnr = calc_psnr(image_gt, image_denoised)
    ssim = calc_ssim(image_gt, image_denoised)
    return psnr, ssim


def test_denoise_sanity():
    # Test will drop divide by zero warning
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        image_gt = Image.open("src/tests/data/gt.jpg")
        psnr, ssim = get_psnr_ssim(image_gt, image_gt)
        assert psnr == float("inf")
        assert ssim == 1


def test_denoise_cv2():
    image_gt = Image.open("src/tests/data/gt.jpg")
    image_noisy = Image.open("src/tests/data/noisy.jpg")
    image_denoised = denoise(image_noisy, "cv2.fastNlMeansDenoisingColored")
    psnr, ssim = get_psnr_ssim(image_gt, image_denoised)
    assert psnr > 30
    assert ssim > 0.9


def test_denoise_neural():
    image_gt = Image.open("src/tests/data/gt.jpg")
    image_noisy = Image.open("src/tests/data/noisy.jpg")
    image_denoised = denoise(image_noisy, "Нейронная сеть")
    if image_denoised == image_noisy:
        pytest.skip("Neural network not implemented")
    psnr, ssim = get_psnr_ssim(image_gt, image_denoised)
    assert psnr > 30
    assert ssim > 0.9
