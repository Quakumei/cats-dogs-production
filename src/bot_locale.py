"""File for storing bot locales"""

LOCALE_RUS: dict[str, str] = {
    "start": "Привет! Я бот, который поможет тебе"
    " очистить изображения от шума!\n",
    "help": """
<b>Команды:</b>
/start - начать работу с ботом
/help - вывести эту справку
/help_algo - вывести справку по методу удаления шума
/denoise - очистить изображение от шума
/cancel - отменить текущую операцию
/gt_metrics - вывести метрику качества очистки от шума
/apply_noise - добавить шум к изображению (по выбору пользователя)
/denoise_video - очистить видео от шума
/add_noise_video - добавить шум к видео (по выбору пользователя)
""",
    "error": "Я не понимаю, что ты от меня хочешь!",
    "denoise_choice": "Выберите метод удаления шума:",
    "denoise_send_image": "Отправьте изображение, которое хотите очистить:",
    "help_algo-cv2.fastNlMeansDenoisingColored": """
**cv2.fastNlMeansDenoisingColored** - метод, основанный на использовании
алгоритма быстрого нелокального среднего фильтрации для удаления шума
из изображения. Плохо работает с s&p, но удовлетворительно с Poisson,
Gaussian и Speckle шумами.

```
def denoise_cv2(image: Image.Image) -> Image.Image:
    # Denoise image with cv2.fastNlMeansDenoisingColored
    image = np.array(image)
    image = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    image = Image.fromarray(image)
    return image

```
""",
    "help_algo-Нейронная сеть": """
**Нейронная сеть** - метод, основанный на использовании
нейронной сети для удаления шума из изображения.

```
WIP
```
""",
    "help_algo-Median filter": """
**Median filter** - метод, основанный на использовании
медианного фильтра для удаления шума из изображения.
Используется для борьбы с salt and pepper шумом.
""",
    "help_algo_start": "Справка по какому из методов вас интересует?",
    "gt_metrics_gt": "Отправьте изображение, которое является незашумленным:",
    "gt_metrics_noisy": "Отправьте изображение, которое является зашумленным:",
    "gt_metrics_ssim": "SSIM: {}",
    "gt_metrics_psnr": "PSNR: {}",
    "gt_metrics_start": "Вычисляю метрики...",
    "cancel": "Отмена",
    "add_noise_image": "Отправьте изображение, которое хотите зашумить:",
    "add_noise_choice": "Выберите метод добавления шума:",
    "add_noise_gauss": "Гауссовский шум",
    "add_noise_salt": "Шум соли и перца",
    "add_noise_poisson": "Шум Пуассона",
    "add_noise_speckle": "Шум спекле",
    "add_noise_start": "Добавляю шум...",
    "add_noise_done": "Шум добавлен!",
    "add_noise_error": "Неизвестный метод добавления шума!",
}
