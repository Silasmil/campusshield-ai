@echo off
setlocal enabledelayedexpansion

REM CampusShield AI - Production Deployment Quick Start (Windows)
REM This script helps setup and verify production deployment

title CampusShield AI - Production Deployment Setup
color 0A

:menu
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║       CampusShield AI - Production Deployment Setup           ║
echo ║                      Windows Version                           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo What would you like to do?
echo.
echo   1) Verify production readiness
echo   2) Generate SECRET_KEY
echo   3) Create .env.production file
echo   4) Run security checks
echo   5) Run deployment report
echo   6) View deployment guide
echo   7) Exit
echo.
set /p choice="Enter choice (1-7): "

if "%choice%"=="1" goto verify
if "%choice%"=="2" goto genkey
if "%choice%"=="3" goto envfile
if "%choice%"=="4" goto security
if "%choice%"=="5" goto report
if "%choice%"=="6" goto guide
if "%choice%"=="7" goto exit
echo Invalid choice. Please try again.
timeout /t 2 >nul
goto menu

:verify
cls
echo.
echo ▶ Verifying production readiness...
echo.
echo ▶ Checking Python packages...
python -c "import django; print(f'Django: {django.__version__}')" >nul 2>&1 && (
    echo [✓] Django installed
) || (
    echo [✗] Django not found
)

python -c "import rest_framework; print('DRF installed')" >nul 2>&1 && (
    echo [✓] Django REST Framework installed
) || (
    echo [✗] Django REST Framework not found
)

echo.
echo ▶ Checking project structure...

if exist "campusshield\manage.py" (
    echo [✓] Found: campusshield\manage.py
) else (
    echo [✗] Missing: campusshield\manage.py
)

if exist "campusshield\campusshield\settings.py" (
    echo [✓] Found: campusshield\campusshield\settings.py
) else (
    echo [✗] Missing: campusshield\campusshield\settings.py
)

if exist "campusshield\incidents\models.py" (
    echo [✓] Found: campusshield\incidents\models.py
) else (
    echo [✗] Missing: campusshield\incidents\models.py
)

if exist "campusshield\ai_engine\__init__.py" (
    echo [✓] Found: campusshield\ai_engine\__init__.py
) else (
    echo [✗] Missing: campusshield\ai_engine\__init__.py
)

echo.
echo ▶ Running Django checks...
cd campusshield
python manage.py check >nul 2>&1 && (
    echo [✓] Django checks passed
) || (
    echo [✗] Django checks failed
    python manage.py check
)
cd ..

echo.
echo [✓] Production readiness verified!
echo.
pause
goto menu

:genkey
cls
echo.
echo ▶ Generating cryptographically secure SECRET_KEY...
echo.

for /f "delims=" %%i in ('python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"') do set SECRET_KEY=%%i

echo.
echo [✓] Generated SECRET_KEY:
echo.
echo     %SECRET_KEY%
echo.
echo [!] Copy this key and paste it into your .env.production file as:
echo     DJANGO_SECRET_KEY=%SECRET_KEY%
echo.
pause
goto menu

:envfile
cls
echo.
echo ▶ Creating .env.production configuration...
echo.

if exist ".env.production" (
    echo [!] .env.production already exists
    set /p overwrite="Overwrite? (y/n): "
    if /i not "!overwrite!"=="y" goto menu
)

if exist ".env.production.example" (
    copy ".env.production.example" ".env.production" >nul
    echo [✓] Created .env.production
) else (
    echo [✗] .env.production.example not found
    pause
    goto menu
)

echo.
echo ▶ Configuration file created. Please edit the following values:
echo.
echo Required settings in .env.production:
echo   1. DJANGO_ENVIRONMENT=production
echo   2. DJANGO_SECRET_KEY=^<generated above^>
echo   3. ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
echo   4. DATABASE_URL=postgresql://user:pass@localhost:5432/campusshield
echo   5. DEBUG=False
echo.

set /p edit="Open .env.production in editor? (y/n): "
if /i "%edit%"=="y" (
    start notepad .env.production
)

pause
goto menu

:security
cls
echo.
echo ▶ Running comprehensive security checks...
echo.

if exist "campusshield\security_check.py" (
    cd campusshield
    python security_check.py
    cd ..
) else (
    echo [✗] security_check.py not found
)

echo.
pause
goto menu

:report
cls
echo.
echo ▶ Running deployment readiness report...
echo.

if exist "generate_deployment_report.py" (
    python generate_deployment_report.py
) else (
    echo [✗] generate_deployment_report.py not found
)

echo.
pause
goto menu

:guide
cls
echo.
echo ▶ Production Deployment Guide
echo.
echo For complete deployment instructions, see: PRODUCTION_DEPLOYMENT.md
echo.

if exist "PRODUCTION_DEPLOYMENT.md" (
    set /p viewguide="View PRODUCTION_DEPLOYMENT.md? (y/n): "
    if /i "!viewguide!"=="y" (
        start notepad PRODUCTION_DEPLOYMENT.md
    )
) else (
    echo [✗] PRODUCTION_DEPLOYMENT.md not found
)

pause
goto menu

:exit
cls
echo.
echo [✓] Goodbye!
echo.
exit /b 0
