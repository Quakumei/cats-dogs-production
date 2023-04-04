# Изображения и MLOps принципы

Проект для курса [MLOps и production подход к ML исследованиям 2.0](https://ods.ai/tracks/ml-in-production-spring-23)

```tree
.github                  - CI/CD
└─── workflows           - Рутины для CI/CD
    └─── lint-and-test.yaml - make lint && make test
requirements
├─── prod.txt            - prod библиотеки
└─── dev.txt             - dev библиотеки
src                      - исходный код
└─── tests               - тесты
    ├─── data            - тестовые данные
    └─── test_denoise.py - тесты для алгоритмов удаления шума
docs
├─── Примеры             - Примеры файлов по которым пишется документация к проекту
└─── ТЗ.docx             - Техническое задание
.pre-commit-config.yaml  - конфигурация pre-commit

```

## Запуск решения

```bash
echo "TELEGRAM_BOT_TOKEN='your-token-here'" >> .env
make install
make run_bot
```

## Связаться с автором

Telegram: [@Quakumei](https://t.me/Quakumei)
