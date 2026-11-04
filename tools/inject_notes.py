#!/usr/bin/env python3
"""Inject speaker notes from a ppt-agent speaker-notes.md into a PPTX.

Usage:
  inject_notes.py <in.pptx> <speaker-notes.md> <out.pptx>

Notes format expected (ppt-agent Phase 7 output):
  ## 第 NN 页 — <标题>
  - 条目一
  - 条目二
Pages whose body only says （本页无单独备注） are skipped.
Requires python-pptx.
"""
import re
import sys

from pptx import Presentation


def parse_notes(md_text):
    sections = {}
    for m in re.finditer(r"## 第 (\d+) 页[^\n]*\n(.*?)(?=\n## 第 |\Z)", md_text, re.S):
        num, body = int(m.group(1)), m.group(2).strip()
        lines = [ln[2:].strip() for ln in body.splitlines() if ln.startswith("- ")]
        text = "\n".join(lines)
        if text and "本页无单独备注" not in text:
            sections[num] = text
    return sections


def main():
    if len(sys.argv) != 4:
        print(__doc__)
        return 2
    src, notes_md, out = sys.argv[1], sys.argv[2], sys.argv[3]
    sections = parse_notes(open(notes_md, encoding="utf-8").read())
    prs = Presentation(src)
    slides = list(prs.slides)
    for i, slide in enumerate(slides, start=1):
        if i in sections:
            slide.notes_slide.notes_text_frame.text = sections[i]
    prs.save(out)
    prs2 = Presentation(out)
    n = sum(
        1
        for s in prs2.slides
        if s.has_notes_slide and s.notes_slide.notes_text_frame.text.strip()
    )
    print(f"saved: {out} | slides: {len(slides)} | slides with notes: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
