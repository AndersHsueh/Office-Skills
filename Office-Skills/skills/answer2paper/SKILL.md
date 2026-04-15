---
name: answer2paper
description: >
  把内容排版成报纸样式的 HTML 页面，保存到 ./paper/index.html，并启动本地 HTTP 服务（端口 1982）方便整屏阅读。
  支持两种输入模式：(1) 直接输入 "answer2paper" → 排版 AI 上一条回复；(2) 输入 "@文件名.md , answer2paper" → 读取指定 Markdown 文件排版。
  当用户说"排版成报纸"、"answer2paper"、"生成报纸"、"转成报纸格式"、"报纸排版"、"paper 格式输出"等，立即触发此技能。
  也适用于 AI 回复内容较长、知识点密集、希望改善阅读体验的场景。
---

# answer2paper

将内容转化为**报纸排版风格**的 HTML 页面，保存为 `./paper/index.html`，并启动本地 HTTP 服务供浏览器查看。

---

## 工作流程

### Step 1：判断内容来源（两种模式）

检查用户的触发语句，判断使用哪种模式：

#### 模式 A：直接触发（无 @ 文件）
```
用户输入示例：answer2paper
              排版成报纸
              生成报纸
```
→ **内容来源：对话中 AI 的上一条回复**。直接将其 Markdown 文本作为待排版内容。

#### 模式 B：指定 Markdown 文件
```
用户输入示例：@notes.md , answer2paper
              @./docs/report.md , answer2paper
              @/path/to/file.md , answer2paper
```
→ **内容来源：@ 后指定的 .md 文件**。执行以下步骤读取：

```bash
# 提取 @ 后的文件路径（去掉 @ 前缀）
FILE_PATH="<从用户输入解析出的路径>"

# 检查文件是否存在
if [ ! -f "$FILE_PATH" ]; then
  echo "❌ 文件不存在：$FILE_PATH"
  echo "请检查路径是否正确。"
  exit 1
fi

# 读取文件内容
CONTENT=$(cat "$FILE_PATH")
echo "✅ 已读取：$FILE_PATH（$(wc -l < "$FILE_PATH") 行）"
```

若文件不存在，**立即停止并告知用户**，不继续生成。

路径解析规则：
- `@notes.md` → 当前工作目录下的 `notes.md`
- `@./subdir/file.md` → 相对路径
- `@/absolute/path.md` → 绝对路径

### Step 2：检查并备份已有文件

```bash
mkdir -p ./paper
if [ -f "./paper/index.html" ]; then
  TIMESTAMP=$(date +%Y%m%d-%H%M%S)
  mv ./paper/index.html "./paper/index-${TIMESTAMP}.html"
  echo "已备份为 index-${TIMESTAMP}.html"
fi
```

### Step 3：解析内容结构

将 Markdown 内容分析为以下元素：

| 元素 | 说明 |
|------|------|
| `headline` | 最重要的主标题（H1 或首句概要） |
| `subheadline` | 副标题或摘要句 |
| `sections[]` | 各章节，含 title + body |
| `quotes[]` | 值得突出的引言或关键句 |
| `facts[]` | 数据、列表要点 |
| `byline` | 来源标注，固定为 "AI · answer2paper" |

### Step 4：生成 HTML

读取 references/layout.md 中的完整模板，按内容填入，写出 ./paper/index.html。

**详细规范见 → references/layout.md**

### Step 5：启动服务

```bash
# 检查端口是否已在监听
if lsof -i:1982 > /dev/null 2>&1 || ss -tlnp | grep -q 1982; then
  echo "服务已在运行 http://localhost:1982"
else
  cd ./paper && nohup python3 -m http.server 1982 > /tmp/paper-server.log 2>&1 &
  sleep 1
  echo "服务已启动: http://localhost:1982"
fi
```

### Step 6：告知用户

模式 A 回复示例：
```
✅ 报纸已生成（来源：AI 上一条回复）
📄 ./paper/index.html
🌐 http://localhost:1982
（若旧文件存在，已备份为 index-YYYYMMDD-HHMMSS.html）
```

模式 B 回复示例：
```
✅ 报纸已生成（来源：@notes.md）
📄 ./paper/index.html
🌐 http://localhost:1982
（若旧文件存在，已备份为 index-YYYYMMDD-HHMMSS.html）
```

---

## 关键设计原则

- **颜色极简**：仅用纸色底(#F5F0E8) + 黑/深灰文字 + 点缀色(深红 #8B0000)
- **多栏布局**：主体 2~3 栏，大标题跨全栏
- **字体清晰**：正文衬线体(Georgia/'Noto Serif SC')，标题黑体
- **报头装饰**：顶部报名、日期、期号，SVG 横线分隔
- **无外部依赖**：所有样式内联，离线可用

---

## 参考文件

- `references/layout.md` — 完整 HTML/CSS 模板和设计规范（**必读后再生成**）
