# «API: интерфейс взаимодействия программ»

<h1 align="center">Привет всем! Меня зовут <a href="https://daniilshat.ru/" target="_blank">Алексей</a> 
<img src="https://github.com/blackcater/blackcater/raw/main/images/Hi.gif" height="32"/></h1>

## Бот-ассистент для телеграмма

В этом задании нужно написать Telegram-бота, который будет обращаться к API сервиса Практикум Домашка и узнавать статус вашей домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — принял её ревьюер или вернул на доработку.

![image](https://github.com/AlexeyVodopyanov/homework_bot/assets/106692645/bea5b624-af0f-47e7-87f8-d6e436160bb1)

Этот проект представляет собой Telegram-бота для отслеживания статуса домашней работы на сервисе Яндекс.Практикум. Бот проверяет статус домашней работы через API и отправляет обновления в Telegram-чат.

## Описание

Homework Bot предназначен для студентов Яндекс.Практикума, чтобы они могли получать уведомления о статусе своих домашних работ непосредственно в Telegram. Бот проверяет статус работ на платформе Яндекс.Практикум через API и отправляет уведомления в Telegram, если статус изменился.

## Установка и запуск

Для локального запуска проекта выполните следующие шаги:

1. Создайте и активируйте виртуальное окружение:
    ```sh
    python -m venv .venv
    
    source .venv\Scripts\activate
    ```

2. Установите зависимости:
    ```sh
    pip install -r requirements.txt
    ```

3. Создайте файл `.env` в корне проекта и добавьте необходимые переменные окружения.

4. Запустите бота:
    ```sh
    python homework.py
    ```

## Переменные окружения

Создайте файл `.env` в корне проекта и добавьте следующие переменные:

PRACTICUM_TOKEN=<Ваш токен API Яндекс.Практикум>

TELEGRAM_TOKEN=<Ваш токен API Telegram Bot>

TELEGRAM_CHAT_ID=<Ваш Chat ID в Telegram>


![image](https://github.com/AlexeyVodopyanov/homework_bot/assets/106692645/a39d66db-97cd-4323-b7bf-914d2e8ae74b)


Готов мой первый проект в Яндекс.Практикум! Этот проект — практическая реализация моих знаний и опыта.

## Технологии

- VSCode
- PyChram
- Python 3.9
- Telegram Bot API
- Яндекс.Практикум API
- Requests
- python-dotenv
- PyTelegramBotAPI (telebot)

![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
