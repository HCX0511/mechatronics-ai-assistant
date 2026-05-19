@echo off
cd /d "%~dp0"
set APP_HOST=0.0.0.0
set APP_PORT=5000
set FLASK_DEBUG=false

echo Starting website...
echo Local: http://127.0.0.1:5000
echo LAN:   http://10.87.120.219:5000
echo.
echo Keep this window open while the website is in use.
echo.

"C:\Users\86189\AppData\Local\Programs\Python\Python314\python.exe" app.py
pause
