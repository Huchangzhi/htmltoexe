const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const fs = require('fs');

// 创建浏览器窗口
function createWindow() {
  // 读取配置文件
  let config = {
    appName: 'My Web App',
    websiteUrl: 'https://www.example.com',
    iconPath: './icon.png',
    electron: {
      width: 1200,
      height: 800,
      resizable: true,
      fullscreen: false,
      frame: true,
      transparent: false,
      backgroundColor: '#ffffff',
      webPreferences: {
        nodeIntegration: false,
        contextIsolation: true
      }
    }
  };

  // 尝试从 config.json 读取配置
  const configPath = path.join(__dirname, 'config.json');
  if (fs.existsSync(configPath)) {
    try {
      const configFile = fs.readFileSync(configPath, 'utf8');
      const loadedConfig = JSON.parse(configFile);
      
      // 合并配置
      config = { ...config, ...loadedConfig };
    } catch (err) {
      console.error('读取配置文件失败:', err);
    }
  }

  // 创建浏览器窗口
  const mainWindow = new BrowserWindow({
    width: config.electron.width || 1200,
    height: config.electron.height || 800,
    resizable: config.electron.resizable !== false,
    fullscreen: config.electron.fullscreen || false,
    frame: config.electron.frame !== false,
    transparent: config.electron.transparent || false,
    backgroundColor: config.electron.backgroundColor || '#ffffff',
    icon: path.join(__dirname, 'icon.png'),
    webPreferences: {
      ...config.electron.webPreferences,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // 加载网站
  mainWindow.loadURL(config.websiteUrl);

  // 打开开发者工具（可选）
  // mainWindow.webContents.openDevTools();

  // 当窗口关闭时
  mainWindow.on('closed', () => {
    app.quit();
  });
}

// 当 Electron 完成初始化时
app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

// 当所有窗口都关闭时退出应用
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});