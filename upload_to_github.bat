@echo off
echo ========================================
echo GitHub Upload Script
echo ========================================
echo.

echo Checking Git installation...
git --version
if errorlevel 1 (
    echo ERROR: Git is not installed!
    echo Please install Git from: https://git-scm.com/
    pause
    exit /b 1
)

echo.
echo Current directory:
cd

echo.
echo Initializing Git repository...
git init

echo.
echo Adding remote repository...
git remote add origin https://github.com/Aman-Husain-123/GenerativeAI_Learning_Journey.git 2>nul
if errorlevel 1 (
    echo Remote already exists, updating...
    git remote set-url origin https://github.com/Aman-Husain-123/GenerativeAI_Learning_Journey.git
)

echo.
echo Checking current status...
git status

echo.
echo Adding all files...
git add .

echo.
echo Committing changes...
git commit -m "Initial commit: Complete Generative AI Learning Journey - Added LangChain Agents, MediChatbot, FastAPI projects, and more"

echo.
echo Setting main branch...
git branch -M main

echo.
echo Pushing to GitHub...
echo You may be prompted for your GitHub credentials
echo Use your Personal Access Token as password
git push -u origin main

echo.
echo ========================================
echo Upload Complete!
echo ========================================
echo.
echo Visit your repository at:
echo https://github.com/Aman-Husain-123/GenerativeAI_Learning_Journey
echo.
pause
