---
name: ppt-forge
description: PPT 全流程融合技能·自包含版（ppt-agent 干活主体 × 多模型审核 × ppt-master 只取转制，全部组件随包 vendor 分发，装这一个包即可，不需要再装 ppt-agent / ppt-master）：材料/主题 → 需求确认（用户把关）→ 大纲规划（用户审批 Hard Stop）→ ppt-agent 逐页 SVG 生成 → 逐页审查修复＋整体审查（审查引擎在 Phase 6 开工前先由用户确认：默认推荐 Gemini，备选 Grok / 豆包 / DeepSeek / 其它 Gemini 模型 / Muse 自审；选定引擎中途不通时再停下问用户换哪个）→ Phase 7 组装并交付 SVG 包 → Phase 8 生成 PPT：转制原生可编辑 PPTX（包内 vendor 的 svg_to_pptx 转制链）前先请用户确认，不直接生成 → 双交付（SVG 包＋PPTX，含演讲备注）。用户要做 PPT、演示、汇报材料时默认且严格按此流程跑；风格不预设默认，在需求确认时由用户确认，技能只给推荐。用户给参考 PPT／截图／色板说「加一套风格」时，不走做 PPT 流程，按本技能「添加自定义风格」指令实测提取参数、建风格文件、完成注册并出样张验证。团队安装与依赖见包内 README.md。
---

# PPT Forge（PPT 锻造坊 · 全融合自包含版）

2026-11-04 用户拍板融合定名；同日升级为自包含版：**ppt-agent 的工作流、ppt-master 的转制链、审查小工具全部 vendor 进本包**，团队成员只装 ppt-forge 一个包就能跑全流程，不再单独装 ppt-agent / ppt-master。归属与许可证见 `vendor/NOTICE.md`。

## 路径与本地映射（开工先定这四个变量）

- `FORGE`＝本技能目录（本文件所在目录）。下文所有包内路径都相对它，**不要再去引用包外的 ppt-agent / ppt-master 安装**。
- `PY_PPTX`＝装了 python-pptx 的 python。团队机：`pip install -r <FORGE>/requirements.txt` 后的 `python3`；发起人本机：`~/workspace/tools/pptx-venv/bin/python`。
- `RUN_DIR`＝`~/workspace/openspec/changes/<change-id>`（工作区产物目录约定）。
- Gemini 审查调用＝`python3 <FORGE>/tools/gemini_api.py`，API Key 走环境变量 `GEMINI_API_KEY`（各自在 https://aistudio.google.com/apikey 申请；发起人本机亦可用其连接器 helper，等价替换）。

包内结构：
- `vendor/ppt-agent/`：干活主体的工作流原件——`AGENT_WORKFLOW.md`（宿主映射与阶段总纲）、`references/workflow.md`（阶段细节权威）、`references/agents/`（四角色）、`shared/`（18 种风格 YAML、提示词注册表、预览模板）
- `vendor/ppt-master/scripts/`：仅转制链脚本闭包（project_manager / svg_quality_checker / svg_to_pptx 及依赖）
- `vendor/ppt-master/LICENSE`、`vendor/NOTICE.md`：许可证与归属
- `tools/gemini_api.py`（审查传输）、`tools/inject_notes.py`（备注注入）、`references/spec-lock-flat-template.md`（转制锁模板）

## 固定约定（用户口径，不可漂移）

