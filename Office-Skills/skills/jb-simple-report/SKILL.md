---
name: jb-simple-report
description: "金碧物业项目群工作简报生成技能。根据（每日更新）金碧工时及进展详情表.xlsx，生成每日工作简报Markdown文件。触发场景：(1)用户说'生成日报'、'生成工作简报'、'创建日报'；(2)用户提供Excel文件要求生成简报；(3)用户提到金碧项目日报、简报生成。"
license: MIT
---

# 金碧工作简报生成

根据工时明细表Excel生成每日工作简报Markdown文件。

## 输入文件

- `（每日更新）金碧工时及进展详情表.xlsx`
- 格式参考：同目录下 `spec-sample.md`

## 执行流程

### 1. 读取Excel

使用 conda Python + calamine 引擎读取（openpyxl有兼容性问题）：

```bash
/opt/miniconda3/bin/python -c "
import pandas as pd
df = pd.read_excel('（每日更新）金碧工时及进展详情表.xlsx', sheet_name='4月', engine='calamine', header=None)
"
```

### 2. 确定列索引

| 日期 | 列索引 |
|------|--------|
| 04-01 | col5 |
| 04-07 | col11 |
| 04-08 | col12 |
| 04-09 | col13 |
| ... | col = 日期 + 4 |

### 3. 提取数据

```python
for row in range(len(df)):
    col1 = df.iloc[row, 1]  # 姓名
    col3 = df.iloc[row, 3]  # 类目
    col_data = df.iloc[row, 列索引]  # 每日数据

    if col3 == '工作日报' and pd.notna(col_data):
        # 工作内容
    elif col3 == '风险卡点' and pd.notna(col_data):
        # 风险卡点
```

### 4. 归类板块

| 板块 | 人员 |
|------|------|
| 计费部分 | 邓金玉、凌有策、彭宗鑫、王永生、曾文峰 |
| 旅游部分 | 刘家同、周宇澄、曾文峰(旅游)、林坚贤 |
| 工单部分 | 侯海兵、朱铜、王朝晖、叶鸿杰 |
| 闪送部分 | 熊晓龙 |
| 现场管理协调 | 向琰恒、杨欢 |

### 5. 识别未提交人员

对比所有工作日报行，有日期列数据=已提交，无数据=未提交。

注意：熊峰名字灰色表示已离职，不计入未提交。

### 6. 输出格式

遵循 spec-sample.md 格式：
- 日期标题（`# MMDD 工作进展简报`）
- 各板块今日进展 + 预计明天工作
- 风险卡点
- 备注（请假等）
- 未提交日报人员

## 输出文件

保存到日报点目录：`03-金碧800-计费平台/日报点/YYYY-MM-DD.md`
