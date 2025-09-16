import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from data_manager import DataManager
import os

class DishWeightGUI:
    """宴席菜品配料统计GUI主界面"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("宴席菜品配料统计系统")
        self.root.geometry("1200x800")
        
        # 初始化数据管理器
        self.data_manager = DataManager()
        
        # 创建界面
        self.create_widgets()
        self.refresh_all_data()
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # 食材管理选项卡
        self.create_ingredients_tab()
        
        # 菜品管理选项卡
        self.create_dishes_tab()
        
        # 宴席管理选项卡
        self.create_menus_tab()
        
        # 统计分析选项卡
        self.create_analysis_tab()
    
    def create_ingredients_tab(self):
        """创建食材管理选项卡"""
        ingredients_frame = ttk.Frame(self.notebook)
        self.notebook.add(ingredients_frame, text="食材管理")
        
        # 上半部分：添加/编辑食材
        input_frame = ttk.LabelFrame(ingredients_frame, text="添加/编辑食材")
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 食材名称
        ttk.Label(input_frame, text="食材名称:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ingredient_name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.ingredient_name_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        # 单位
        ttk.Label(input_frame, text="单位:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.ingredient_unit_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.ingredient_unit_var, width=10).grid(row=0, column=3, padx=5, pady=5)
        
        # 单价
        ttk.Label(input_frame, text="单价:").grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        self.ingredient_price_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.ingredient_price_var, width=10).grid(row=0, column=5, padx=5, pady=5)
        
        # 按钮
        ttk.Button(input_frame, text="添加食材", command=self.add_ingredient).grid(row=0, column=6, padx=5, pady=5)
        ttk.Button(input_frame, text="更新食材", command=self.update_ingredient).grid(row=0, column=7, padx=5, pady=5)
        ttk.Button(input_frame, text="删除食材", command=self.delete_ingredient).grid(row=0, column=8, padx=5, pady=5)
        
        # 下半部分：食材列表
        list_frame = ttk.LabelFrame(ingredients_frame, text="食材列表")
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 创建表格
        columns = ("ID", "食材名称", "单位", "单价")
        self.ingredients_tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.ingredients_tree.heading(col, text=col)
            self.ingredients_tree.column(col, width=100)
        
        # 滚动条
        scrollbar_ing = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.ingredients_tree.yview)
        self.ingredients_tree.configure(yscrollcommand=scrollbar_ing.set)
        
        self.ingredients_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_ing.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 绑定选择事件
        self.ingredients_tree.bind("<<TreeviewSelect>>", self.on_ingredient_select)
        
        self.selected_ingredient_id = None
    
    def create_dishes_tab(self):
        """创建菜品管理选项卡"""
        dishes_frame = ttk.Frame(self.notebook)
        self.notebook.add(dishes_frame, text="菜品管理")
        
        # 左侧：菜品列表
        left_frame = ttk.LabelFrame(dishes_frame, text="菜品列表")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 菜品列表（带滚动条）
        listbox_frame = ttk.Frame(left_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.dishes_listbox = tk.Listbox(listbox_frame, height=20)
        dishes_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.dishes_listbox.yview)
        self.dishes_listbox.configure(yscrollcommand=dishes_scrollbar.set)
        
        self.dishes_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        dishes_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.dishes_listbox.bind("<<ListboxSelect>>", self.on_dish_select)
        
        # 菜品操作按钮
        dish_btn_frame = ttk.Frame(left_frame)
        dish_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(dish_btn_frame, text="新建菜品", command=self.new_dish).pack(side=tk.LEFT, padx=2)
        ttk.Button(dish_btn_frame, text="保存菜品", command=self.save_dish).pack(side=tk.LEFT, padx=2)
        ttk.Button(dish_btn_frame, text="删除菜品", command=self.delete_dish).pack(side=tk.LEFT, padx=2)
        
        # 右侧：菜品详情
        right_frame = ttk.LabelFrame(dishes_frame, text="菜品详情")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 菜品名称
        name_frame = ttk.Frame(right_frame)
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(name_frame, text="菜品名称:").pack(side=tk.LEFT)
        self.dish_name_var = tk.StringVar()
        ttk.Entry(name_frame, textvariable=self.dish_name_var, width=30).pack(side=tk.LEFT, padx=5)
        
        # 配料表格
        ttk.Label(right_frame, text="配料清单:").pack(anchor=tk.W, padx=5, pady=(10, 0))
        
        # 配料输入框架
        ingredient_input_frame = ttk.Frame(right_frame)
        ingredient_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 食材选择下拉框
        ttk.Label(ingredient_input_frame, text="选择食材:").grid(row=0, column=0, padx=2, pady=2)
        self.dish_ingredient_var = tk.StringVar()
        self.dish_ingredient_combo = ttk.Combobox(ingredient_input_frame, textvariable=self.dish_ingredient_var, width=15)
        self.dish_ingredient_combo.grid(row=0, column=1, padx=2, pady=2)
        
        # 绑定输入事件以支持模糊搜索
        self.dish_ingredient_combo.bind('<KeyRelease>', self.on_ingredient_search)
        self.dish_ingredient_combo.bind('<Button-1>', self.on_ingredient_combo_click)
        self.dish_ingredient_combo.bind('<<ComboboxSelected>>', self.on_ingredient_selected)
        
        # 用量输入
        ttk.Label(ingredient_input_frame, text="用量:").grid(row=0, column=2, padx=2, pady=2)
        self.dish_amount_var = tk.StringVar()
        ttk.Entry(ingredient_input_frame, textvariable=self.dish_amount_var, width=10).grid(row=0, column=3, padx=2, pady=2)
        
        # 添加配料按钮
        ttk.Button(ingredient_input_frame, text="添加配料", command=self.add_dish_ingredient).grid(row=0, column=4, padx=2, pady=2)
        ttk.Button(ingredient_input_frame, text="删除配料", command=self.remove_dish_ingredient).grid(row=0, column=5, padx=2, pady=2)
        
        # 配料列表
        dish_ing_columns = ("食材名称", "用量", "单位")
        self.dish_ingredients_tree = ttk.Treeview(right_frame, columns=dish_ing_columns, show="headings", height=12)
        
        for col in dish_ing_columns:
            self.dish_ingredients_tree.heading(col, text=col)
            self.dish_ingredients_tree.column(col, width=100)
        
        self.dish_ingredients_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.selected_dish_id = None
        self.current_dish_ingredients = {}
    
    def create_menus_tab(self):
        """创建宴席管理选项卡"""
        menus_frame = ttk.Frame(self.notebook)
        self.notebook.add(menus_frame, text="宴席管理")
        
        # 左侧：宴席列表
        left_frame = ttk.LabelFrame(menus_frame, text="宴席列表")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 宴席列表（带滚动条）
        menu_listbox_frame = ttk.Frame(left_frame)
        menu_listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.menus_listbox = tk.Listbox(menu_listbox_frame, height=20)
        menu_scrollbar = ttk.Scrollbar(menu_listbox_frame, orient=tk.VERTICAL, command=self.menus_listbox.yview)
        self.menus_listbox.configure(yscrollcommand=menu_scrollbar.set)
        
        self.menus_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        menu_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.menus_listbox.bind("<<ListboxSelect>>", self.on_menu_select)
        
        # 宴席操作按钮
        menu_btn_frame = ttk.Frame(left_frame)
        menu_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(menu_btn_frame, text="新建宴席", command=self.new_menu).pack(side=tk.LEFT, padx=2)
        ttk.Button(menu_btn_frame, text="保存宴席", command=self.save_menu).pack(side=tk.LEFT, padx=2)
        ttk.Button(menu_btn_frame, text="删除宴席", command=self.delete_menu).pack(side=tk.LEFT, padx=2)
        
        # 右侧：宴席详情
        right_frame = ttk.LabelFrame(menus_frame, text="宴席详情")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 宴席名称
        name_frame = ttk.Frame(right_frame)
        name_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(name_frame, text="宴席名称:").pack(side=tk.LEFT)
        self.menu_name_var = tk.StringVar()
        ttk.Entry(name_frame, textvariable=self.menu_name_var, width=30).pack(side=tk.LEFT, padx=5)
        
        # 餐桌数量
        table_frame = ttk.Frame(right_frame)
        table_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(table_frame, text="餐桌数量:").pack(side=tk.LEFT)
        self.menu_table_count_var = tk.StringVar(value="1")
        ttk.Entry(table_frame, textvariable=self.menu_table_count_var, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Label(table_frame, text="桌").pack(side=tk.LEFT)
        
        # 菜品添加框架
        dish_input_frame = ttk.Frame(right_frame)
        dish_input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(dish_input_frame, text="选择菜品:").grid(row=0, column=0, padx=2, pady=2)
        self.menu_dish_var = tk.StringVar()
        self.menu_dish_combo = ttk.Combobox(dish_input_frame, textvariable=self.menu_dish_var, width=15)
        self.menu_dish_combo.grid(row=0, column=1, padx=2, pady=2)
        
        # 绑定菜品搜索和选择事件
        self.menu_dish_combo.bind('<KeyRelease>', self.on_dish_search)
        self.menu_dish_combo.bind('<Button-1>', self.on_dish_combo_click)
        self.menu_dish_combo.bind('<<ComboboxSelected>>', self.on_dish_selected)
        
        ttk.Label(dish_input_frame, text="份数:").grid(row=0, column=2, padx=2, pady=2)
        self.menu_quantity_var = tk.StringVar()
        ttk.Entry(dish_input_frame, textvariable=self.menu_quantity_var, width=10).grid(row=0, column=3, padx=2, pady=2)
        
        ttk.Button(dish_input_frame, text="添加菜品", command=self.add_menu_dish).grid(row=0, column=4, padx=2, pady=2)
        ttk.Button(dish_input_frame, text="删除菜品", command=self.remove_menu_dish).grid(row=0, column=5, padx=2, pady=2)
        
        # 菜品列表
        menu_dish_columns = ("菜品名称", "份数")
        self.menu_dishes_tree = ttk.Treeview(right_frame, columns=menu_dish_columns, show="headings", height=12)
        
        for col in menu_dish_columns:
            self.menu_dishes_tree.heading(col, text=col)
            self.menu_dishes_tree.column(col, width=150)
        
        self.menu_dishes_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.selected_menu_id = None
        self.current_menu_dishes = {}
    
    def create_analysis_tab(self):
        """创建统计分析选项卡"""
        analysis_frame = ttk.Frame(self.notebook)
        self.notebook.add(analysis_frame, text="统计分析")
        
        # 上半部分：宴席选择和计算
        control_frame = ttk.LabelFrame(analysis_frame, text="宴席食材统计")
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 宴席选择
        select_frame = ttk.Frame(control_frame)
        select_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(select_frame, text="选择宴席:").pack(side=tk.LEFT)
        self.analysis_menu_var = tk.StringVar()
        self.analysis_menu_combo = ttk.Combobox(select_frame, textvariable=self.analysis_menu_var, width=20)
        self.analysis_menu_combo.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(select_frame, text="计算食材用量", command=self.calculate_ingredients).pack(side=tk.LEFT, padx=5)
        ttk.Button(select_frame, text="导出食材统计", command=self.export_menu_statistics).pack(side=tk.LEFT, padx=5)
        
        # 数据管理框架
        data_mgmt_frame = ttk.LabelFrame(analysis_frame, text="数据管理")
        data_mgmt_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 数据文件信息
        info_frame = ttk.Frame(data_mgmt_frame)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(info_frame, text="数据文件路径:").pack(side=tk.LEFT)
        self.data_path_var = tk.StringVar()
        data_path_entry = ttk.Entry(info_frame, textvariable=self.data_path_var, state="readonly", width=50)
        data_path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 数据管理按钮
        mgmt_btn_frame = ttk.Frame(data_mgmt_frame)
        mgmt_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(mgmt_btn_frame, text="刷新数据", command=self.refresh_all_data).pack(side=tk.LEFT, padx=2)
        ttk.Button(mgmt_btn_frame, text="查看数据信息", command=self.show_data_info).pack(side=tk.LEFT, padx=2)
        
        # 下半部分：统计结果
        result_frame = ttk.LabelFrame(analysis_frame, text="食材用量统计")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 统计结果表格
        result_columns = ("食材名称", "总用量", "单位", "单价", "总价")
        self.result_tree = ttk.Treeview(result_frame, columns=result_columns, show="headings", height=15)
        
        for col in result_columns:
            self.result_tree.heading(col, text=col)
            self.result_tree.column(col, width=120)
        
        # 滚动条
        scrollbar_result = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar_result.set)
        
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_result.pack(side=tk.RIGHT, fill=tk.Y)
    
    # 食材管理相关方法
    def add_ingredient(self):
        """添加食材"""
        name = self.ingredient_name_var.get().strip()
        unit = self.ingredient_unit_var.get().strip()
        price_str = self.ingredient_price_var.get().strip()
        
        if not name or not unit:
            messagebox.showerror("错误", "请填写食材名称和单位")
            return
        
        try:
            price = float(price_str) if price_str else 0.0
        except ValueError:
            messagebox.showerror("错误", "单价必须是数字")
            return
        
        self.data_manager.add_ingredient(name, unit, price)
        self.refresh_ingredients()
        self.clear_ingredient_inputs()
        messagebox.showinfo("成功", "食材添加成功")
    
    def update_ingredient(self):
        """更新食材"""
        if not self.selected_ingredient_id:
            messagebox.showerror("错误", "请先选择要更新的食材")
            return
        
        name = self.ingredient_name_var.get().strip()
        unit = self.ingredient_unit_var.get().strip()
        price_str = self.ingredient_price_var.get().strip()
        
        if not name or not unit:
            messagebox.showerror("错误", "请填写食材名称和单位")
            return
        
        try:
            price = float(price_str) if price_str else 0.0
        except ValueError:
            messagebox.showerror("错误", "单价必须是数字")
            return
        
        self.data_manager.update_ingredient(self.selected_ingredient_id, name, unit, price)
        self.refresh_ingredients()
        self.clear_ingredient_inputs()
        messagebox.showinfo("成功", "食材更新成功")
    
    def delete_ingredient(self):
        """删除食材"""
        if not self.selected_ingredient_id:
            messagebox.showerror("错误", "请先选择要删除的食材")
            return
        
        # 获取要删除的食材信息
        ingredients = self.data_manager.get_ingredients()
        if self.selected_ingredient_id not in ingredients:
            messagebox.showerror("错误", "选择的食材不存在")
            return
        
        ingredient_name = ingredients[self.selected_ingredient_id]["name"]
        
        if messagebox.askyesno("确认", f"确定要删除食材 '{ingredient_name}' 吗？\n\n注意：如果有菜品正在使用此食材，将无法删除。"):
            # 尝试删除食材
            success = self.data_manager.delete_ingredient(self.selected_ingredient_id)
            
            if success:
                self.refresh_ingredients()
                self.clear_ingredient_inputs()
                messagebox.showinfo("成功", f"食材 '{ingredient_name}' 删除成功")
            else:
                # 检查具体失败原因
                used_in_dishes = []
                dishes = self.data_manager.get_dishes()
                for dish_id, dish_info in dishes.items():
                    if self.selected_ingredient_id in dish_info["ingredients"]:
                        used_in_dishes.append(dish_info["name"])
                
                if used_in_dishes:
                    messagebox.showerror("删除失败", 
                                       f"无法删除食材 '{ingredient_name}'\n\n" +
                                       f"该食材正被以下菜品使用：\n" +
                                       "\n".join([f"• {dish}" for dish in used_in_dishes]) +
                                       "\n\n请先从相关菜品中移除此食材，然后再尝试删除。")
                else:
                    messagebox.showerror("删除失败", f"删除食材 '{ingredient_name}' 时发生未知错误")
    
    def on_ingredient_select(self, event):
        """食材选择事件"""
        selection = self.ingredients_tree.selection()
        if selection:
            item = self.ingredients_tree.item(selection[0])
            values = item['values']
            
            # 确保ID是字符串类型
            self.selected_ingredient_id = str(values[0])
            
            # 填充输入框
            self.ingredient_name_var.set(values[1])
            self.ingredient_unit_var.set(values[2])
            self.ingredient_price_var.set(values[3])
    
    def clear_ingredient_inputs(self):
        """清空食材输入框"""
        self.ingredient_name_var.set("")
        self.ingredient_unit_var.set("")
        self.ingredient_price_var.set("")
        self.selected_ingredient_id = None
    
    def refresh_ingredients(self):
        """刷新食材列表"""
        # 清空表格
        for item in self.ingredients_tree.get_children():
            self.ingredients_tree.delete(item)
        
        # 重新加载数据
        ingredients = self.data_manager.get_ingredients()
        for ing_id, ing_info in ingredients.items():
            self.ingredients_tree.insert("", tk.END, values=(
                ing_id, ing_info["name"], ing_info["unit"], ing_info["price"]
            ))
        
        # 更新下拉框
        self.update_ingredient_combos()
    
    def update_ingredient_combos(self):
        """更新食材下拉框"""
        ingredients = self.data_manager.get_ingredients()
        # 存储食材名称到ID的映射
        self.ingredient_name_to_id = {}
        ingredient_names = []
        
        for ing_id, ing_info in ingredients.items():
            name = ing_info['name']
            display_name = f"{name} ({ing_id})"
            ingredient_names.append(display_name)
            # 同时支持纯名称和带ID的格式查找
            self.ingredient_name_to_id[name] = ing_id
            self.ingredient_name_to_id[display_name] = ing_id
        
        self.all_ingredient_names = ingredient_names
        self.dish_ingredient_combo['values'] = ingredient_names
    
    def on_ingredient_search(self, event):
        """食材搜索事件处理"""
        # 在中文等输入法组合输入阶段（Windows 常见为 keycode 229 / VK_PROCESSKEY）不更新/弹出，避免覆盖候选上屏
        if hasattr(event, 'keycode') and event.keycode == 229:
            return
        
        search_text = self.dish_ingredient_var.get().lower()
        if not hasattr(self, 'all_ingredient_names'):
            return
        
        if search_text == "":
            # 如果搜索框为空，显示所有食材
            self.dish_ingredient_combo['values'] = self.all_ingredient_names
        else:
            # 模糊搜索匹配
            filtered_names = [name for name in self.all_ingredient_names 
                            if search_text in name.lower()]
            self.dish_ingredient_combo['values'] = filtered_names
        
        # 安全地在非输入法组合阶段、且内容有变更时弹出下拉，避免干扰上屏
        try:
            keysym = getattr(event, 'keysym', '')
            keycode = getattr(event, 'keycode', None)
            if keycode != 229 and search_text is not None and search_text != "":
                # 避免方向键/功能键触发
                if keysym not in ('Up','Down','Left','Right','Return','Escape','Tab','Shift_L','Shift_R','Control_L','Control_R','Alt_L','Alt_R'):
                    self.root.after(60, self._popup_ingredient_dropdown)
        except Exception:
            pass
    
    def _popup_ingredient_dropdown(self):
        """安全地弹出食材下拉框"""
        try:
            if self.dish_ingredient_combo.winfo_exists():
                self.dish_ingredient_combo.event_generate('<Down>')
        except Exception:
            pass
    
    def on_ingredient_combo_click(self, event):
        """食材下拉框点击事件"""
        # 点击时显示所有食材
        if hasattr(self, 'all_ingredient_names'):
            self.dish_ingredient_combo['values'] = self.all_ingredient_names
    
    def on_ingredient_selected(self, event):
        """食材选择事件处理"""
        # 当用户从下拉列表中选择食材时，将选中的食材填充到文本框
        selected_value = self.dish_ingredient_combo.get()
        if selected_value:
            self.dish_ingredient_var.set(selected_value)
    
    def on_dish_search(self, event):
        """菜品搜索事件处理"""
        # 在中文等输入法组合输入阶段（Windows 常见为 keycode 229 / VK_PROCESSKEY）不更新/弹出，避免覆盖候选上屏
        if hasattr(event, 'keycode') and event.keycode == 229:
            return
        
        search_text = self.menu_dish_var.get().lower()
        if not hasattr(self, 'all_dish_names'):
            return
        
        if search_text == "":
            # 如果搜索框为空，显示所有菜品
            self.menu_dish_combo['values'] = self.all_dish_names
        else:
            # 模糊搜索匹配
            filtered_names = [name for name in self.all_dish_names 
                            if search_text in name.lower()]
            self.menu_dish_combo['values'] = filtered_names
        
        # 安全地在非输入法组合阶段、且内容有变更时弹出下拉，避免干扰上屏
        try:
            keysym = getattr(event, 'keysym', '')
            keycode = getattr(event, 'keycode', None)
            if keycode != 229 and search_text is not None and search_text != "":
                # 避免方向键/功能键触发
                if keysym not in ('Up','Down','Left','Right','Return','Escape','Tab','Shift_L','Shift_R','Control_L','Control_R','Alt_L','Alt_R'):
                    self.root.after(60, self._popup_dish_dropdown)
        except Exception:
            pass
    
    def _popup_dish_dropdown(self):
        """安全地弹出菜品下拉框"""
        try:
            if self.menu_dish_combo.winfo_exists():
                self.menu_dish_combo.event_generate('<Down>')
        except Exception:
            pass
    
    def on_dish_combo_click(self, event):
        """菜品下拉框点击事件"""
        # 点击时显示所有菜品
        if hasattr(self, 'all_dish_names'):
            self.menu_dish_combo['values'] = self.all_dish_names
    
    def on_dish_selected(self, event):
        """菜品选择事件处理"""
        # 当用户从下拉列表中选择菜品时，将选中的菜品填充到文本框
        selected_value = self.menu_dish_combo.get()
        if selected_value:
            self.menu_dish_var.set(selected_value)
    
    # 菜品管理相关方法
    def new_dish(self):
        """新建菜品"""
        self.selected_dish_id = None
        self.dish_name_var.set("")
        self.current_dish_ingredients = {}
        self.refresh_dish_ingredients_tree()
    
    def save_dish(self):
        """保存菜品"""
        name = self.dish_name_var.get().strip()
        if not name:
            messagebox.showerror("错误", "请填写菜品名称")
            return
        
        if not self.current_dish_ingredients:
            messagebox.showerror("错误", "请至少添加一种配料")
            return
        
        if self.selected_dish_id:
            # 更新现有菜品
            self.data_manager.update_dish(self.selected_dish_id, name, self.current_dish_ingredients)
            messagebox.showinfo("成功", "菜品更新成功")
        else:
            # 添加新菜品
            self.data_manager.add_dish(name, self.current_dish_ingredients)
            messagebox.showinfo("成功", "菜品添加成功")
        
        self.refresh_dishes()
    
    def delete_dish(self):
        """删除菜品"""
        if not self.selected_dish_id:
            messagebox.showerror("错误", "请先选择要删除的菜品")
            return
        
        if messagebox.askyesno("确认", "确定要删除这个菜品吗？"):
            self.data_manager.delete_dish(self.selected_dish_id)
            self.refresh_dishes()
            self.new_dish()
            messagebox.showinfo("成功", "菜品删除成功")
    
    def add_dish_ingredient(self):
        """添加菜品配料"""
        ingredient_text = self.dish_ingredient_var.get().strip()
        amount_str = self.dish_amount_var.get().strip()
        
        if not ingredient_text or not amount_str:
            messagebox.showerror("错误", "请选择食材并填写用量")
            return
        
        try:
            amount = float(amount_str)
        except ValueError:
            messagebox.showerror("错误", "用量必须是数字")
            return
        
        # 解析食材ID - 支持多种输入方式
        ingredient_id = None
        
        # 首先检查是否在映射表中
        if hasattr(self, 'ingredient_name_to_id') and ingredient_text in self.ingredient_name_to_id:
            ingredient_id = self.ingredient_name_to_id[ingredient_text]
        # 如果不在映射表中，尝试传统的解析方式
        elif "(" in ingredient_text and ")" in ingredient_text:
            ingredient_id = ingredient_text.split("(")[-1].split(")")[0]
        # 如果都不匹配，尝试按纯名称查找
        else:
            ingredients = self.data_manager.get_ingredients()
            for ing_id, ing_info in ingredients.items():
                if ing_info['name'].lower() == ingredient_text.lower():
                    ingredient_id = ing_id
                    break
        
        if not ingredient_id:
            messagebox.showerror("错误", "请选择有效的食材")
            return
        
        self.current_dish_ingredients[ingredient_id] = amount
        self.refresh_dish_ingredients_tree()
        
        # 清空输入
        self.dish_ingredient_var.set("")
        self.dish_amount_var.set("")
    
    def remove_dish_ingredient(self):
        """删除菜品配料"""
        selection = self.dish_ingredients_tree.selection()
        if not selection:
            messagebox.showerror("错误", "请先选择要删除的配料")
            return
        
        item = self.dish_ingredients_tree.item(selection[0])
        ingredient_name = item['values'][0]
        
        # 找到对应的食材ID
        ingredients = self.data_manager.get_ingredients()
        ingredient_id = None
        for ing_id, ing_info in ingredients.items():
            if ing_info["name"] == ingredient_name:
                ingredient_id = ing_id
                break
        
        if ingredient_id and ingredient_id in self.current_dish_ingredients:
            del self.current_dish_ingredients[ingredient_id]
            self.refresh_dish_ingredients_tree()
    
    def on_dish_select(self, event):
        """菜品选择事件"""
        selection = self.dishes_listbox.curselection()
        if selection:
            dish_text = self.dishes_listbox.get(selection[0])
            # 解析菜品ID
            if "(" in dish_text and ")" in dish_text:
                self.selected_dish_id = dish_text.split("(")[-1].split(")")[0]
                
                # 加载菜品信息
                dishes = self.data_manager.get_dishes()
                if self.selected_dish_id in dishes:
                    dish_info = dishes[self.selected_dish_id]
                    self.dish_name_var.set(dish_info["name"])
                    self.current_dish_ingredients = dish_info["ingredients"].copy()
                    self.refresh_dish_ingredients_tree()
    
    def refresh_dishes(self):
        """刷新菜品列表"""
        self.dishes_listbox.delete(0, tk.END)
        
        dishes = self.data_manager.get_dishes()
        for dish_id, dish_info in dishes.items():
            self.dishes_listbox.insert(tk.END, f"{dish_info['name']} ({dish_id})")
        
        # 更新下拉框
        self.update_dish_combos()
    
    def update_dish_combos(self):
        """更新菜品下拉框"""
        dishes = self.data_manager.get_dishes()
        dish_names = [f"{dish_info['name']} ({dish_id})" for dish_id, dish_info in dishes.items()]
        
        # 存储所有菜品名称用于搜索
        self.all_dish_names = dish_names
        self.menu_dish_combo['values'] = dish_names
        self.analysis_menu_combo['values'] = []  # 这里应该是宴席列表，稍后更新
    
    def refresh_dish_ingredients_tree(self):
        """刷新菜品配料表格"""
        # 清空表格
        for item in self.dish_ingredients_tree.get_children():
            self.dish_ingredients_tree.delete(item)
        
        # 重新加载数据
        ingredients = self.data_manager.get_ingredients()
        for ing_id, amount in self.current_dish_ingredients.items():
            if ing_id in ingredients:
                ing_info = ingredients[ing_id]
                self.dish_ingredients_tree.insert("", tk.END, values=(
                    ing_info["name"], amount, ing_info["unit"]
                ))
    
    # 宴席管理相关方法
    def new_menu(self):
        """新建宴席"""
        self.selected_menu_id = None
        self.menu_name_var.set("")
        self.menu_table_count_var.set("1")
        self.current_menu_dishes = {}
        self.refresh_menu_dishes_tree()
    
    def save_menu(self):
        """保存宴席"""
        name = self.menu_name_var.get().strip()
        table_count_str = self.menu_table_count_var.get().strip()
        
        if not name:
            messagebox.showerror("错误", "请填写宴席名称")
            return
        
        if not self.current_menu_dishes:
            messagebox.showerror("错误", "请至少添加一道菜品")
            return
        
        try:
            table_count = int(table_count_str) if table_count_str else 1
            if table_count <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("错误", "餐桌数量必须是正整数")
            return
        
        if self.selected_menu_id:
            # 更新现有宴席
            self.data_manager.update_menu(self.selected_menu_id, name, self.current_menu_dishes, table_count)
            messagebox.showinfo("成功", "宴席更新成功")
        else:
            # 添加新宴席
            self.data_manager.add_menu(name, self.current_menu_dishes, table_count)
            messagebox.showinfo("成功", "宴席添加成功")
        
        self.refresh_menus()
    
    def delete_menu(self):
        """删除宴席"""
        if not self.selected_menu_id:
            messagebox.showerror("错误", "请先选择要删除的宴席")
            return
        
        if messagebox.askyesno("确认", "确定要删除这个宴席吗？"):
            if self.selected_menu_id in self.data_manager.data["menus"]:
                del self.data_manager.data["menus"][self.selected_menu_id]
                self.data_manager.save_data()
            self.refresh_menus()
            self.new_menu()
            messagebox.showinfo("成功", "宴席删除成功")
    
    def add_menu_dish(self):
        """添加宴席菜品"""
        dish_text = self.menu_dish_var.get().strip()
        quantity_str = self.menu_quantity_var.get().strip()
        
        if not dish_text or not quantity_str:
            messagebox.showerror("错误", "请选择菜品并填写份数")
            return
        
        try:
            quantity = int(quantity_str)
        except ValueError:
            messagebox.showerror("错误", "份数必须是整数")
            return
        
        # 解析菜品ID
        if "(" in dish_text and ")" in dish_text:
            dish_id = dish_text.split("(")[-1].split(")")[0]
        else:
            messagebox.showerror("错误", "请选择有效的菜品")
            return
        
        self.current_menu_dishes[dish_id] = quantity
        self.refresh_menu_dishes_tree()
        
        # 清空输入
        self.menu_dish_var.set("")
        self.menu_quantity_var.set("")
    
    def remove_menu_dish(self):
        """删除宴席菜品"""
        selection = self.menu_dishes_tree.selection()
        if not selection:
            messagebox.showerror("错误", "请先选择要删除的菜品")
            return
        
        item = self.menu_dishes_tree.item(selection[0])
        dish_name = item['values'][0]
        
        # 找到对应的菜品ID
        dishes = self.data_manager.get_dishes()
        dish_id = None
        for d_id, d_info in dishes.items():
            if d_info["name"] == dish_name:
                dish_id = d_id
                break
        
        if dish_id and dish_id in self.current_menu_dishes:
            del self.current_menu_dishes[dish_id]
            self.refresh_menu_dishes_tree()
    
    def on_menu_select(self, event):
        """宴席选择事件"""
        selection = self.menus_listbox.curselection()
        if selection:
            menu_text = self.menus_listbox.get(selection[0])
            # 解析宴席ID
            if "(" in menu_text and ")" in menu_text:
                self.selected_menu_id = menu_text.split("(")[-1].split(")")[0]
                
                # 加载宴席信息
                menus = self.data_manager.get_menus()
                if self.selected_menu_id in menus:
                    menu_info = menus[self.selected_menu_id]
                    self.menu_name_var.set(menu_info["name"])
                    self.current_menu_dishes = menu_info["dishes"].copy()
                    # 加载餐桌数量，如果没有则默认为1
                    table_count = menu_info.get("table_count", 1)
                    self.menu_table_count_var.set(str(table_count))
                    self.refresh_menu_dishes_tree()
    
    def refresh_menus(self):
        """刷新宴席列表"""
        self.menus_listbox.delete(0, tk.END)
        
        menus = self.data_manager.get_menus()
        for menu_id, menu_info in menus.items():
            self.menus_listbox.insert(tk.END, f"{menu_info['name']} ({menu_id})")
        
        # 更新分析页面的宴席下拉框
        menu_names = [f"{menu_info['name']} ({menu_id})" for menu_id, menu_info in menus.items()]
        self.analysis_menu_combo['values'] = menu_names
    
    def refresh_menu_dishes_tree(self):
        """刷新宴席菜品表格"""
        # 清空表格
        for item in self.menu_dishes_tree.get_children():
            self.menu_dishes_tree.delete(item)
        
        # 重新加载数据
        dishes = self.data_manager.get_dishes()
        for dish_id, quantity in self.current_menu_dishes.items():
            if dish_id in dishes:
                dish_info = dishes[dish_id]
                self.menu_dishes_tree.insert("", tk.END, values=(
                    dish_info["name"], quantity
                ))
    
    # 统计分析相关方法
    def calculate_ingredients(self):
        """计算宴席食材用量"""
        menu_text = self.analysis_menu_var.get().strip()
        if not menu_text:
            messagebox.showerror("错误", "请选择宴席")
            return
        
        # 解析宴席ID
        if "(" in menu_text and ")" in menu_text:
            menu_id = menu_text.split("(")[-1].split(")")[0]
        else:
            messagebox.showerror("错误", "请选择有效的宴席")
            return
        
        # 计算食材用量
        total_ingredients = self.data_manager.calculate_ingredients_for_menu(menu_id)
        
        # 清空结果表格
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)
        
        # 显示结果
        ingredients = self.data_manager.get_ingredients()
        total_cost = 0
        
        for ing_id, amount in total_ingredients.items():
            if ing_id in ingredients:
                ing_info = ingredients[ing_id]
                cost = amount * ing_info["price"]
                total_cost += cost
                
                self.result_tree.insert("", tk.END, values=(
                    ing_info["name"], 
                    f"{amount:.2f}", 
                    ing_info["unit"], 
                    f"¥{ing_info['price']:.2f}", 
                    f"¥{cost:.2f}"
                ))
        
        # 添加总计行 - 使用不同的标签来突出显示
        self.result_tree.insert("", tk.END, values=(
            "==== 总计 ====", "", "", "", f"¥{total_cost:.2f}"
        ), tags=('total',))
        
        # 配置总计行样式
        self.result_tree.tag_configure('total', background='lightblue', font=('Arial', 10, 'bold'))
    
    def export_menu_statistics(self):
        """导出当前宴席的食材统计到Excel"""
        menu_text = self.analysis_menu_var.get().strip()
        if not menu_text:
            messagebox.showerror("错误", "请先选择宴席并计算食材用量")
            return
        
        # 解析宴席ID和名称
        if "(" in menu_text and ")" in menu_text:
            menu_id = menu_text.split("(")[-1].split(")")[0]
            menu_name = menu_text.split("(")[0].strip()
        else:
            messagebox.showerror("错误", "请选择有效的宴席")
            return
        
        from datetime import datetime
        
        # 自动生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_menu_name = "".join(c for c in menu_name if c.isalnum() or c in (' ', '-', '_')).strip()
        default_filename = f"宴席食材统计_{safe_menu_name}_{timestamp}.xlsx"
        
        filename = filedialog.asksaveasfilename(
            initialfile=default_filename,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="保存宴席食材统计"
        )
        
        if filename:
            # 确保文件名以.xlsx结尾
            if not filename.lower().endswith('.xlsx'):
                filename += '.xlsx'
                
            if self.data_manager.export_menu_statistics(menu_id, menu_name, filename):
                messagebox.showinfo("成功", f"宴席食材统计已导出到 {filename}")
            else:
                messagebox.showerror("错误", "导出失败")
    
    def show_data_info(self):
        """显示数据信息"""
        try:
            data_path = self.data_manager.get_data_file_path()
            ingredients_count = len(self.data_manager.get_ingredients())
            dishes_count = len(self.data_manager.get_dishes())
            menus_count = len(self.data_manager.get_menus())
            
            import os
            file_size = 0
            if os.path.exists(data_path):
                file_size = os.path.getsize(data_path)
            
            info_text = f"""数据文件信息：
            
文件路径：{data_path}
文件大小：{file_size} 字节
            
数据统计：
• 食材数量：{ingredients_count} 个
• 菜品数量：{dishes_count} 个  
• 宴席数量：{menus_count} 个

数据版本：{self.data_manager.data.get('version', '1.0')}
最后更新：{self.data_manager.data.get('last_modified', '未知')}"""
            
            messagebox.showinfo("数据信息", info_text)
            
        except Exception as e:
            messagebox.showerror("错误", f"获取数据信息失败：{str(e)}")
    
    def update_data_path_display(self):
        """更新数据文件路径显示"""
        try:
            data_path = self.data_manager.get_data_file_path()
            self.data_path_var.set(data_path)
        except Exception as e:
            self.data_path_var.set(f"获取路径失败：{str(e)}")
    
    def refresh_all_data(self):
        """刷新所有数据"""
        self.refresh_ingredients()
        self.refresh_dishes()
        self.refresh_menus()
        self.update_data_path_display()
    
    def run(self):
        """运行程序"""
        # 初始化时更新数据路径显示
        self.update_data_path_display()
        self.root.mainloop()

if __name__ == "__main__":
    app = DishWeightGUI()
    app.run()