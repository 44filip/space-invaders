import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["pygame", "random", "sys", "os"],
    "include_files": ["sprites/", "variables.py"],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("main.py", base=base, target_name="ScuffedSpaceInvaders.exe"),
]

setup(
    name="Scuffed Space Invaders",
    version="1.0",
    description="A Pygame experiment",
    options={"build_exe": build_exe_options},
    executables=executables,
)