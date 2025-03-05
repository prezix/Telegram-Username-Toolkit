import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import logging
from tqdm import tqdm
import re
import time
import random

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("checker.log", encoding='utf-8')
    ]
)

# Регулярное выражение для валидации никнейма
USERNAME_REGEX = re.compile(r'^[A-Za-z0-9_]{5,32}$')  # Telegram требует от 5 до 32 символов

# Лок для потокобезопасной записи в файл
lock = threading.Lock()

# Загрузка прокси из файла
def load_proxies(proxy_file='proxies.txt'):
    try:
        with open(proxy_file, 'r', encoding='utf-8') as f:
            proxies = [line.strip() for line in f if line.strip()]
        if not proxies:
            logging.warning('Список прокси пуст.')
        return proxies
    except FileNotFoundError:
        logging.error(f'Файл прокси {proxy_file} не найден.')
        return []

# Функция для получения случайного прокси
def get_random_proxy(proxies):
    if not proxies:
        return None
    return random.choice(proxies)

# Функция для проверки доступности никнейма
def check_username(session, username, available_file, wrong_file, proxies, retries=3, delay=2):
    if not USERNAME_REGEX.match(username):
        logging.warning(f'Никнейм "{username}" не соответствует требованиям. Пропуск.')
        with lock:
            wrong_file.write(f'{username} (недопустимый формат)\n')
        return

    url = f'https://t.me/{username}'
    for attempt in range(1, retries + 1):
        proxy = get_random_proxy(proxies)
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        try:
            response = session.get(url, timeout=10, proxies=proxy_dict)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                square_1 = soup.find('div', class_='tgme_body_wrap')
                square = square_1.find('div', class_='tgme_page_extra') if square_1 else None

                with lock:
                    if square is None:
                        logging.info(f'{username} is available')
                        # Немедленно записываем доступный никнейм
                        with open(available_file, 'a', encoding='utf-8') as af:
                            af.write(f'{username}\n')
                    else:
                        logging.info(f'{username} is not available')
                        wrong_file.write(f'{username}\n')
                return
            elif response.status_code == 404:
                with lock:
                    logging.info(f'{username} is available (404)')
                    # Немедленно записываем доступный никнейм
                    with open(available_file, 'a', encoding='utf-8') as af:
                        af.write(f'{username}\n')
                return
            elif response.status_code in [429, 503]:
                logging.warning(f'Получен статус код {response.status_code} для {username}. Возможно, лимит запросов.')
                # Можно добавить увеличение задержки или смену прокси
            else:
                logging.warning(f'Получен статус код {response.status_code} для {username}')
        except requests.RequestException as e:
            logging.error(f'Ошибка при проверке {username} с прокси {proxy}: {e}')
        
        if attempt < retries:
            logging.info(f'Повторная попытка {username} (попытка {attempt + 1}/{retries}) через {delay} секунд...')
            time.sleep(delay)
    
    # Если все попытки исчерпаны
    logging.error(f'Не удалось проверить {username} после {retries} попыток.')
    with lock:
        wrong_file.write(f'{username} (ошибка проверки)\n')

# Основная логика
def main():
    # Фиксированные параметры
    input_file = 'username.txt'        # Файл с никнеймами для проверки
    available_output = 'available.txt' # Файл для доступных никнеймов
    wrong_output = 'wrong.txt'         # Файл для недоступных никнеймов
    max_workers = 8                     # Количество потоков
    delay_between_submissions = 0.1     # Задержка между отправкой запросов (в секундах)
    proxy_file = 'proxies.txt'          # Файл с прокси

    # Загружаем прокси
    proxies = load_proxies(proxy_file)
    if not proxies:
        logging.warning('Продолжение без прокси.')

    # Читаем никнеймы из файла
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            usernames = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error(f'Файл {input_file} не найден.')
        return

    total = len(usernames)
    logging.info(f'Начинаем проверку {total} никнеймов с использованием {max_workers} потоков.')

    # Открываем файл для записи недоступных никнеймов
    with open(wrong_output, 'w', encoding='utf-8') as wrong_file, \
         requests.Session() as session, \
         ThreadPoolExecutor(max_workers=max_workers) as executor:

        # Настройка заголовков для сессии
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                          'AppleWebKit/537.36 (KHTML, like Gecko) ' +
                          'Chrome/85.0.4183.102 Safari/537.36'
        })

        # Создаём генератор задач
        futures = []
        for username in usernames:
            futures.append(executor.submit(check_username, session, username, available_output, wrong_file, proxies))
            time.sleep(delay_between_submissions)

        # Отслеживаем прогресс с помощью tqdm
        for _ in tqdm(as_completed(futures), total=total, desc='Проверка никнеймов'):
            pass

    logging.info('Проверка завершена.')

if __name__ == "__main__":
    main()
