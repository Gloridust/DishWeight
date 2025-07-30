#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动化打包脚本
使用cx_Freeze进行Windows应用程序打包
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, description):
    """运行命令并处理输出"""
    print(f"\n{'='*50}")
    print(f"正在执行: {description}")
    print(f"命令: {cmd}")
    print('='*50)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        if result.stdout:
            print("标准输出:")
            print(result.stdout)
        
        if result.stderr:
            print("错误输出:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} 成功完成")
            return True
        else:
            print(f"❌ {description} 失败，返回码: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False

def check_requirements():
    """检查依赖"""
    print("检查Python环境和依赖...")
    print(f"Python版本: {sys.version}")
    
    required_packages = ['pandas', 'numpy', 'openpyxl', 'cx_Freeze']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} 已安装")
        except ImportError:
            print(f"❌ {package} 未安装")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n需要安装缺失的包: {', '.join(missing_packages)}")
        if input("是否自动安装缺失的包? (y/n): ").lower() == 'y':
            cmd = f"{sys.executable} -m pip install {' '.join(missing_packages)}"
            return run_command(cmd, "安装缺失的包")
        else:
            return False
    
    return True

def clean_build_dirs():
    """清理构建目录"""
    print("\n清理旧的构建文件...")
    dirs_to_clean = ['build', 'dist', '__pycache__', 'build_cxfreeze']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ 删除目录: {dir_name}")
            except Exception as e:
                print(f"❌ 删除目录 {dir_name} 失败: {e}")



def try_cxfreeze():
    """使用cx_Freeze进行打包"""
    print("\n" + "="*60)
    print("使用cx_Freeze打包")
    print("="*60)
    
    # 确保cx_Freeze已安装
    install_cmd = f"{sys.executable} -m pip install --upgrade cx_Freeze>=8.0.0"
    if not run_command(install_cmd, "安装/升级cx_Freeze"):
        return False
    
    # 使用setup文件打包
    if os.path.exists("setup_cxfreeze.py"):
        cmd = f"{sys.executable} setup_cxfreeze.py build"
        if run_command(cmd, "使用cx_Freeze打包"):
            build_dir = "build_cxfreeze"
            if os.path.exists(build_dir):
                exe_files = list(Path(build_dir).glob("**/DishWeight.exe"))
                if exe_files:
                    print("✅ cx_Freeze打包成功！")
                    print(f"可执行文件位置: {os.path.abspath(exe_files[0])}")
                    return True
    
    return False

def main():
    """主函数"""
    print("宴席菜品配料统计系统 - 自动化打包工具")
    print("="*60)
    
    # 检查环境
    if not check_requirements():
        print("❌ 环境检查失败，请手动安装依赖后重试")
        return False
    
    # 清理构建目录
    clean_build_dirs()
    
    # 使用cx_Freeze进行打包
    success = try_cxfreeze()
    
    if success:
        print("\n" + "="*60)
        print("🎉 打包成功完成！")
        print("="*60)
        print("请在build_cxfreeze/目录中找到可执行文件")
    else:
        print("\n" + "="*60)
        print("❌ 所有打包方法都失败了")
        print("="*60)
        print("建议:")
        print("1. 检查Python版本是否为3.8-3.11")
        print("2. 尝试更新所有依赖包")
        print("3. 查看上面的错误信息进行排查")
        print("4. 考虑使用虚拟环境重新安装依赖")
    
    input("\n按回车键退出...")
    return success

if __name__ == "__main__":
    main() 