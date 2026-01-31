const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');

// 读取配置文件
function loadConfig() {
  // 首先尝试从可执行文件同级目录读取配置
  const configPath = path.join(path.dirname(process.execPath), 'config.json');

  console.log(`尝试从 ${configPath} 读取配置文件`);

  if (fs.existsSync(configPath)) {
    try {
      const configData = fs.readFileSync(configPath, 'utf8');
      console.log('配置文件内容:', configData);
      const parsedConfig = JSON.parse(configData);
      console.log('解析后的配置:', parsedConfig);
      return parsedConfig;
    } catch (err) {
      console.error('解析配置文件失败:', err);
      // 返回默认配置
      return {
        websiteUrl: 'https://www.example.com',
        windowOptions: {
          width: 1200,
          height: 800,
          resizable: true,
          webPreferences: {
            nodeIntegration: false,
            contextIsolation: true
          }
        }
      };
    }
  } else {
    // 如果没有配置文件，使用默认配置
    console.log('未找到配置文件，使用默认设置');
    return {
      websiteUrl: 'https://www.example.com',
      windowOptions: {
        width: 1200,
        height: 800,
        resizable: true,
        webPreferences: {
          nodeIntegration: false,
          contextIsolation: true
        }
      }
    };
  }
}

function createWindow() {
  const config = loadConfig();

  const windowOptions = {
    width: config.windowOptions?.width || 1200,
    height: config.windowOptions?.height || 800,
    resizable: config.windowOptions?.resizable !== false,
    webPreferences: {
      ...(config.windowOptions?.webPreferences || {}),
      nodeIntegration: config.windowOptions?.webPreferences?.nodeIntegration !== false,
      contextIsolation: config.windowOptions?.webPreferences?.contextIsolation !== false
    }
  };

  // 如果有图标路径，添加图标
  if (config.iconPath) {
    const iconPath = path.resolve(path.dirname(process.execPath), config.iconPath);
    if (fs.existsSync(iconPath)) {
      windowOptions.icon = iconPath;
    }
  }

  const mainWindow = new BrowserWindow(windowOptions);
  mainWindow.loadURL(config.websiteUrl);

  // 生产环境下隐藏菜单栏
  mainWindow.setMenuBar(false);
  mainWindow.setAutoHideMenuBar(true);

  // 打开开发者工具（仅开发环境）
  // mainWindow.webContents.openDevTools();
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});