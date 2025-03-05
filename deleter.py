import re
import logging
import sys

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("filter_usernames.log", encoding='utf-8')
    ]
)

# Регулярное выражение для валидации никнейма
USERNAME_REGEX = re.compile(r'^[A-Za-z0-9_]{5,32}$')  # Telegram требует от 5 до 32 символов

def filter_usernames():
    """
    Функция для фильтрации никнеймов по формату.
    Читает никнеймы из 'username.txt' и разделяет их на 'valid_usernames.txt' и 'invalid_usernames.txt'.
    """
    input_file = 'username.txt'             # Входной файл с никнеймами
    valid_output = 'valid_usernames.txt'    # Файл для допустимых никнеймов
    invalid_output = 'invalid_usernames.txt' # Файл для недопустимых никнеймов

    # Чтение никнеймов из входного файла
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            usernames = [line.strip() for line in f if line.strip()]
        logging.info(f'Загружено {len(usernames)} никнеймов из файла {input_file}.')
    except FileNotFoundError:
        logging.error(f'Файл {input_file} не найден.')
        return
    except Exception as e:
        logging.error(f'Ошибка при чтении файла {input_file}: {e}')
        return

    valid_usernames = []
    invalid_usernames = []

    # Фильтрация никнеймов
    for username in usernames:
        if USERNAME_REGEX.match(username):
            valid_usernames.append(username)
        else:
            invalid_usernames.append(username)

    # Запись допустимых никнеймов в файл
    try:
        with open(valid_output, 'w', encoding='utf-8') as vf:
            for uname in valid_usernames:
                vf.write(f'{uname}\n')
        logging.info(f'Записано {len(valid_usernames)} допустимых никнеймов в файл {valid_output}.')
    except Exception as e:
        logging.error(f'Ошибка при записи в файл {valid_output}: {e}')

    # Запись недопустимых никнеймов в файл
    try:
        with open(invalid_output, 'w', encoding='utf-8') as inf:
            for uname in invalid_usernames:
                inf.write(f'{uname}\n')
        logging.info(f'Записано {len(invalid_usernames)} недопустимых никнеймов в файл {invalid_output}.')
    except Exception as e:
        logging.error(f'Ошибка при записи в файл {invalid_output}: {e}')

if __name__ == "__main__":
    filter_usernames()
