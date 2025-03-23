@echo off
echo Запуск серверу розробки Django...

:: Активуєм віртуальне середовище
call venv\Scripts\activate.bat

:: Запускаєм сервер
echo.
echo Сервер запущено! Відкрийте браузер та перейдіть за адресою:
echo http://127.0.0.1:8000/
echo.
echo Для зупинки серверу натисніть Ctrl+C
echo.

python manage.py runserver 