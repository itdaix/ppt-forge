# ppt-forge

## 介绍
<img width="2240" height="1400" alt="image" src="https://github.com/user-attachments/assets/2445ad56-0784-4bb5-841b-2e1f6de2a22f" />
<img width="2240" height="1400" alt="image" src="https://github.com/user-attachments/assets/b30d0e73-b4ee-4614-a959-2b4f09ae818e" />




| 阶段 | 说明 | 人工介入 |
|---|---|---|
| Phase 1 初始化 | 给这次任务建专属文件夹和任务脚手架，把你发的材料登记归档 | **提供原始材料**：把要做成 PPT 的材料（文件、文档、数据）或主题发过来，任务由此启动 |
| Phase 2 需求确认 | 先做背景调研，再推导受众、目的、核心信息、语气、约束；风格给推荐 | **确认需求内容，并选定风格**（18 种风格里挑一套，技能只推荐、你拍板） |
| Phase 3 素材收集 | 以你给的材料为主，按章节并行做外部调研补充，来源逐项标明 | 无（材料有缺口时，可能向你核对一处事实） |
| Phase 4 大纲审批 | 用金字塔原理出大纲：共几页、每页讲什么、重点在哪 | **审批大纲**（可要求修改后重新呈批；通过后才开始生成） |
| Phase 5 策划稿 | 逐页先出简版 SVG 草图，把每页的内容和版式定个大概 | 无 |
| Phase 6 逐页生成＋审查 | 逐页出正式设计稿，多模型逐页审查打分、不过门就修复，再做整体审查 | 需要确认审核模型 |
| Phase 7 组装交付 | 按审查清单组装 SVG 包（逐页 SVG＋HTML 预览＋演讲备注）并汇报审查结果 | 无 |
| Phase 8 生成 PPT | 转制成原生可编辑 PPTX、注入备注、回渲抽验后交付 | **确认是否生成 PPTX**（你确认后才转制） |

## 安装

1. 把 `ppt-forge` 整个文件夹放进你的技能目录。
2. 装 Python 依赖（转制 PPTX 用）：
   `pip install -r ppt-forge/requirements.txt`
   （受 PEP 668 限制的系统先建 venv 再装，venv 里的 python 即技能里说的 PY_PPTX。）
3. 审查用 Gemini 时，各自申请 API Key 并设置环境变量：
   在 https://aistudio.google.com/apikey 建 Key，然后 `export GEMINI_API_KEY=<你的Key>`。
   不配 Key 也能用：审查环节可由使用人确认后改用其它模型或 Muse 自审（流程见 SKILL.md）。
4. （可选）装 LibreOffice，用于转制后的回渲抽验；没有也能出 PPTX，只是少一道目检。

## 使用

直接说「用 ppt-forge 做一份 XXX 的 PPT」即可，流程按上面 8 个阶段推进。
交付物是双份：SVG 包（zip）＋原生可编辑 PPTX（含演讲备注）。

## 风格列表

包内有 18 种风格（`vendor/ppt-agent/shared/references/styles/*.yaml`）。**没有默认风格**：每次做 PPT 时在 Phase 2 需求确认那一步选定，技能会按材料性质给出推荐和理由，**由你确认选哪套**，技能不能替你定。

