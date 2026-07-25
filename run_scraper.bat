@echo off
REM Navigate to the project directory
cd /d "c:\Users\leola\OneDrive\Documents\Fortitude Valley Property"

REM Ensure uv is in the PATH for this session
set PATH=C:\Users\leola\.local\bin;%PATH%

REM Run the Python scraper script using uv
uv run --with requests --with beautifulsoup4 --with urllib3 main.py
