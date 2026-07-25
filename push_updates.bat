@echo off
echo ========================================================
echo   Updating GitHub Repository for Streamlit Cloud
echo ========================================================
echo.
"%TEMP%\mingit\cmd\git.exe" push -u origin main --force
echo.
echo ========================================================
echo   Push complete! 
echo   Streamlit Cloud will now automatically update 
echo   https://fortitude-valley-property.streamlit.app/
echo ========================================================
pause
