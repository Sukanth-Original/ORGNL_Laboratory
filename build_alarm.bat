@echo off
setlocal enabledelayedexpansion

:: Set the working directory to the script's location
cd /d "%~dp0"

:: Package Python script to EXE
pip install pyinstaller
pyinstaller --onefile --name "SmartAlarm" --clean main_alarm.py

:: Create desktop shortcut
set SCRIPT="%TEMP%\%RANDOM%-%RANDOM%-%RANDOM%-%RANDOM%.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\SmartAlarm.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%CD%\dist\SmartAlarm.exe" >> %SCRIPT%
echo oLink.WorkingDirectory = "%CD%\dist" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%
cscript /nologo %SCRIPT%
del %SCRIPT%

:: Cleanup build files
rmdir /s /q build
rmdir /s /q __pycache__
del /q SmartAlarm.spec

echo ------------------------------------------
echo BUILD COMPLETE!
echo Shortcut created on desktop: SmartAlarm.lnk
echo ------------------------------------------
pause
