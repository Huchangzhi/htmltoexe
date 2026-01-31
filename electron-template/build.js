#!/usr/bin/env node

/**
 * 构建脚本 - 用于预打包 Electron 应用
 * 此脚本将在 GitHub Actions 中运行
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('开始构建 Electron 应用...');

try {
  // 检查是否安装了依赖
  console.log('检查依赖...');
  if (!fs.existsSync('./node_modules')) {
    console.log('安装依赖...');
    execSync('npm install', { stdio: 'inherit' });
  }

  // 构建应用
  console.log('构建应用...');
  execSync('npm run build', { stdio: 'inherit' });

  console.log('构建完成！');
  console.log('预打包的 Electron 应用已准备就绪。');
} catch (error) {
  console.error('构建过程中出现错误:', error.message);
  process.exit(1);
}