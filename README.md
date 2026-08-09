# meme-researcher — 网络梗考古研究员（Agent Skill，设计 v1）

深挖版网络梗考古 skill：七层 MSM 方法 + 跨调查索引 + 验证门 + HITL 发布复核。依赖 meme-digger 的脚本套件。

> **状态：设计 v1 定稿，待实现。** 本仓库目前是完整规格 + 设计文档 + UI 原型；实现时以 [meme-digger](../meme-digger/) 为底座。

## 安装（实现后）

1. 安装 [meme-digger](../meme-digger/)（脚本套件底座）。
2. 复制本目录到 `~/.pi/agent/skills/meme-researcher/`（pi）/ `~/.claude/skills/meme-researcher/`（Claude Code）。
3. （pi）如需 subagent 化：按 `references/meme-researcher-subagent-design.md` 生成 `~/.pi/agent/agents/meme-researcher.md` 配置。

## 结构

```
meme-researcher/
├── SKILL.md                         # 七层 MSM 方法 + 验证门 + 工作区（入口）
└── references/
    ├── meme-researcher-subagent-design.md   # 深度设计文档（问题建模 + MSM）
    ├── SPECIFICATION.md                     # to-spec 完整规格（22 条用户故事）
    ├── AI-AESTHETIC-STYLE.md                # 五层风格记忆方法
    ├── RESEARCH.html / RESEARCH-TRAINING.html  # 调研与训练课程
    └── prototype/meme-report-prototype.html # 报告页 UI 原型
```

## 与 meme-digger 的关系

| | meme-digger | meme-researcher |
|---|---|---|
| 定位 | 单次调查工作流 | 研究员 subagent（更严谨/更深） |
| 方法 | 9 步刨根问底 | 七层 MSM + 跨调查索引 |
| 验证 | 质量标准清单 | 强制验证门 + HITL 发布复核 |
| 依赖 | 无 | 依赖 meme-digger 脚本 |

## License

MIT © Sgt_BaiXiao
