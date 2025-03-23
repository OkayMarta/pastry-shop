@echo off
echo Скидання бази даних...

:: Активуємо віртуальне середовище
call venv\Scripts\activate.bat

:: Видаляємо стару базу даних та файли міграцій
IF EXIST db.sqlite3 (
    echo Видалення існуючої бази даних...
    del /f db.sqlite3
)

IF EXIST shop\migrations\*.py (
    echo Видалення файлів міграцій...
    del /f shop\migrations\*.py
    echo Створення нового файлу __init__.py...
    type nul > shop\migrations\__init__.py
)

:: Створюємо нові міграції та застосовуємо їх
echo Створення нових міграцій...
python manage.py makemigrations shop

echo Застосування міграцій...
python manage.py migrate

:: Створюємо суперкористувача
echo Створення суперкористувача...
echo.
echo УВАГА: Зараз вам потрібно буде ввести дані для суперкористувача
echo (логін, email та пароль)
echo.
python manage.py createsuperuser

echo.
echo Готово! База даних успішно скинута та перестворена.
echo Створено нового суперкористувача.

pause