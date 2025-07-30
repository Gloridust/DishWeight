#!/usr/bin/env python3
"""
宴席菜品配料统计系统启动脚本
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main import DishWeightGUI
    
    if __name__ == "__main__":
        print("正在启动宴席菜品配料统计系统...")
        app = DishWeightGUI()
        app.run()
        
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保已安装所需依赖包:")
    print("pip install pandas openpyxl")
    sys.exit(1)
    
except Exception as e:
    print(f"程序启动失败: {e}")
    sys.exit(1)