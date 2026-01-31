import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def select_icon():
    """打开文件对话框选择图标文件."""
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.ico *.jpg *.jpeg"), ("All Files", "*.*")])
    icon_entry.delete(0, tk.END)
    icon_entry.insert(0, file_path)

def select_output_path():
    """打开文件对话框选择输出文件夹."""
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_path)

def load_config():
    """从 config.json 加载配置"""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 如果配置文件不存在，返回默认配置
        return {
            "appName": "My Web App",
            "websiteUrl": "https://www.example.com",
            "iconPath": "./icon.png",
            "outputDir": "./dist"
        }
    except Exception as e:
        messagebox.showerror("错误", f"加载配置文件失败: {e}")
        return None

def save_config(config, filepath=None):
    """保存配置到 config.json"""
    try:
        if filepath is None:
            filepath = 'config.json'  # 默认路径
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        messagebox.showerror("错误", f"保存配置文件失败: {e}")
        return False

def modify_electron_app():
    """修改预打包的 Electron 应用配置"""
    # 获取用户输入
    name = name_entry.get().strip()
    url = url_entry.get().strip()
    icon_path = icon_entry.get().strip()
    output_path = output_entry.get().strip()

    if not name or not url:
        messagebox.showerror("错误", "名称和网址不能为空!")
        return

    if not output_path:
        messagebox.showerror("错误", "输出路径不能为空!")
        return

    # 定义路径 - 在当前目录下查找 webview.exe (预构建的 Electron 应用)
    electron_exe = "webview.exe"  # 预构建的 Electron 应用

    # 检查预构建的 Electron 应用是否存在
    if not os.path.exists(electron_exe):
        messagebox.showerror("错误", f"未找到预构建的 Electron 应用 '{electron_exe}'! 请确保已下载完整的包.")
        return

    # 创建输出目录
    final_output_path = os.path.join(output_path, name)
    if not os.path.exists(final_output_path):
        os.makedirs(final_output_path)

    # 复制预构建的 Electron 应用到输出目录
    try:
        output_exe = os.path.join(final_output_path, f"{name}.exe")
        shutil.copy2(electron_exe, output_exe)
    except Exception as e:
        messagebox.showerror("错误", f"复制 Electron 应用失败: {e}")
        return

    # 创建配置文件 - 这个配置文件会被 Electron 应用读取
    config = {
        "websiteUrl": url,
        "iconPath": icon_path if icon_path else "./icon.png",
        "windowOptions": {
            "width": 1200,
            "height": 800,
            "resizable": True,
            "webPreferences": {
                "nodeIntegration": True,  # Windows 7 兼容性考虑
                "contextIsolation": False  # Windows 7 兼容性考虑
            }
        }
    }

    # 保存配置到输出目录
    config_path = os.path.join(final_output_path, "config.json")
    if not save_config(config, config_path):
        return

    # 如果提供了图标，则复制到输出目录
    if icon_path and os.path.exists(icon_path):
        try:
            output_icon_path = os.path.join(final_output_path, os.path.basename(icon_path))
            shutil.copy2(icon_path, output_icon_path)

            # 更新配置文件中的图标路径
            config["iconPath"] = os.path.basename(icon_path)
            # 重新保存配置文件以更新图标路径
            if not save_config(config, config_path):
                return
        except Exception as e:
            messagebox.showerror("错误", f"复制图标文件失败: {e}")
            return

    messagebox.showinfo("成功", f"Web 应用已成功生成! 文件位于 '{final_output_path}'.\n\n您可以直接运行 {name}.exe 来启动应用。\n\n注意：{name}.exe 会读取同目录下的 config.json 文件来加载网站。")

# 创建 Tkinter 图形界面
root = tk.Tk()
root.title("网页转exe - Electron版")

# 从配置文件加载默认值
default_config = load_config()
if default_config:
    default_name = default_config.get("appName", "")
    default_url = default_config.get("websiteUrl", "")
    default_icon = default_config.get("iconPath", "")
else:
    default_name = ""
    default_url = ""
    default_icon = ""

# 网站名称
tk.Label(root, text="应用名称:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
name_entry = tk.Entry(root, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=5)
if default_name:
    name_entry.insert(0, default_name)

# 网站网址
tk.Label(root, text="网站网址:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
url_entry = tk.Entry(root, width=40)
url_entry.grid(row=1, column=1, padx=10, pady=5)
if default_url:
    url_entry.insert(0, default_url)

# 图标路径
tk.Label(root, text="图标路径:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
icon_entry = tk.Entry(root, width=40)
icon_entry.grid(row=2, column=1, padx=10, pady=5)
if default_icon:
    icon_entry.insert(0, default_icon)
icon_button = tk.Button(root, text="选择", command=select_icon)
icon_button.grid(row=2, column=2, padx=10, pady=5)

# 输出路径
tk.Label(root, text="输出路径:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
output_entry = tk.Entry(root, width=40)
output_entry.grid(row=3, column=1, padx=10, pady=5)
output_button = tk.Button(root, text="选择", command=select_output_path)
output_button.grid(row=3, column=2, padx=10, pady=5)

# 修改按钮
modify_button = tk.Button(root, text="生成", command=modify_electron_app, bg="green", fg="white")
modify_button.grid(row=4, column=0, columnspan=3, pady=10)

# 运行 Tkinter 主循环
root.mainloop()
