#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": [
        "PyQt5", "pandas", "openpyxl", "PIL", "reportlab", "numpy",
        "io", "base64", "datetime", "sys", "os"
    ],
    "excludes": ["tkinter", "unittest", "email", "http", "urllib", "xml"],
    "include_files": [
        ("templates/", "templates/"),
        ("assets/", "assets/"),
        ("models/", "models/"),
    ],
    "optimize": 2,
    "include_msvcrt": True
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="Cable Tag Printer",
    version="1.0.0",
    description="Application for printing cable tags with handwriting conversion",
    author="Lukin001655",
    options={"build_exe": build_exe_options},
    executables=[
        Executable(
            "main.py",
            base=base,
            target_name="CableTagPrinter.exe"
        )
    ]
)