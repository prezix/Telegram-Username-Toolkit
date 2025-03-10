# Telegram Username Toolkit

**Telegram Username Toolkit** — это универсальный набор инструментов для работы с никнеймами в Telegram. Он объединяет фильтрацию, генерацию вариантов и проверку доступности никнеймов в одном проекте.

## 📌 Что входит в Toolkit?

### 🔍 Фильтрация никнеймов (`deleter.py`)
- Читает список никнеймов из файла и валидирует их по требованиям Telegram:
  - От **5** до **32** символов
  - Латинские буквы, цифры и символ **подчёркивания** (`_`)
- Разделяет никнеймы на **допустимые** и **недопустимые**
- Логирование позволяет отслеживать процесс фильтрации и выявлять ошибки

### 🎨 Генерация вариантов (`gener.py`)
- Создаёт **альтернативные версии** никнеймов, заменяя символы:
  - `a` → `4`, `@`  
  - `o` → `0`, `()`
  - `e` → `3`, `€` и т. д.
- Позволяет создавать **уникальные и креативные** никнеймы в стиле "leetspeak"
- Полезно для обхода ограничений при выборе никнейма

### ✅ Проверка доступности (`main.py`)
- Массово проверяет доступность никнеймов в Telegram
- Использует **многопоточность**, работу через **прокси** и парсинг HTML с помощью `BeautifulSoup`
- Определяет, какие никнеймы **доступны**, а какие уже **заняты**

---

## 🚀 Основные преимущества

### 🛠️ **Модульность и масштабируемость**
- Каждый скрипт можно использовать **отдельно** или в составе общей системы
- Легко адаптируется под **различные задачи**

### ⚡ **Высокая производительность**
- Многопоточная проверка никнеймов
- Работа через **прокси** для ускорения обработки больших списков

### 🎭 **Гибкость и креативность**
- Генерация вариантов никнеймов позволяет **экспериментировать**
- Создание запоминающихся и **оригинальных комбинаций**

### 📜 **Подробное логирование**
- Все процессы снабжены **детальными логами**
- Упрощает **отладку** и помогает быстро выявлять ошибки

---

## 📦 Установка и использование
```bash
# Клонирование репозитория
git clone https://github.com/username/telegram-username-toolkit.git
cd telegram-username-toolkit

# Запуск фильтрации никнеймов
python deleter.py

# Генерация вариантов никнеймов
python gener.py

# Проверка доступности никнеймов
python main.py
```
