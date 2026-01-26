---
name: 优化omo配置
description: This skill should be used when the user asks to "optimize oh-my-opencode configuration", "test opencode models", "update omo config", "find fastest models", or wants to systematically test available OpenCode models and optimize agent configurations based on test results.
version: 1.0.0
---

# 优化omo配置 (Optimize Oh-My-OpenCode Configuration)

## Purpose

This skill provides a systematic workflow to test all available OpenCode models, measure their response times, and optimize the `oh-my-opencode.json` configuration to use the fastest and most reliable models. It helps users migrate away from unavailable models (like Anthropic without API keys) to working alternatives.

## When to Use This Skill

Use this skill when:
- User wants to test which OpenCode models are available and working
- User needs to optimize oh-my-opencode configuration for speed
- User has API keys configured but doesn't know which models work best
- User wants to replace unavailable models (e.g., `anthropic/*` without API key)
- User asks to "find the fastest models" or "optimize model selection"

## Workflow Overview

The skill follows a three-phase workflow:

1. **Phase 1: Model Testing** - Systematically test models from all configured providers
2. **Phase 2: Results Analysis** - Generate comprehensive report with recommendations
3. **Phase 3: Configuration Optimization** - Update `oh-my-opencode.json` with best models

## Phase 1: Model Testing

### Step 1.1: Identify Configured Providers

Read `~/.config/opencode/opencode.jsonc` to identify configured providers with API keys:

```bash
cat ~/.config/opencode/opencode.jsonc | grep -A 5 '"provider"'
```

Common providers:
- `github-copilot` - GitHub Copilot (check subscription)
- `google` - Google AI (Gemini models)
- `xai` - X.AI (Grok models)
- `nvidia` - NVIDIA (various models)
- `openrouter` - OpenRouter (free and paid models)
- `dashscope` / `alibaba-cn` - Alibaba Cloud DashScope (Qwen, DeepSeek)
- `opencode` - Built-in OpenCode Zen models
- `openai` with custom baseURL - Local LM Studio

### Step 1.2: Test Models by Provider

For each provider, test representative models using:

```bash
opencode run -m "provider/model-name" "Say OK" 2>&1
```

**Test systematically in parallel** (run multiple tests concurrently):
- GitHub Copilot: `github-copilot/claude-sonnet-4.5`, `claude-opus-4.5`, `claude-haiku-4.5`
- X.AI: `xai/grok-4`, `xai/grok-4-fast`, `xai/grok-3`, `xai/grok-3-fast`
- Google: `google/gemini-2.5-flash`, `google/gemini-3-flash-preview`
- Alibaba: `alibaba-cn/qwen3-max`, `alibaba-cn/deepseek-r1`
- NVIDIA: `nvidia/minimaxai/minimax-m2.1`, `nvidia/deepseek-ai/deepseek-r1`
- OpenRouter: `openrouter/deepseek/deepseek-r1:free`, `openrouter/qwen/qwen3-coder:free`
- OpenCode Zen: `opencode/gpt-5-nano`, `opencode/big-pickle`
- Local LM Studio: Check if service is running first with `curl http://127.0.0.1:1234/v1/models`

**Record for each model:**
- Status: ✅ Working / ❌ Failed / ⏳ Timeout / ⚠️ Issues
- Response time (in seconds)
- Error messages if any
- Any special notes (e.g., "requires enabling in settings")

### Step 1.3: Handle Special Cases

**GitHub Copilot models:**
- If model returns "not supported", note: "Requires enabling at https://github.com/settings/copilot/features"
- Only test models listed in Copilot settings

**LM Studio local models:**
- First verify service is running: `curl -s http://127.0.0.1:1234/v1/models`
- If OpenCode call fails but direct API works, note compatibility issue
- Test direct API: `curl -X POST http://127.0.0.1:1234/v1/chat/completions -d '...'`

**Timeout models:**
- Set timeout to 30 seconds
- If timeout occurs, mark as ⏳ and note "Response too slow (>30s)"

## Phase 2: Results Analysis

### Step 2.1: Generate Test Report

Create comprehensive report at `~/temp/models.md` with:

**Header section:**
```markdown
# OpenCode 可用模型测试报告

**生成时间**: YYYY-MM-DD HH:MM
**测试环境**: macOS/Linux/Windows, China/Global network

## 已配置的提供商
[List all providers with status]
```

**Provider sections:**
For each provider, create a table:

```markdown
### N. Provider Name

| 状态 | 模型 | 响应时间 | 备注 |
|------|------|----------|------|
| ✅ | `provider/model` | ~Xs | 描述 |

**结论**:
- Summary of provider status
- Performance notes
- Recommendations
```

**Recommendations section:**
```markdown
## 推荐配置方案

### 替换策略
[Table mapping old models to recommended replacements]

### Agent 模型分配建议
[Table with agent types and recommended models]

### 成本和速度平衡
[Speed ranking of models]
```

**Summary section:**
```markdown
## 总结

**可用提供商排名** (按速度):
1. 🥇 Provider - Xms (description)
2. 🥈 Provider - Xms (description)
...

**不可用**:
- [List unavailable models/providers]
```

