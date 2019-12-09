import os
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
                     "include_msvcr": True,
                     "silent": True,
                     "build_exe":os.getenv("EXEDIR"),
                     "zip_include_packages": "*",
                     "zip_exclude_packages": "",
                     "packages": ["pkg_resources._vendor"],
                     "excludes": ["tkinter","scipy","cv2","PySide","numpy","PyQt4"],
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = "Console"
if 0:
    if sys.platform == "win32":
        base = "Win32GUI"

target = Executable(
    script="main.py", base=base, icon="favicon.ico"
    )
setup(  name = "Python application",
        version = "1.0",
        description = "(C) 2019 Ioan Coman",
        options = {"build_exe": build_exe_options},
        executables = [target])

