---
name: publish-my-skills
description: 发布自己开发的 Claude Code 技能到 GitHub 仓库 Office-Skills。用户可以指定一个或多个技能名称,如果不指定则发布最近创建的技能。自动检测是新建还是更新。
---

# 发布我的 Skills

这个技能帮助你将本地开发的 Claude Code 技能发布到 GitHub 仓库 `Office-Skills`。

## 触发短语

- "发布我的 skills"
- "发布技能 [技能名称]"
- "把 [技能名称] 发布到 GitHub"
- "publish my skills"
- "发布最近的技能"

## 工作流程

### 阶段 1: 识别要发布的技能

#### 如果用户指定了技能名称

```bash
# 单个技能
用户: "发布技能 optimize-omo-config"

# 多个技能
用户: "发布技能 optimize-omo-config, weekly-rpt-skill"
```

处理逻辑:
1. 解析技能名称列表
2. 在 `~/.claude/skills/` 目录中查找对应技能
3. 验证技能目录是否存在
4. 如果技能不存在,提示用户并列出可用技能

#### 如果用户未指定技能名称

```bash
用户: "发布我的 skills"
用户: "发布最近的技能"
```

处理逻辑:
1. 扫描 `~/.claude/skills/` 目录
2. 按修改时间排序,找出最近修改的技能
3. 排除系统插件技能(通过 @ 符号或特定路径识别)
4. 选择最近 1-3 个修改的技能
5. 向用户确认: "检测到最近修改的技能: [列表], 是否发布这些技能?"

### 阶段 2: 检查技能结构

对每个待发布的技能,验证其结构:

```bash
~/.claude/skills/技能名称/
├── SKILL.md          # 必需: 主技能文档
├── README.md         # 可选: 详细说明
├── examples/         # 可选: 示例文件
├── scripts/          # 可选: 辅助脚本
├── references/       # 可选: 参考资料
└── *.py, *.sh, *.js  # 可选: 工具脚本
```

**必需检查**:
- `SKILL.md` 必须存在
- `SKILL.md` 开头必须有 YAML frontmatter (name, description)

**警告检查**:
- 如果缺少 README.md,提示用户(但不阻止发布)
- 如果技能目录为空或只有配置文件,提示用户

### 阶段 3: 准备 GitHub 仓库

```bash
# 1. 检查仓库是否存在
cd ~/workspace/Office-Skills 2>/dev/null

# 如果不存在,克隆仓库
if [ $? -ne 0 ]; then
  cd ~/workspace
  git clone https://github.com/AndersHsueh/Office-Skills.git
fi

# 2. 更新到最新
cd ~/workspace/Office-Skills
git pull origin main

# 3. 创建技能目录
mkdir -p skills/
```

### 阶段 4: 检测是新建还是更新

对每个技能:

```bash
SKILL_NAME="optimize-omo-config"
REPO_SKILL_PATH="~/workspace/Office-Skills/skills/$SKILL_NAME"

if [ -d "$REPO_SKILL_PATH" ]; then
  echo "✓ 技能 $SKILL_NAME 已存在,准备更新"
  ACTION="更新"
else
  echo "✓ 技能 $SKILL_NAME 不存在,准备新建"
  ACTION="新建"
fi
```

**相同内容检测**:

```bash
# 比较 SKILL.md 文件
LOCAL_SKILL="~/.claude/skills/$SKILL_NAME/SKILL.md"
REPO_SKILL="$REPO_SKILL_PATH/SKILL.md"

if diff -q "$LOCAL_SKILL" "$REPO_SKILL" > /dev/null 2>&1; then
  echo "⚠️ 技能 $SKILL_NAME 内容相同,无需更新"
  SKIP=true
else
  echo "✓ 检测到变更,继续处理"
  SKIP=false
fi
```

### 阶段 5: 复制技能文件

```bash
SKILL_NAME="optimize-omo-config"
LOCAL_PATH="~/.claude/skills/$SKILL_NAME"
REPO_PATH="~/workspace/Office-Skills/skills/$SKILL_NAME"

# 创建目标目录
mkdir -p "$REPO_PATH"

# 复制所有文件
cp -r "$LOCAL_PATH/"* "$REPO_PATH/"

# 列出已复制的文件
echo "已复制文件:"
ls -lh "$REPO_PATH"
```

### 阶段 6: 更新 README.md

检查仓库的 `README.md` 是否包含该技能:

