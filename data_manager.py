import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional
import pandas as pd

class DataManager:
    """数据管理类，负责食材、菜品数据的存储和管理"""
    
    def __init__(self, data_file: str = "dish_data.json"):
        # 获取程序运行目录，确保在打包成exe后能正确定位数据文件
        if getattr(sys, 'frozen', False):
            # 如果是打包后的exe文件
            self.app_dir = os.path.dirname(sys.executable)
        else:
            # 如果是Python脚本
            self.app_dir = os.path.dirname(os.path.abspath(__file__))
        
        # 数据文件的完整路径
        self.data_file = os.path.join(self.app_dir, data_file)
        
        # 初始化数据结构
        self.data = {
            "version": "1.0",  # 数据版本号
            "created_time": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "ingredients": {},  # 食材库 {id: {"name": str, "unit": str, "price": float}}
            "dishes": {},       # 菜品库 {id: {"name": str, "ingredients": {ingredient_id: amount}}}
            "menus": {}         # 宴席菜单 {id: {"name": str, "dishes": {dish_id: quantity}}}
        }
        
        # 确保数据目录存在
        self._ensure_data_directory()
        
        # 加载数据
        self.load_data()
    
    def _ensure_data_directory(self):
        """确保数据目录存在且可写"""
        try:
            if not os.path.exists(self.app_dir):
                os.makedirs(self.app_dir, exist_ok=True)
            
            # 测试目录是否可写
            test_file = os.path.join(self.app_dir, "test_write.tmp")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            
        except Exception as e:
            print(f"数据目录创建或写入测试失败: {e}")
            # 如果无法写入程序目录，尝试使用用户目录
            import tempfile
            self.app_dir = tempfile.gettempdir()
            self.data_file = os.path.join(self.app_dir, "dish_data.json")
            print(f"已切换到临时目录: {self.app_dir}")
    
    def load_data(self):
        """从文件加载数据"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    
                # 数据版本兼容性处理
                if isinstance(loaded_data, dict):
                    if "version" not in loaded_data:
                        # 旧版本数据格式，进行升级
                        self._upgrade_data_format(loaded_data)
                    else:
                        self.data.update(loaded_data)
                        self.data["last_modified"] = datetime.now().isoformat()
                
                print(f"数据加载成功，文件路径: {self.data_file}")
                
            else:
                print("数据文件不存在，将创建新的数据文件")
                self.save_data()
                    
        except json.JSONDecodeError as e:
            print(f"数据文件格式错误: {e}")
            print("将使用默认数据结构")
            self.save_data()
        except Exception as e:
            print(f"加载数据失败: {e}")
            print("将使用默认数据结构")
            self.save_data()
    
    def _upgrade_data_format(self, old_data):
        """升级旧版本数据格式"""
        print("检测到旧版本数据格式，正在升级...")
        self.data["ingredients"] = old_data.get("ingredients", {})
        self.data["dishes"] = old_data.get("dishes", {})
        self.data["menus"] = old_data.get("menus", {})
        self.data["last_modified"] = datetime.now().isoformat()
        print("数据格式升级完成")
    
    def save_data(self):
        """保存数据到文件"""
        try:
            # 更新最后修改时间
            self.data["last_modified"] = datetime.now().isoformat()
            
            # 保存数据到临时文件，然后重命名（原子操作）
            temp_file = self.data_file + ".tmp"
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            
            # 原子性替换文件
            if os.path.exists(temp_file):
                if os.path.exists(self.data_file):
                    os.remove(self.data_file)
                os.rename(temp_file, self.data_file)
            
            print(f"数据保存成功，文件路径: {self.data_file}")
            
        except Exception as e:
            print(f"保存数据失败: {e}")
            # 如果保存失败，尝试清理临时文件
            temp_file = self.data_file + ".tmp"
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
    
    def get_data_file_path(self):
        """获取数据文件路径"""
        return self.data_file
    
    # 食材管理
    def add_ingredient(self, name: str, unit: str, price: float = 0.0) -> str:
        """添加食材"""
        ingredient_id = str(len(self.data["ingredients"]) + 1)
        self.data["ingredients"][ingredient_id] = {
            "name": name,
            "unit": unit,
            "price": price
        }
        self.save_data()
        return ingredient_id
    
    def get_ingredients(self) -> Dict:
        """获取所有食材"""
        return self.data["ingredients"]
    
    def update_ingredient(self, ingredient_id: str, name: str, unit: str, price: float):
        """更新食材信息"""
        if ingredient_id in self.data["ingredients"]:
            self.data["ingredients"][ingredient_id] = {
                "name": name,
                "unit": unit,
                "price": price
            }
            self.save_data()
    
    def delete_ingredient(self, ingredient_id: str):
        """删除食材"""
        if ingredient_id in self.data["ingredients"]:
            del self.data["ingredients"][ingredient_id]
            self.save_data()
    
    # 菜品管理
    def add_dish(self, name: str, ingredients: Dict[str, float]) -> str:
        """添加菜品"""
        dish_id = str(len(self.data["dishes"]) + 1)
        self.data["dishes"][dish_id] = {
            "name": name,
            "ingredients": ingredients
        }
        self.save_data()
        return dish_id
    
    def get_dishes(self) -> Dict:
        """获取所有菜品"""
        return self.data["dishes"]
    
    def update_dish(self, dish_id: str, name: str, ingredients: Dict[str, float]):
        """更新菜品信息"""
        if dish_id in self.data["dishes"]:
            self.data["dishes"][dish_id] = {
                "name": name,
                "ingredients": ingredients
            }
            self.save_data()
    
    def delete_dish(self, dish_id: str):
        """删除菜品"""
        if dish_id in self.data["dishes"]:
            del self.data["dishes"][dish_id]
            self.save_data()
    
    # 宴席菜单管理
    def add_menu(self, name: str, dishes: Dict[str, int]) -> str:
        """添加宴席菜单"""
        menu_id = str(len(self.data["menus"]) + 1)
        self.data["menus"][menu_id] = {
            "name": name,
            "dishes": dishes
        }
        self.save_data()
        return menu_id
    
    def get_menus(self) -> Dict:
        """获取所有宴席菜单"""
        return self.data["menus"]
    
    def calculate_ingredients_for_menu(self, menu_id: str) -> Dict[str, float]:
        """计算宴席所需食材总量"""
        if menu_id not in self.data["menus"]:
            return {}
        
        menu = self.data["menus"][menu_id]
        total_ingredients = {}
        
        for dish_id, quantity in menu["dishes"].items():
            if dish_id in self.data["dishes"]:
                dish = self.data["dishes"][dish_id]
                for ingredient_id, amount in dish["ingredients"].items():
                    if ingredient_id in total_ingredients:
                        total_ingredients[ingredient_id] += amount * quantity
                    else:
                        total_ingredients[ingredient_id] = amount * quantity
        
        return total_ingredients
    
    def export_to_excel(self, filename: str):
        """导出数据到Excel"""
        try:
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                # 导出食材表
                ingredients_data = []
                for ing_id, ing_info in self.data["ingredients"].items():
                    ingredients_data.append({
                        "ID": ing_id,
                        "食材名称": ing_info["name"],
                        "单位": ing_info["unit"],
                        "单价": ing_info["price"]
                    })
                
                if ingredients_data:
                    df_ingredients = pd.DataFrame(ingredients_data)
                    df_ingredients.to_excel(writer, sheet_name="食材库", index=False)
                
                # 导出菜品表
                dishes_data = []
                for dish_id, dish_info in self.data["dishes"].items():
                    dish_name = dish_info["name"]
                    for ing_id, amount in dish_info["ingredients"].items():
                        if ing_id in self.data["ingredients"]:
                            ing_name = self.data["ingredients"][ing_id]["name"]
                            unit = self.data["ingredients"][ing_id]["unit"]
                            dishes_data.append({
                                "菜品ID": dish_id,
                                "菜品名称": dish_name,
                                "食材名称": ing_name,
                                "用量": amount,
                                "单位": unit
                            })
                
                if dishes_data:
                    df_dishes = pd.DataFrame(dishes_data)
                    df_dishes.to_excel(writer, sheet_name="菜品配方", index=False)
                
                # 导出宴席菜单表
                menus_data = []
                for menu_id, menu_info in self.data["menus"].items():
                    menu_name = menu_info["name"]
                    for dish_id, quantity in menu_info["dishes"].items():
                        if dish_id in self.data["dishes"]:
                            dish_name = self.data["dishes"][dish_id]["name"]
                            menus_data.append({
                                "宴席ID": menu_id,
                                "宴席名称": menu_name,
                                "菜品名称": dish_name,
                                "份数": quantity
                            })
                
                if menus_data:
                    df_menus = pd.DataFrame(menus_data)
                    df_menus.to_excel(writer, sheet_name="宴席菜单", index=False)
            
            return True
        except Exception as e:
            print(f"导出Excel失败: {e}")
            return False