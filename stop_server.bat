@echo off
echo Зупинка серверу Django...
echo ----------------------------------------

:: Знаходимо процес Python, який запущено з параметром manage.py runserver
for /f "tokens=2" %%a in ('tasklist ^| findstr "python.exe"') do (
    taskkill /PID %%a /F
)

echo.
echo Сервер Django зупинено!
echo Можете закрити це вікно.

pause 