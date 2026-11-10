# -*- coding: utf-8 -*-
"""校验生成的 PPT：页数、每页文本、图片位置、表格尺寸。"""
import sys
from pptx import Presentation
from pptx.util import Emu

sys.stdout.reconfigure(encoding="utf-8")

path = sys.argv[1]
prs = Presentation(path)
print("slide size:", prs.slide_width / 914400, "x", prs.slide_height / 914400, "in")
print("slides:", len(prs.slides))
for i, slide in enumerate(prs.slides, start=1):
    texts = []
    pics = 0
    tables = 0
    for sh in slide.shapes:
        if sh.shape_type == 13:
            pics += 1
        if sh.has_table:
            tables += 1
        if sh.has_text_frame:
            t = sh.text_frame.text.strip()
            if t:
                texts.append(t.replace("\n", " / "))
    print(f"--- p{i}: pic={pics} table={tables}")
    for t in texts[:6]:
        print("   ", t[:70])
