import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = "C:\\Users\\A1\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\A1\\AppData\\Local\\Programs\\Python\\Python36-32\\tcl\\tk8.6"

executables = [cx_Freeze.Executable("pong.py")]

cx_Freeze.setup(
    name = "Pong",
    version = "0.1",
    author = "Sudip Sarker",
    options = {"build_exe":{"packages":["pygame"],
                            "include_files":["bounce.ogg","woosh.ogg", "pong.png"]}},
    description = "Arcade Pong",
    executables = executables
    )