- **风格由用户确认，技能只推荐**（2026-11-04 用户改定）：没有预设默认风格，不许跳过风格确认。Phase 2 需求确认时，把风格作为确认项之一摆给用户：列出候选（business 通用商务、thinkway 九慧公司风，必要时加其余适用风格），并给出技能推荐＋一句理由（按材料性质判断，如公司材料／对外场合优先推荐 thinkway，一般商务汇报推荐 business）；**用户确认哪套就用哪套，未经确认不锁定风格、不开生成**。用户在委托时已点名风格的，视为已确认，照其点名执行。
- 可选风格 `thinkway`（`--style=thinkway`，2026-11-04 用户拍板加入）：上海九慧（Thinkway）公司风，参数实测自公司介绍 PPT（青蓝 #117598＋金黄 #FFC000、微软雅黑、直角扁平卡片）。风格文件 `vendor/ppt-agent/shared/references/styles/thinkway.yaml` 已注册进包内 index.json；其 `brand_furniture` 段是 YAML 代币之外的家具规范——**用 thinkway 时必须照它逐页绘制**：内容/目录/数据页的顶部双色条（蓝长段＋金短段）、标题下细线、页脚细线＋左下 Thinkway 字标（资产在 `vendor/ppt-agent/shared/assets/thinkway/`）＋页码＋右下公司名；封面/尾页用组合标＋金色标语，不套条脚。在 Phase 2 作为候选向用户推荐（公司材料／对外场合优先推荐），由用户确认后才用。
- **人把关四步**：Phase 2 需求确认、Phase 4 大纲审批、Phase 6 开工前确认审查模型、Phase 8 生成 PPT 前的确认。其余阶段自动推进，不逐步请示。
- 用户给全材料时 Phase 2 先按材料推导填好、只问缺口，确认动作不能省。
- 材料没有的数据一律不编（钟点、量化指标、角色标签同理）。
- 交付＝**双份**：output/ 的 SVG 包（zip）＋转制后的原生 PPTX，两者都作附件交付。
- 审查分数必须标明引擎，不同引擎的分数不混报。

## 前半程：生成（ppt-agent 阶段）

严格按 `vendor/ppt-agent/AGENT_WORKFLOW.md` 与 `vendor/ppt-agent/references/workflow.md` 执行（RUN_DIR 结构、slide-status.json 原子写协议都在那边，本技能不复述）。

质量门（与审查量规一致）：加权 ≥7.0、布局 ≥6、可读性 ≥6、无 Critical；修复路由 full_rethink ≤1 轮、layout_restructure/content_reduction ≤2 轮、attribute_change ≤1 轮；全页审完才许整体审查，整体只自动修 priority-1、最多重跑 1 次。

审查：多模型制，用户确认（2026-11-04 用户定版；同日晚间改定为每趟开工前确认）：
- **Phase 6 开工前先确认审查模型（每趟必走，不确认不开审）**：把可选引擎摆给用户——默认推荐 **Gemini**（`tools/gemini_api.py ask --prompt-file <审查提示词+SVG全文>`，模型 `gemini-3-flash-preview`，**免费层约 20 次/天**；逐页「审查＋修复＋复审」约 3 次/页，先按页数算审查预算、页数多的先向用户说明额度安排）；备选见下池。用户点名哪个就用哪个审全程。
- **选定引擎中途不通或额度耗尽 → 停下来再问用户，不许自作主张换、也不许直接跳 Muse 自审**：由用户点名确认后才换，量规不变，分数标注实际引擎。备选池与接通状态（2026-11-04 在发起人环境验明；换机器/换时间须复验）：
  - 其它 Gemini 模型 — 同一 helper 换 `--model`，先 `models` 探活（2.5 代对新用户关闭、Pro 免费额度为 0，以实测为准）
  - Muse 自审 — 随时可用（渲染逐页目检＋源码量测，review_mode 记 `claude_full`、manifest 注明 supplementary_review）
  - Grok — 未接通（无 xAI 连接器；点名时先走 API 接入再审）
  - 豆包文本模型 — 未接通（豆包语音 TTS 不是文本模型；点名时先接 Ark 文本 API）
  - DeepSeek — 未接通（点名时先接 DeepSeek API）
- 审查未全量完成的页面不得假报「已审」：status 写 technical_only 并在交付时如实说明。

Phase 7 完成、SVG 包交付后，进入 Phase 8。

## Phase 8：生成 PPT（转制原生 PPTX）——开工前先经用户确认（2026-11-04 用户改定）

**Hard Stop：不直接生成。** 先把 Phase 7 的 SVG 包交付给用户，请用户确认是否生成 PPTX；用户确认后才跑下面的转制链。用户说先不生成，就停在 SVG 包交付，转制不启动。用户在最初委托里已明确要 PPTX 成品的，视为已确认，可直接转制。

（转制链：包内 ppt-master 转制链，2026-11-04 实测打通）

工程目录：`~/workspace/projects/<name>_<YYYYMMDD>`。全程只动工程副本——**用户已验收的 RUN_DIR/output SVG 原稿一个字不改**，质量门要求的规范化只落在工程副本上。命令里的脚本全部来自 `vendor/ppt-master/scripts/`（记作 `MS`）：

