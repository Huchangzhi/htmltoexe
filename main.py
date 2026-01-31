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

def save_config(config):
    """保存配置到 config.json"""
    try:
        with open('config.json', 'w', encoding='utf-8') as f:
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

    # 定义路径
    electron_template_dir = "electron-template"  # 预打包的 Electron 应用模板
    modified_app_dir = "my-electron-app"  # 修改后的应用目录

    # 检查 Electron 模板是否存在
    if not os.path.exists(electron_template_dir):
        messagebox.showerror("错误", f"未找到 Electron 模板文件夹 '{electron_template_dir}'! 请确保已下载预打包的 Electron 框架.")
        return

    # 创建修改后的应用目录
    try:
        if os.path.exists(modified_app_dir):
            shutil.rmtree(modified_app_dir)  # 如果已存在,删除它
        shutil.copytree(electron_template_dir, modified_app_dir)
    except Exception as e:
        messagebox.showerror("错误", f"复制 Electron 模板失败: {e}")
        return

    # 更新配置文件
    config = {
        "appName": name,
        "websiteUrl": url,
        "iconPath": icon_path if icon_path else "./icon.png",
        "outputDir": output_path,
        "electron": {
            "width": 1200,
            "height": 800,
            "resizable": True,
            "fullscreen": False,
            "frame": True,
            "transparent": False,
            "backgroundColor": "#ffffff",
            "webPreferences": {
                "nodeIntegration": False,
                "contextIsolation": True
            }
        }
    }

    # 保存配置到应用目录
    config_path = os.path.join(modified_app_dir, "config.json")
    if not save_config(config):
        return

    # 如果提供了图标，则复制到应用目录
    if icon_path and os.path.exists(icon_path):
        try:
            app_icon_path = os.path.join(modified_app_dir, "icon.png")
            shutil.copy(icon_path, app_icon_path)
        except Exception as e:
            messagebox.showerror("错误", f"复制图标文件失败: {e}")
            return

    # 移动到最终输出路径
    try:
        final_output_path = os.path.join(output_path, name)
        if os.path.exists(final_output_path):
            shutil.rmtree(final_output_path)  # 如果目标路径已存在,删除它
        shutil.move(modified_app_dir, final_output_path)

        # 同时复制 config.json 到输出目录（以便 Electron 应用启动时读取）
        shutil.copy(config_path, os.path.join(final_output_path, "config.json"))
    except Exception as e:
        messagebox.showerror("错误", f"移动应用到输出目录失败: {e}")
        return

    messagebox.showinfo("成功", f"Electron 应用已成功生成! 文件位于 '{final_output_path}'.")

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