| 风格 | 长什么样 | 建议用在什么 PPT 上 |
|---|---|---|
| business 商务专业 | 藏蓝＋橙，圆角卡片，干净权威 | 一般工作汇报、项目启动会、方案汇报——没特殊要求时的稳妥之选 |
| thinkway 九慧公司风 | 青蓝 #117598＋金黄 #FFC000、微软雅黑、直角扁平卡片，自带品牌家具规范与 logo 资产 | 上海九慧（Thinkway）的公司材料、对外正式场合 |
| blueprint 蓝图 | 工程制图风，网格与线条感强 | 技术方案、系统架构、工程类汇报 |
| tech 科技现代 | 深色底＋亮色点缀，科技感 | 产品发布、技术分享、科技主题 |
| minimal 极简 | 大量留白，元素极少 | 高层汇报、品牌展示，内容少而精的场合 |
| editorial-infographic 编辑信息图 | 杂志式排版，擅长数据叙事 | 数据报告、市场分析、行业洞察 |
| scientific 科学学术 | 学术蓝，数据结构严谨 | 研究报告、学术答辩、实验数据汇报 |
| bold-editorial 大胆编辑 | 超大标题、强对比，杂志封面感 | 品牌故事、观点输出、发布会 |
| creative 创意大胆 | 高饱和配色，构图动感 | 创意提案、活动策划、年轻向主题 |
| notion 文档风 | 像 Notion 文档，层级清楚 | 内部知识分享、流程说明、培训材料 |
| chalkboard 黑板风 | 黑板粉笔手绘感 | 教学课件、课堂类培训 |
| sketch-notes 手绘笔记 | 速写涂鸦风，轻松随意 | 头脑风暴、创意讨论、非正式分享 |
| vector-illustration 矢量插画 | 扁平几何插画，色彩明快 | 产品介绍、轻松科普、亲子主题 |
| watercolor 水彩 | 柔和晕染，文艺梦幻 | 生活方式、品牌故事、文艺主题 |
| vintage 复古 | 棕褐做旧，经典字体 | 历史回顾、周年纪念、文化主题 |
| fantasy-animation 奇幻动画 | 紫＋金，梦幻发光 | 游戏、动漫、娱乐主题 |
| intuition-machine 直觉机器 | 深色＋荧光绿粉，AI 神经感 | AI 与前沿科技主题分享 |
| pixel-art 像素风 | 8-bit 像素，复古好玩 | 游戏主题、趣味活动、年轻向内部活动 |

## 添加新风格

想给风格库里加一套新风格（比如照着某个现成模板做），两种办法：

**办法一：让 Muse 照着参考材料建（推荐）**
把参考材料发给 Muse——一份现成的 PPT、几张截图，或品牌色板/规范——说「照这个加一套风格，叫 XX」。它会实测提取主题色、字体、卡片样式等参数，生成风格文件并完成注册。包内的 thinkway 就是这样从一份公司介绍 PPT 里量出来的。

**办法二：自己写风格文件**

1. 在 `vendor/ppt-agent/shared/references/styles/` 下新建 `<风格名>.yaml`，照任意现有风格（如 `business.yaml`）的 9 段结构填：`name`（显示名）、`mood`（一句气质描述）、`color_scheme`（色板）、`typography`（字体与字号）、`card_style`（卡片样式）、`gradients`（渐变）、`elevation`（阴影）、`decoration`（装饰元素）、`slide_type_overrides`（封面、目录、尾页等特殊页的覆盖规则）。带公司 logo、页眉页脚这类固定元素的，再加一段 `brand_furniture` 写明每页的画法。
2. 在 `vendor/ppt-agent/shared/index.json` 的 `resources` 里注册一条：`id` 写 `style-<风格名>`、`domain` 写 `style`、`file_path` 写 `styles/<风格名>.yaml`，再填 `keywords` / `description` / `use_cases`，并把 `total_count.styles` 加 1。**少了这步，流程里选不到这套风格。**
3. 有 logo 等图片资产的，放进 `vendor/ppt-agent/shared/assets/<风格名>/`。注意：生成的页面里图片必须以 base64 形式嵌进 SVG，外链图片在渲染时会被丢弃。

加完后在上面的风格列表里补一行，并用新风格跑一页样张目检，确认效果再正式使用。

## 包内结构

- `SKILL.md` — 流程本体（唯一入口）
- `vendor/ppt-agent/` — 生成阶段工作流原件（AGENT_WORKFLOW.md ＋ references/ ＋ shared/，含 18 种风格与 thinkway 品牌资产）
- `vendor/ppt-master/` — 转制链脚本（scripts/ 闭包）＋ LICENSE
- `vendor/NOTICE.md` — 组件归属与许可证说明
- `tools/` — gemini_api.py（审查传输）、inject_notes.py（备注注入）
- `references/spec-lock-flat-template.md` — 转制锁模板
- `requirements.txt` — python-pptx

上游：ppt-agent https://github.com/zengwenliang416/ppt-agent （MIT）；ppt-master https://github.com/hugohe3/ppt-master （MIT）。
