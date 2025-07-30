import sys
from cx_Freeze import setup, Executable
import os

# 需要包含的模块
includes = [
    "tkinter",
    "tkinter.ttk", 
    "tkinter.messagebox",
    "tkinter.filedialog",
    "pandas",
    "numpy", 
    "openpyxl",
    "json",
    "datetime",
    "os",
    "sys",
    "tempfile"
]

# 需要包含的文件
include_files = []

# 排除的模块（减少打包体积）
excludes = [
    "matplotlib",
    "scipy",
    "PyQt5",
    "PySide2",
    "PySide6",
    "tkinter.test",
    "unittest",
    "test"
]

# 设置executable选项
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # 不显示控制台窗口

# 创建可执行文件配置
executables = [
    Executable(
        script="main.py",
        base=base,
        target_name="DishWeight.exe",
        icon=None  # 可以在这里指定图标文件
    )
]

setup(
    name="宴席菜品配料统计系统",
    version="1.0",
    description="用于宴席菜品配料统计和成本计算的工具",
    options={
        "build_exe": {
            "includes": includes,
            "excludes": excludes,
            "include_files": include_files,
            "build_exe": "build_cxfreeze",
            "optimize": 2,
            "packages": ["pandas", "numpy", "openpyxl", "tkinter"]
        }
    },
    executables=executables
) 