@echo off
echo ========================================
echo Multimodal Explanation System - Installation
echo ========================================
echo.

echo Step 1: Installing Backend Dependencies...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing Python packages...
pip install -r requirements.txt

if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Please edit backend\.env and add your OpenAI API key!
    echo.
)

cd ..

echo.
echo Step 2: Installing Frontend Dependencies...
cd frontend
call npm install
cd ..

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit backend\.env and add your OPENAI_API_KEY
echo 2. Run start.bat to launch the application
echo.
pause
