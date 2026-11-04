# NOTICE — vendored components

ppt-forge 是自包含融合包，下列组件随包分发，各自遵循其上游许可证：

- **ppt-agent**（`vendor/ppt-agent/`）：https://github.com/zengwenliang416/ppt-agent ，MIT License，v1.0.0。
  本包收录的是经 Muse 宿主适配的副本（AGENT_WORKFLOW.md ＋ references/ ＋ shared/），并按 ppt-forge 的多模型审查口径改写了审查传输一行；流程与阶段定义与上游一致。
- **ppt-master 转制链**（`vendor/ppt-master/`）：https://github.com/hugohe3/ppt-master ，MIT License（全文见 `vendor/ppt-master/LICENSE`）。
  本包仅收录 svg→pptx 转制所需的脚本闭包（scripts/ 的一部分），不含其模板库与生成管线。
- **tools/gemini_api.py、tools/inject_notes.py**：ppt-forge 自带小工具，无第三方代码。

分发本包时请保留本文件与上述许可证。
