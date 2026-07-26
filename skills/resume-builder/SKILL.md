---
name: resume-builder
description: 从零生成或全面优化一份中文简历，并导出 docx / pdf / markdown 多种格式。用 STAR 法则改写经历、做 ATS 关键词覆盖率检查、根据行业（互联网产品 / 技术 / 金融 / 通用）选模板。当用户说"帮我写简历 / 优化简历 / 简历不会写 / 我的简历太弱了 / 简历看起来不专业 / 简历改一改 / 给我做个简历模板 / 简历导出 / 简历加点关键词"，或者上传 .pdf/.docx 简历后说"看看怎么改"时，必须触发本 skill。即使用户只问"我的简历有什么问题"也要触发。
---

# Resume Builder（简历生成与优化）

这个 skill 干三件事：

1. **结构化生成**：从用户经历产出一份符合中文求职市场审美的简历
2. **STAR 法则改写**：把"参与了 X"这种弱句子，改写成"通过 X 实现 Y，结果 Z"
3. **ATS 关键词优化 + 多模板导出**：保证简历能过自动筛选，并支持 docx/pdf/md

不做：JD 定向改写（那是 jd-resume-tailor 的事，请在那里做"针对某 JD 改简历"）

---

## 何时触发

- "帮我写一份简历"
- "我的简历太弱了 / 没有亮点 / 看起来不专业"
- "把这段经历用 STAR 改一下"
- "简历里关键词够不够"
- "导出 PDF / docx 简历"
- 用户上传简历但没明确说"针对某 JD 改" → 触发本 skill；如果说了"针对 X 公司 / X 岗位改" → 调用 jd-resume-tailor

---

## 工作流

### Step 1: 摸清简历当前状态

如果用户**有简历文件**（.pdf / .docx / .md / .txt）：
- pdf 走 pdf skill 解析
- docx 走 docx skill 解析
- 提取出：基本信息、教育、工作经历、项目经历、技能、其他

如果用户**没有简历**：
- 用 AskUserQuestion 收集信息（参考 `references/intake_questions.md` 里的问题清单）
- 一次问 3~4 个问题，分轮收集，避免劝退

### Step 2: 选模板

读取 `references/templates/` 决定结构：

- 互联网产品 / 运营 / PM → `templates/internet.md`
- 技术 / 研发 / 数据 → `templates/tech.md`
- 金融 / 咨询 / 商科 → `templates/finance.md`
- 通用 / 跨行业 → `templates/general.md`

如果用户没指定方向，用通用模板，但**询问一句**："你下一步主要往什么方向投？我可以用更适合那个方向的版式。"

### Step 3: 用 STAR 改写每段经历

读取 `references/star_rewrite_guide.md`，对每条工作 / 项目经历做 STAR 改写。

**STAR 不是死板的四段式**，而是确保每条 bullet 都有：
- **背景信号**（一句话点出问题大小或情境）
- **动作**（你具体做了什么，要有动词）
- **结果**（数字 / 百分比 / 排名 / 规模）

如果用户提供的信息里**没有数字**，要主动追问："这个项目用户量大概是多少？""这个优化大概提了多少？记不准的话给个量级也行。"

### Step 4: ATS 关键词检查

调用脚本：

```bash
python scripts/ats_check.py --resume <resume.md> \
    --industry internet \
    [--jd <jd.txt>]
```

脚本会：
1. 抽取简历里的关键词
2. 对照行业关键词库（来自 job-intent-tracker 或本 skill 的 `references/keywords/`）
3. 输出"已覆盖 / 建议补充"两个清单
4. 给出 ATS 友好度评分（字体单一性、表格使用、特殊符号、图片等）

**ATS 友好的硬规则**：
- 不要用 word 表格放经历（很多 ATS 解析不了）
- 不要把日期放在装饰性图片里
- 不要写两栏布局（有些 ATS 会按列读，导致顺序混乱）
- 不要插图标 / emoji 在标题里
- 字体用宋体 / 思源宋体 / Arial / Helvetica 之一

### Step 5: 多格式导出

读取 `references/export_guide.md`，按用户需求选择：

**docx 导出**（最通用，国内 HR 优先要 docx）：
- 调用 docx skill
- 用 `assets/resume_template.docx` 作为模板（如果存在）

