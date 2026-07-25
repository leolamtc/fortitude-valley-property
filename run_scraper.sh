#!/bin/bash

# Navigate to the project directory
cd "c:/Users/leola/OneDrive/Documents/Fortitude Valley Property" || exit

# Ensure uv is in the PATH (adjust if uv is installed elsewhere in your WSL/bash environment)
export PATH="$HOME/.local/bin:$PATH"

# Run the Python scraper script using uv
uv run --with requests --with beautifulsoup4 --with urllib3 main.py
