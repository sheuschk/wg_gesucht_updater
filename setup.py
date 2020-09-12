import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
includefiles = ['geckodriver.exe']
build_exe_options = {'include_files': includefiles, "packages": ["os"], "excludes": ["tkinter"]}


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None


setup(name="wg_gesucht",
      version="0.1",
      description="WG gesucht!",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])
