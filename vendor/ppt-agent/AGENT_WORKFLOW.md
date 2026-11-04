---
name: ppt-agent
description: 用户指定的 PPT 标准工作流（zengwenliang416/ppt-agent 的 Muse 适配版）：材料/主题 → 需求调研确认 → 素材收集 → 金字塔大纲规划（用户审批，Hard Stop）→ 逐页规划草稿 → Bento Grid 设计稿 + 逐页审查修复 → 交付 SVG + HTML 预览 + 演讲备注。用户给材料或主题要做 PPT、演示、汇报材料时默认且严格按此流程跑；风格不预设默认，在 Phase 2 需求确认时由用户确认、技能只推荐，输出 HTML/SVG 用户已接受。
---

# PPT Agent（用户钦定的 PPT 标准流程）

上游：https://github.com/zengwenliang416/ppt-agent （MIT，v1.0.0）。本文件是 ppt-forge 自包含版随包分发的适配副本，插件根＝ppt-forge 包内的 `vendor/ppt-agent/`（上游仓库原件不随包分发，要对照原文去 GitHub）。

完整原文工作流在 `references/workflow.md`（开工前必读，它是阶段细节的权威）；四个阶段智能体的角色定义在 `references/agents/`（research-core / content-core / slide-core / review-core）；共享注册表与参考在 `shared/`（`shared/index.json` 风格与提示词注册表、`shared/references/styles/*.yaml` 17 种风格、`shared/references/prompts/*.md`、`shared/assets/preview-template.html`）。

## 宿主映射（Claude 插件语义 → 本机）

| 原文 | 本机执行 |
| --- | --- |
| `Task(subagent_type="ppt-agent:X-core", prompt=...)` | `subagent.spawn`：把 `references/agents/X-core.md` 全文＋本次参数（run_dir、mode、slide_index 等）写进子代理任务说明 |
| `AskUserQuestion`（Hard Stop） | 在聊天里把问题/大纲摆出来并**停住等用户回复**，不回复不推进 |
| 插件根 `skills/_shared/...` | 本技能 `shared/...` |
| `RUN_DIR=openspec/changes/<change-id>` | `~/workspace/openspec/changes/<change-id>`，产物名与原文完全一致 |
| Gemini 审查（gemini CLI） | **走 AI Studio API，不用 CLI**：review-core 把审查提示词＋该页 SVG 全文拼成一个文本文件，用 ppt-forge 自带的 `tools/gemini_api.py ask --prompt-file <文件>` 调用（API Key 走环境变量 `GEMINI_API_KEY`，在 https://aistudio.google.com/apikey 自行申请），模型默认 `gemini-3-flash-preview`。`review_engine: gemini-api`，正常打分（加权 ≥7.0、布局 ≥6、可读性 ≥6 质量门照旧）。审查引擎在 Phase 6 开工前先由用户确认（默认推荐 Gemini）；API 调用失败（429/503/网络）时再按 ppt-forge SKILL.md 的多模型确认制停下问用户换哪个模型，不自作主张降级 |
| Phase 7 `open index.html` | 本机打不开用户浏览器：把 `output/` 整夹打包 zip 作为附件交付，并给出逐页 SVG 路径 |

## 用户已定的固定约定（覆盖原文的可选项）

- **风格由用户确认，技能只推荐**（2026-11-04 用户改定，覆盖原文 Phase 1 的风格选择方式）：没有预设默认风格；Phase 2 需求确认时列出候选风格＋技能推荐与理由，用户确认哪套用哪套，未经确认不锁定风格。用户显式指定风格或 `--brand-colors` 时视为已确认，照其执行。细则以 ppt-forge SKILL.md「固定约定」为准。
- **输出 HTML + SVG 可接受**（用户 2026-11-04 明确），不强求 PPTX；需要 PPTX 时再走 ppt-master 转制并向用户说明。
- **人只把关两处**：Phase 2 需求确认、Phase 4 大纲审批。其余（排版、配色、布局、配图、字段、图标）全部由流程自动完成，不再逐项问用户。（ppt-forge 层另有两处用户确认：Phase 6 开工前确认审查模型、Phase 8 生成 PPT 前的确认，以 ppt-forge SKILL.md 为准。）
- 用户把材料和需求给全时，Phase 2 先把能从材料推导的答案填好、只问缺口，但**确认动作不能省**。
- 大纲未经用户批准、`outline.json` 未写入 `"approved": true`，**禁止进入 Phase 5**。

## 七个阶段（细节以 references/workflow.md 为准）

1. **Init** — 解析 `--style/--brand-colors/--pages/--run-id`；生成 change-id 与 RUN_DIR；写 OpenSpec 脚手架（proposal.md / tasks.md / input.md）。带 `--run-id` 时按原文的断点规则续跑（先删孤儿 `slide-status.tmp.json`，只信校验过的 `slide-status.json`）。
2. **需求调研（Hard Stop）** — research-core 做背景调研 → `research-context.md`；向用户确认受众、目的、核心信息（3–5 条）、语气、特殊约束 → `requirements.md`。
3. **素材收集** — 按章节并行派 research-core（各自写 `materials-<slug>.md`，带上 research-context 避免重复），主会话串行合并为 `materials.md`。用户自带材料充足时，本阶段以整理用户材料为主、外部搜索为辅，并在 materials.md 里标明来源。
4. **大纲规划（Hard Stop）** — content-core 用金字塔原理（`shared/references/prompts/outline-architect.md`）产出 `outline.json` + `outline-preview.md`；把大纲以"目录＋每节页数＋每页标题/内容/重点"的形式给用户审批；用户要改 → content-core `mode=revise` 增量修改后重新呈批；批准后写 `"approved": true`。
5. **规划草稿** — content-core `mode=draft` 逐页出简版 SVG 到 `drafts/`，写 `draft-manifest.json`；每完成 3 页即可与 Phase 6 流水线重叠。
6. **设计稿 + 审查** — 每页必须走完 slide-core 设计（Bento Grid＋风格 token，`slides/slide-{nn}.svg`）→ review-core 审查（`reviews/review-{nn}.md`）→ 按建议类型路由修复（full_rethink 重出 ≤1 轮；layout_restructure / content_reduction 带 fixes_json ≤2 轮；attribute_change 定点补丁 ≤1 轮）。进度按原文原子写协议维护 `slide-status.json`。全部页审完才许做整体审查（review-core `mode=holistic` → `reviews/review-holistic.md`，只自动修 priority-1，最多重跑 1 次），最后汇总 `review-manifest.json`。质量门：加权 ≥7.0、布局 ≥6、可读性 ≥6（技术校验模式下以硬规则 pass/fail 为准）。
7. **交付（Hard Stop）** — 依 review-manifest 把终稿 SVG 收进 `output/`；用 `shared/assets/preview-template.html` 生成 `output/index.html`（标题、品牌标记、强调色、SLIDES_JSON 占位符按原文替换）；从 outline.json 的 notes 字段生成 `output/speaker-notes.md`（含总时长估算）；向用户汇报：总页数、风格、审查引擎、逐页分数/状态/修复轮次、警告页、整体分、平均分、输出路径与续跑命令。

## Fallback（原文规则，照守）

- 调研失败 → 只用用户需求继续，标注可信度下降。
- 素材部分失败 → 用已有素材继续。
- 某页审查修复到上限仍不过 → 接受并在交付汇总里标 `accepted_with_warning`。
- 不许跳过逐页审查直接整体审查或交付。
