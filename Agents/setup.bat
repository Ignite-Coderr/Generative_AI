@echo off
echo ========================================
echo Agents Project Setup
echo ========================================
echo.

echo Creating virtual environment with Python 3.10...
py -3.10 -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python 3.10 is installed
    pause
    exit /b 1
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Registering Jupyter kernel...
python -m ipykernel install --user --name=agents_py310 --display-name="Python 3.10 (Agents)"

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start working:
echo 1. Activate the environment: venv\Scripts\activate
echo 2. Start Jupyter: jupyter notebook
echo 3. Open index.ipynb
echo 4. Select kernel: Python 3.10 (Agents)
echo.
pause
