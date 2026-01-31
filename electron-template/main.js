const { app, BrowserWindow } = require('electron');
const path = require('path');
const fs = require('fs');

// 读取配置文件
function loadConfig() {
  // 尝试多个位置查找配置文件
  let configPath;

  // 1. 首先尝试从当前工作目录读取（用户运行exe的目录）
  configPath = path.join(process.cwd(), 'config.json');
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
    }
  }

  // 2. 尝试从可执行文件同级目录读取配置（标准情况）
  configPath = path.join(path.dirname(process.execPath), 'config.json');
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
    }
  }

  // 3. 如果在标准位置找不到，尝试从 resources 目录读取（打包后的情况）
  if (process.resourcesPath) {
    configPath = path.join(process.resourcesPath, 'config.json');
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
      }
    }
  }

  // 如果都没有找到配置文件，使用默认配置
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