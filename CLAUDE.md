# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository stores Claude Code skills for office/productivity use. Skills are available in two forms:

- **`.skill` file** (root): `answer2paper.skill` — a packaged ZIP archive for distribution
- **`Office-Skills/` directory**: Full source of all skills for development

## Skills Overview

| 技能 | 用途 | 触发词 |
|------|------|--------|
| `answer2paper` | 将 AI 回复或 Markdown 排版成报纸风格 HTML | `answer2paper` / `排版成报纸` |
| `api-fox-bug-finder` | 检测 Apifox 恶意域名痕迹 | `排查 Apifox` / `检查 apifox.it.com` |
| `jb-simple-report` | 根据 Excel 生成金碧物业工作简报 | `生成日报` / `生成工作简报` |
| `optimize-omo-config` | 测试并优化 oh-my-opencode 模型配置 | `优化我的 omo 配置` |
| `publish-my-skills` | 将技能发布到 GitHub | `发布我的 skills` |
| `update-gh-host` | 更新本地 GitHub hosts 加速访问 | `更新 GitHub hosts` |

## Skill Package Format

Each skill in `Office-Skills/skills/<skill-name>/` contains:

```
├── SKILL.md          # 技能主逻辑
├── README.md         # 使用说明
└── references/       # 模板/参考资料（可选）
```

## answer2paper Skill Details

**触发词:** `answer2paper`, `排版成报纸`, `生成报纸`, `转成报纸格式`

**两种模式:**
- Mode A: `answer2paper` → 排版 AI 上一条回复
- Mode B: `@path/to/file.md , answer2paper` → 读取指定 Markdown 文件

**输出:**
- `./paper/index.html`（每次触发前自动备份旧文件）
- 本地 HTTP 服务端口 **1982**

**设计约束:**
- 颜色：底色 `#F5F0E8`，文字 `#1A1A1A`，点缀 `#8B0000`
- 字体：Noto Serif SC（联网）/ Georgia（离线）
- 无外部 JS 依赖，纯静态 HTML
- 2~3 栏布局，短内容自动选2栏
