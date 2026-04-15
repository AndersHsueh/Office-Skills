# Update GitHub Hosts 技能使用说明

## 功能简介

此技能用于自动更新本地系统的hosts文件，通过将GitHub相关域名映射到最佳IP地址来解决访问慢和图片加载问题。

此技能支持从主要源和备用源（Gitee镜像）获取最新的hosts内容，确保在网络受限情况下也能更新成功。

## 使用方法

### 1. 手动运行脚本

```bash
python update_gh_host.py
```

### 2. 通过Qwen Code使用技能（推荐）

**重要提示：由于修改hosts文件需要系统级权限，在Linux/macOS系统上需要使用sudo权限运行**

```bash
sudo qwen -y -p "使用技能更新HOST文件让github可用"
```

当您遇到GitHub访问慢或图片加载问题时，可以直接使用上述命令，它会自动执行以下操作：
- 获取最新的GitHub域名IP映射数据
- 备份当前hosts文件
- 更新GitHub相关条目
- 自动刷新DNS缓存以确保更改立即生效

## 支持的操作系统

- Windows
- macOS
- Linux

## 注意事项

1. **权限要求**：修改hosts文件需要管理员权限
   - Windows系统：请以管理员身份运行终端或IDE
   - Linux/macOS系统：需要使用sudo权限运行技能
2. **自动备份**：脚本会在修改前自动备份原hosts文件
3. **安全机制**：如果更新过程中出现错误，脚本会自动恢复备份文件
4. **DNS刷新**：更新完成后会自动刷新DNS缓存，确保更改立即生效

## 故障排除

如果遇到问题，请检查：
- 是否有足够的权限修改hosts文件（在Linux/macOS上是否使用了sudo）
- 网络连接是否正常（用于获取最新hosts内容）
- hosts文件是否被其他程序占用

## 技术细节

此技能基于GitHub520项目（https://github.com/521xueweihan/GitHub520）实现，该项目通过定期检测GitHub相关域名的最佳IP地址，生成优化的hosts条目，从而提升访问速度和稳定性。技能会自动刷新DNS缓存，确保更改立即生效。