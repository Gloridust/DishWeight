#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXE打包脚本
自动化打包宴席菜品食材统计系统为可执行文件

使用方法:
python build_exe.py
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """检查PyInstaller是否已安装"""
    try:
        import PyInstaller
        print("✓ PyInstaller 已安装")
        return True
    except ImportError:
        print("✗ PyInstaller 未安装")
        return False

def install_pyinstaller():
    """安装PyInstaller"""
    print("正在安装 PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller 安装成功")
        return True
    except subprocess.CalledProcessError:
        print("✗ PyInstaller 安装失败")
        return False

def build_exe():
    """构建可执行文件"""
    print("开始构建可执行文件...")
    
    # 清理之前的构建文件
    if os.path.exists("build"):
        print("清理 build 目录...")
        shutil.rmtree("build")
    
    if os.path.exists("dist"):
        print("清理 dist 目录...")
        shutil.rmtree("dist")
    
    # 运行PyInstaller
    try:
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "build_exe.spec",
            "--clean"
        ])
        print("✓ 可执行文件构建成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ 构建失败: {e}")
        return False

def copy_data_files():
    """复制必要的数据文件到输出目录"""
    dist_dir = os.path.join("dist", "DishWeight")
    if not os.path.exists(dist_dir):
        print("✗ 输出目录不存在")
        return False
    
    # 复制示例数据文件
    if os.path.exists("dish_data_sample.json"):
        shutil.copy2("dish_data_sample.json", dist_dir)
        print("✓ 示例数据文件已复制")
    
    # 复制说明文档
    if os.path.exists("README.md"):
        shutil.copy2("README.md", dist_dir)
        print("✓ 说明文档已复制")
    
    # 创建启动说明文件
    startup_info = """宴席菜品食材统计系统 - 可执行版本

使用说明:
1. 双击 DishWeight.exe 启动程序
2. 数据文件 dish_data.json 将自动创建在程序同目录下
3. 可以导入 dish_data_sample.json 作为示例数据
4. 程序会自动创建数据备份文件

注意事项:
- 请确保程序目录有写入权限
- 数据文件会自动保存在程序同目录下
- 建议定期创建数据备份

技术支持:
如有问题，请查看 README.md 文档
"""
    
    with open(os.path.join(dist_dir, "使用说明.txt"), "w", encoding="utf-8") as f:
        f.write(startup_info)
    print("✓ 使用说明已创建")
    
    return True

def main():
    """主函数"""
    print("=" * 50)
    print("宴席菜品食材统计系统 - EXE打包工具")
    print("=" * 50)
    
    # 检查PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            print("无法安装PyInstaller，请手动安装后重试")
            return False
    
    # 构建可执行文件
    if not build_exe():
        print("构建失败，请检查错误信息")
        return False
    
    # 复制数据文件
    if not copy_data_files():
        print("数据文件复制失败")
        return False
    
    print("\n" + "=" * 50)
    print("打包完成！")
    print("可执行文件位置: dist/DishWeight/")
    print("主程序: dist/DishWeight/DishWeight.exe")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)