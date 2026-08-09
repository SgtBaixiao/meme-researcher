# meme-researcher/ — 规格与原型

网络梗考古研究员 subagent 的完整规格 + 报告页 UI 原型（仅娱乐用途）。

## 目录

```
meme-researcher/
├── SPECIFICATION.md                     # 完整规格（to-spec 模板）：问题/方案/22条用户故事/实现决策/测试决策/范围/备注
├── AI-AESTHETIC-STYLE.md                # 新增需求：训练 AI 特定美学风格的完整方法（五层风格记忆）
├── prototype/
│   └── meme-report-prototype.html       # 报告页 UI 原型：三种截然不同的方案（可切换）
└── README.md                            # 本文件
```

## 快速使用

- **原型**：双击打开 `prototype/meme-report-prototype.html`，底部悬浮栏切换三种风格；或地址栏 `?variant=a|b|c`。
- **规格**：阅读 `SPECIFICATION.md`，其中"Implementation Decisions"已锁定 5 项悬而未决问题（验证者/多义梗/知识库/梗图验证/娱乐边界）。
- **美学训练**：`AI-AESTHETIC-STYLE.md` 回答了"如何训练 AI 具有特定美学风格的 HTML 外观"——五层风格记忆（宣言→令牌→黄金样例→技能→评测闭环），含 7 步落地清单。

## 三方案定位（选型用）

> **已定稿（2026-08）**：统一改造为新 house-style（极简纸质·米白+橙·红分割线），见用户级 `house-style` 技能与 `meme-digger/templates/encyclopedia.css`。本原型仅供选型回顾。

| 方案 | 气质 | 适合 |
|---|---|---|
| A 百科经典 | 蓝白、可信、信息密度高（侧栏目录） | 默认百科页（现 make_report.py 模板的进化版） |
| B 杂志卡片 | 暖纸色、编辑感、横向时间轴、双栏 | 阅读体验优先、轻传播场景 |
| C 暗色档案馆 | 终端/霓虹、代码味、纵向时间线 | 极客/圈层向传播 |

## 关联

- 方法调研：`../meme-researcher-subagent-design.md`
- 现有实现：`~/.pi/agent/skills/meme-digger/`（脚本套件 + skill + HTML 生成器）

> 原型为扔弃型（prototype 技能规范）：选定方案后，将样式合并进 `meme-digger/templates/encyclopedia.css` 并淘汰本文件。
