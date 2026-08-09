---
name: meme-researcher
description: 网络梗考古研究员（深挖版，subagent 化）。输入一个梗（最好带出现场景），执行七层 MSM 方法（意图澄清→平台路由→查询扩展→信源分级→评论区挖掘→时间线重构→交叉验证→合成），产出带证据链/时间线/梗图/来源介绍的单文件 Meme 百科 HTML。比 meme-digger 更深一层：跨调查索引、验证门、HITL 发布复核。依赖 meme-digger skill 的脚本套件。当用户需要更严谨、更深度的梗考古（多义梗消歧、时间线锚定、反讽识别）时使用。
license: MIT
compatibility: pi, Claude Code（Agent Skills 标准）
metadata:
  author: Sgt_BaiXiao
  version: "0.1.0"
  status: design-v1（规格已定稿，待实现）
  homepage: https://github.com/SgtBaixiao/meme-researcher
---

# Meme Researcher — 网络梗考古研究员

一个自动**网络梗考古研究员**：输入一个梗，自动完成"意图澄清 → 平台路由 → 多源检索 → 评论区挖掘 → 时间线重构 → 交叉验证 → 梗图收集 → 单文件百科 HTML"，全程把证据、上下文、产出物管理在**文件系统而非上下文窗口**里。

> 仅娱乐用途：不做热度预测、不做商业分析。

## 依赖

- **meme-digger skill**（脚本套件 + 9 步工作流）：先安装 meme-digger，本 skill 复用其 `scripts/`（bili_search / bili_comments / bili_memes / tieba_search / make_report 等）。
- 完整设计与规格：`references/` 目录（见文末）。

## 七层 MSM 方法（本 skill 的灵魂）

| 层 | 内容 | 关键动作 |
|---|---|---|
| L0 意图澄清 | **HITL，先于一切** | 问用户：在哪看到？什么平台？什么场景？什么时候？"它让你觉得好笑/奇怪/愤怒的点"？→ 产出查询词表 + 义项假设 |
| L1 平台路由 | 按起源倾向选首攻平台 | B站（扩散/评论共识，免登录✅）→ 贴吧（起源考据，需 cookie）→ 微博/知乎/KYM（降级/待验证） |
| L2 查询扩展 | 多义词必须消歧 | 原名/拼音缩写/英文/谐音/表情包关键词/话题标签 → 词表循环 |
| L3 信源分级 | 不把网友考证当事实 | 确凿（原始链接/时间戳）/ 网友考证 / 流传说法 / 待考证，四级标注 |
| L4 评论区挖掘 | 社区记忆的主战场 | 高赞=集体认知；专有名词=发散线索；争吵=争议点 |
| L5 时间线重构 | 精确到月 | 萌芽→爆发→消退，逐事件锚定信源 |
| L6 交叉验证 | ≥2 独立信源才写"确认" | 反讽/伪史论必须标注（语义反转是梗的常态） |
| L7 合成交付 | 单文件自包含 HTML | 起源/时间线/含义/例句/梗图图鉴/衍生/数据/信源/注意事项 |

## 工作区与交付

- 工作区：`meme-research/<梗名-slug>/`（00-计划 → 01-b站搜索 → 02-评论区 → 03-贴吧 → 04-发散线索 → 05-梗图 → 06-来源考证 → 报告 → 百科.html），沿用 meme-digger 的分文件结构。
- **跨调查索引**（本 skill 新增）：维护 `meme-index.json`，实现梗间互跳与去重（同梗多次调查时合并证据）。
- 最终交付：**单文件 Meme 百科 HTML**（make_report.py 生成，house-style 纸质风格）。

## 验证门（内建，不可跳过）

1. 每条关键论断带信源且链接可点开；事实/传闻/待考证分标注。
2. 至少 2 个独立信源一致才写"确认"。
3. 反讽/伪史论/黑色幽默内容标注"反讽"。
4. **HITL 发布复核**：报告完成 → 向用户展示证据链与"仍不确定"清单 → 用户确认后才算交付。
5. 多义梗：必须展示"按场景选择了哪个义项"及理由。

## 边界与安全

- 不传播谣言与恶意抹黑；争议内容只陈述"网络说法"并标注风险。
- 涉及低俗/违规梗：正常科普可以，不教唆、不美化、不过度展开。
- 梗图版权：只下载用于分析，报告中保留原图 URL 与出处。

## references（设计文档与原型）

- `references/meme-researcher-subagent-design.md` — 深度设计文档（问题建模：多义/时效/平台隔离/图文双模态/变体演化/语义反转/社区记忆；MSM 七层）
- `references/SPECIFICATION.md` — to-spec 完整规格（问题/方案/22 条用户故事/实现决策/测试决策）
- `references/AI-AESTHETIC-STYLE.md` — 五层风格记忆（宣言→令牌→黄金样例→技能→评测闭环）
- `references/RESEARCH.html` / `RESEARCH-TRAINING.html` — 调研与训练课程（知识来源：Anthropic multi-agent 研究系统等）
- `references/prototype/meme-report-prototype.html` — 报告页 UI 原型（三方案选型回顾）

> 实现状态：设计 v1 定稿，未实现。实现时以 meme-digger 为底座，把本 SKILL.md 的七层方法 + 验证门并入 agent 配置。
