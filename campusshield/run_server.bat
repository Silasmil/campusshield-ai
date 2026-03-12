@echo off
REM CampusShield Development Server Startup Script

echo Starting CampusShield Development Server...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if django-extensions is installed
pip show django-extensions >nul 2>&1
if errorlevel 1 (
    echo Installing django-extensions for HTTPS support...
    pip install django-extensions werkzeug -q
)

REM Check if SSL certificates exist, if not create them
if not exist "ssl_certs\cert.pem" (
    echo.
    echo Generating self-signed SSL certificates...
    mkdir ssl_certs
    REM Use OpenSSL if available
    where openssl >nul 2>&1
    if errorlevel 1 (
        echo WARNING: OpenSSL not found. Using HTTP only.
        echo To enable HTTPS, install OpenSSL or generate certificates manually.
        python manage.py runserver 0.0.0.0:8000
    ) else (
        openssl genrsa -out ssl_certs\key.pem 2048
        openssl req -new -x509 -key ssl_certs\key.pem -out ssl_certs\cert.pem -days 365 -subj "/C=US/ST=State/L=City/O=Campus/CN=localhost"
        echo SSL certificates generated successfully!
        echo.
        python manage.py runserver_plus --cert ssl_certs/cert.pem --key ssl_certs/key.pem 0.0.0.0:8000
    )
) else (
    echo SSL certificates found. Starting HTTPS server...
    echo.
    python manage.py runserver_plus --cert ssl_certs/cert.pem --key ssl_certs/key.pem 0.0.0.0:8000
)

pause
