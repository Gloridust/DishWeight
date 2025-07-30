# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller configuration file for Windows
For building DishWeight system executable on Windows

Usage:
pyinstaller build_windows.spec
"""

import os
import sys

# Get current directory
current_dir = os.path.dirname(os.path.abspath(SPEC))

block_cipher = None

a = Analysis(
    ['main.py'],  # Main program file
    pathex=[current_dir],  # Search path
    binaries=[],
    datas=[
        ('README.md', '.'),  # Include documentation
        ('USAGE.md', '.'),   # Include user manual
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'pandas',
        'openpyxl',
        'json',
        'uuid',
        'datetime',
        'os',
        'sys',
        'tempfile',
        'shutil',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'PyQt5',
        'PySide6',
        'PyQt6',
        'PySide2',
        'matplotlib',
        'IPython',
        'jupyter',
        'numpy.random._pickle',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DishWeight',  # Executable name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Can add icon file path here
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DishWeight'  # Output directory name
)