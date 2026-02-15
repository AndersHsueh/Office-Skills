---
name: update-gh-host
description: 更新本地hosts文件以优化GitHub访问速度，解决访问慢和图片加载问题
---

# Update GitHub Hosts 技能

此技能用于更新本地系统的hosts文件，通过将GitHub相关域名映射到最佳IP地址来解决访问慢和图片加载问题。

## 功能说明

- 获取最新的GitHub相关域名和IP地址映射
- 支持主要源和备用源（Gitee镜像）获取hosts内容
- 自动更新本地hosts文件
- 自动刷新DNS缓存以使更改立即生效
- 支持Windows、Linux和macOS系统
- 保留现有hosts文件内容，只更新GitHub相关条目

## 使用场景

当用户遇到以下问题时使用此技能：
- GitHub访问速度缓慢
- GitHub项目中的图片无法加载
- 需要优化GitHub相关服务的访问体验

## 操作步骤

1. 获取最新的GitHub域名IP映射数据
2. 备份当前hosts文件
3. 在hosts文件中查找并替换GitHub相关条目
4. 添加新的GitHub域名IP映射
5. 自动刷新DNS缓存以确保更改立即生效

## 注意事项

- 需要管理员权限才能修改hosts文件
- 修改前会自动备份原文件
- 不同操作系统hosts文件位置不同：
  - Windows: `C:\\Windows\\System32\\drivers\\etc\\hosts`
  - Linux/macOS: `/etc/hosts`
- 修改后会自动刷新DNS缓存，确保更改立即生效

## DNS刷新命令（自动执行）

- Windows: `ipconfig /flushdns`
- Linux: `sudo nscd restart` 或 `sudo systemctl restart systemd-resolved`
- macOS: `sudo killall -HUP mDNSResponder`