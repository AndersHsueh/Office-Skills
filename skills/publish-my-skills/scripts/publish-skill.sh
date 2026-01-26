#!/bin/bash
set -e

# 发布技能到 Skills-Vo-Anders 仓库的辅助脚本
# 用法: ./publish-skill.sh [skill-name1] [skill-name2] ...
# 如果不提供参数,发布最近修改的技能

REPO_URL="https://github.com/AndersHsueh/Skills-Vo-Anders"
REPO_PATH="$HOME/workspace/Skills-Vo-Anders"
SKILLS_SOURCE="$HOME/.claude/skills"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; }

# 查找技能
find_skills() {
    if [ $# -eq 0 ]; then
        info "未指定技能,查找最近修改的技能..."
        find "$SKILLS_SOURCE" -maxdepth 1 -type d \
            ! -name "skills" ! -path "$SKILLS_SOURCE" \
            -exec stat -f "%m %N" {} \; 2>/dev/null | \
            sort -rn | head -3 | cut -d' ' -f2-
    else
        for skill in "$@"; do
            echo "$SKILLS_SOURCE/$skill"
        done
    fi
}

# 验证技能结构
validate_skill() {
    local skill_path=$1
    local skill_name=$(basename "$skill_path")
    
    [ ! -d "$skill_path" ] && error "技能不存在: $skill_name" && return 1
    [ ! -f "$skill_path/SKILL.md" ] && error "缺少 SKILL.md: $skill_name" && return 1
    grep -q "^---" "$skill_path/SKILL.md" || { error "SKILL.md 缺少 YAML frontmatter: $skill_name"; return 1; }
    
    success "验证通过: $skill_name"
    return 0
}

# 准备仓库
prepare_repo() {
    if [ ! -d "$REPO_PATH" ]; then
        info "克隆仓库: $REPO_URL"
        cd "$(dirname "$REPO_PATH")"
        git clone "$REPO_URL" "$(basename "$REPO_PATH")"
    else
        info "更新仓库: $REPO_PATH"
        cd "$REPO_PATH"
        git pull origin main
    fi
}

# 检测变更类型
detect_action() {
    local skill_name=$1
    local repo_skill_path="$REPO_PATH/skills/$skill_name"
    
    [ ! -d "$repo_skill_path" ] && echo "新建" && return 0
    diff -qr "$SKILLS_SOURCE/$skill_name" "$repo_skill_path" > /dev/null 2>&1 && echo "相同" && return 1
    echo "更新" && return 0
}

# 复制技能文件
copy_skill() {
    local skill_name=$1
    local src="$SKILLS_SOURCE/$skill_name"
    local dst="$REPO_PATH/skills/$skill_name"
    
    mkdir -p "$dst"
    rsync -av --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' \
        --exclude='*.tmp' --exclude='node_modules' "$src/" "$dst/"
    success "复制文件到: skills/$skill_name/"
}

# Git 提交
commit_and_push() {
    local skill_name=$1
    local action=$2
    
    cd "$REPO_PATH"
    git add skills/ README.md 2>/dev/null || true
    
    if [ "$action" = "新建" ]; then
        git commit -m "Add skill: $skill_name" -m "新增技能文档和相关文件"
    else
        git commit -m "Update skill: $skill_name" -m "更新技能文档和相关文件"
    fi
    
    git push origin main
    success "推送到 GitHub: $skill_name"
}

# 主流程
main() {
    info "开始发布技能..."
    local skills=$(find_skills "$@")
    
    prepare_repo
    
    local published=0 skipped=0 failed=0
    
    while IFS= read -r skill_path; do
        local skill_name=$(basename "$skill_path")
        echo ""
        info "处理技能: $skill_name"
        
        validate_skill "$skill_path" || { ((failed++)); continue; }
        
        local action=$(detect_action "$skill_name")
        [ "$action" = "相同" ] && info "内容相同,跳过: $skill_name" && ((skipped++)) && continue
        
        copy_skill "$skill_name"
        commit_and_push "$skill_name" "$action"
        ((published++))
    done <<< "$skills"
    
    echo ""
    echo "================================"
    success "发布完成!"
    echo "  发布: $published 个 | 跳过: $skipped 个 | 失败: $failed 个"
    echo "================================"
    info "GitHub: $REPO_URL"
}

main "$@"
