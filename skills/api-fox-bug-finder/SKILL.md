---
name: api-fox-bug-finder
description: 检测 Apifox 恶意域名 (apifox.it.com) 安全问题。当用户提到"排查 Apifox"、"检查 apifox.it.com"、"公司安全通知 apifox"、"apifox 中毒"、"apifox 卸载"、或"安全漏洞排查"时使用此技能。支持 macOS / Linux / Windows 三平台，自动检测 Network Persistent State、Apifox 安装目录、hosts 文件、Git 凭证。
---

# ApiFox 安全排查

## 概述

检测系统中是否存在 Apifox 恶意域名 `apifox.it.com` 的痕迹，并输出标准化报告。

## 恶意域名

`apifox.it.com` — 已被确认含有后门的域名，攻击者可通过 Chromium 系应用的 Network Persistent State 文件持久化 DNS 记录，实现长连接后门。

## 排查步骤

### Step 1 — 执行检测脚本

脚本路径: `{SKILL_BASE}/scripts/check.py`

```bash
python3 {SKILL_BASE}/scripts/check.py
```

> 脚本自动检测当前系统类型（macOS / Linux / Windows），并执行对应检测逻辑。

### Step 2 — 解读结果

脚本会输出以下四类检查结果：

| 检查项 | 说明 |
|---|---|
| Network Persistent State | Chromium 系应用的 DNS 缓存，恶意域名在此持久化即代表感染 |
| Apifox 安装目录 | 检测 `~/Library/Application Support/apifox`（macOS）等路径 |
| hosts 文件 | 检查是否被劫持指向恶意域名 |
| Git 凭证 | 检查 gitconfig 和 .git-credentials 是否含恶意 URL |

### Step 3 — 生成报告

根据脚本结果，按以下模板输出中文报告：

```
# 🔍 Apifox 安全排查报告

**排查时间**: <当前时间>
**系统**: <macOS/Linux/Windows>
**结果**: [CLEAN / WARNING / INFECTED]

## 检查详情

| 检查项 | 状态 | 说明 |
|---|---|---|
| Network Persistent State | ✅/❌ | ... |
| Apifox 安装目录 | ✅/⚠️ | ... |
| hosts 文件 | ✅/❌ | ... |
| Git 凭证 | ✅/❌ | ... |

## 处理建议

[CLEAN] 无需处理，可放心使用。
[WARNING] 建议卸载当前 Apifox，前往官网下载最新版（2.8.21）重装。
[INFECTED] 立即执行：
  1. 断网
  2. 彻底卸载 Apifox，结束所有相关进程
  3. 轮换所有凭证（SSH 私钥、Git Token、服务器密码等）
```

## 三平台检测路径对照

| 平台 | Network Persistent State | Apifox 数据目录 |
|---|---|---|
| macOS | `~/Library/Application Support/*/Network Persistent State` | `~/Library/Application Support/apifox` |
| Linux | `~/.config/*/Network Persistent State` | `~/.config/apifox`, `~/.local/share/apifox` |
| Windows | `%AppData%\apifox\Network Persistent State` | `%AppData%\apifox`, `%LOCALAPPDATA%\apifox` |

## 参考资料

详见: https://blog.csdn.net/weixin_47126666/article/details/159476269
