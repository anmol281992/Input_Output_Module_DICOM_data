#This  code Snippet generates the .exe file. You would need to install cx_freeze module to generate the executable.
#In order to generate the executable for Input_output_module run "python setup.py build" on the command prompt. Install cx_freeze module inorder to run setup.py

import sys
from cx_Freeze import setup, Executable
import os
# Dependencies are automatically detected, but it might need fine tuning.
# Please enter all the dependencies below under label "packages"
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
