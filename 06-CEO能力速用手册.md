---
title: CEO 能力速用手册（非开发型创始人）
version: V28.1
date: 2026-06-16
status: active
category: reference
author: williammacst
related: [CLAUDE.md, 4-step-workflow.md]
---

# CEO 能力速用手册

> 给"互联网产品 + 运营 + 项目管理 + 交付 + 创业者"身份的你。
> 核心痛点不是缺能力——18 plugins 几乎全装齐——而是**装了没用起来**。
> 用法：直接对 Claude 说下面"口语触发"那列的话即可。

---

## 一、你的价值链已落地度（V28.1 实测）

```
澄清优化 ✅  →  极限压榨 ✅  →  测试可用 ✅(已补产品级自证)  →  交付 ✅  →  归档 🟡(按需)
```

- **澄清**：模糊提示词自动评分优化（clarity_scorer hook），说话不用很精确
- **压榨**：说"火力全开/队长"→ 15 并发 + opus + 四步骨架自动编排
- **测试**：4-step Step4 Gate2.5 已增"产品级自证"——Web 自动截图、文档转 PDF 预览，你不看代码也能确认可用
- **归档**：重大成果按需归档到 `deliverables/`（不每任务 spam）

---

## 二、CEO 刚需能力 Top 10（都已装，照着说就能用）

| # | 你想干的事 | 直接对 Claude 说 | 背后能力 |
|---|---|---|---|
| 1 | 把想法/PRD 拆成可执行任务 | "把这个方案拆成 issues" | to-issues skill + github |
| 2 | 任务/项目落到 Notion | "把这些任务建到 Notion" | notion 插件 |
| 3 | 竞品/市场深度调研 | "深度调研一下 X 赛道，要多源验证" | deep-research（≥3 通道+≥2 源） |
| 4 | 生成 PPT/Word/Excel 商业材料 | "做一份融资路演 PPT" / "生成季度运营 Excel" | pptx/docx/xlsx + 品牌主题 |
| 5 | PRD/提案结构化共创 | "我们一起写这个产品的 PRD" | doc-coauthoring + product-manager-toolkit（RICE 优先级/访谈分析） |
| 6 | 定时自动化运营报表 | "每周一早 9 点自动汇总上周数据发我" | /schedule（cron 远程 agent） |
| 7 | 内部汇报/领导沟通文案 | "写一份给董事会的项目状态更新" | internal-comms skill |
| 8 | 笔记/碎片 → 可发布文章 | "把这堆笔记整理成一篇对外稿，去掉 AI 味" | writing-shape + humanize-chinese |
| 9 | 产品 Demo/落地页原型 | "快速做一个这个功能的可点击原型" | prototype / web-artifacts-builder |
| 10 | 个人知识库沉淀检索 | "把这次决策存进知识库" / "我之前关于 X 的笔记呢" | obsidian-vault + qmd 本地语义搜索 |

---

## 三、3 个高频组合拳（口语直接说）

1. **"队长，调研 X + 出对比表 + 做成 PPT"** → deep-research → 结构化分析 → pptx，一条龙
2. **"队长，把这个 PRD 拆 issues 建到 Notion，每周跟进"** → to-issues → notion → /schedule
3. **"火力全开，做个 X 的 MVP，做好测试可用了再告诉我"** → 四步骨架全开 + Gate2.5 产品级自证

---

## 四、别做的（避免过度工程）

- 不再装新 MCP/插件（已够用，多装只增启动失败面）
- 不给每个任务都强制归档（noise；重大成果才归档）
- 不自己看代码验证——让 Claude 跑起来截图自证（Gate2.5）
