# ppt-forge 安装说明（团队版）

ppt-forge 是自包含技能包：PPT 全流程（需求确认 → 大纲审批 → 逐页 SVG 生成 → 多模型审查 → 转原生可编辑 PPTX）所需的
ppt-agent 工作流与 ppt-master 转制链都已 vendor 在包内，**不需要再单独安装 ppt-agent 或 ppt-master**。

## 安装

1. 把 `ppt-forge` 整个文件夹放进你的 Muse 技能目录（发起人环境为 `~/workspace/custom-skills/`）。
2. 装 Python 依赖（转制 PPTX 用）：
   `pip install -r ppt-forge/requirements.txt`
   （受 PEP 668 限制的系统先建 venv 再装，venv 里的 python 即技能里说的 PY_PPTX。）
3. 审查用 Gemini 时，各自申请 API Key 并设置环境变量：
   在 https://aistudio.google.com/apikey 建 Key，然后 `export GEMINI_API_KEY=<你的Key>`。
   不配 Key 也能用：审查环节可由使用人确认后改用其它模型或 Muse 自审（流程见 SKILL.md）。
4. （可选）装 LibreOffice，用于转制后的回渲抽验；没有也能出 PPTX，只是少一道目检。

## 使用

对 Muse 说「用 ppt-forge 做一份 XXX 的 PPT」即可。全程只有三步需要你把关：**需求确认**（含风格确认，见下）、**大纲审批**、**生成 PPT 前的确认**（Phase 8：SVG 包先交付，你确认后才转制成 PPTX，不会直接生成）。
交付物是双份：SVG 包（zip）＋原生可编辑 PPTX（含演讲备注）。

## 风格（需求确认时定，没有默认）

包内有 18 种风格（`vendor/ppt-agent/shared/references/styles/*.yaml`），每次做 deck 时在需求确认那一步选定：
技能会按材料性质给出推荐和理由，**由你确认选哪套**，技能不能替你定。常用两套：

- `business` — 通用商务风（藏蓝＋橙，圆角卡片），适合一般汇报。
- `thinkway` — 上海九慧（Thinkway）公司风（青蓝 #117598＋金黄 #FFC000、微软雅黑、直角扁平卡片），
  自带品牌家具规范与 logo 资产（顶部双色条、页脚字标等，细则在该风格文件的 `brand_furniture` 段），
  适合公司材料与对外场合。

其余 16 种（blueprint、minimal、notion、tech 等）同样可选，需求确认时让 Muse 列出来即可。

## 包内结构

- `SKILL.md` — 流程本体（唯一入口）
- `vendor/ppt-agent/` — 生成阶段工作流原件（AGENT_WORKFLOW.md ＋ references/ ＋ shared/，含 18 种风格与 thinkway 品牌资产）
- `vendor/ppt-master/` — 转制链脚本（scripts/ 闭包）＋ LICENSE
- `vendor/NOTICE.md` — 组件归属与许可证说明
- `tools/` — gemini_api.py（审查传输）、inject_notes.py（备注注入）
- `references/spec-lock-flat-template.md` — 转制锁模板
- `requirements.txt` — python-pptx

上游：ppt-agent https://github.com/zengwenliang416/ppt-agent （MIT）；ppt-master https://github.com/hugohe3/ppt-master （MIT）。
