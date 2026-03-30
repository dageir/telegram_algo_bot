# 📘 Урок: Работа с API на примере TMDB

> **Цель:** Научиться получать данные из внешнего сервиса через API.

---

## 1️⃣ Что такое API

```
API (Application Programming Interface)
=
Набор правил для обмена данными между программами через интернет.
```

### Техническая схема:

```
Твой код (Python)  →  HTTP-запрос  →  Сервер TMDB
       ↑                                  ↓
       └─────── JSON-ответ ──────────────┘
```

### Компоненты запроса:

|Компонент|Описание|
|---|---|
|**URL (Endpoint)**|Адрес функции API (например, `/search/movie`)|
|**Метод**|Тип запроса (`GET`, `POST`, `PUT`, `DELETE`)|
|**Параметры**|Данные, передаваемые в запросе (ключ, запрос, язык)|
|**Заголовки**|Метаданные запроса (авторизация, формат)|
|**Тело**|Данные для отправки (для `POST`/`PUT`)|

---

## 2️⃣ Пошаговая инструкция: TMDB API

### Шаг 1: Регистрация

1. Перейди на [themoviedb.org](https://www.themoviedb.org/?spm=a2ty_o01.29997173.0.0.34fd5171MscR8Q)
2. Нажми **Sign Up** (вверху справа)
3. Заполни форму (email, логин, пароль)
4. Подтверди email

### Шаг 2: Получение API-ключа

1. Кликни на аватар → **Settings**
2. В левом меню выбери **API**
3. Нажми **Create** (создать ключ)
4. Выбери **Developer** (для обучения)
5. Заполни форму:
    - **Application Name:** `My Movie Bot`
    - **Application URL:** `http://localhost`
    - **Application Summary:** `Educational project`
6. Нажми **Submit**
7. Скопируй **API Key (v3 auth)** — это твоя строка доступа

> ⏱ Ключ активируется в течение 1–2 часов. Если получаешь `401` — подожди.

### Шаг 3: Проверка ключа в браузере

Открой в браузере (подставь свой ключ):

```
https://api.themoviedb.org/3/search/movie?api_key=ТВОЙ_КЛЮЧ&query=Матрица&language=ru-RU
```

**Ожидаемый результат:** JSON-ответ с данными о фильмах.

---

## 3️⃣ Запрос из Python

### Базовый код:

```python
import requests

API_KEY = 'твой_ключ_tmdb'

def search_movie(movie_name):
    url = 'https://api.themoviedb.org/3/search/movie'
    
    params = {
        'api_key': API_KEY,
        'query': movie_name,
        'language': 'ru-RU',
        'page': 1
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Ошибка: {response.status_code}')
        return None

# Использование
data = search_movie('Матрица')
if data and data['results']:
    print(data['results'][0]['title'])
```

### Разбор кода:

|Строка|Назначение|
|---|---|
|`requests.get()`|Отправка HTTP GET-запроса|
|`params`|Параметры запроса (автоматически добавляются в URL)|
|`response.status_code`|Код ответа сервера|
|`response.json()`|Преобразование ответа в словарь Python|

---

## 4️⃣ Структура ответа TMDB

### Пример JSON:

```json
{
  "page": 1,
  "results": [
    {
      "id": 603,
      "title": "Матрица",
      "overview": "Описание...",
      "vote_average": 8.7,
      "poster_path": "/f89U3ADr1oiB1s9GkdPOEpXUk5H.jpg",
      "release_date": "1999-03-30"
    }
  ],
  "total_pages": 5,
  "total_results": 100
}
```

### Доступ к данным в Python:

```python
data = search_movie('Матрица')

# Первый фильм
film = data['results'][0]

# Отдельные поля
title = film['title']
rating = film['vote_average']
description = film['overview']
poster_path = film['poster_path']

# Ссылка на постер
poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
```

---

## 5️⃣ Основные эндпоинты TMDB

|Запрос|URL|Метод|
|---|---|---|
|Поиск фильма|`/search/movie`|GET|
|Поиск сериала|`/search/tv`|GET|
|Фильм по ID|`/movie/{id}`|GET|
|Сериал по ID|`/tv/{id}`|GET|
|Популярные фильмы|`/movie/popular`|GET|
|Актёры фильма|`/movie/{id}/credits`|GET|
|Похожее|`/movie/{id}/similar`|GET|

### Пример — фильм по ID:

```python
def get_movie_by_id(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    params = {'api_key': API_KEY, 'language': 'ru-RU'}
    response = requests.get(url, params=params)
    return response.json()

# Бойцовский клуб
film = get_movie_by_id(550)
print(film['title'])
```

---

## 6️⃣ Обработка ошибок

### Коды ответов:

|Код|Значение|Действие|
|---|---|---|
|`200`|✅ Успех|Продолжай работу|
|`401`|❌ Неверный ключ|Проверь API_KEY|
|`404`|❌ Не найдено|Проверь ID или название|
|`429`|⚠️ Лимит запросов|Добавь паузу|
|`500`|❌ Ошибка сервера|Повтори позже|

### Шаблон с обработкой:

```python
import requests
import time

def safe_request(url, params):
    try:
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print('Ошибка: неверный API-ключ')
        elif response.status_code == 429:
            print('Лимит запросов. Ждём 5 секунд...')
            time.sleep(5)
            return safe_request(url, params)
        else:
            print(f'Ошибка API: {response.status_code}')
        
        return None
        
    except requests.exceptions.Timeout:
        print('Превышено время ожидания')
        return None
    except requests.exceptions.RequestException as e:
        print(f'Ошибка соединения: {e}')
        return None
```

---

## 7️⃣ Безопасное хранение ключа

### ❌ Не делай так:

```python
API_KEY = 'a1b2c3d4e5f6...'  # В коде — опасно!
```

### ✅ Делай так:

**Файл `config.py`:**

```python
TMDB_API_KEY = 'a1b2c3d4e5f6...'
BOT_TOKEN = '123456:AAHdqTcvCH1vGWJxfSeofSAs0K5PALDsaw'
```

**Файл `main.py`:**

```python
from config import TMDB_API_KEY, BOT_TOKEN

# Использование
params = {'api_key': TMDB_API_KEY}
```

**Файл `.gitignore` (если используешь Git):**

```
config.py
__pycache__/
*.pyc
```

---

## 8️⃣ Полный рабочий пример

```python
import requests
from config import TMDB_API_KEY

def get_movie_info(title):
    """Поиск фильма и возврат основных данных"""
    
    url = 'https://api.themoviedb.org/3/search/movie'
    params = {
        'api_key': TMDB_API_KEY,
        'query': title,
        'language': 'ru-RU'
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        return None
    
    data = response.json()
    
    if not data['results']:
        return None
    
    film = data['results'][0]
    
    poster = film.get('poster_path')
    poster_url = f'https://image.tmdb.org/t/p/w500{poster}' if poster else None
    
    return {
        'title': film['title'],
        'rating': film['vote_average'],
        'overview': film['overview'] or 'Описание недоступно',
        'year': film['release_date'][:4] if film.get('release_date') else 'N/A',
        'poster': poster_url
    }

# Тест
if __name__ == '__main__':
    movie = get_movie_info('Интерстеллар')
    if movie:
        print(f"🎬 {movie['title']} ({movie['year']})")
        print(f"⭐ Рейтинг: {movie['rating']}")
        print(f"📝 {movie['overview'][:100]}...")
    else:
        print('Фильм не найден')
```

---

## 9️⃣ Чек-лист перед запуском

- Зарегистрирован аккаунт на TMDB
- Получен API-ключ (v3 auth)
- Ключ сохранён в `config.py`
- Установлена библиотека `requests` (`pip install requests`)
- Проверен запрос в браузере
- Обработаны основные ошибки (401, 404, 429)
- Ключ не загружен в публичный репозиторий

---

## 📝 Практическое задание

1. Получи API-ключ на TMDB. (необязательно)
2. Проверь его в браузере (поиск фильма).
3. Напиши функцию `search_movie(name)`, которая возвращает название и рейтинг.
4. Добавь обработку ошибок (если ключ неверный или фильм не найден).
5. Вынеси ключ в отдельный файл `config.py`.
6. **Бонус:** Добавь команду в своего бота для поиска фильмов.

---

> 🎯 **Итог:** API — это стандартный способ получения данных из внешних сервисов. TMDB предоставляет бесплатный доступ с понятной документацией. Ключ хранится в секрете, запросы обрабатываются через `requests`, ответ приходит в JSON.