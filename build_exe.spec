# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller 配置文件
用于将宴席菜品食材统计系统打包成可执行文件

使用方法:
1. 安装 PyInstaller: pip install pyinstaller
2. 运行打包命令: pyinstaller build_exe.spec
3. 生成的可执行文件位于 dist/DishWeight/ 目录下
"""

import os
import sys

# 获取当前目录
current_dir = os.path.dirname(os.path.abspath(SPEC))

block_cipher = None

a = Analysis(
    ['main.py'],  # 主程序文件
    pathex=[current_dir],  # 搜索路径
    binaries=[],
    datas=[
        ('README.md', '.'),  # 包含说明文档
        ('USAGE.md', '.'),   # 包含用户使用说明
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
        'numpy',
        'scipy',
        'IPython',
        'jupyter',
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
    name='DishWeight',  # 可执行文件名
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 可以添加图标文件路径
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='DishWeight'  # 输出目录名
)