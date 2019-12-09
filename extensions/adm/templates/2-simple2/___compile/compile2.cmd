@echo off

rem set PATH=C:\mingw-w64\x86_64-8.1.0-posix-seh-rt_v6-rev0\mingw64\bin;%PATH%
rem set PATH=C:\winbuilds\bin;%PATH%
rem call C:\Python27\Scripts\nuitka  --mingw64 --module  --no-pyi-file --recurse-none mymod.py



call "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Auxiliary/Build/vcvars64.bat" x86
call C:\Python27\Scripts\nuitka  --module  --no-pyi-file --recurse-none mymod.py


pause
