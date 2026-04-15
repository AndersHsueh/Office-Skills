---
name: jb-everyone-report
description: 读取金碧物业项目组企业微信在线工时表（每日更新）金碧工时及进展详情表，提取全员工时与进展数据，输出 TSV 文件。当用户说「读取工时表」「获取金碧工时」「拉取每日工时」「jb-everyone-report」时使用此技能。依赖 macOS Chrome 已登录的企业微信文档 Session（Cookie）和 playwright-cli。
---

# jb-everyone-report

从企业微信在线文档自动读取金碧项目全员工时表，输出 TSV 文件。

## 使用方式

运行 `scripts/read_weixin_doc.py`：

```bash
# 读取并保存（默认输出到 weixin_doc_output.tsv）
python3 ~/.iss/skills/jb-everyone-report/scripts/read_weixin_doc.py

# 指定输出文件名
python3 ~/.iss/skills/jb-everyone-report/scripts/read_weixin_doc.py --output 金碧工时.tsv

# 网络慢时增加等待时间
python3 ~/.iss/skills/jb-everyone-report/scripts/read_weixin_doc.py --output 金碧工时.tsv --wait 10
```

## 前置要求

- macOS，Chrome 浏览器中已登录企业微信文档（`doc.weixin.qq.com`）
- 已安装 `pycryptodome`：`pip install pycryptodome`
- 已安装 `playwright-cli`（全局命令可用）

## 技术说明

脚本通过以下步骤提取数据：
1. 从 macOS Keychain 获取 Chrome 加密密钥，解密 `doc.weixin.qq.com` 的 Cookie
2. 用 playwright-cli 以 Chrome 启动浏览器，注入 Cookie 后刷新文档页面
3. 通过拦截浏览器 copy 事件（或 `navigator.clipboard.readText`）触发全选复制，获取完整 TSV

## 文档 URL

默认读取：`https://doc.weixin.qq.com/sheet/e3_AT8ADwZoAGgCNTrZqBm7TQGy3wNRD?scode=AP0AqQfLAAojyki8bcAc4AdgZHADI&tab=000001`

如需读取其他文档，用 `--url` 参数指定。