```bash
SKILL_NAME="optimize-omo-config"
README="~/workspace/Office-Skills/README.md"

# 检查技能是否已在 README 中
if ! grep -q "$SKILL_NAME" "$README"; then
  echo "✓ 需要在 README 中添加技能说明"
  
  # 从 SKILL.md 提取信息
  SKILL_DESC=$(grep "^description:" "$REPO_PATH/SKILL.md" | sed 's/description: //')
  
  # 在 README 的 "可用技能" 部分添加
  # (这里需要智能插入,保持 README 格式)
fi
```

### 阶段 7: Git 提交和推送

```bash
cd ~/workspace/Office-Skills

# 添加所有变更
git add skills/
git add README.md

# 生成提交信息
if [ "$ACTION" = "新建" ]; then
  COMMIT_MSG="Add skill: $SKILL_NAME

- $SKILL_DESC
"
else
  COMMIT_MSG="Update skill: $SKILL_NAME

- 更新技能文档和相关文件
"
fi

# 提交
git commit -m "$COMMIT_MSG"

# 推送
git push origin main
```

### 阶段 8: 报告结果

为每个技能生成报告:

```markdown
✅ 技能发布成功: optimize-omo-config

**操作**: 新建
**路径**: skills/optimize-omo-config/
**提交**: a1b2c3d
**包含文件**:
  - SKILL.md (主文档)
  - README.md (详细说明)
  - examples/ (2个示例文件)

**GitHub**: https://github.com/AndersHsueh/Office-Skills/tree/main/skills/optimize-omo-config
```

如果内容相同:

```markdown
ℹ️ 技能已是最新: optimize-omo-config

**状态**: 仓库中的版本与本地版本完全相同
**路径**: skills/optimize-omo-config/
**无需操作**

**GitHub**: https://github.com/AndersHsueh/Office-Skills/tree/main/skills/optimize-omo-config
```

## 错误处理

### 错误 1: 技能不存在

```
❌ 错误: 技能 'xxx' 不存在

在 ~/.claude/skills/ 中未找到该技能。

可用的技能:
  - optimize-omo-config
  - weekly-rpt-skill
  - 售前方案生成
  - 记录工作笔记

请检查技能名称是否正确。
```

### 错误 2: 缺少 SKILL.md

```
❌ 错误: 技能 'xxx' 缺少 SKILL.md 文件

技能目录 ~/.claude/skills/xxx 存在,但缺少必需的 SKILL.md 文件。

请确保技能包含:
  - SKILL.md (必需)
  - 包含 YAML frontmatter (name, description)
```

### 错误 3: Git 推送失败

```
❌ 错误: 推送到 GitHub 失败

可能原因:
  - 网络连接问题 (中国大陆可能需要 VPN)
  - 认证失败 (检查 gh auth status)
  - 冲突 (需要先 git pull)

建议操作:
  1. 检查网络: ping github.com
  2. 检查认证: gh auth status
  3. 手动推送: cd ~/workspace/Office-Skills && git push
```

## 高级用法

### 批量发布

```bash
用户: "发布技能 skill1, skill2, skill3"
```

系统会:
1. 逐个检查和复制技能
2. 一次性提交所有变更
3. 生成汇总报告

### 强制更新

```bash
用户: "强制更新技能 optimize-omo-config"
```

即使内容相同也重新发布(用于修复损坏的文件)。

### 预览模式

```bash
用户: "预览发布技能 optimize-omo-config"
```

显示将要执行的操作,但不实际提交:
- 显示文件差异
- 显示提交信息
- 不执行 git push

## 配置

### GitHub 仓库配置

默认仓库: `https://github.com/AndersHsueh/Office-Skills`

如果需要更改:
1. 在技能目录创建 `.publish-config`
2. 指定自定义仓库 URL

```json
{
  "repo_url": "https://github.com/USERNAME/REPO",
  "repo_path": "~/workspace/REPO",
  "skills_dir": "skills"
}
```

### 忽略文件

创建 `.publishignore` 在技能目录:

```
__pycache__/
*.pyc
.DS_Store
*.tmp
node_modules/
```

## 最佳实践

### 1. 技能命名

使用小写字母和连字符:
- ✅ `optimize-omo-config`
- ✅ `weekly-rpt-skill`
- ❌ `OptimizeOmoConfig` (驼峰命名)
- ❌ `optimize_omo_config` (下划线)

### 2. SKILL.md 结构

