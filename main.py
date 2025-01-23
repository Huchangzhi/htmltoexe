import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def select_icon():
    """打开文件对话框选择图标文件."""
    file_path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico"), ("All Files", "*.*")])
    icon_entry.delete(0, tk.END)
    icon_entry.insert(0, file_path)

def select_output_path():
    """打开文件对话框选择输出文件夹."""
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, folder_path)

def modify_nativefier():
    """复制 yc 文件夹并修改副本中的 nativefier.json 文件和图标."""
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
    original_folder = "yc"
    modified_folder = "exe"
    nativefier_json_path = os.path.join(modified_folder, "resources", "app", "nativefier.json")
    icon_target_path = os.path.join(modified_folder, "resources", "app", "icon.ico")

    # 检查原始文件夹是否存在
    if not os.path.exists(original_folder):
        messagebox.showerror("错误", f"未找到原始文件夹 '{original_folder}'!")
        return

    # 创建副本文件夹
    try:
        if os.path.exists(modified_folder):
            shutil.rmtree(modified_folder)  # 如果副本已存在,删除它
        shutil.copytree(original_folder, modified_folder)
    except Exception as e:
        messagebox.showerror("错误", f"复制文件夹失败:{e}")
        return

    # 修改 nativefier.json 文件
    try:
        with open(nativefier_json_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # 确保完全替换
        data["name"] = name
        data["targetUrl"] = url
        data["win32metadata"] = {
            "ProductName": name,
            "InternalName": name,
            "FileDescription": name
        }

        # 保存修改
        with open(nativefier_json_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("错误", f"修改 nativefier.json 失败:{e}")
        return

    # 替换图标文件
    if icon_path:
        try:
            shutil.copy(icon_path, icon_target_path)
        except Exception as e:
            messagebox.showerror("错误", f"替换图标失败:{e}")
            return

    # 移动副本文件夹到输出路径
    try:
        final_output_path = os.path.join(output_path, modified_folder)
        if os.path.exists(final_output_path):
            shutil.rmtree(final_output_path)  # 如果目标路径已存在,删除它
        shutil.move(modified_folder, final_output_path)
    except Exception as e:
        messagebox.showerror("错误", f"移动文件夹失败:{e}")
        return

    messagebox.showinfo("成功", f"exe已成功生成!文件位于 '{final_output_path}'.")

# 创建 Tkinter 图形界面
root = tk.Tk()
root.title("网页转exe")

# 网站名称
tk.Label(root, text="网站名称:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
name_entry = tk.Entry(root, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=5)

# 网站网址
tk.Label(root, text="网站网址:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
url_entry = tk.Entry(root, width=40)
url_entry.grid(row=1, column=1, padx=10, pady=5)

# 图标路径
tk.Label(root, text="图标路径:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
icon_entry = tk.Entry(root, width=40)
icon_entry.grid(row=2, column=1, padx=10, pady=5)
icon_button = tk.Button(root, text="选择", command=select_icon)
icon_button.grid(row=2, column=2, padx=10, pady=5)

# 输出路径
tk.Label(root, text="输出路径:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
output_entry = tk.Entry(root, width=40)
output_entry.grid(row=3, column=1, padx=10, pady=5)
output_button = tk.Button(root, text="选择", command=select_output_path)
output_button.grid(row=3, column=2, padx=10, pady=5)

# 修改按钮
modify_button = tk.Button(root, text="生成", command=modify_nativefier, bg="green", fg="white")
modify_button.grid(row=4, column=0, columnspan=3, pady=10)

# 运行 Tkinter 主循环
root.mainloop()
