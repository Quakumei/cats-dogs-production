"""Aiogram Telegram bot to serve the model"""

import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv

from bot_locale import LOCALE_RUS
from denoise import denoise, pil_to_telegram, telegram_to_pil


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
# TODO: Use CLI to specify config
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
# Handlers
# ========================================


class FormDenoise(StatesGroup):
    denoise_method = State()
    image = State()


class FormDenoiseHelp(StatesGroup):
    denoise_method = State()


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
                    types.KeyboardButton(text="Нейронная сеть"),
                ],
            ],
            resize_keyboard=True,
        ),
    )


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
                ],
                [
                    types.KeyboardButton(text="Нейронная сеть"),
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


async def main():
    """Start the bot"""
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
