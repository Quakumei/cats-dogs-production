# Telgram bot api
from aiogram import Bot, Dispatcher, types, executor
import aiogram.utils.exceptions

# Logging
import logging
logging.basicConfig(level=logging.INFO)

# Environment variables
from dotenv import load_dotenv
from os import getenv
from hashlib import sha256
load_dotenv()

# + Config --------------+
BOT_TOKEN: str = getenv("TELEGRAM_BOT_PRIVATE_KEY")
assert type(BOT_TOKEN) == str, "TELEGRAM_BOT_PRIVATE_KEY is not set in .env file"
HELP_FILE: str = 'bot_texts/help.txt'
# +----------------------+

def load_string_banner(file:str) -> list[str]:
    with open(file, encoding="utf8") as f:
        result = ''.join(f.readlines())
    return result
help_message : str = load_string_banner(HELP_FILE)


# Load token from .env file
token_sha = sha256(BOT_TOKEN.encode()).hexdigest()
logging.info(f"Token SHA256: {token_sha[:16]}...{token_sha[-16:]}")


# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def strip_command(text:str) -> str:
    """
        Убирает /команду из строки
    """
    text_split = text.split(' ')
    if len(text_split) == 1:
        return ''
    return ' '.join(text.split(' ')[1:])


# /start
# /help
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(help_message)

# /echo
from actions.generate_echo import generate_echo
@dp.message_handler(commands=['echo'])
async def echo(message: types.Message):
    text_arg = generate_echo(strip_command(message.text))
    if text_arg:
        await message.answer(text_arg)
    else:
        await message.answer("/echo [text], пожалуйста.")

# Любая картинка
from actions.denoise import denoise_cv2, denoise_nn, denoise_echo, denoise_metrics
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def image(message: types.Message):
    METHODS = {
        'nn': denoise_nn,
        'cv2': denoise_cv2,
        'echo': denoise_echo,
    }
    image = message.photo
    image = await bot.download_file_by_id(image[-1].file_id)
    image = image.read()

    # Все методы обработки
    for method in METHODS:
        try:
            await message.answer(f"Method: {method}...")
            image_processed = METHODS[method](image)
        except Exception as e:
            await message.answer(f"Exception: {e}")
            continue
        if image_processed is None:
            await message.answer(f"Not implemented")
            continue
        else:
            metrics: str = denoise_metrics(image, image_processed)
        await message.answer_photo(image_processed)
        await message.answer(metrics)




# Если пользователь ввел не команду, то предложить вывести справку
@dp.message_handler()
async def callout(message: types.Message):
    await message.answer('/help - посмотреть справку')



if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except aiogram.utils.exceptions.TelegramAPIError as e:
        logging.error(e)