const { contextBridge, ipcRenderer } = require('electron');

// 安全地暴露一些 API 给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  getConfig: () => ipcRenderer.invoke('get-config')
});