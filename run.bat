@echo off
cls
echo ===================================================
echo               KA LANGUAGE LAUNCHER                 
echo ===================================================
echo.

:: Ask the user for permission to execute the test script
set /p user_choice="Do you want to run test.ka? (Y/N): "

:: Check if the user typed N or n (No)
if /i "%user_choice%"=="N" goto exit_program

:: Check if the user typed Y or y (Yes)
if /i "%user_choice%"=="Y" goto run_script

:: If they type anything else, warn them and ask again
echo Invalid input. Please type Y or N.
pause
goto :eof

:run_script
echo.
echo Permission granted. Initializing Ka compiler...
echo ---------------------------------------------------
python ka.py test.ka
echo ---------------------------------------------------
echo Execution finished successfully.
pause
exit

:exit_program
echo.
echo Permission denied. Exiting launcher...
timeout /t 3 >nul
exit
