@echo off
echo ==========================================
echo   Dijital Kuran Hocam (Windows Baslatma)
echo ==========================================

echo.
echo Adim 1: Kutuphaneler kontrol ediliyor...
pip install -r requirements.txt

echo.
echo Adim 2: Ngrok baslatiliyor (Tunel aciliyor)...
start "Ngrok Tünel" cmd /k "ngrok http 8080"

echo.
echo Adim 3: Frontend Sunucusu (Web Sitesi) aciliyor...
start "Frontend Sunucu" cmd /k "python server.py"

echo.
echo Adim 4: Yapay Zeka (Beyin) baslatiliyor...
echo.
echo Her sey hazir! Tarayicinizdan http://localhost:8000 adresine gidin.
echo.

python custom_llm_server.py
pause
