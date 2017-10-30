# This  code Snippet generates the .exe file. You would need to install cx_freeze module to generate the executable.

import sys
from cx_Freeze import setup, Executable
import os
# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os", "numpy", "dicom", "sys", "tkinter"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Fine the following two lines based on location of TCK and TK libraries in python.
os.environ['TCL_LIBRARY'] = "C:/ProgramData/Anaconda3/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/ProgramData/Anaconda3/tcl/tk8.6"
setup(  name = "input_output_module",
        version = "0.1",
        description = "My I/O application!",
        options = {"build_exe": build_exe_options},
        executables = [Executable("input_output_module.py", base=base)])
