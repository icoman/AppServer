@echo off

call "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/vcvars64.bat" amd64
call C:\Python372-64\Scripts\nuitka  --module --no-pyi-file --recurse-none ../__init__.py

pause
