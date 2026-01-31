const { app, BrowserWindow, Menu, shell } = require('electron');
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
    appName: 'Web Application', // 添加默认应用名称
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

// 创建关于对话框
function showAboutDialog() {
  const config = loadConfig();
  const appName = config.appName || 'Web Application';
  const iconPath = config.iconPath ? path.resolve(path.dirname(process.execPath), config.iconPath) : '';

  // 读取 package.json 获取版本号
  let appVersion = '2.0.0'; // 默认版本
  try {
    // 尝试从 resources/app/package.json 读取（Electron 打包后的位置）
    let packageJsonPath = path.join(process.resourcesPath, 'app', 'package.json');
    if (!fs.existsSync(packageJsonPath)) {
      // 如果不在 resources/app 中，尝试在可执行文件同级目录
      packageJsonPath = path.join(path.dirname(process.execPath), 'package.json');
    }

    if (fs.existsSync(packageJsonPath)) {
      const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
      appVersion = packageJson.version || appVersion;
    } else {
      // 如果 resources/app/package.json 不存在，尝试读取 asar 包内的 package.json
      // 通过 require 读取 asar 包内的 package.json
      try {
        const appPackage = require(path.join(process.resourcesPath, 'app.asar', 'package.json'));
        appVersion = appPackage.version || appVersion;
      } catch (asarErr) {
        console.error('读取 asar 包内的 package.json 失败:', asarErr);
      }
    }
  } catch (err) {
    console.error('读取版本号失败:', err);
  }

  // 创建一个简单的关于对话框窗口
  const aboutWindow = new BrowserWindow({
    width: 400,
    height: 350,
    resizable: false,
    modal: true,
    parent: BrowserWindow.getFocusedWindow(),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  // 设置窗口标题
  aboutWindow.setTitle('关于 ' + appName);

  // 创建关于页面的HTML内容
  let logoHtml = '';
  if (iconPath && fs.existsSync(iconPath)) {
    // 如果图标存在，将其编码为 base64 以便在 HTML 中显示
    const logoData = fs.readFileSync(iconPath);
    const logoBase64 = logoData.toString('base64');
    const logoExt = path.extname(iconPath).substring(1); // 获取文件扩展名，去掉点号
    logoHtml = `<img src="data:image/${logoExt};base64,${logoBase64}" alt="Logo" class="logo">`;
  } else {
    // 如果没有图标，显示一个占位符
    logoHtml = `<div class="logo-placeholder">🌐</div>`;
  }

  const aboutHTML = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="UTF-8">
      <title>关于 ${appName}</title>
      <style>
        body {
          font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif;
          padding: 20px;
          background: #f5f5f5;
          margin: 0;
        }
        .container {
          text-align: center;
          max-width: 350px;
          margin: 0 auto;
        }
        .logo {
          width: 80px;
          height: 80px;
          margin-bottom: 15px;
          border-radius: 8px;
        }
        .logo-placeholder {
          width: 80px;
          height: 80px;
          margin: 0 auto 15px;
          font-size: 40px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: #ddd;
          border-radius: 8px;
        }
        h2 {
          margin-top: 0;
          color: #333;
        }
        .info {
          background: white;
          padding: 20px;
          border-radius: 8px;
          box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .link {
          color: #0969da;
          text-decoration: none;
          font-weight: 500;
        }
        .link:hover {
          text-decoration: underline;
        }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="info">
          ${logoHtml}
          <h2>${appName}</h2>
          <p>版本: ${appVersion}</p>
          <p>powerd by <a href="#" class="link" onclick="openLink('https://github.com/huchangzhi/htmltoexe')">htmltoexe</a></p>
        </div>
      </div>
      <script>
        function openLink(url) {
          // 通过 IPC 发送到主进程打开外部链接
          if (typeof require !== 'undefined') {
            const { ipcRenderer } = require('electron');
            ipcRenderer.send('open-external-link', url);
          }
        }
      </script>
    </body>
    </html>
  `;

  aboutWindow.loadURL('data:text/html;charset=utf-8,' + encodeURIComponent(aboutHTML));

  // 监听打开外部链接事件
  aboutWindow.webContents.on('ipc-message', (event, channel, url) => {
    if (channel === 'open-external-link') {
      shell.openExternal(url);
    }
  });
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

  // 创建自定义菜单
  const menuTemplate = [
    {
      label: '关于',
      click: () => showAboutDialog()
    }
  ];

  const menu = Menu.buildFromTemplate(menuTemplate);
  Menu.setApplicationMenu(menu);

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
