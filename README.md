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