**pdf 导出**（最终投递版）：
- 推荐流程：先 docx → 再用 word/libreoffice 转 pdf
- 直接生成 pdf 用 reportlab 比较丑，不推荐
- 调用 pdf skill 做后处理（加密 / 元数据清理）

**markdown 导出**（备份 + GitHub）：
- 直接写 .md 文件即可

**默认行为**：除非用户指定，同时输出 docx + md 两个版本。

### Step 6: 自检 & 反馈

输出后做一次自检（写到聊天里给用户看，不用单独存文件）：

```
✓ 长度：< 1 页（应届）/ ≤ 2 页（社招）
✓ 联系方式齐全（手机 + 邮箱，可选 GitHub/作品集）
✓ 每段经历都有量化结果
✓ 关键词覆盖率（vs <industry> 行业库）：__%
✓ ATS 友好度：__/10
⚠ 待用户确认：<还需要补的信息>
```

---

## 反模式（不要做）

- ❌ 帮用户编数字（说"提升 30%"但用户根本没说过）—— 必须基于用户提供的信息，不知道就标 `[待补充：具体数字]`
- ❌ 用形容词堆砌（"具有出色的沟通能力" "认真负责" "有上进心"）—— 删掉
- ❌ 一段经历写超过 5 条 bullet —— 太密会被 HR 跳过
- ❌ 写"自我评价"长篇 —— 国内现在不流行，1~2 行 summary 即可
- ❌ 把所有公司都写一样的 bullet 数 —— 重要的多写，次要的少写
- ❌ 把"熟悉 / 了解 / 会用"当能力描述 —— 改成"用 X 做了 Y"

## 与其他 skill 的协作

- 用户接着说"针对这家公司改一下" → 转 `jd-resume-tailor`
- 用户接着说"准备面试" → 转 `interview-prep`
- 用户没确定方向就来改简历 → 先反问"你打算投什么方向？"，必要时转 `job-intent-tracker`

---

## Cross-References / 技能联动

| Skill | 何时改用 |
|---|---|
| [`../docx/`](../docx/SKILL.md) | 规范 Z.AI docx 技能 —— JS/docx-js 流水线，含 7 种封面 recipe（R1–R7）、`scenes/resume.md` 简历场景、`postcheck.py` 14 项自动校验。当需要在简历生成阶段精细控制字体/段落/缩进/Heading 层级时改用。 |
| [`../pdf/`](../pdf/SKILL.md) | 规范 Z.AI pdf 技能 —— 四条产线（Report/Creative/Academic/Process），含 `briefs/resume.md` ATS-safe 简历模板与 `briefs/creative-fixed-canvas.md` 创意行业简历子路径。当需要 ATS-safe PDF 或创意行业视觉简历时改用。 |
| [`../minimax-docx/`](../minimax-docx/SKILL.md) | C#/.NET OpenXML SDK 流水线，含 `Samples/AestheticRecipeSamples.cs` 13 种风格 recipe（含 ModernCorporate、ExecutiveBrief）。当需要在 .NET 端精细控制简历排版时改用。 |
| [`../minimax-pdf/`](../minimax-pdf/SKILL.md) | Token-based 设计系统 PDF 流水线，含 `resume` 文档类型（typographic 封面 + DM Serif Display）。当需要设计感强的 PDF 简历时改用。 |
| [`../jd-resume-tailor/`](../jd-resume-tailor/SKILL.md) | 针对特定 JD 改写简历 —— 当用户明确说"针对 X 公司 / X 岗位改简历"时改用，而非本技能的"通用简历优化"。 |

### 跨技能共享规则

- **格式选择**：中文求职市场默认 DOCX（HR 系统友好）；外企 / 创意行业默认 PDF（视觉一致性）；ATS 强约束场景用 ATS-safe 单列 PDF（`pdf` 技能的 `briefs/resume.md`）。
- **STAR 法则统一**：所有简历技能（本技能、`jd-resume-tailor`、`docx` 的 `scenes/resume.md`、`pdf` 的 `briefs/resume.md`）都使用 STAR 法则改写经历 —— "通过 X 实现 Y，结果 Z"。不可仅替换为动词开头却无量化结果。
- **ATS 关键词覆盖率**：所有 ATS-friendly 简历必须显式做关键词覆盖率检查，并报告命中率与缺失关键词。仅靠"看起来专业"不算 ATS 通过。
- **多格式导出**：当用户要求"导出 PDF / docx 简历"时，必须同时输出可下载文件，不可只输出 Markdown。
