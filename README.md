# Office-Skills

> 办公效率技能集 — 专为 Claude Code / OpenCode 打造的可复用技能库。
> 收录那些真正在日常办公中能省力的技能：排版、环境配置、工作流自动化。

---

## 技能列表

### answer2paper · 报纸排版

把 AI 的长篇回复或本地 Markdown 文件，自动排版成报纸样式的 HTML 页面，在浏览器整屏阅读。

多栏布局 + 引言块 + 关键要点框，告别线性滚动。本地端口 1982 实时预览，输出纯静态 HTML 可直接分发存档。

**触发**：`answer2paper` / `排版成报纸` / `@文件路径 , answer2paper`

---

### optimize-omo-config · 优化 omo 配置

系统化测试各家 AI 模型响应速度，自动优化 oh-my-opencode 配置文件，找出最快、最划算的模型组合。

**触发**：`优化我的 omo 配置` / `测试 opencode 模型`

---

### publish-my-skills · 发布技能

自动将本地开发的 Claude Code 技能发布到 GitHub，智能判断新建或更新，跳过相同内容，支持批量操作。

**触发**：`发布我的 skills` / `发布技能 [技能名称]`

---

### update-gh-host · 更新 GitHub Hosts

自动从远端拉取最新的 GitHub IP 映射并写入本地 hosts 文件，解决国内 GitHub 访问慢、图片无法加载的问题。支持主源与 Gitee 镜像双源切换。

**触发**：`更新 GitHub hosts` / 直接运行 `update_gh_host.py`

---

## 安装方式

进入对应技能目录，将 `SKILL.md` 的内容加载进 Claude Code 的 Project Instructions，或直接将技能文件夹路径添加到插件配置中。

## 目录结构

```
skills/
└── skill-name/
    ├── SKILL.md          # 技能主逻辑
    ├── README.md         # 使用说明
    └── references/       # 模板/参考资料（可选）
```

---

*MIT License · by Anders Hsueh*