### Step 2.2: Analyze Performance Patterns

**Group models by speed:**
- Extremely fast: 2-5 seconds
- Fast: 5-15 seconds
- Moderate: 15-30 seconds
- Slow: 30-60 seconds
- Very slow: >60 seconds or timeout

**Identify best models for each use case:**
- **Critical decisions** (sisyphus, oracle): Fastest + most capable (e.g., `xai/grok-4`, `alibaba-cn/qwen3-max`)
- **Fast tasks** (explore, librarian): Fastest available (e.g., `alibaba-cn/qwen3-max`, `xai/grok-4-fast`)
- **Writing/docs**: Best Chinese support if needed (e.g., `alibaba-cn/qwen3-max`)
- **Frontend**: Best UI/UX understanding (e.g., `github-copilot/claude-sonnet-4.5`)
- **Multimodal**: Best vision capabilities (e.g., `google/gemini-2.5-flash`)

### Step 2.3: Create Replacement Mapping

Map problematic current models to best replacements:

```markdown
| 当前配置 | 问题 | 推荐替换 | 原因 |
|---------|------|----------|------|
| `anthropic/claude-opus-4-5` | 需要 API Key | `xai/grok-4` | 极快 (4s) |
| `anthropic/claude-haiku-4-5` | 需要 API Key | `alibaba-cn/qwen3-max` | 极快 (4s) |
```

## Phase 3: Configuration Optimization

### Step 3.1: Read Current Configuration

Read `~/.config/opencode/oh-my-opencode.json`:

```bash
cat ~/.config/opencode/oh-my-opencode.json
```

Identify:
- Which agents use unavailable models
- Which agents use slow models that have faster alternatives
- Which categories need updating

### Step 3.2: Apply Optimization Strategy

**Priority 1: Replace unavailable models**
- Any `anthropic/*` models without API key
- Any models that returned errors in testing
- Any deprecated/end-of-life models

**Priority 2: Upgrade to faster alternatives**
- Models with faster equivalents (e.g., `grok-3` → `grok-4`)
- Models based on user preferences (e.g., avoid DeepSeek if user requests)

**Priority 3: Optimize by agent role**

```json
{
  "agents": {
    "sisyphus": { "model": "fastest-capable-model" },
    "oracle": { "model": "fastest-capable-model" },
    "explore": { "model": "fastest-light-model" },
    "librarian": { "model": "fastest-light-model" },
    "document-writer": { "model": "best-chinese-model-if-needed" },
    "frontend-ui-ux-engineer": { "model": "best-ui-model" },
    "multimodal-looker": { "model": "best-vision-model" }
  },
  "categories": {
    "ultrabrain": { "model": "fastest-capable-model" },
    "quick": { "model": "fastest-light-model" },
    "writing": { "model": "best-chinese-model-if-needed" }
  }
}
```

### Step 3.3: Update Configuration File

Use the Edit tool to update `~/.config/opencode/oh-my-opencode.json`:

**For agents section:**
```bash
# Replace all occurrences of old model with new model
# Update comments to reflect new model and reasoning
```

**For categories section:**
```bash
# Apply same replacement logic
# Ensure consistency with agent choices
```

**Preserve structure:**
- Keep all agent names and options (temperature, max_tokens)
- Only update the "model" field and "comment" field
- Maintain JSON formatting

### Step 3.4: Verify Configuration

After updating:

1. **Validate JSON syntax:**
```bash
cat ~/.config/opencode/oh-my-opencode.json | jq '.' > /dev/null
```

2. **Test key models:**
```bash
opencode run -m "new-model-1" "Test OK" 2>&1
opencode run -m "new-model-2" "Test OK" 2>&1
```

3. **Display final configuration:**
```bash
cat ~/.config/opencode/oh-my-opencode.json | jq '.agents | to_entries | map({agent: .key, model: .value.model})'
cat ~/.config/opencode/oh-my-opencode.json | jq '.categories | to_entries | map({category: .key, model: .value.model})'
```

## Best Practices

### Testing Best Practices

1. **Run tests in parallel** - Use multiple bash calls simultaneously for speed
2. **Use reasonable timeouts** - 30 seconds is usually sufficient
3. **Test latest versions first** - e.g., test `grok-4` before `grok-3`
4. **Document everything** - Record all results, even failures
5. **Test direct APIs for local models** - If OpenCode fails, try curl

### Configuration Best Practices

1. **Preserve user preferences** - Ask before making changes user didn't request
2. **Use consistent models** - Don't mix too many different providers unnecessarily
3. **Optimize for speed** - Prefer 4-5 second models over 30+ second models
4. **Consider network location** - In China, prefer `alibaba-cn/*` for speed
5. **Keep comments updated** - Explain why each model was chosen
6. **Test before finalizing** - Verify new models actually work

### Report Best Practices

