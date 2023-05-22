"""FSM Groups"""

from aiogram.dispatcher.filters.state import State, StatesGroup


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
