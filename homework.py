import logging
import os
import time
from typing import Any, Dict, List, NoReturn

import requests
from dotenv import load_dotenv
from telebot import TeleBot

load_dotenv()

PRACTICUM_TOKEN = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

RETRY_PERIOD = int(os.getenv("RETRY_TIME", 600))
ENDPOINT = 'https://practicum.yandex.ru/api/user_api/homework_statuses/'
HEADERS = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}

HOMEWORK_VERDICTS = {
    "approved": 'Работа проверена: ревьюеру всё понравилось. Ура!',
    "reviewing": 'Работа взята на проверку ревьюером.',
    "rejected": 'Работа проверена: у ревьюера есть замечания.',
}


def check_tokens() -> bool:
    """Функция доступ проверка переменнее окружение."""
    return all((PRACTICUM_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID))


def send_message(bot: TeleBot, message: str) -> NoReturn:
    """Функция отправил сообщения чат."""
    logging.debug(f'Отправил бот: {bot} сообщения: {message}')
    try:
        bot.send_message(
            TELEGRAM_CHAT_ID,
            message,
        )
        logging.debug('Прошла успешная отправил сообщения в чат')
    except Exception as error:
        logging.error(f'Ошибка отправил сообщения: {error}')


def get_api_answer(timestamp: int) -> Dict[str, Any]:
    """Функция делает запрос API сервис."""
    payload = {'from_date': timestamp}
    logging.debug(f'{ENDPOINT}, headers {HEADERS}, params {payload}, timeout=5')
    try:
        response = requests.get(ENDPOINT, headers=HEADERS, params=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException as error:
        raise ConnectionError(f'Ошибка запрос API: {error}') from error

    if response.status_code != 200:
        raise AssertionError(f'Неправильный статус код: {response.status_code}')

    return response.json()



def check_response(response: Dict[str, Any]) -> List[Any]:
    """Функция проверял ответ API."""
    logging.debug(f'Начало проверял ответ API: {response}')
    if not isinstance(response, dict):
        raise TypeError('Данных пришел не в вид словарь')
    if 'homeworks' not in response:
        raise KeyError('Нет ключ "homeworks"')
    if 'current_date' not in response:
        raise KeyError('Нет ключ "current_date"')
    if not isinstance(response['homeworks'], list):
        raise TypeError('Данных пришел не в вид список')

    return response.get('homeworks')


def parse_status(homework: Dict[str, Any]) -> str:
    """Функция извлечь статус о конкретной домашняя работа."""
    logging.debug('Начали парсинг статуса')
    homework_name = homework.get('homework_name')
    if not homework_name:
        raise KeyError('Нет ключ "homework_name"')
    status = homework.get('status')
    if not status:
        raise KeyError('Нет ключ "status"')
    verdict = HOMEWORK_VERDICTS.get(status)
    if not verdict:
        raise KeyError('API домашняя вернуть не документы статус')
    return f'Изменился статус проверки работы "{homework_name}". {verdict}'


def check_message(bot: TeleBot, message: str, prev_message: str) -> str:
    """Функция отправил сообщение бот, чтобы он изменил.
    Функция вернуть сообщение, которое уже был отправил.
    """
    if message != prev_message:
        send_message(bot, message)
    else:
        logging.debug('Повтор сообщения, не отправляется боту')
    return message


def main() -> NoReturn:
    """Основная логика работы бота."""
    if not check_tokens():
        logging.critical('Нету токен')
        raise SystemExit('Нету токен')

    try:
        bot = TeleBot(TELEGRAM_TOKEN)
    except Exception as error:
        logging.critical(f'Ошибка создал экземпляр Bot(): {error}')
        raise SystemExit(f'Ошибка создал экземпляр Bot(): {error}')

    timestamp = int(time.time())
    prev_message = ''

    while True:
        try:
            response = get_api_answer(timestamp)
            timestamp = response.get('current_date', timestamp)
            homeworks = check_response(response)
            if homeworks:
                message = parse_status(homeworks[0])
                prev_message = check_message(bot, message, prev_message)
            else:
                logging.debug('Нету данных')

        except ConnectionError as error:
            message = f'Ошибка нет связи соединения: {error}'
            logging.exception(message)
            prev_message = check_message(bot, message, prev_message)
        except TypeError as error:
            message = f'Объект не совпадает тип: {error}'
            logging.exception(message)
            prev_message = check_message(bot, message, prev_message)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logging.exception(message)
            prev_message = check_message(bot, message, prev_message)

        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format=(
            '%(asctime)s - %(levelname)s - %(filename)s.%(funcName)s.'
            '%(lineno)d - %(message)s'
        ),
    )
    main()