1. **Be comprehensive** - Include all test results, not just successes
2. **Provide context** - Explain why models failed or are slow
3. **Give recommendations** - Don't just list results, suggest actions
4. **Use visual indicators** - ✅❌⏳⚠️ for quick scanning
5. **Include examples** - Show exact commands to reproduce results

## Common Issues and Solutions

### Issue: Model shows as "not supported"

**For GitHub Copilot:**
- Check https://github.com/settings/copilot/features
- Model may need to be enabled in settings
- Some models are not available in all regions

**For other providers:**
- Verify API key is correct
- Check if model name changed
- Confirm subscription/access level

### Issue: Model times out

**Possible causes:**
- Model is genuinely slow (>30s response)
- Network issues
- Model may be loading for first time (LM Studio)

**Solutions:**
- Increase timeout for slow models
- Check network connectivity
- For LM Studio, test with direct API call

### Issue: OpenCode can't find model but API works

**Common with LM Studio:**
- OpenCode model naming may not match LM Studio
- Check `opencode.jsonc` for correct model ID mapping
- Verify baseURL is correct: `http://127.0.0.1:1234/v1`

**Solution:**
```json
"openai": {
  "options": {
    "baseURL": "http://127.0.0.1:1234/v1"
  },
  "models": {
    "local-model-name": {
      "id": "actual-model-id-from-lm-studio"
    }
  }
}
```

### Issue: All Alibaba models fail

**Possible causes:**
- Wrong API key
- Network blocked (need VPN if outside China)
- Service downtime

**Check:**
```bash
curl -H "Authorization: Bearer YOUR-API-KEY" \
  https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
  -d '{"model": "qwen-max", "input": {"prompt": "Hello"}}'
```

## Quick Reference Commands

### Test a model
```bash
opencode run -m "provider/model" "Say OK" 2>&1
```

### Check LM Studio status
```bash
curl -s http://127.0.0.1:1234/v1/models | jq -r '.data[].id'
```

### View current oh-my-opencode config
```bash
cat ~/.config/opencode/oh-my-opencode.json | jq '.agents'
```

### Validate JSON
```bash
cat ~/.config/opencode/oh-my-opencode.json | jq '.' > /dev/null && echo "Valid JSON"
```

### List configured providers
```bash
cat ~/.config/opencode/opencode.jsonc | jq '.provider | keys'
```

## Example Workflow

```markdown
User: "Optimize my oh-my-opencode config, test all available models"

1. Identify providers from opencode.jsonc:
   - github-copilot (has subscription)
   - xai (API key: xai-...)
   - google (API key: ...)
   - alibaba-cn (API key: ...)

2. Test models in parallel:
   - xai/grok-4 → ✅ 4s
   - xai/grok-3 → ✅ 13s
   - alibaba-cn/qwen3-max → ✅ 4s
   - google/gemini-2.5-flash → ✅ 27s
   - github-copilot/claude-sonnet-4.5 → ✅ 14s

3. Generate report at ~/temp/models.md:
   - Fastest: grok-4, qwen3-max (4s)
   - Recommendations: Replace grok-3 with grok-4

4. Update oh-my-opencode.json:
   - sisyphus: grok-3 → grok-4
   - oracle: grok-3 → grok-4
   - librarian: keep qwen3-max
   - explore: keep qwen3-max

5. Verify configuration:
   - Test grok-4 → ✅ Works
   - Display final config → User confirms

Done! Configuration optimized.
```

## Output Deliverables

After completing this skill, provide:

1. **Test Report** - `~/temp/models.md` with comprehensive results
2. **Updated Config** - Modified `~/.config/opencode/oh-my-opencode.json`
3. **Summary** - Brief explanation of changes made
4. **Performance Comparison** - Before/after speed comparison if applicable

## Advanced: Provider-Specific Testing

### GitHub Copilot

Models to test:
- `github-copilot/claude-sonnet-4.5` (most likely available)
- `github-copilot/claude-opus-4.5` (may need enabling)
- `github-copilot/claude-haiku-4.5` (may need enabling)
- `github-copilot/gpt-5.2` (if available)
- `github-copilot/gpt-5-mini` (if available)

### X.AI Grok

Test in order (latest first):
- `xai/grok-4` (latest, fastest)
- `xai/grok-4-fast` (latest, optimized)
- `xai/grok-3` (previous version)
- `xai/grok-3-fast` (previous, optimized)

### Alibaba Cloud DashScope

Recommended models:
- `alibaba-cn/qwen3-max` (best quality, fast)
- `alibaba-cn/qwen-max` (previous version)
- `alibaba-cn/deepseek-r1` (alternative)

### Google AI

Models to test:
- `google/gemini-2.5-flash` (latest Flash)
- `google/gemini-2.0-flash-exp` (experimental)
- `google/gemini-3-flash-preview` (preview, may be slow)

## Conclusion

This skill provides a systematic approach to testing and optimizing OpenCode model configurations. Follow the three-phase workflow: test models, analyze results, and optimize configuration. Always document findings in a comprehensive report and verify changes work before finalizing.

Key principles:
- Test systematically
- Document everything
- Prioritize speed
- Verify changes
- Provide clear recommendations
