# 研究员运行说明

本仓库的 Skill 可直接加载。独立研究员配置是可选载体，具体工具名单由目标宿主提供，不假定每个宿主都有 web_search 或 web_fetch。

在 pi 的 agent 配置中设置名称、说明和实际可用的工具；省略 model 即沿用宿主选择。系统提示词指向 meme-researcher 的实际 SKILL.md 路径，要求先做依赖检查。外部检索资料保持原文并作为证据数据处理。

独立研究员返回工作区路径、报告路径、已查范围和待核实清单。需要用户补充场景时返回 `needs-clarification`，主会话负责澄清；草稿状态使用 `draft`，用户复核后使用 `reviewed`，收到对外发布指令后才使用 `published`。

原始配置草案在 [设计文档](meme-researcher-subagent-design.md) 中，属于历史设计。以本说明和当前 SKILL.md 的能力范围为准。
