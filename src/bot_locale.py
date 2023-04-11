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
""",
    "error": "Я не понимаю, что ты от меня хочешь!",
    "denoise_choice": "Выберите метод удаления шума:",
    "denoise_send_image": "Отправьте изображение, которое хотите очистить:",
    "help_algo-cv2.fastNlMeansDenoisingColored": """
**cv2.fastNlMeansDenoisingColored** - метод, основанный на использовании
алгоритма быстрого нелокального среднего фильтрации для удаления шума
из изображения.

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
    "help_algo_start": "Справка по какому из методов вас интересует?",
}
