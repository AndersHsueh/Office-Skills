# Skills-Vo-Anders

个人技能库,用于 OpenCode/Claude Code 的可复用技能文档。

Personal collection of skills for OpenCode/Claude Code.

## 可用技能 Available Skills

### optimize-omo-config (优化omo配置)

系统化测试 OpenCode 模型,优化 oh-my-opencode 配置以提升速度。

Systematically test OpenCode models and optimize oh-my-opencode configuration for speed.

**使用方法 Usage**: 询问 Claude "优化我的 omo 配置" 或 "测试 opencode 模型"

**关键发现 Key Findings**:
- X.AI Grok-4: 4秒响应时间(最快)
- 阿里云 Qwen3-Max: 4秒响应时间
- GitHub Copilot Claude Sonnet 4.5: 14秒响应时间(免费)

### publish-my-skills (发布我的skills)

自动发布本地开发的 Claude Code 技能到 GitHub 仓库 Skills-Vo-Anders。支持批量发布、智能检测更新、跳过相同内容。

Automatically publish locally developed Claude Code skills to GitHub repository Skills-Vo-Anders. Supports batch publishing, smart update detection, and skipping identical content.

**使用方法 Usage**: 
- "发布我的 skills" (发布最近修改的技能)
- "发布技能 [技能名称]" (发布指定技能)
- "publish my skills [skill-name]"

**核心功能 Core Features**:
- ✅ 自动检测本地技能
- ✅ 智能判断新建/更新/相同
- ✅ 完整的 Git 自动化
- ✅ 辅助脚本支持批量操作

## 目录结构 Structure

```
skills/
└── skill-name/
    ├── SKILL.md          # 主技能文档 Main skill documentation
    ├── references/       # 参考资料(可选) Additional reference materials (optional)
    ├── examples/         # 示例(可选) Working examples (optional)
    └── scripts/          # 工具脚本(可选) Utility scripts (optional)
```

## 如何使用技能 How to Use Skills

1. 在 Claude Code 中加载技能目录
2. 使用触发短语激活技能
3. 按照技能文档中的步骤操作

1. Load the skills directory in Claude Code
2. Use trigger phrases to activate skills
3. Follow the steps in the skill documentation

## 环境要求 Environment

- **OpenCode**: 需要安装 oh-my-opencode 插件
- **网络**: 部分模型在中国大陆可能需要 VPN
- **API Keys**: 需要配置相应的模型提供商 API 密钥

- **OpenCode**: Requires oh-my-opencode plugin
- **Network**: Some models may require VPN in China mainland
- **API Keys**: Provider API keys must be configured

## 许可 License

MIT

---

*Created by Anders Hsueh | 创建于 2026-01-26*
