# -*- coding: utf-8 -*-
"""生成答辩 PPT：9 页、16:9、无动画、全部可编辑文本。"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
os.makedirs(ASSETS, exist_ok=True)

FONT = "Microsoft YaHei"
DARK = RGBColor(0x11, 0x18, 0x27)
GRAY = RGBColor(0x6B, 0x72, 0x80)
LIGHT = RGBColor(0xF3, 0xF4, 0xF6)
SOFT = RGBColor(0xEF, 0xF6, 0xFF)
BLUE = RGBColor(0x25, 0x63, 0xEB)
RED = RGBColor(0xDC, 0x26, 0x26)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def style_run(run, size, bold=False, color=DARK, ascii_font=None):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = ascii_font or FONT
    rPr = run._r.get_or_add_rPr()
    ea = rPr.find(qn("a:ea"))
    if ea is None:
        ea = rPr.makeelement(qn("a:ea"), {})
        rPr.append(ea)
    ea.set("typeface", FONT)
    latin = rPr.find(qn("a:latin"))
    if latin is not None:
        latin.set("typeface", ascii_font or FONT)


def text(slide, left, top, width, height, content, size=18, bold=False,
         color=DARK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, spacing=1.15,
         ascii_font=None):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    for i, line in enumerate(content.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        r = p.add_run()
        r.text = line
        style_run(r, size, bold, color, ascii_font)
    return box


def rect(slide, left, top, width, height, fill=LIGHT, line=None,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.08):
    s = slide.shapes.add_shape(shape, Inches(left), Inches(top), Inches(width), Inches(height))
    s.fill.solid()
    s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(1)
    s.shadow.inherit = False
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        try:
            s.adjustments[0] = radius
        except Exception:
            pass
    return s


def new_slide(prs, title, page):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    text(slide, 0.9, 0.5, 11.6, 0.8, title, size=30, bold=True)
    rect(slide, 0.9, 1.42, 0.9, 0.06, fill=BLUE, shape=MSO_SHAPE.RECTANGLE)
    text(slide, 0.9, 6.95, 7, 0.32, "货运调度仿真系统 · 一阶段答辩", size=10, color=GRAY)
    text(slide, 11.6, 6.95, 0.9, 0.32, str(page), size=11, color=GRAY, align=PP_ALIGN.RIGHT)
    return slide


def make_compare_image(path):
    """两个方案横向对比：左＝两点线性插值（走弦），右＝沿折线弧长插值（贴线）。"""
    W, H = 1800, 640
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    try:
        f_title = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 30)
        f_note = ImageFont.truetype(r"C:\Windows\Fonts\msyh.ttc", 22)
    except Exception:
        f_title = ImageFont.load_default()
        f_note = f_title

    GREY = (229, 231, 235)
    RED = (220, 38, 38)
    BLUE = (37, 99, 235)
    LIGHT_BLUE = (147, 197, 253)

    def panel(x0, title, sub):
        d.text((x0, 26), title, font=f_title, fill=(17, 24, 39))
        d.text((x0, 70), sub, font=f_note, fill=(107, 114, 128))

        bx0, bx1 = x0 + 20, x0 + 700
        by0, by1 = 130, 560
        gap = 24
        bw = (bx1 - bx0 - gap * 2) / 3
        bh = (by1 - by0 - gap * 2) / 3
        for r in range(3):
            for c in range(3):
                bx = bx0 + c * (bw + gap)
                by = by0 + r * (bh + gap)
                d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=10, fill=GREY)

        gx1 = bx0 + bw + gap / 2
        gx2 = bx0 + 2 * (bw + gap) + gap / 2
        gy1 = by0 + bh + gap / 2
        gy2 = by0 + 2 * (bh + gap) + gap / 2
        route = [
            (x0 + 40, by1 - 18),
            (gx1, by1 - 18),
            (gx1, gy2),
            (gx2, gy2),
            (gx2, gy1),
            (bx1 - 12, gy1),
            (bx1 - 12, by0 - 30),
        ]
        return route

    def dashed(draw, pts, color, width=5, dash=18, gap=14):
        import math
        for i in range(len(pts) - 1):
            x1, y1 = pts[i]
            x2, y2 = pts[i + 1]
            dx, dy = x2 - x1, y2 - y1
            L = math.hypot(dx, dy)
            if L == 0:
                continue
            ux, uy = dx / L, dy / L
            t = 0.0
            while t < L:
                e = min(t + dash, L)
                draw.line([(x1 + ux * t, y1 + uy * t), (x1 + ux * e, y1 + uy * e)],
                          fill=color, width=width)
                t = e + gap

    def closest_on(route, p):
        import math
        best = (1e18, route[0])
        for i in range(len(route) - 1):
            ax, ay = route[i]
            bx, by = route[i + 1]
            vx, vy = bx - ax, by - ay
            L2 = vx * vx + vy * vy
            t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - ax) * vx + (p[1] - ay) * vy) / L2))
            q = (ax + vx * t, ay + vy * t)
            dist = math.hypot(p[0] - q[0], p[1] - q[1])
            if dist < best[0]:
                best = (dist, q)
        return best

    # 左：旧方案
    route = panel(60, "旧：两点线性插值", "进度按两点之间的比例推进")
    dashed(d, route, LIGHT_BLUE, width=5)
    d.line([route[0], route[-1]], fill=RED, width=8)
    d.ellipse([route[0][0]-9, route[0][1]-9, route[0][0]+9, route[0][1]+9], fill=RED)
    d.ellipse([route[-1][0]-9, route[-1][1]-9, route[-1][0]+9, route[-1][1]+9], fill=RED)
    # 偏差标注：弦的中点画到折线最近点
    mx = (route[0][0] + route[-1][0]) / 2
    my = (route[0][1] + route[-1][1]) / 2
    _, q = closest_on(route, (mx, my))
    dashed(d, [(mx, my), q], (156, 163, 175), width=3, dash=10, gap=8)
    d.text((mx + 14, my - 6), "最大偏差", font=f_note, fill=(220, 38, 38))
    d.text((mx + 14, my + 26), "6.7 km", font=f_note, fill=(220, 38, 38))

    # 右：新方案
    route2 = panel(1000, "新：沿折线弧长插值", "进度按已走公里数推进")
    d.line(route2, fill=BLUE, width=8, joint="curve")
    for pt in [route2[0], route2[-1]]:
        d.ellipse([pt[0]-9, pt[1]-9, pt[0]+9, pt[1]+9], fill=BLUE)

    # 底部结论
    d.text((60, 592), "同一条路线、同一个起终点：左边每一段都走弦，右边每一段都贴线",
           font=f_note, fill=(107, 114, 128))

    img.save(path, "PNG")


# ---------------------------------------------------------------- 生成
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# 1 封面
s = prs.slides.add_slide(prs.slide_layouts[6])
text(s, 0.9, 0.7, 6, 0.4, "第一阶段汇报", size=13, color=GRAY)
text(s, 0.9, 2.15, 11.5, 1.0, "货运调度仿真系统", size=48, bold=True)
text(s, 0.9, 3.25, 11.5, 0.7, "基于概率状态机与真实路网", size=24, color=GRAY)
rect(s, 0.9, 4.15, 2.0, 0.08, fill=BLUE, shape=MSO_SHAPE.RECTANGLE)
text(s, 0.9, 4.65, 11.5, 1.2,
     "答辩人：×××          学号：×××\n指导教师：×××          日期：2026.11",
     size=15, color=DARK, spacing=1.6)

# 2 为什么做
s = new_slide(prs, "为什么做仿真", 2)
cards = [
    ("空驶率高", "靠人工经验派单\n车与货经常对不上"),
    ("等待不可控", "装卸、故障、缺货\n都是随机事件"),
    ("路径失真", "直线距离\n不等于真实里程"),
]
x = 0.9
for head, body in cards:
    rect(s, x, 2.0, 3.55, 2.4, fill=LIGHT)
    text(s, x + 0.4, 2.35, 2.8, 0.5, head, size=21, bold=True)
    text(s, x + 0.4, 3.0, 2.9, 1.1, body, size=15, color=GRAY, spacing=1.5)
    x += 3.95
text(s, 0.9, 5.3, 11.5, 0.6, "目标：用仿真代替真车实验，观察调度策略的效果", size=19, bold=True, color=BLUE)

# 3 架构与特色
s = new_slide(prs, "系统架构与三个特点", 3)
BOX_LINE = RGBColor(0xD1, 0xD5, 0xDB)

# 高德 API（云）
rect(s, 0.9, 1.88, 3.4, 0.75, fill=WHITE, line=BOX_LINE)
text(s, 1.15, 1.98, 3.0, 0.35, "高德地图 API", size=14, bold=True)
text(s, 1.15, 2.3, 3.0, 0.28, "地图瓦片 · 驾车路径规划", size=10, color=GRAY)
rect(s, 2.58, 2.63, 0.02, 0.37, fill=GRAY, shape=MSO_SHAPE.RECTANGLE)
text(s, 2.72, 2.66, 1.2, 0.3, "HTTPS", size=9, color=GRAY)

# 浏览器 / 前端
rect(s, 0.9, 3.0, 3.4, 1.9, fill=WHITE, line=BOX_LINE)
text(s, 1.15, 3.12, 3.0, 0.35, "浏览器（前端）", size=16, bold=True)
text(s, 1.15, 3.55, 3.05, 0.3, "Vue 3 + Vite + 高德 JS API", size=12, color=DARK)
text(s, 1.15, 3.9, 3.05, 0.3, "① 开发期：Vite 5173（代理 → 8080）", size=10.5, color=GRAY)
text(s, 1.15, 4.2, 3.05, 0.3, "② 演示：打包进后端，同源 8080", size=10.5, color=GRAY)
text(s, 1.15, 4.55, 3.05, 0.28, "*.html / 静态资源", size=9.5, color=GRAY)

# 箭头 1
text(s, 4.32, 3.72, 0.76, 0.45, "→", size=20, color=GRAY, align=PP_ALIGN.CENTER)
text(s, 4.3, 4.1, 0.8, 0.3, "HTTP", size=9, color=GRAY, align=PP_ALIGN.CENTER)

# Spring Boot
rect(s, 5.1, 2.55, 3.4, 2.55, fill=WHITE, line=BOX_LINE)
text(s, 5.35, 2.7, 3.0, 0.35, "Spring Boot（8080）", size=16, bold=True)
text(s, 5.35, 3.15, 3.0, 0.3, "Controller", size=12, color=DARK)
text(s, 5.35, 3.48, 3.0, 0.3, "Service：仿真循环 / 路线", size=11, color=DARK)
text(s, 5.35, 3.81, 3.0, 0.3, "Mapper（7 个 XML）", size=12, color=DARK)
text(s, 5.35, 4.14, 3.0, 0.3, "Entity", size=12, color=DARK)

# 箭头 2
text(s, 8.52, 3.72, 0.76, 0.45, "→", size=20, color=GRAY, align=PP_ALIGN.CENTER)
text(s, 8.5, 4.1, 0.8, 0.3, "MyBatis", size=9, color=GRAY, align=PP_ALIGN.CENTER)

# 数据库
rect(s, 9.3, 3.0, 3.2, 1.9, fill=WHITE, line=BOX_LINE)
text(s, 9.55, 3.12, 2.7, 0.35, "MariaDB", size=16, bold=True)
text(s, 9.55, 3.55, 2.7, 0.3, "库：traffic", size=12, color=DARK)
text(s, 9.55, 3.88, 2.7, 0.3, "8 张表", size=12, color=DARK)
text(s, 9.55, 4.21, 2.7, 0.3, "localhost:3306", size=11, color=GRAY)

chips = ["概率状态机", "真实路网", "可验证的一致性"]
x = 0.9
for c in chips:
    rect(s, x, 5.45, 3.5, 0.55, fill=SOFT)
    text(s, x, 5.55, 3.5, 0.35, c, size=15, bold=True, color=BLUE, align=PP_ALIGN.CENTER)
    x += 3.85

text(s, 0.9, 6.1, 11.5, 0.3, "10 辆车  ·  88 家工厂  ·  4 个城市（成都 / 德阳 / 眉山 / 资阳）", size=12, color=DARK)
text(s, 0.9, 6.45, 11.5, 0.28, "前端 1 秒轮询 · 后端 5 秒推进一步 · 全部落库  |  后端 42 个类 / 2133 行 · 前端 17 个文件 / 1570 行 · 8 张表",
     size=10, color=GRAY)

# 4 运行逻辑
s = new_slide(prs, "运行逻辑：一个仿真线程 + while 主循环", 4)
text(s, 0.9, 1.68, 6.0, 0.28, "SimulationService.java（节选）", size=9, color=GRAY)
rect(s, 0.9, 1.98, 7.5, 4.2, fill=RGBColor(0x1F, 0x29, 0x37))
code = (
    "private void runLoop() {\n"
    "    while (running) {\n"
    "        try {\n"
    "            tickOnce();\n"
    "        } catch (Exception e) {\n"
    "            log.error(\"第 {} 轮执行异常\", tick + 1, e);\n"
    "        }\n"
    "        try {\n"
    "            Thread.sleep(props.getTickSeconds() * 1000L);\n"
    "        } catch (InterruptedException e) {\n"
    "            Thread.currentThread().interrupt();\n"
    "            break;\n"
    "        }\n"
    "    }\n"
    "    running = false;\n"
    "}\n"
    "\n"
    "public void tickOnce() {\n"
    "    transactionTemplate.executeWithoutResult(st -> doTick());\n"
    "}\n"
    "\n"
    "private synchronized void doTick() {\n"
    "    tick++;\n"
    "    simMinutes += props.getMinutesPerTick();\n"
    "    List<Vehicle> vehicles = vehicleMapper.selectAllNotDeleted();\n"
    "    generateMissions(vehicles);"
)
text(s, 1.15, 2.06, 7.05, 4.0, code, size=8.5,
     color=RGBColor(0xE5, 0xE7, 0xEB), spacing=1.1, ascii_font="Consolas")

bullets = [
    ("单线程推进", "start() 里只 new 一个 sim-loop 线程，串行改车辆"),
    ("整轮一个事务", "tickOnce() 用 TransactionTemplate 包住 doTick()"),
    ("可随时暂停", "running=false + interrupt()，立即打断 sleep"),
    ("异常隔离", "单轮失败只记日志，循环不退出"),
]
y = 1.85
for head, body in bullets:
    rect(s, 8.65, y + 0.06, 0.09, 0.42, fill=BLUE, shape=MSO_SHAPE.RECTANGLE)
    text(s, 8.9, y, 3.8, 0.35, head, size=13, bold=True)
    text(s, 8.9, y + 0.32, 3.85, 0.3, body, size=9.5, color=GRAY)
    y += 1.05

text(s, 0.9, 6.28, 11.6, 0.3,
     "退出循环：stop() 置 running=false 并 interrupt() → sleep 抛异常 → break → 线程结束",
     size=9.5, color=GRAY)
text(s, 0.9, 6.56, 11.6, 0.3,
     "reset()：停线程 + 清空任务 + 车辆停回工厂点位  |  一轮 5 秒 = 仿真 5 分钟",
     size=9.5, color=GRAY)

# 5 状态机
s = new_slide(prs, "车辆状态：概率转移，不是固定链路", 5)
text(s, 0.9, 1.95, 4.0, 0.5, "6 个状态 · 36 个转移概率", size=18, bold=True)
text(s, 0.9, 2.55, 4.2, 1.5,
     "抽样：随机取 1~100，按行概率累加落区间", size=13, color=GRAY, spacing=1.5)
text(s, 0.9, 3.45, 4.3, 1.8,
     "例：接单行驶这一行\n1~5 继续接单\n6~95 转装货\n96~100 转等待",
     size=13, color=DARK, spacing=1.5)
text(s, 0.9, 5.45, 4.2, 0.6, "矩阵只决定状态，\n接哪一单交给下一层。", size=13, bold=True, color=BLUE, spacing=1.4)
text(s, 4.6, 5.55, 8.0, 0.3, "统一车速 60 km/h：1 km = 1 分钟；一轮 5 秒 = 仿真 5 分钟", size=11, color=GRAY)

header = ["从 \\ 到", "接单行驶", "装货", "运货行驶", "卸货", "停留等待", "空闲"]
rows = [
    ["接单行驶", "0.05", "0.90", "0.00", "0.00", "0.05", "0.00"],
    ["装货", "0.00", "0.02", "0.95", "0.02", "0.01", "0.00"],
    ["运货行驶", "0.00", "0.00", "0.00", "0.98", "0.02", "0.00"],
    ["卸货", "0.00", "0.00", "0.00", "0.00", "0.02", "0.98"],
    ["停留等待", "0.10", "0.05", "0.05", "0.00", "0.20", "0.60"],
    ["空闲", "0.90", "0.00", "0.00", "0.00", "0.10", "0.00"],
]
shape = s.shapes.add_table(7, 7, Inches(5.5), Inches(1.95), Inches(7.1), Inches(3.9))
table = shape.table
table.columns[0].width = Inches(1.4)
for i in range(1, 7):
    table.columns[i].width = Inches(0.95)
table.rows[0].height = Inches(0.48)
for i in range(1, 7):
    table.rows[i].height = Inches(0.44)

for j, h in enumerate(header):
    cell = table.cell(0, j)
    cell.text = ""
    p = cell.text_frame.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = h
    style_run(r, 10, True, WHITE)
    cell.fill.solid()
    cell.fill.fore_color.rgb = RGBColor(0x37, 0x41, 0x51)

for i, row in enumerate(rows, start=1):
    for j, v in enumerate(row):
        cell = table.cell(i, j)
        cell.text = ""
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = v
        style_run(r, 10, j == 0, DARK)
        cell.fill.solid()
        cell.fill.fore_color.rgb = SOFT if i == 1 else WHITE

# 5 任务与抢单
s = new_slide(prs, "任务怎么来，车怎么抢", 6)
text(s, 0.9, 1.95, 11.5, 0.4, "按缺口供给，避免车多把任务抢空", size=15, color=GRAY)
rect(s, 0.9, 2.55, 11.5, 1.0, fill=SOFT)
text(s, 0.9, 2.78, 11.5, 0.5,
     "本轮新增 = min( 空闲车数 - 待接单数 , tasksPerTick = 5 )",
     size=20, bold=True, color=BLUE, align=PP_ALIGN.CENTER)

text(s, 0.9, 3.95, 11.5, 0.4, "抢单：条件更新，影响行数 = 1 才算成功", size=15, color=GRAY)
rect(s, 0.9, 4.5, 11.5, 1.35, fill=RGBColor(0x1F, 0x29, 0x37))
text(s, 1.25, 4.72, 10.9, 1.0,
     "UPDATE mission SET car_id = ?, status = '接单中'\nWHERE id = ? AND status = '待接单'",
     size=15, color=RGBColor(0xE5, 0xE7, 0xEB), spacing=1.5)

text(s, 0.9, 6.05, 11.5, 0.4, "→ 一车一单、一单只被抢一次", size=14, bold=True, color=DARK)

# 7 真实路网（两种插值方案对比）
img_path = os.path.join(ASSETS, "route-compare.png")
make_compare_image(img_path)
s = new_slide(prs, "车怎么动：两种插值方案对比", 7)
s.shapes.add_picture(img_path, Inches(0.9), Inches(1.66), width=Inches(11.4))

text(s, 0.95, 5.76, 5.4, 0.3, "旧：p = (1 - t)·A + t·B", size=12, bold=True, color=RED)
text(s, 0.95, 6.06, 5.4, 0.3, "t 是两点之间的比例，拐弯处被拉直、走弦", size=10, color=GRAY)

text(s, 6.95, 5.76, 5.4, 0.3, "新：s = 投影弧长，p = pointAt(s + 5km)", size=12, bold=True, color=BLUE)
text(s, 6.95, 6.06, 5.4, 0.3, "进度是公里数，每个采样点都落在折线上", size=10, color=GRAY)

text(s, 0.9, 6.42, 11.6, 0.35,
     "20.7km 直角折线：旧方案中点偏出 6.7km，新方案 11 个采样点距折线 0.000km",
     size=12, bold=True, color=DARK, align=PP_ALIGN.CENTER)

# 7 验证
s = new_slide(prs, "验证：一致性 + 性能", 8)
rect(s, 0.9, 2.0, 5.5, 2.5, fill=LIGHT)
text(s, 1.25, 2.3, 4.8, 0.8, "5 / 5", size=40, bold=True, color=BLUE)
text(s, 1.25, 3.25, 4.9, 1.0, "次采样均满足\n总数 = 待运 + 在途 + 已运抵", size=14, color=DARK, spacing=1.4)

rect(s, 6.9, 2.0, 5.5, 2.5, fill=LIGHT)
text(s, 7.25, 2.3, 4.9, 0.8, "540 → 110 ms", size=32, bold=True, color=BLUE)
text(s, 7.25, 3.25, 4.9, 1.0, "压力测试 50 辆 / 当前演示 10 辆\n每轮计算耗时（整轮合并事务后）", size=13, color=DARK, spacing=1.4)

text(s, 0.9, 4.95, 11.5, 0.4, "接口 /sim/state 响应 30~60ms  ·  前端 1 秒轮询无压力",
     size=14, color=GRAY, align=PP_ALIGN.CENTER)

# 8 现场演示
s = new_slide(prs, "现场演示", 9)
steps = [
    ("1", "车辆状态与概率转移"),
    ("2", "拐弯时贴着道路走"),
    ("3", "任务看板实时变化"),
    ("4", "重置后重新开始"),
]
y = 2.15
for num, label in steps:
    rect(s, 0.9, y, 0.55, 0.55, fill=BLUE, shape=MSO_SHAPE.OVAL)
    text(s, 0.9, y + 0.12, 0.55, 0.35, num, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    text(s, 1.75, y + 0.08, 10, 0.4, label, size=19)
    y += 0.95
text(s, 0.9, 6.1, 11.5, 0.4, "如网络异常，立刻切换录屏兜底", size=13, color=GRAY)

# 9 总结
s = new_slide(prs, "总结", 10)
items = [
    ("概率状态机", "车辆行为不再写死，能体现随机波动"),
    ("真实路网", "工厂与路线来自真实数据，轨迹可信"),
    ("一致性验证", "状态守恒 + 原子抢单，结果可校验"),
]
y = 2.0
for head, body in items:
    rect(s, 0.9, y, 0.09, 0.5, fill=BLUE, shape=MSO_SHAPE.RECTANGLE)
    text(s, 1.25, y + 0.02, 3.4, 0.4, head, size=18, bold=True)
    text(s, 4.7, y + 0.05, 7.6, 0.4, body, size=15, color=GRAY)
    y += 0.95
rect(s, 0.9, 5.0, 11.5, 0.02, fill=RGBColor(0xE5, 0xE7, 0xEB), shape=MSO_SHAPE.RECTANGLE)
text(s, 0.9, 5.25, 11.5, 0.4, "不足与下一步", size=15, bold=True)
text(s, 0.9, 5.7, 11.5, 0.6,
     "车辆与任务的匹配算法仍较简单、参数缺少系统实验 → 下一步补匹配度打分与敏感性分析",
     size=14, color=GRAY)

out = os.path.join(os.path.dirname(BASE), sys.argv[1] if len(sys.argv) > 1 else "答辩_交通管理仿真系统.pptx")
prs.save(out)
print("saved:", out)
print("slides:", len(prs.slides))
