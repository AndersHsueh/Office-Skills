# answer2paper Layout 规范

## 色彩系统（极简）

```css
--paper-bg:     #F5F0E8;   /* 纸张底色 */
--ink-primary:  #1A1A1A;   /* 主文字色 */
--ink-secondary:#4A4A4A;   /* 次级文字 */
--ink-light:    #888888;   /* 辅助/注释 */
--accent:       #8B0000;   /* 点缀色：深红（仅用于报头、引言线、分类标签） */
--rule-color:   #C8BFA8;   /* 分割线颜色 */
--column-gap:   2.2rem;
```

禁止使用其他颜色。背景一律 `--paper-bg`，不加 box-shadow 或渐变。

---

## HTML 完整模板

以下是生成 `index.html` 的基础结构，**根据实际内容填写 {{占位符}}**：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{HEADLINE}} — Daily Brief</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;700&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --paper-bg:    #F5F0E8;
    --ink-primary: #1A1A1A;
    --ink-secondary:#4A4A4A;
    --ink-light:   #888888;
    --accent:      #8B0000;
    --rule-color:  #C8BFA8;
    --col-gap:     2.2rem;
  }

  body {
    background: var(--paper-bg);
    color: var(--ink-primary);
    font-family: 'Noto Serif SC', Georgia, 'Times New Roman', serif;
    font-size: 15px;
    line-height: 1.7;
    max-width: 1100px;
    margin: 0 auto;
    padding: 2rem 2.5rem 4rem;
  }

  /* ── 报头 Masthead ── */
  .masthead {
    text-align: center;
    border-top: 3px solid var(--ink-primary);
    border-bottom: 1px solid var(--ink-primary);
    padding: 0.6rem 0 0.5rem;
    margin-bottom: 0.3rem;
  }
  .masthead-meta {
    display: flex;
    justify-content: space-between;
    font-size: 11px;
    color: var(--ink-light);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: 0.05em;
    margin-bottom: 0.2rem;
  }
  .masthead-name {
    font-size: 2.8rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.1;
    font-family: 'Noto Serif SC', Georgia, serif;
  }
  .masthead-tagline {
    font-size: 11px;
    color: var(--ink-light);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-top: 0.2rem;
    font-family: 'Helvetica Neue', Arial, sans-serif;
  }

  /* ── SVG 装饰横线 ── */
  .rule-ornament {
    width: 100%;
    height: 12px;
    margin: 0.4rem 0;
    display: block;
  }

  /* ── 主标题区 Hero ── */
  .hero {
    border-bottom: 2px solid var(--ink-primary);
    padding-bottom: 1rem;
    margin-bottom: 1.2rem;
  }
  .hero-kicker {
    font-size: 11px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.4rem;
  }
  .hero-headline {
    font-size: 2.4rem;
    font-weight: 700;
    line-height: 1.15;
    letter-spacing: -0.02em;
    margin-bottom: 0.6rem;
  }
  .hero-subhead {
    font-size: 1.05rem;
    color: var(--ink-secondary);
    line-height: 1.5;
    max-width: 72ch;
  }
  .hero-byline {
    margin-top: 0.5rem;
    font-size: 11px;
    color: var(--ink-light);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: 0.05em;
  }

  /* ── 多栏布局 ── */
  .columns-3 {
    column-count: 3;
    column-gap: var(--col-gap);
    column-rule: 1px solid var(--rule-color);
  }
  .columns-2 {
    column-count: 2;
    column-gap: var(--col-gap);
    column-rule: 1px solid var(--rule-color);
  }

  /* ── 文章块 Article ── */
  .article {
    break-inside: avoid;
    margin-bottom: 1.4rem;
  }
  .article-label {
    font-size: 10px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    border-top: 2px solid var(--accent);
    padding-top: 0.3rem;
    margin-bottom: 0.4rem;
    display: inline-block;
  }
  .article h2 {
    font-size: 1.15rem;
    font-weight: 700;
    line-height: 1.3;
    margin-bottom: 0.4rem;
    letter-spacing: -0.01em;
  }
  .article h3 {
    font-size: 0.95rem;
    font-weight: 700;
    margin: 0.7rem 0 0.2rem;
  }
  .article p {
    font-size: 0.92rem;
    line-height: 1.75;
    margin-bottom: 0.5rem;
    text-align: justify;
    hyphens: auto;
  }
  .article ul, .article ol {
    padding-left: 1.2em;
    margin-bottom: 0.5rem;
  }
  .article li {
    font-size: 0.9rem;
    line-height: 1.65;
    margin-bottom: 0.15rem;
  }

  /* ── 引言 Pull Quote ── */
  .pull-quote {
    border-left: 3px solid var(--accent);
    padding: 0.5rem 0.8rem;
    margin: 1rem 0;
    break-inside: avoid;
  }
  .pull-quote p {
    font-size: 1.05rem;
    font-style: italic;
    line-height: 1.5;
    color: var(--ink-secondary);
  }

  /* ── 要点框 Fact Box ── */
  .fact-box {
    border: 1px solid var(--rule-color);
    padding: 0.7rem 0.9rem;
    margin: 1rem 0;
    break-inside: avoid;
  }
  .fact-box-title {
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    color: var(--ink-light);
    margin-bottom: 0.4rem;
  }
  .fact-box li {
    font-size: 0.88rem;
    line-height: 1.6;
  }

  /* ── 横跨全栏的分节标题 ── */
  .section-break {
    column-span: all;
    border-top: 1px solid var(--rule-color);
    border-bottom: 1px solid var(--rule-color);
    padding: 0.3rem 0;
    margin: 1.2rem 0;
    font-size: 10px;
    font-family: 'Helvetica Neue', Arial, sans-serif;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--ink-light);
    text-align: center;
  }

  /* ── 页脚 ── */
  footer {
    border-top: 2px solid var(--ink-primary);
    margin-top: 2rem;
    padding-top: 0.5rem;
    font-size: 10px;
    color: var(--ink-light);
    font-family: 'Helvetica Neue', Arial, sans-serif;
    display: flex;
    justify-content: space-between;
  }

  /* ── 响应式 ── */
  @media (max-width: 768px) {
    .columns-3, .columns-2 { column-count: 1; }
    .hero-headline { font-size: 1.8rem; }
    .masthead-name { font-size: 2rem; }
    body { padding: 1rem 1.2rem 3rem; }
  }
  @media (max-width: 480px) {
    body { font-size: 14px; }
  }

  code {
    font-family: 'Courier New', monospace;
    font-size: 0.85em;
    background: rgba(0,0,0,0.06);
    padding: 0.1em 0.3em;
    border-radius: 2px;
  }
  pre {
    background: rgba(0,0,0,0.05);
    padding: 0.8rem;
    overflow-x: auto;
    font-size: 0.82rem;
    line-height: 1.5;
    border-left: 2px solid var(--rule-color);
    margin: 0.5rem 0;
  }
  pre code { background: none; padding: 0; }
  
  strong { font-weight: 700; }
  em { font-style: italic; }
  a { color: var(--ink-primary); text-decoration: underline; text-underline-offset: 2px; }
