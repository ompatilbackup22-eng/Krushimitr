@echo off
echo ========================================
echo    SOIL DETECTION - MOBILE ACCESS
echo ========================================
echo.
echo Starting Flask application...
start "Flask App" cmd /k "python app.py"
echo.
echo Waiting 5 seconds for Flask to start...
timeout /t 5 /nobreak >nul
echo.
echo Starting ngrok tunnel...
start "ngrok Tunnel" cmd /k "ngrok http 5000"
echo.
echo ========================================
echo    SETUP COMPLETE!
echo ========================================
echo.
echo Your mobile access URLs:
echo - Public: https://7727e97cc470.ngrok-free.app
echo - Local:  http://192.168.1.14:5000
echo.
echo ngrok Dashboard: http://localhost:4040
echo.
echo Press any key to exit...
pause >nul
