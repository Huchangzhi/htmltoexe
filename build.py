import subprocess
import sys
import os

def install_pyinstaller():
    """安装 PyInstaller"""
    try:
        import pyinstaller
    except ImportError:
        print("正在安装 PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_exe():
    """构建 exe 文件"""
    try:
        print("正在构建 exe 文件...")
        # 使用 pyinstaller 打包
        subprocess.run([
            "pyinstaller", 
            "--onefile", 
            "--windowed", 
            "--add-data", "config.json;.", 
            "--name", "htmltoexe", 
            "main.py"
        ], check=True)
        print("构建成功！exe 文件位于 dist/htmltoexe.exe")
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_pyinstaller()
    build_exe()