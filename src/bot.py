"""Aiogram Telegram bot to serve the model"""

import asyncio
import io
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

from bot_locale import LOCALE_RUS
from denoise import (AVAILABLE_NOISES, apply_noise, calc_psnr, calc_ssim,
                     denoise, pil_to_telegram, telegram_to_pil)
from video_denoise import moviepy_to_telegram, telegram_to_moviepy


def get_env(
    required: list = False, filter: bool = True, use_dotenv: bool = True
) -> dict:
    """Get required environment variables"""
    # Load environment variables
    if use_dotenv:
        load_dotenv()

    res = os.environ

    # Check if all required variables are set
    for var in required:
        if var not in res:
            raise ValueError(f"Environment variable {var} is not set!")

    # Filter out non-required variables
    if filter:
        res = {k: v for k, v in res.items() if k in required}

    return res


# ========================================
# Bot initialization & Config
# ========================================
LOGGING_LEVEL = logging.INFO
USE_DOTENV = True
# ========================================
required_envs = ["TELEGRAM_BOT_TOKEN"]
get_env(required=required_envs, use_dotenv=USE_DOTENV)
TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
locale = LOCALE_RUS
# ========================================
bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=LOGGING_LEVEL)
# ========================================

# ========================================
# FSM Groups
# ========================================


class FormDenoise(StatesGroup):
    denoise_method = State()
    image = State()


class FormDenoiseHelp(StatesGroup):
    denoise_method = State()


class FormDenoiseMetrics(StatesGroup):
    denoise_method = State()
    ground_truth_image = State()
    noisy_image = State()


class ApplyNoise(StatesGroup):
    noise_type = State()
    image = State()


class ApplyNoiseVideo(StatesGroup):
    noise_type = State()
    video = State()


# ========================================
# Handlers
# ========================================


@dp.message_handler(commands=["cancel"], state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    """Cancel command handler"""
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply(
        locale["cancel"], reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(commands=["apply_noise"])
async def apply_noise_start(message: types.Message):
    """Apply noise command handler"""
    await ApplyNoise.noise_type.set()
    await message.reply(
        locale["add_noise_choice"],
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                AVAILABLE_NOISES,
                ["/cancel"],
            ],
            resize_keyboard=True,
        ),
    )


@dp.message_handler(state=ApplyNoise.noise_type)
async def apply_noise_type(message: types.Message, state: FSMContext):
    """Apply noise type handler"""
    # Clean keyboard
    await state.update_data(noise_type=message.text)
    await ApplyNoise.next()
    await message.reply(
        locale["add_noise_image"], reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(
    state=ApplyNoise.image, content_types=types.ContentTypes.PHOTO
)
async def apply_noise_image(message: types.Message, state: FSMContext):
    """Apply noise image handler"""
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    noise_type = data["noise_type"]
    image = data["image"]
    await state.finish()

    await message.reply(locale["add_noise_start"])

    img = await bot.download_file_by_id(image)
    image = telegram_to_pil(img.read())
    try:
        noisy_image = apply_noise(image, noise_type)
        await message.reply_photo(pil_to_telegram(noisy_image))
        await message.reply(locale["add_noise_done"])
    except ValueError as e:
        await message.reply(locale["add_noise_error"])
        logging.error(e)


@dp.message_handler(commands=["apply_noise_video"])
async def apply_noise_video_start(message: types.Message):
    """Apply noise command handler"""
    await ApplyNoiseVideo.noise_type.set()
    await message.reply(
        locale["add_noise_choice"],
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                AVAILABLE_NOISES,
                ["/cancel"],
            ],
            resize_keyboard=True,
        ),
    )


@dp.message_handler(state=ApplyNoiseVideo.noise_type)
async def apply_noise_video_type(message: types.Message, state: FSMContext):
    """Apply noise type handler"""
    # Clean keyboard
    await state.update_data(noise_type=message.text)
    await ApplyNoiseVideo.next()
    await message.reply(
        locale["add_noise_video"], reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(
    state=ApplyNoiseVideo.video, content_types=types.ContentTypes.VIDEO
)
async def apply_noise_video_process(message: types.Message, state: FSMContext):
    """Apply noise image handler"""
    await state.update_data(video=message.video.file_id)
    data = await state.get_data()
    # noise_type = data["noise_type"]
    video = data["video"]
    await state.finish()

    await message.reply(locale["add_noise_start"])

    video: io.BytesIO = await bot.download_file_by_id(video)
    video_mp = telegram_to_moviepy(video)
    try:
        # noisy_video = apply_noise_video(video_mp, noise_type)
        noisy_tg_video = moviepy_to_telegram(video_mp)
        await message.reply_video(noisy_tg_video)
        await message.reply(locale["add_noise_done"])
    except ValueError as e:
        await message.reply(locale["add_noise_error"])
        logging.error(e)


@dp.message_handler(commands=["gt_metrics"])
async def gt_metrics_start(message: types.Message):
    """GT metrics command handler"""
    await FormDenoiseMetrics.denoise_method.set()
    await message.reply(
        locale["denoise_choice"],
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(
                        text="cv2.fastNlMeansDenoisingColored"
                    ),
                ],
                [
                    # types.KeyboardButton(text="Нейронная сеть"),
                ],
            ],
            resize_keyboard=True,
        ),
    )


