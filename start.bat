@echo off
REM Kill all Python processes
taskkill /F /IM python.exe

REM Wait for a moment
timeout /t 2 /nobreak >nul

REM Set the working directory to the script's directory
cd /d "%~dp0"

REM Launch the launcher.py script using the full path to python.exe
"C:\Users\Youssef\AppData\Local\Programs\Python\Python310\python.exe" "%~dp0launcher.py"

timeout /t 5 /nobreak >nul
