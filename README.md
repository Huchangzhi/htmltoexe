# HTML to EXE

快速将网页打包成桌面应用程序的工具，支持 Nativefier 和 Electron 两种方式。

## 功能特性

- 🚀 快速打包：一键将网页转换为桌面应用
- 🎨 自定义配置：支持自定义应用名称、图标等
- ⚡ 两种引擎：支持 Nativefier 和 Electron 打包方式
- 📁 配置文件：通过 config.json 管理应用配置

## 使用方法

### 方式一：使用预打包的 Electron 框架

1. 下载预构建的 `htmltoexe.exe` 工具
2. 准备好您的网站 URL 和应用图标
3. 运行 `htmltoexe.exe`
4. 在界面中填写应用名称、网站 URL、选择图标和输出路径
5. 点击“生成”按钮

### 方式二：手动配置

1. 创建 `config.json` 文件，配置您的应用参数：

```json
{
  "appName": "My Web App",
  "websiteUrl": "https://www.example.com",
  "iconPath": "./icon.png",
  "outputDir": "./dist",
  "electron": {
    "width": 1200,
    "height": 800,
    "resizable": true,
    "fullscreen": false,
    "frame": true,
    "transparent": false,
    "backgroundColor": "#ffffff",
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
- `electron-template/`: Electron 应用模板
- `.github/workflows/build-electron.yml`: GitHub Actions 构建配置

GitHub Actions 会在每次提交时自动构建 Electron 框架，用户只需下载预构建的工具即可使用。

## 下载

[下载 htmltoexe 工具](https://github.com/Huchangzhi/htmltoexe/releases/download/v1.0.1/htmltoexe.exe)

## 许可证

MIT License