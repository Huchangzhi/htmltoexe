# HTML to EXE

快速将网页打包成桌面应用程序的工具，支持 Nativefier 和 Electron 两种方式。

## 功能特性

- 🚀 快速打包：一键将网页转换为桌面应用
- 🎨 自定义配置：支持自定义应用名称、图标等
- ⚡ 两种引擎：支持 Nativefier 和 Electron 打包方式
- 📁 配置文件：通过 config.json 管理应用配置

## 使用方法

### 方式一：使用预打包的工具（推荐）

1. 从 Actions 下载完整的包：
   - `htmltoexe-complete` - 完整的应用包（包含 htmltoexe.exe 和预构建的 webview.exe）
2. 解压后运行 `htmltoexe.exe`
3. 在界面中填写应用名称、网站 URL、选择图标和输出路径
4. 点击"生成"按钮，程序会自动创建定制化的 Web 应用
5. 生成的应用包含一个 exe 文件和一个 config.json 配置文件
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
- `electron-template/`: Electron 应用模板（用于构建预打包的 webview.exe）
- `.github/workflows/build-electron.yml`: GitHub Actions 构建配置

GitHub Actions 会在每次提交时自动构建完整的 `htmltoexe-complete` 包，其中包含 htmltoexe.exe 和预构建的 webview.exe，用户下载后即可使用。

## 技术栈

- Python: 用于构建用户界面和配置管理
- Electron: 用于创建跨平台桌面应用 (兼容 Windows 7 及以上版本)
- Node.js: 用于构建和打包工具链
- PyInstaller: 用于将 Python 脚本打包为独立的 exe 文件

## Windows 7 兼容性

本工具支持在 Windows 7 及更高版本的系统上运行。为确保最佳兼容性，Electron 版本已设置为 11.5.0，这是对 Windows 7 支持较好的版本。

## 下载

由于现在采用新的构建方式，您需要从 GitHub Actions 中下载构建产物：

1. 访问 [Actions 页面](../../actions)
2. 点击最新的构建任务
3. 下载以下构件之一：
   - `htmltoexe-complete` - 完整的应用包（推荐）
   - 或分别下载 `htmltoexe-exe` 和 `electron-framework`

如果下载的是完整包，解压后直接运行 htmltoexe.exe 即可。

## 许可证

MIT License