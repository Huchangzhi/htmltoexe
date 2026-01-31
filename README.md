# HTML to EXE

快速将网页打包成桌面应用程序的工具，支持 Electron 方式。

## 功能特性

- 🚀 快速打包：一键将网页转换为桌面应用
- 🎨 自定义配置：支持自定义应用名称、图标等
- ⚡ Electron 引擎：使用 Electron 打包方式
- 📁 配置文件：通过 config.json 管理应用配置
- 💻 Windows 7 兼容：支持在 Windows 7 及以上版本运行

## 使用方法

### 方式一：使用预打包的工具（推荐）

1. 从 Releases 页面下载完整的包：
   - `htmltoexe-complete-vX.X.X.zip` - 完整的应用包（包含 htmltoexe.exe 和 electron-framework 目录）
2. 解压后运行 `htmltoexe.exe`
3. 在界面中填写应用名称、网站 URL、选择图标和输出路径
4. 点击"生成"按钮，程序会自动创建定制化的 Web 应用
5. 生成的应用包含一个独立的文件夹，其中有一个 exe 文件和一个 config.json 配置文件
6. 运行 exe 文件即可启动定制化的 Web 应用

### 方式二：手动配置

1. 创建 `config.json` 文件，配置您的应用参数：

```json
{
  "websiteUrl": "https://www.example.com",
  "iconPath": "./icon.png",
  "windowOptions": {
    "width": 1200,
    "height": 800,
    "resizable": true,
    "webPreferences": {
      "nodeIntegration": false,
      "contextIsolation": true
    }
  }
}
```

2. 运行 `python main.py` 启动图形界面

## 开发者说明

对于开发者，项目包含以下组件：

- `main.py`: 主程序，提供图形界面
- `config.json`: 默认配置文件
- `electron-template/`: Electron 应用模板（用于构建预打包的 electron-framework）
- `.github/workflows/build-electron.yml`: GitHub Actions 构建配置
- `.github/workflows/release.yml`: GitHub Actions 发布配置（手动触发）

构建流程：
1. GitHub Actions 构建 Electron 应用（生成 electron-framework 目录）
2. 构建 htmltoexe.exe
3. 将两者打包成 htmltoexe-complete 压缩包
4. 发布到 Releases 页面

## 技术栈

- Python: 用于构建用户界面和配置管理
- Electron: 用于创建跨平台桌面应用 (兼容 Windows 7 及以上版本)
- Node.js: 用于构建和打包工具链
- PyInstaller: 用于将 Python 脚本打包为独立的 exe 文件

## Windows 7 兼容性

本工具支持在 Windows 7 及更高版本的系统上运行。为确保最佳兼容性，Electron 版本已设置为 22.3.27，这是支持 Windows 7 的最后一个版本。

## 下载

从 [Releases 页面](../../releases) 下载最新版本：

1. 访问 [Releases 页面](../../releases)
2. 下载最新的 `htmltoexe-complete-vX.X.X.zip` 文件
3. 解压后即可使用

## 如何发布新版本

维护者可以使用手动触发的 Actions 发布新版本：

1. 访问 Actions 页面
2. 选择 "Release HTMLtoEXE" 工作流
3. 点击 "Run workflow"
4. 输入版本号（如 1.0.0）和发布说明
5. Actions 会自动构建并创建新的 Release

## 许可证

MIT License