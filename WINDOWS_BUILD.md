# Windows Build Guide

## 系统要求 / System Requirements

- Windows 10 或更高版本 / Windows 10 or higher
- Python 3.8+ 已安装 / Python 3.8+ installed
- 至少 2GB 可用磁盘空间 / At least 2GB free disk space

## 构建方法 / Build Methods

### 方法一：使用批处理文件 / Method 1: Using Batch File

1. 双击运行 `build_windows.bat`
2. 等待构建完成
3. 可执行文件将生成在 `dist/DishWeight/` 目录下

### 方法二：使用Python脚本 / Method 2: Using Python Script

```bash
python build_windows.py
```

### 方法三：直接使用PyInstaller / Method 3: Direct PyInstaller

```bash
# 安装PyInstaller / Install PyInstaller
pip install pyinstaller

# 使用spec文件构建 / Build using spec file
pyinstaller build_windows.spec

# 或者直接构建 / Or build directly
pyinstaller --onedir --windowed --name="DishWeight" ^
    --exclude-module=PyQt5 ^
    --exclude-module=PySide6 ^
    --exclude-module=matplotlib ^
    --add-data="README.md;." ^
    --add-data="USAGE.md;." ^
    main.py
```

## 常见问题解决 / Troubleshooting

### 问题1：PyInstaller安装失败
**解决方案：**
```bash
# 升级pip
python -m pip install --upgrade pip

# 重新安装PyInstaller
pip install pyinstaller
```

### 问题2：构建过程中出现模块冲突
**解决方案：**
- 使用提供的 `build_windows.spec` 文件，已排除冲突模块
- 或手动添加 `--exclude-module` 参数

### 问题3：生成的EXE文件无法运行
**解决方案：**
1. 检查是否安装了所有依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 尝试在命令行中运行以查看错误信息：
   ```bash
   dist\DishWeight\DishWeight.exe
   ```

### 问题4：缺少数据文件
**解决方案：**
- 确保 `README.md` 和 `USAGE.md` 文件存在于项目根目录
- 构建脚本会自动复制这些文件到输出目录

## 输出文件说明 / Output Files

构建成功后，`dist/DishWeight/` 目录包含：

- `DishWeight.exe` - 主程序可执行文件
- `_internal/` - 程序依赖文件目录
- `README.md` - 项目说明文档
- `USAGE.md` - 用户使用手册
- `Usage Instructions.txt` - 快速使用说明

## 分发说明 / Distribution Notes

要分发程序给其他用户：

1. 将整个 `dist/DishWeight/` 目录复制给用户
2. 用户只需双击 `DishWeight.exe` 即可运行
3. 确保用户的Windows系统满足最低要求
4. 程序会在首次运行时自动创建 `dish_data.json` 数据文件

## 技术支持 / Technical Support

如遇到其他问题，请：
1. 检查Python和依赖包版本
2. 查看构建过程中的错误信息
3. 参考项目文档中的故障排除部分