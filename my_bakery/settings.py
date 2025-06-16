"""
Налаштування Django проєкту my_bakery.

Згенеровано командою 'django-admin startproject' для Django 5.1.6.

Для отримання додаткової інформації про цей файл див.:
https://docs.djangoproject.com/en/5.1/topics/settings/

Повний список налаштувань та їх значень див. за адресою:
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Завантажуємо змінні оточення з файлу .env, що знаходиться в кореневій папці проекту.
# Це дозволяє зберігати конфіденційні дані (паролі, ключі API) окремо від коду.
load_dotenv()

# Визначення базової директорії проекту (папка, що містить manage.py).
# BASE_DIR використовується для побудови шляхів до інших файлів та папок проекту.
BASE_DIR = Path(__file__).resolve().parent.parent


# Налаштування для швидкого старту розробки - не підходять для продакшн-середовища.
# Див. https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/ для деталей розгортання.

# ПОПЕРЕДЖЕННЯ ПРО БЕЗПЕКУ: зберігайте секретний ключ, що використовується у продакшн-середовищі, в таємниці!
# SECRET_KEY завантажується зі змінних оточення або використовує тимчасовий ключ для розробки.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-your-secret-key-here')

# ПОПЕРЕДЖЕННЯ ПРО БЕЗПЕКУ: не запускайте проект з увімкненим режимом відладки (debug) у продакшн-середовищі!
# DEBUG_MODE визначає, чи показувати детальні сторінки помилок.
# Значення завантажується зі змінних оточення (за замовчуванням 'True').
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Список дозволених хостів/доменів, з яких може обслуговуватися сайт.
# Завантажується зі змінних оточення (за замовчуванням '127.0.0.1,localhost').
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')


# Визначення встановлених додатків Django
INSTALLED_APPS = [
    # Стандартні додатки Django
    'django.contrib.admin',          # Адміністративна панель
    'django.contrib.auth',           # Система автентифікації
    'django.contrib.contenttypes',   # Фреймворк для типів контенту
    'django.contrib.sessions',       # Механізм сесій
    'django.contrib.messages',       # Фреймворк для повідомлень (flash messages)
    'django.contrib.staticfiles',    # Управління статичними файлами (CSS, JS, зображення)

    # Сторонні додатки
    'django_cleanup.apps.CleanupConfig', # Автоматичне видалення файлів з MEDIA_ROOT при видаленні відповідних об'єктів моделей

    # Власні додатки проекту
    'shop.apps.ShopConfig',          # Основний додаток магазину
]

# Порядок проміжних обробників (Middleware)
# Middleware обробляють запити та відповіді на різних етапах.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',      # Забезпечує різні аспекти безпеки
    'django.contrib.sessions.middleware.SessionMiddleware', # Керує сесіями
    'django.middleware.common.CommonMiddleware',          # Додає загальні налаштування (наприклад, обробка слешів в URL)
    'django.middleware.csrf.CsrfViewMiddleware',          # Захист від CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Додає об'єкт user до запиту
    'django.contrib.messages.middleware.MessageMiddleware',   # Підтримка фреймворку повідомлень
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Захист від клікджекінгу
]

# Головний файл конфігурації URL-адрес проекту.
ROOT_URLCONF = 'my_bakery.urls'

# Налаштування шаблонів Django
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Шлях до папки з глобальними шаблонами (якщо є, зараз не використовується активно).
        'DIRS': [BASE_DIR / 'templates'],
        # Дозволяє Django шукати шаблони всередині папок 'templates' кожного встановленого додатку.
        'APP_DIRS': True,
        'OPTIONS': {
            # Контекстні процесори додають змінні до контексту кожного шаблону.
            'context_processors': [
                'django.template.context_processors.debug',    # Змінні для відладки
                'django.template.context_processors.request',  # Об'єкт request
                'django.contrib.auth.context_processors.auth', # Інформація про користувача та права доступу
                'django.contrib.messages.context_processors.messages', # Повідомлення для користувача
            ],
        },
    },
]

# WSGI-додаток, що використовується серверами для запуску проекту.
WSGI_APPLICATION = 'my_bakery.wsgi.application'


# Налаштування бази даних
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Використовується SQLite база даних
        'NAME': BASE_DIR / 'db.sqlite3',        # Шлях до файлу бази даних (db.sqlite3 у корені проекту)
    }
}


# Валідатори паролів
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
# Використовуються для перевірки надійності паролів користувачів.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Налаштування інтернаціоналізації (i18n)
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'uk'          # Мова сайту за замовчуванням (українська)
TIME_ZONE = 'Europe/Kiev'     # Часовий пояс
USE_I18N = True               # Вмикає систему перекладів Django
USE_TZ = True                 # Вмикає підтримку часових поясів для дат та часу


# Налаштування статичних файлів (CSS, JavaScript, зображення, що є частиною коду)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = 'static/' # URL-префікс для статичних файлів
# Додаткові шляхи, де Django шукатиме статичні файли (окрім папок 'static' у додатках).
STATICFILES_DIRS = [
    BASE_DIR / 'static', # Папка 'static' у корені проекту
]

# Налаштування медіафайлів (файли, завантажені користувачами або через адмін-панель)
MEDIA_URL = 'media/' # URL-префікс для медіафайлів
MEDIA_ROOT = BASE_DIR / 'media' # Шлях у файловій системі до папки, де зберігаються медіафайли

# Тип поля для первинного ключа (primary key) за замовчуванням для нових моделей.
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' # Використовує 64-бітні цілі числа

# Налаштування електронної пошти для надсилання повідомлень
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # Використання SMTP для надсилання пошти
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')         # SMTP-сервер (завантажується з .env, за замовчуванням для Gmail)
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))                 # Порт SMTP-сервера (завантажується з .env)
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'   # Використання TLS-шифрування (завантажується з .env)

# Облікові дані для SMTP-сервера (завантажуються з .env).
# Важливо: ці дані не повинні бути жорстко закодовані у файлі settings.py.
# Значення за замовчуванням використовуються, якщо відповідні змінні не знайдені в .env,
# але вони не дозволять успішно надіслати пошту без коректних даних.
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'configure-your-email@example.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'configure-your-password')

# Адреса електронної пошти, що вказується як відправник ("From:") за замовчуванням.
# Якщо не задано в .env, використовується EMAIL_HOST_USER.
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER)
# Адреса електронної пошти для отримання адміністративних сповіщень (наприклад, про нові замовлення).
# Якщо не задано в .env, використовується EMAIL_HOST_USER.
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', EMAIL_HOST_USER)