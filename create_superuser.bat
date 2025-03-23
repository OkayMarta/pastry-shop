@echo off
echo Створення суперкористувача Django...
echo ----------------------------------------

:: Активуємо віртуальне середовище
call venv\Scripts\activate.bat

:: Створюємо суперкористувача
python manage.py createsuperuser

echo.
echo Суперкористувач створений успішно!
echo Тепер ви можете увійти в адмін-панель за адресою: http://127.0.0.1:8000/admin/

pause 