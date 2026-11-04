<!-- spec-lock flat 模板：手写到 ppt-master 工程根目录 spec_lock.md。
     scaffold-lock 在工程目录名不含 format 时会失败，直接用本模板改值即可。
     色板/字体按本份 PPT 的 SVG 实测值填；typography 须覆盖 SVG 中反复出现（≥3 次）的字号，
     否则质量门会以 undeclared font-size recurrence 拦截——补声明角色即可，不要改 SVG。 -->
<!-- ppt-master-schema: spec-lock/v1 -->
# Execution Lock

## canvas
- viewBox: 0 0 1280 720
- format: PPT 16:9

## communication
- primary_language: zh-CN
- audience: <听众>
- objective: <目标>
- core_message: <核心信息>
- consumption_mode: balanced

## mode
- mode: briefing

## visual_style
- visual_style: custom
- visual_style_behavior: <本份 PPT 的视觉口径一句话>

## colors
- background: #FFFFFF
- secondary_bg: <卡片底色>
- primary: <主色>
- accent: <点缀色>
- secondary_accent: <次色>
- body_text: <正文色>
- secondary_text: <次级文字色>
- divider: <分隔线色>
- positive: <绿>
- warning: <橙/黄>
- negative: <红>

## typography
- font_family: "DM Sans", Inter, "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif
- title_family: "DM Sans", Inter, "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif
- body_family: "DM Sans", Inter, "PingFang SC", "Noto Sans SC", "Microsoft YaHei", sans-serif
- body: 15
- title: 34
- title_compact: 30
- card_number: 25
- subtitle: 20
- lead: 20
- annotation: 14
- footnote: 12
- display: 44
- hero: 44

## icons
- library: none
- inventory: none

## images
- inventory: none

## page_rhythm
- P01: anchor
- P02: anchor
- <P03 起按页填 dense / anchor>

## pptx_structure
- mode: flat
- template_reuse_scope: style

## forbidden
- `mask`, `<style>`, `class`, external CSS, `<foreignObject>`, `textPath`, `@font-face`, `<animate*>`, `<set>`, `<script>` / event attributes, `<iframe>`
- HTML named entities in text; write typography as raw Unicode and escape XML reserved characters