</style>
</head>
<body>

<!-- 报头 -->
<header class="masthead">
  <div class="masthead-meta">
    <span>{{DATE_FULL}}</span>
    <span>AI · ANSWER2PAPER</span>
    <span>Vol. 1</span>
  </div>
  <div class="masthead-name">Daily Brief</div>
  <div class="masthead-tagline">Knowledge · Clarity · Depth</div>
</header>

<!-- SVG 装饰线 -->
<svg class="rule-ornament" viewBox="0 0 800 12" xmlns="http://www.w3.org/2000/svg">
  <line x1="0" y1="6" x2="340" y2="6" stroke="#C8BFA8" stroke-width="1"/>
  <rect x="345" y="2" width="8" height="8" fill="#8B0000" transform="rotate(45 349 6)"/>
  <line x1="355" y1="6" x2="445" y2="6" stroke="#8B0000" stroke-width="1"/>
  <rect x="447" y="2" width="8" height="8" fill="#8B0000" transform="rotate(45 451 6)"/>
  <line x1="457" y1="6" x2="800" y2="6" stroke="#C8BFA8" stroke-width="1"/>
</svg>

<!-- 主标题区 -->
<section class="hero">
  <div class="hero-kicker">{{KICKER}}</div>
  <h1 class="hero-headline">{{HEADLINE}}</h1>
  <p class="hero-subhead">{{SUBHEADLINE}}</p>
  <div class="hero-byline">{{BYLINE}} · {{DATE_SHORT}}</div>
