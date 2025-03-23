@echo off
echo Створення віртуального середовища...

:: Перевіряємл, чи існує venv
IF EXIST venv (
    echo Видалення існуючого віртуального середовища...
    rmdir /s /q venv
)

:: Створюємо нове віртуальне середовище
python -m venv venv
echo Віртуальне середовище створено.

:: Активовуємо віртуальне середовище і встановлюємо залежності
echo Встановлення залежностей...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo Готово! Віртуальне середовище налаштовано та всі залежності встановлені:
pip list

echo.
echo Для активації середовища використовуйте команду: call venv\Scripts\activate.bat

pause 