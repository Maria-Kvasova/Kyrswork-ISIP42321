@echo off
chcp 1251 >nul
echo ========================================
echo   Maria Beauty - Zapusk proekta
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv\" (
    echo [1/4] Sozdayu virtualnoe okruzhenie...
    python -m venv venv
)

echo [2/4] Aktiviruyu okruzhenie...
call venv\Scripts\activate

echo [3/4] Ustanavlivayu biblioteki...
pip install -q -r requirements.txt

echo [4/4] Primenyayu migracii...
python manage.py migrate

echo.
echo ========================================
echo   PROEKT GOTOV!
echo   Otkroy v brauzere: http://127.0.0.1:8000/
echo   Admin: admin / Admin123
echo ========================================
echo.
echo Ne zakryvay eto okno, poka polzueshsya saytom!
echo.

python manage.py runserver
pause