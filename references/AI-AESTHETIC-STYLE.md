# 如何训练 AI 具有特定美学风格的 HTML 外观设计

> 需求来源：训练 agent，使其产出的 HTML 外观具有固定的特定美学风格。
> 适用范围：pi agent harness（meme-researcher 及其报告页、任意 HTML 产物）。
> 本文回答"如何做"——给出可直接落地的方法，并说明何时不需要（也不需要）模型微调。

---

## 0. 核心理念：对 agent 而言，"训练"= 可复用的风格记忆

模型微调（fine-tune）是重武器：要造数据集、跑 GPU、维护多版本，且一旦想换风格就要重训。对运行在 harness 里的 agent（如 pi）来说，**同样效果几乎总能通过"分层风格记忆"达成**——把美学编码进 agent 可持续读取的资产里，每次生成时自动加载。收益：可即时迭代、可多风格并存、成本为零。

> 类比：不是教 AI"学会画画"，而是给 AI 一本**必读的设计手册 + 若干黄金范例**，并让它每次动笔前翻手册。

## 1. 五层风格记忆架构（由浅入深）

### L1 美学宣言（Aesthetic Statement）—— 用语言锁定气质
一段精确的自然语言，定义：整体气质、情绪、参照物、硬性禁忌。

```markdown
## 美学宣言（示例："暗色档案馆"）
气质：冷峻、档案感、克制；像深夜的地下数据库，不讨好、但可靠。
参照：BBS 老终端、NASA 任务手册、黑胶封套。
情绪：好奇、庄严、微妙的幽默。
禁忌：不用渐变糖果色；不用圆角大卡片；不用 emoji 做装饰；
      标题一律大写+等宽字体；间距宁大勿小。
```

**要点**：写"禁忌"比写"要什么"更有效——模型对禁止项的执行力显著高于抽象描述。

### L2 设计令牌（Design Tokens）—— 把美学变成可校验的数据
颜色/字体/字号/间距/圆角/阴影/动效，全部结构化为 JSON（或 CSS 变量）。这是 AI 最容易精确执行、也最容易被回归检查的一层。

```json
{
  "tokens": {
    "color.bg": "#0b0d14",
    "color.surface": "#0e1220",
    "color.line": "#2c3450",
    "color.ink": "#d7dce6",
    "color.accent": "#a855f7",
    "color.accent-2": "#8fd3ff",
    "font.mono": "ui-monospace, Consolas, 'PingFang SC', monospace",
    "radius": "0px",
    "space": 8,
    "shadow": "none",
    "motion": "100ms ease-out"
  }
}
```

### L3 黄金样例（Gold Examples）—— 给 AI 看"长什么样"
2-5 个**完整的、获奖级** HTML 参考文件（带注释：哪个 token 用在哪个属性、为什么）。few-shot 的效果远胜任何文字描述——模型模仿样例的能力是它最强的能力之一。

```
aesthetic/gold/
├── 01-archive-dashboard.html   # 参考1：数据页
├── 02-archive-article.html     # 参考2：长文页（本项目的报告页即此类）
└── 03-archive-error-page.html  # 参考3：小元素
```

每个样例头部注释写明：`本页示范：<tokens 子集> | 章节锚点结构 | 断点行为`。

### L4 技能化包装（Skill-ification）—— 装进 harness 的渐进披露机制
把 L1-L3 打包成一个 **pi skill**（与 meme-digger 同级）：

```
~/.pi/agent/skills/<美学名>/            # 例：aesthetic-archive-dark
├── SKILL.md          # 美学宣言 + 用法规范（何时调用、如何用 tokens/样例）
├── tokens.json       # L2 设计令牌
└── gold/             # L3 黄金样例（3 个 HTML）
```

agent 每次设计 HTML 前 `read` 该 SKILL.md（渐进披露：描述常驻、细节按需加载），
并强制："必须从 tokens.json 取值，不得自创颜色/字体；布局对照 gold/ 样例"。
**这就构成了"训练"：风格成为 agent 每次工作前的必读上下文。**

### L5 评测闭环（Eval Loop）—— 让风格越用越准
- **评分卡**：每次产出后按 5 项打分（气质符合 / 令牌合规 / 布局节奏 / 响应式 / 禁忌零违例），由用户或复核 subagent 打。
- **回归检查（可脚本化）**：检查产出的 CSS 里是否出现 tokens.json 之外的色值/字号/圆角；不合格即拒收。
- **迭代**：连续 3 次低分 → 更新美学宣言/补黄金样例（"用新样例说话"，别只改措辞）。
- 这是闭环：风格记忆随使用进化，不需要重训模型。

## 2. pi harness 的具体落地方式（从轻到重）

| 方式 | 位置 | 适用 |
|---|---|---|
| 技能 | `~/.pi/agent/skills/<美学名>/`（全局）或项目 `.pi/skills/` | **推荐**：设计任务时自动/手动加载 |
| Prompt 模板 | `~/.pi/agent/prompts/*.md` → `/设计页` | 需要人触发、带参数注入 |
| 常驻偏好 | 项目 `.pi/APPEND_SYSTEM.md`（信任后加载） | 希望"默认气质"全局生效 |
| Agent 配置 | `~/.pi/agent/agents/*.md` frontmatter/正文 | 绑定到具体 subagent（如 meme-researcher 专属 house style） |
| 扩展（自定义工具） | `~/.pi/extensions/` | 做"令牌合规 lint"等自动检查工具 |

**推荐组合**：技能（L4 主载体）+ 绑定到 meme-researcher 的 agent 规范（强制调用）+ 评分卡（L5）。

## 3. 与 meme-researcher 的结合（本次落地建议）

报告页三方案原型（`prototype/meme-report-prototype.html`）正好可以当"选美"素材：

1. **选定 house style**：A/B/C 三方案择一（或混合），把该方案的 CSS 提炼为 tokens.json + 黄金样例。
2. **打包为美学技能**：如 `aesthetic-encyclopedia`，SKILL.md 引用原型为黄金样例。
3. **绑定**：meme-researcher 规范加一句"报告页必须按 <美学名> 技能产出"。
4. **替换模板**：`meme-digger/templates/encyclopedia.css` 改为从 tokens.json 生成，保证"训练所得"即"模板所现"。
5. **回归**：make_report.py 产物跑令牌合规检查。

## 4. 何时才需要真正的模型微调？（以及为什么这里不需要）

微调只在以下情况值得：风格极其抽象（无法用语言+样例描述）、需要模型"内化"而非"查阅"、推理阶段不能加载上下文（如离线 API）。对本项目（agent 场景、产物是 HTML、有上下文可加载）——**五层风格记忆已足够且更优**。若未来真要微调：LoRA 微调在 HTML/CSS 语料上，数据集形态为 `(设计任务描述 → 符合风格的 HTML)`，成本高、维护重，非必要不启动。

## 5. 从今天就能做的 7 步清单

1. 从三方案原型里挑出目标风格（或写你自己的美学宣言）。
2. 写 L1 宣言（30 分钟，禁忌优先）。
3. 把宣言中的颜色/字体/间距抽成 L2 tokens.json（可复用现有原型 CSS 变量）。
4. 挑 2-3 个原型/成品页做黄金样例，头部加注释。
5. 建技能目录（SKILL.md + tokens.json + gold/）。
6. 在 meme-researcher agent 规范里绑定该技能。
7. 首次产出后打评分卡，迭代 2-3 轮。