```markdown
---
name: skill-name
description: 简短描述(一句话)
---

# 技能标题

详细介绍...

## 触发短语

- 短语 1
- 短语 2

## 工作流程

### 步骤 1
...

## 示例

...
```

### 3. 包含 README.md

虽然不是必需的,但强烈建议包含 README.md:
- 提供更详细的使用说明
- 包含示例输入输出
- 记录已知问题和限制

### 4. 版本控制

在 SKILL.md 的 frontmatter 中添加版本:

```yaml
---
name: skill-name
description: 描述
version: 1.0.0
updated: 2026-01-26
---
```

## 实现提示(给 Claude)

### 关键函数

```bash
# 1. 查找技能
find_skills() {
  local pattern=$1
  if [ -z "$pattern" ]; then
    # 返回最近修改的技能
    ls -td ~/.claude/skills/*/ | head -3
  else
    # 返回匹配的技能
    echo ~/.claude/skills/$pattern/
  fi
}

# 2. 验证技能
validate_skill() {
  local skill_path=$1
  [ -f "$skill_path/SKILL.md" ] || return 1
  grep -q "^---" "$skill_path/SKILL.md" || return 1
  return 0
}

# 3. 检测变更
detect_changes() {
  local local_path=$1
  local repo_path=$2
  
  if [ ! -d "$repo_path" ]; then
    echo "新建"
    return 0
  fi
  
  if diff -qr "$local_path" "$repo_path" > /dev/null 2>&1; then
    echo "相同"
    return 1
  fi
  
  echo "更新"
  return 0
}

# 4. 复制技能
copy_skill() {
  local src=$1
  local dst=$2
  mkdir -p "$dst"
  rsync -av --exclude='.publishignore' "$src/" "$dst/"
}
```

### 执行顺序

1. **解析用户输入** → 获取技能名称列表
2. **查找技能** → 在 ~/.claude/skills/ 中定位
3. **验证技能** → 检查 SKILL.md 和结构
4. **准备仓库** → git clone/pull
5. **检测变更** → 判断新建/更新/相同
6. **复制文件** → rsync 到仓库
7. **更新 README** → 添加新技能说明
8. **Git 提交** → commit + push
9. **生成报告** → 向用户报告结果

### 注意事项

- **中国网络**: 可能需要提示用户检查 VPN
- **大文件**: 警告用户 GitHub 有文件大小限制
- **冲突**: 如果 git pull 有冲突,提示手动解决
- **认证**: 使用 `gh` CLI,确保已登录

## 示例对话

### 示例 1: 发布指定技能

```
用户: 发布技能 optimize-omo-config

助手: 
✓ 找到技能: optimize-omo-config
✓ 验证技能结构: 通过
✓ 克隆仓库: Office-Skills
✓ 检测变更: 更新 (检测到 SKILL.md 有变化)
✓ 复制文件: 
  - SKILL.md (主文档)
  - examples/test-models.sh
✓ 更新 README.md
✓ 提交: Update skill: optimize-omo-config
✓ 推送: 成功

✅ 技能发布成功!

GitHub: https://github.com/AndersHsueh/Office-Skills/tree/main/skills/optimize-omo-config
```

### 示例 2: 发布最近技能

```
用户: 发布我的 skills

助手:
检测到最近修改的技能:
  1. publish-my-skills (刚刚)
  2. weekly-rpt-skill (2天前)

是否发布这些技能? (yes/no)

用户: yes

助手:
[处理 publish-my-skills]
✓ 新建技能
✓ 复制文件...
✓ 提交...

[处理 weekly-rpt-skill]  
ℹ️ 内容相同,跳过

完成! 发布了 1 个技能,跳过了 1 个相同的技能。
```

### 示例 3: 技能已存在

```
用户: 发布技能 optimize-omo-config

助手:
✓ 找到技能: optimize-omo-config
✓ 验证技能结构: 通过
✓ 更新仓库: 最新
✓ 检测变更: 内容相同

ℹ️ 技能 optimize-omo-config 已是最新版本,无需更新。

仓库中的版本与本地版本完全相同。

GitHub: https://github.com/AndersHsueh/Office-Skills/tree/main/skills/optimize-omo-config
```

## 总结

这个技能自动化了将本地技能发布到 GitHub 的完整流程:
- ✅ 自动检测技能
- ✅ 智能判断新建/更新
- ✅ 跳过相同内容
- ✅ 更新 README
- ✅ Git 自动化
- ✅ 详细报告

使用这个技能,你只需要说 "发布我的 skills",剩下的交给 Claude!
