@echo off

py "%~dp0mailtable.py" --input "%~1" --output "%~dp1%~n1.ini" --converttext

if %ERRORLEVEL% NEQ 0 pause