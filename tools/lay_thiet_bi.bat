@echo off
for /f "skip=1 tokens=1" %%i in ('adb devices') do (
    if not "%%i"=="" echo %%i
)
pause