</section>

<!-- 正文多栏 -->
<main class="columns-3">

  <!-- 示例：普通文章块 -->
  <article class="article">
    <span class="article-label">{{SECTION_LABEL}}</span>
    <h2>{{SECTION_TITLE}}</h2>
    <p>{{SECTION_BODY}}</p>
  </article>

  <!-- 示例：引言块 -->
  <div class="pull-quote">
    <p>{{PULL_QUOTE_TEXT}}</p>
  </div>

  <!-- 示例：要点框 -->
  <div class="fact-box">
    <div class="fact-box-title">关键要点</div>
    <ul>
      <li>{{FACT_1}}</li>
      <li>{{FACT_2}}</li>
    </ul>
  </div>

  <!-- 跨栏分节线 -->
  <div class="section-break">{{SECTION_BREAK_LABEL}}</div>

  <!-- 更多文章块继续... -->

</main>

<!-- 页脚 -->
<footer>
  <span>Generated by answer2paper</span>
  <span>{{DATE_FULL}}</span>
  <span>http://localhost:1982</span>
</footer>

</body>
</html>
```

---

## 内容映射规则

| 占位符 | 填写规则 |
|--------|----------|
| `{{HEADLINE}}` | Markdown 第一个 H1，或前 20 字概要 |
| `{{KICKER}}` | 主题词，如"技术分析 / 知识总结 / 方案设计" |
| `{{SUBHEADLINE}}` | 第一段的关键句，不超过 60 字 |
| `{{BYLINE}}` | 固定 "AI · answer2paper" |
| `{{DATE_FULL}}` | 完整日期，如 "2026年3月15日 星期日" |
| `{{DATE_SHORT}}` | "2026-03-15" |
| `{{SECTION_LABEL}}` | 章节类型标签，如 "核心概念 / 操作步骤 / 注意事项" |
| `{{PULL_QUOTE_TEXT}}` | 从原文提取的最精彩一句话（1~2 句） |
| `{{FACT_N}}` | 列表项或数据点 |
| `{{SECTION_BREAK_LABEL}}` | 如 "深度分析 · Continued" |

---

## 排版策略

### 当内容有明显章节（多个 H2/H3）
- 每个 H2 → 一个 `<article>` 块
- H3 → 块内 `<h3>` 子标题
- 列表 → 直接 `<ul>/<ol>`
- 代码块 → `<pre><code>`

### 当内容是连续段落
- 前 2 段 → hero subheadline + 第一栏首段
- 中间段落 → 按自然段分配到各栏
- 提取 1~2 个关键句 → pull-quote

### 当内容含大量列表
- 前几项 → fact-box（"关键要点"）
- 其余 → article 内普通列表

### 栏数选择
- 内容 < 300 字 → 2 栏
- 内容 300~800 字 → 3 栏
- 内容 > 800 字 → 3 栏 + 多个 section-break

---

## 禁止事项

- ❌ 不加背景图片或纹理图
- ❌ 不用蓝色、绿色、紫色等彩色
- ❌ 不加圆角 > 2px 的卡片
- ❌ 不加 box-shadow
- ❌ 不引用外部图片（img 标签）
- ❌ 不使用 CDN 字体以外的资源（字体失败时 Georgia 兜底）
