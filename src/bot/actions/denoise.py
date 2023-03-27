import cv2
import numpy as np

def convert_image_to_cv2(image):
    """
    Convert image to cv2 format
    """
    nparr = np.frombuffer(image, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

def convert_back_to_telegram(image):
    """
    Convert image back to telegram format
    """
    is_success, im_buf_arr = cv2.imencode(".jpg", image)
    byte_im = im_buf_arr.tobytes()
    return byte_im

def denoise_cv2(img):
    """
    https://docs.opencv.org/3.4/d1/d79/group__imgproc__hist.html#ga4a0e1e1231a7573694a1a1b718cefefe
    """
    img_converted = convert_image_to_cv2(img)
    img_res = cv2.fastNlMeansDenoisingColored(img_converted, None, 10, 10, 7, 21)
    return convert_back_to_telegram(img_res)

def denoise_nn(img):
    """

    """
    return None

def denoise_echo(img):
    """
    Return the same image
    """
    return img

def denoise_metrics(img_original, img_processed) -> str:
    """
    Calculate metrics
    """
    img_original = convert_image_to_cv2(img_original)
    img_processed = convert_image_to_cv2(img_processed)

    # Calculate PSNR
    psnr = cv2.PSNR(img_original, img_processed)
    res = "PSNR: " + str(psnr) + " dB" + "\n"

    # Calculate SSIM
    # ssim = cv2.SSIM(img_original, img_processed)
    # res += "SSIM: " + str(ssim) + "\n"

    return res