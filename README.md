# meme-researcher

网络梗考古研究 Skill：整理起源、义项、评论区线索与传播时间线，交付带证据与来源的 HTML 草稿。

当前仓库提供 MSM 流程规范、依赖检查和证据文件校验。平台检索与 HTML 生成依赖 [meme-digger](https://github.com/SgtBaixiao/meme-digger)。跨调查索引自动合并、额外平台适配和视觉自动复核尚未实现。

## 使用

将本仓库放入目标宿主的 Skill 目录，读取 [SKILL.md](SKILL.md)。安装位置按宿主实际设置选择，pi 的独立研究员配置见 [运行说明](references/runtime.md)。

Python 3.10+，无外部 Python 依赖：

```bash
python3 scripts/check_research.py doctor --meme-digger /absolute/path/to/meme-digger
python3 scripts/check_research.py validate /absolute/path/to/evidence.json
python3 -m unittest discover -s tests -v
```

依赖检查确认文件齐备，平台访问情况由实际请求验证。证据校验检查结构、引用与已声明的来源链，事实核查和独立性复核仍由研究员完成。格式见 [证据契约](references/evidence-contract.md)。

研究结果可作为草稿交付审阅，明确保留未确认事项；用户复核与对外发布分别记录状态。Cookie 使用 meme-digger 的本地配置，运行资料不提交到仓库。

## 维护

当前使用入口是 SKILL.md 和 scripts；[references](references/README.md) 保存需求、设计、教学材料和页面原型。原规格中的 L0–L7 实际包含八个阶段，当前入口统一称 MSM 流程。

GitHub CI 在干净环境运行工具回归，检查当前使用文档的本地链接。MIT，作者 Sgt_BaiXiao。