1. 建工程：`python3 $MS/project_manager.py init <name> --dir ~/workspace/projects --quick-generate`
2. 拷入终稿 SVG：`cp <RUN_DIR>/output/slide-*.svg <proj>/svg_output/`（命名须 slide-NN.svg）。
3. 写 spec_lock.md：flat 模板见 `references/spec-lock-flat-template.md`（scaffold-lock 在目录名无 format 时会失败，手写即可）。色板/字体按本份 PPT 的 SVG 实测值填。
4. 质量门：`$PY_PPTX $MS/svg_quality_checker.py <proj> --canonical-authoring --stage final --json`，要求 blocking errors＝0（warnings 可放行）。已验两类门禁修复（仅工程副本）：
   - 「undeclared font-size recurrence」→ 把反复出现的字号（如 30、25）在 spec_lock typography 里补声明为命名角色（title_compact、card_number），不改 SVG。
   - 单值 `stroke-dasharray="4"` → 规范化为 `"4 4"`（SVG 语义等值，零视觉变化）。
5. 导出：`$PY_PPTX $MS/svg_to_pptx.py <proj> --no-notes`，产物 `exports/<proj>_<HHMMSS>.pptx`；postflight `passed-with-warnings` 可接受，`quality_gate=passed` 为准。
6. 注入演讲备注：`$PY_PPTX <FORGE>/tools/inject_notes.py <导出.pptx> <RUN_DIR>/output/speaker-notes.md <定稿.pptx>`。
7. 回渲验收：LibreOffice 转 PDF → pdftoppm 抽验**封面＋最密一页＋本轮动过修复的页**，与 SVG 渲染对照；python-pptx 复开核对页数与备注页数（无 LibreOffice 时至少做页数/备注核对，并如实说明未回渲）。
8. 定稿落位：成品 PPTX 拷入 `<RUN_DIR>/output/`，中文交付名，作附件交付；工程目录保留供后续定点改稿。

转制口径如实告知用户：几何 1:1 量测转原生形状、文字可编辑；字体按 SVG 字体栈写入（DM Sans/Inter＋PingFang/微软雅黑回退），无该字体的机器自动回退；卡片阴影等效果由编译器近似。

## 指令：添加自定义风格（2026-11-04 用户要求加入，与 README「添加新风格」一节对应）

用户给参考材料（现成 PPT／截图／色板／品牌规范）并说「加一套风格」「添加风格」「照这个做一套风格，叫 XX」一类的话时，**不走上面的做 PPT 流程**，直接按本节把这套风格建进风格库：

1. **定名**：用户给了名字就用它（英文小写连字符作文件名与风格 id）；没给就按来源拟一个，先让用户确认。
2. **实测提取，不许凭感觉编参数**：参考是 PPTX → 解包读主题 XML（theme 配色与字体）、母版 XML（页眉页脚版式）与全稿颜色／字号统计；是截图或色板 → 取色实测。参数来源在交付时说清（thinkway 即此法建成：以原稿 theme 为准，deck 里的手工色不算主题色）。
3. **写风格文件**：`vendor/ppt-agent/shared/references/styles/<名>.yaml`，9 段结构（name／mood／color_scheme／typography／card_style／gradients／elevation／decoration／slide_type_overrides）；参考里有 logo、页眉页脚等固定元素的，加 `brand_furniture` 段写明每类页面（内容／目录／封面／尾页）的画法。
4. **注册**：`vendor/ppt-agent/shared/index.json` 的 `resources` 加一条（id＝`style-<名>`、domain＝`style`、file_path＝`styles/<名>.yaml`、keywords／description／use_cases），`total_count.styles` +1。**漏注册＝Phase 2 选不到这套风格，等于没加。**
5. **资产**：logo 等图片放 `vendor/ppt-agent/shared/assets/<名>/`；页面里引用必须以 base64 data URI 嵌入（外链在 LibreOffice 渲染时会被丢弃）；从 deck 提取的 PNG 用到深色底上之前，先查有没有低透明度残留描边。
6. **补文档**：包内 `README.md`「风格列表」表补一行（风格名／长什么样／建议用在什么 PPT 上）。
7. **出样张验证**：用新风格生成一页样张（优先目录页或内容页，最能看出色板与品牌家具），渲染目检后把样张交给用户确认；**用户没点头前不算加完**。