@dp.message_handler(state=FormDenoiseMetrics.denoise_method)
async def gt_metrics_method(message: types.Message, state: FSMContext):
    """GT metrics method handler"""
    await state.update_data(denoise_method=message.text)
    await FormDenoiseMetrics.next()
    await message.reply(
        locale["gt_metrics_gt"], reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(
    state=FormDenoiseMetrics.ground_truth_image,
    content_types=types.ContentTypes.PHOTO,
)
async def gt_metrics_ground_truth_image(
    message: types.Message, state: FSMContext
):
    """GT metrics ground truth image handler"""
    await state.update_data(ground_truth_image=message.photo[-1].file_id)
    await FormDenoiseMetrics.next()
    await message.reply(locale["gt_metrics_noisy"])


@dp.message_handler(
    state=FormDenoiseMetrics.noisy_image,
    content_types=types.ContentTypes.PHOTO,
)
async def gt_metrics_noisy_image(message: types.Message, state: FSMContext):
    """GT metrics noisy image handler"""
    await state.update_data(noisy_image=message.photo[-1].file_id)
    data = await state.get_data()
    denoise_method = data["denoise_method"]
    ground_truth_image = data["ground_truth_image"]
    noisy_image = data["noisy_image"]
    await state.finish()

    await message.reply(locale["gt_metrics_start"])

    gt_img = await bot.download_file_by_id(ground_truth_image)
    ground_truth_image = telegram_to_pil(gt_img.read())
    ns_img = await bot.download_file_by_id(noisy_image)
    noisy_image = telegram_to_pil(ns_img.read())
    denoised_image = denoise(noisy_image, denoise_method)
    ssim = calc_ssim(ground_truth_image, denoised_image)
    psnr = calc_psnr(ground_truth_image, denoised_image)
    metrics_message = (
        "Метрики:\n"
        + locale["gt_metrics_psnr"].format(psnr)
        + "\n"
        + locale["gt_metrics_ssim"].format(ssim)
    )
    await message.reply_photo(pil_to_telegram(denoised_image))
    await message.reply(metrics_message)


@dp.message_handler(commands=["help_algo"])
async def help_algo_start(message: types.Message):
    """Help algo command handler"""
    await FormDenoiseHelp.denoise_method.set()
    await message.reply(
        locale["help_algo_start"],
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(
                        text="cv2.fastNlMeansDenoisingColored"
                    ),
                    types.KeyboardButton(text="cv2.medianBlur"),
                ],
                [
                    # types.KeyboardButton(text="Нейронная сеть"),
                ],
            ],
            resize_keyboard=True,
        ),
    )


@dp.message_handler(state=FormDenoiseHelp.denoise_method)
async def help_algo_method(message: types.Message, state: FSMContext):
    """Help algo method handler"""
    await state.update_data(denoise_method=message.text)
    # Get data
    data = await state.get_data()
    await message.reply(
        locale[f"help_algo-{data['denoise_method']}"],
        reply_markup=types.ReplyKeyboardRemove(),
        parse_mode="Markdown",
    )
    await state.finish()


@dp.message_handler(commands=["denoise"])
async def denoise_start(message: types.Message):
    """Denoise command handler"""
    await FormDenoise.denoise_method.set()
    await message.reply(
        locale["denoise_choice"],
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(
                        text="cv2.fastNlMeansDenoisingColored"
                    ),
                ],
                [
                    types.KeyboardButton(text="cv2.medianBlur"),
                ],
            ],
            resize_keyboard=True,
        ),
    )


@dp.message_handler(state=FormDenoise.denoise_method)
async def denoise_method(message: types.Message, state: FSMContext):
    """Denoise method handler"""
    await state.update_data(denoise_method=message.text)
    await FormDenoise.next()
    await message.reply(
        locale["denoise_send_image"],
    )


@dp.message_handler(
    state=FormDenoise.image, content_types=types.ContentTypes.PHOTO
)
async def denoise_image(message: types.Message, state: FSMContext):
    """Denoise image handler"""
    await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    await message.reply(
        f"Метод: {data['denoise_method']}",
        reply_markup=types.ReplyKeyboardRemove(),
    )
    await state.finish()

    # Fetch image
    img = await bot.download_file_by_id(data["image"])
    img = img.read()

    # Denoise image
    img = telegram_to_pil(img)
    processed_image = denoise(img, data["denoise_method"])
    processed_image = pil_to_telegram(processed_image)

    # Reply with the image
    await message.reply_photo(
        photo=processed_image,
    )


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    """Start command handler"""
    await message.reply(
        locale["start"],
        parse_mode="HTML",
    )


@dp.message_handler(commands=["help"])
async def help(message: types.Message):
    """Help command handler"""
    await message.reply(
        locale["help"],
        parse_mode="HTML",
    )


@dp.message_handler()
async def general(message: types.Message):
    """Any text message will be processed here"""
    await message.reply(
        locale["error"],
        parse_mode="HTML",
    )


# ========================================
# Main
# ========================================


import click

async def main_loop():
    """Start the bot"""
    await dp.start_polling(bot)

@click.command()
@click.option("--debug", "-d", is_flag=True, help="Enable debug mode")
def main(debug: bool):
    """Start the bot"""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main_loop())