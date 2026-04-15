# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

Office-Skills 是一个 Claude Code 技能库，收集办公场景中实用的 AI 技能。目前包含以下技能：

| 技能 | 用途 | 触发词 |
|------|------|--------|
| `answer2paper` | 将 AI 回复或 Markdown 排版成报纸风格 HTML | `answer2paper` / `排版成报纸` |
| `api-fox-bug-finder` | 检测 Apifox 恶意域名 `apifox.it.com` 痕迹 | `排查 Apifox` / `检查 apifox.it.com` |
| `jb-simple-report` | 根据 Excel 生成金碧物业工作简报 | `生成日报` / `生成工作简报` |
| `optimize-omo-config` | 测试并优化 oh-my-opencode 模型配置 | `优化我的 omo 配置` |
| `publish-my-skills` | 将技能发布到 GitHub | `发布我的 skills` |
| `update-gh-host` | 更新本地 GitHub hosts 加速访问 | `更新 GitHub hosts` |

## Skill Package Structure

每个技能目录下包含：

```
skills/<skill-name>/
├── SKILL.md          # 技能主逻辑（必读）
├── README.md         # 使用说明
└── references/       # 模板/参考资料（可选）
```

**SKILL.md 前置说明（YAML frontmatter）：**

```yaml
---
name: <skill-name>
description: "技能描述，说明触发场景和使用方式"
---
```

## Common Workflows

### 读取技能内容

```bash
# 查看所有技能
ls skills/

# 查看特定技能详情
cat skills/<skill-name>/SKILL.md
```

### 发布技能

使用 `publish-my-skills` 技能：
```
发布我的 skills
```

### 报纸排版

```
answer2paper                                    # 排版 AI 上一条回复
@path/to/file.md , answer2paper                 # 排版指定 Markdown 文件
```

输出到 `./paper/index.html`，本地服务端口 1982。

### 生成工作简报

需要 Excel 文件 `（每日更新）金碧工时及进展详情表.xlsx`，输出 Markdown 到 `03-金碧800-计费平台/日报点/`。

## Architecture Notes

- 这是一个纯技能库，没有构建系统或测试套件
- 技能通过读取 `SKILL.md` 并按指令执行
- `answer2paper` 会调用 `references/layout.md` 中的 HTML 模板
- `jb-simple-report` 使用 conda Python（`/opt/miniconda3/bin/python`）配合 calamine 引擎读取 Excel
