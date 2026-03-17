@echo off
REM Setup script for School SaaS local development on Windows
REM This batch file sets up the development environment

echo.
echo ========================================
echo School SaaS - Local Development Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [OK] Found: %PYTHON_VERSION%
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo Virtual environment already exists, skipping...
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
if errorlevel 1 (
    echo WARNING: pip upgrade had issues, continuing anyway...
)
echo [OK] pip upgraded
echo.

REM Install requirements
if exist "requirements.txt" (
    echo Installing dependencies from requirements.txt...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
) else (
    echo ERROR: requirements.txt not found
    pause
    exit /b 1
)
echo.

REM Set FLASK_APP
echo Setting FLASK_APP environment variable...
set FLASK_APP=app.py
echo [OK] FLASK_APP set to app.py
echo.

REM Initialize database
echo Initializing database...
if not exist "data.db" (
    echo Creating database...
    python -c "from app import app, db; app.app_context().push(); db.create_all(); print('[OK] Database created')"
    if errorlevel 1 (
        echo WARNING: Database creation encountered issues
        echo You may need to run manually: flask db upgrade
    )
) else (
    echo Database already exists
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Ensure .env file is configured
echo   2. Run the development server:
echo      python app.py
echo   3. API will be available at http://localhost:5000
echo.
echo Useful commands:
echo   - Run server: python app.py
echo   - Flask shell: flask shell
echo   - Database migrations: flask db migrate -m "Description"
echo.
pause
