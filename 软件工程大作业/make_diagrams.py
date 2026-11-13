# -*- coding: utf-8 -*-
"""为大作业报告绘制 UML 图与甘特图（输出 PNG）。"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")
os.makedirs(ASSETS, exist_ok=True)

FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
INK = (31, 41, 55)
GREY = (107, 114, 128)
LINE = (75, 85, 99)
BLUE = (37, 99, 235)
LIGHT_BLUE = (239, 246, 255)
LIGHT_GREY = (243, 244, 246)
AMBER = (245, 158, 11)
GREEN = (16, 185, 129)


def font(size):
    return ImageFont.truetype(FONT_PATH, size)


def text_w(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0], b[3] - b[1]


def wrap(d, s, f, max_w):
    lines, cur = [], ""
    for ch in s:
        if ch == "\n":
            lines.append(cur)
            cur = ""
            continue
        if text_w(d, cur + ch, f)[0] > max_w and cur:
            lines.append(cur)
            cur = ch
        else:
            cur += ch
    if cur:
        lines.append(cur)
    return lines


def box(d, x, y, w, h, text, f, fill=LIGHT_BLUE, outline=BLUE, radius=12, fg=INK):
    d.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline, width=2)
    lines = wrap(d, text, f, w - 24)
    lh = text_w(d, "国", f)[1] + 8
    total = lh * len(lines)
    ty = y + (h - total) / 2
    for i, ln in enumerate(lines):
        tw = text_w(d, ln, f)[0]
        d.text((x + (w - tw) / 2, ty + i * lh), ln, font=f, fill=fg)


def ellipse(d, cx, cy, rx, ry, text, f, fill=LIGHT_BLUE, outline=BLUE, fg=INK):
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=fill, outline=outline, width=2)
    lines = wrap(d, text, f, rx * 2 - 20)
    lh = text_w(d, "国", f)[1] + 6
    ty = cy - lh * len(lines) / 2
    for i, ln in enumerate(lines):
        tw = text_w(d, ln, f)[0]
        d.text((cx - tw / 2, ty + i * lh), ln, font=f, fill=fg)


def arrow(d, p1, p2, color=LINE, width=2, label=None, f=None, dash=False, offset=(0, -14)):
    x1, y1 = p1
    x2, y2 = p2
    if dash:
        total = math.hypot(x2 - x1, y2 - y1)
        if total == 0:
            return
        ux, uy = (x2 - x1) / total, (y2 - y1) / total
        t, seg = 0.0, 14
        while t < total - seg:
            d.line([(x1 + ux * t, y1 + uy * t), (x1 + ux * (t + seg), y1 + uy * (t + seg))],
                   fill=color, width=width)
            t += seg * 2
    else:
        d.line([p1, p2], fill=color, width=width)
    # 箭头
    ang = math.atan2(y2 - y1, x2 - x1)
    size = 12
    a1 = ang + math.radians(155)
    a2 = ang - math.radians(155)
    d.polygon([(x2, y2),
               (x2 + size * math.cos(a1), y2 + size * math.sin(a1)),
               (x2 + size * math.cos(a2), y2 + size * math.sin(a2))], fill=color)
    if label:
        mx, my = (x1 + x2) / 2 + offset[0], (y1 + y2) / 2 + offset[1]
        tw = text_w(d, label, f)[0]
        d.rectangle([mx - tw / 2 - 4, my - 2, mx + tw / 2 + 4, my + 20], fill="white")
        d.text((mx - tw / 2, my), label, font=f, fill=GREY)




def trim(img, pad=12):
    from PIL import ImageChops
    bg = Image.new("RGB", img.size, (255, 255, 255))
    bbox = ImageChops.difference(img, bg).getbbox()
    if not bbox:
        return img
    x0, y0, x1, y1 = bbox
    return img.crop((max(0, x0 - pad), max(0, y0 - pad),
                     min(img.width, x1 + pad), min(img.height, y1 + pad)))


def new_canvas(w, h, title=None, f=None):
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    if title:
        d.text((40, 24), title, font=f, fill=INK)
    return img, d


# ---------------------------------------------------------------- 用例图
def draw_usecase(path):
    W, H = 1500, 980
    f_t, f_a, f_u = font(34), font(24), font(21)
    img, d = new_canvas(W, H, None, f_t)

    # 系统边界
    d.rounded_rectangle([380, 100, 1120, 920], radius=18, outline=LINE, width=2)
    d.text((470, 116), "货运调度仿真系统", font=font(24), fill=INK)

    # 参与者
    def actor(x, y, name):
        d.ellipse([x - 16, y - 46, x + 16, y - 14], outline=INK, width=2)
        d.line([(x, y - 14), (x, y + 26)], fill=INK, width=2)
        d.line([(x - 26, y - 2), (x + 26, y - 2)], fill=INK, width=2)
        d.line([(x, y + 26), (x - 20, y + 62)], fill=INK, width=2)
        d.line([(x, y + 26), (x + 20, y + 62)], fill=INK, width=2)
        tw = text_w(d, name, f_a)[0]
        d.text((x - tw / 2, y + 74), name, font=f_a, fill=INK)

    actor(170, 250, "调度员")
    actor(1330, 250, "系统管理员")
    actor(170, 780, "高德地图 API")

    uses = [
        (600, 210, "启动 / 暂停仿真"),
        (880, 210, "重置仿真"),
        (600, 330, "查看实时状态"),
        (880, 330, "查看任务看板"),
        (600, 450, "抓取真实工厂"),
        (880, 450, "管理工厂信息"),
        (600, 570, "查看车辆列表"),
        (880, 570, "路径规划与回写"),
        (600, 690, "查看路线折线"),
        (880, 690, "导出仿真数据"),
    ]
    for cx, cy, name in uses:
        ellipse(d, cx, cy, 118, 42, name, f_u)

    def link(x1, y1, x2, y2):
        d.line([(x1, y1), (x2, y2)], fill=LINE, width=2)

    # 调度员：仿真控制 + 查看
    for cy in (210, 330, 450, 570, 690):
        link(222, 250, 482, cy)
    # 系统管理员：工厂数据 + 重置 + 导出
    for cy in (210, 450, 690):
        link(1278, 250, 998, cy)
    # 高德 API：路径规划
    link(222, 780, 762, 590)

    d.text((430, 942), "说明：实线为参与者与用例之间的关联；高德地图 API 作为外部系统参与路径规划。",
           font=font(18), fill=GREY)
    trim(img).save(path)


# ---------------------------------------------------------------- 活动图
def draw_activity(path):
    W, H = 1200, 1250
    f_t, f_s = font(32), font(20)
    img, d = new_canvas(W, H, None, f_t)

    cx = 560
    y = 110

    def start(y):
        d.ellipse([cx - 22, y, cx + 22, y + 44], fill=INK)
        return y + 44

    def action(y, label, h=64, w=380):
        box(d, cx - w / 2, y, w, h, label, f_s)
        return y + h

    def decide(y, label, h=90, w=380):
        d.polygon([(cx, y), (cx + w / 2, y + h / 2), (cx, y + h), (cx - w / 2, y + h / 2)],
                  fill=(255, 251, 235), outline=AMBER, width=2)
        lines = wrap(d, label, f_s, w - 70)
        lh = text_w(d, "国", f_s)[1] + 6
        ty = y + h / 2 - lh * len(lines) / 2
        for i, ln in enumerate(lines):
            tw = text_w(d, ln, f_s)[0]
            d.text((cx - tw / 2, ty + i * lh), ln, font=f_s, fill=INK)
        return y + h

    def end(y):
        d.ellipse([cx - 26, y, cx + 26, y + 52], outline=INK, width=3)
        d.ellipse([cx - 16, y + 10, cx + 16, y + 42], fill=INK)

    y = start(y)
    arrow(d, (cx, y), (cx, y + 40))
    y += 40
    y = action(y, "启动仿真：running = true")
    arrow(d, (cx, y), (cx, y + 34)); y += 34
    y = action(y, "创建 daemon 线程 sim-loop")
    arrow(d, (cx, y), (cx, y + 34)); y += 34
    y = action(y, "进入 while(running) 主循环", h=58)
    arrow(d, (cx, y), (cx, y + 30)); y += 30

    # 循环体
    loop_top = y
    y = action(y, "按缺口生成任务")
    arrow(d, (cx, y), (cx, y + 26)); y += 26
    y = action(y, "逐车推进：扣时间 / 沿折线前进")
    arrow(d, (cx, y), (cx, y + 26)); y += 26
    y = action(y, "状态结束？")
    arrow(d, (cx, y), (cx, y + 28)); y += 28
    y = action(y, "按马尔科夫矩阵抽样下一状态")
    arrow(d, (cx, y), (cx, y + 26)); y += 26
    y = action(y, "整轮写入数据库（单事务）")

    # 判断
    arrow(d, (cx, y), (cx, y + 30)); y += 30
    y = decide(y, "running ?")
    # 循环回边
    left_x = 300
    d.line([(cx - 190, y - 45 + 45), (left_x, y)], fill=LINE, width=2)
    d.line([(left_x, y), (left_x, loop_top + 20)], fill=LINE, width=2)
    arrow(d, (left_x, loop_top + 20), (cx - 200, loop_top + 20))
    d.text((left_x - 40, loop_top + 60), "是", font=f_s, fill=GREEN)
    d.text((left_x - 128, (loop_top + y) / 2), "睡眠 5 秒", font=font(18), fill=GREY)

    # 否 -> 结束
    arrow(d, (cx, y + 90), (cx, y + 130))
    d.text((cx + 12, y + 96), "否", font=f_s, fill=(220, 38, 38))
    y = y + 130
    end(y)
    trim(img).save(path)


# ---------------------------------------------------------------- 顺序图
def draw_sequence(path):
    W, H = 1500, 860
    f_t, f_s = font(32), font(20)
    img, d = new_canvas(W, H, None, f_t)

    actors = [(220, "调度员"), (550, "浏览器（Vue）"), (890, "SimulationService"), (1230, "MariaDB")]
    top = 150
    for x, name in actors:
        box(d, x - 105, top - 56, 210, 56, name, f_s, fill=LIGHT_GREY, outline=LINE)
        d.line([(x, top), (x, 790)], fill=LINE, width=2)

    def msg(y, x1, x2, label, dashed=False):
        arrow(d, (x1, y), (x2, y), dash=dashed, offset=(0, -26))
        tw = text_w(d, label, f_s)[0]
        d.rectangle([(x1 + x2) / 2 - tw / 2 - 4, y - 30, (x1 + x2) / 2 + tw / 2 + 4, y - 8], fill="white")
        d.text(((x1 + x2) / 2 - tw / 2, y - 28), label, font=f_s, fill=INK)

    msg(210, 220, 550, "点击「启动仿真」")
    msg(262, 550, 890, "POST /sim/start")
    msg(314, 890, 1230, "读取车辆与任务")
    msg(366, 1230, 890, "结果集", dashed=True)
    msg(418, 890, 550, "200 OK（running=true）", dashed=True)
    msg(482, 550, 890, "GET /sim/state（每 1 秒）")
    msg(534, 890, 1230, "查询车辆 / 任务")
    msg(586, 1230, 890, "结果集", dashed=True)
    msg(638, 890, 550, "JSON 快照", dashed=True)
    msg(700, 550, 890, "PUT /routes/{id}/points")
    msg(752, 890, 1230, "更新折线并重算里程")

    d.text((120, 800), "说明：虚线为返回消息；浏览器收到快照后按折线插值渲染动画（约 20 帧/秒）。",
           font=font(18), fill=GREY)
    trim(img).save(path)


# ---------------------------------------------------------------- 包图
def draw_package(path):
    W, H = 1300, 800
    f_t, f_s = font(32), font(21)
    img, d = new_canvas(W, H, None, f_t)

    def pkg(x, y, w, h, name, items):
        d.rectangle([x, y - 26, x + 120, y], fill=(219, 234, 254), outline=BLUE, width=2)
        d.text((x + 10, y - 23), name, font=f_s, fill=INK)
        d.rectangle([x, y, x + w, y + h], fill="white", outline=BLUE, width=2)
        ty = y + 12
        for it in items:
            d.text((x + 14, ty), it, font=font(18), fill=GREY)
            ty += 26

    pkg(480, 100, 340, 76, "controller", ["FactoryController  SimulationController"])
    pkg(480, 236, 340, 106, "service", ["SimulationService", "RouteService", "FactoryService"])
    pkg(880, 236, 300, 76, "dto", ["SimStateDto  VehicleDto"])
    pkg(120, 400, 340, 100, "mapper", ["VehicleMapper  MissionMapper", "RouteMapper"])
    pkg(760, 400, 320, 100, "util", ["GeoUtil  PolylineUtil", "AmapRouteClient"])
    pkg(120, 570, 340, 76, "entity", ["Vehicle  Mission  Route  Factory"])
    pkg(480, 570, 340, 86, "enums / config", ["VehicleState  MissionStatus", "SimProperties"])

    arrow(d, (650, 176), (650, 236), label="调用", f=f_s, offset=(16, -10))
    arrow(d, (560, 342), (300, 398), label="调用", f=f_s, offset=(-24, -12))
    arrow(d, (740, 342), (900, 398), label="依赖", f=f_s, offset=(28, -12))
    arrow(d, (650, 342), (650, 570), label="依赖", f=f_s, offset=(16, -10))
    arrow(d, (290, 500), (290, 570), label="映射", f=f_s, offset=(16, -10))
    arrow(d, (820, 262), (880, 262), label="返回", f=f_s, offset=(0, -26))
    trim(img).save(path)


# ---------------------------------------------------------------- 类图
def draw_class(path):
    W, H = 1620, 1050
    f_t, f_s, f_n = font(32), font(19), font(21)
    img, d = new_canvas(W, H, None, f_t)

    def cls(x, y, w, name, attrs, methods):
        head = 46
        body = 24 * (len(attrs) + len(methods)) + 34
        d.rectangle([x, y, x + w, y + head], fill=(219, 234, 254), outline=INK, width=2)
        tw = text_w(d, name, f_n)[0]
        d.text((x + (w - tw) / 2, y + 10), name, font=f_n, fill=INK)
        d.rectangle([x, y + head, x + w, y + head + body], fill="white", outline=INK, width=2)
        ty = y + head + 8
        for a in attrs:
            d.text((x + 12, ty), a, font=f_s, fill=INK)
            ty += 24
        d.line([(x, ty + 2), (x + w, ty + 2)], fill=INK, width=1)
        ty += 10
        for m in methods:
            d.text((x + 12, ty), m, font=f_s, fill=GREY)
            ty += 24
        return (x, y, w, head + body)

    cls(60, 110, 330, "SimulationService", [
        "- running : boolean",
        "- tick : int",
        "- simThread : Thread",
        "- props : SimProperties",
    ], [
        "+ start() / stop() / reset()",
        "+ tickOnce()",
        "- doTick()",
        "- advance(v, m)",
    ])

    cls(500, 110, 300, "Vehicle", [
        "- id : int",
        "- currentAction : int",
        "- currentLatitude : Double",
        "- currentLongitude : Double",
        "- remainingTime : int",
    ], ["+ getters / setters"])

    cls(940, 110, 300, "Factory", [
        "- id : int",
        "- factoryName : String",
        "- factoryLatitude : Double",
        "- factoryLongitude : Double",
    ], ["+ getters / setters"])

    cls(500, 450, 300, "Mission", [
        "- id : int",
        "- status : String",
        "- carId : Integer",
        "- factoryId : int",
        "- destFactoryId : int",
        "- routeId : Integer",
    ], ["+ getters / setters"])

    cls(940, 450, 320, "VehicleState", [
        "<<enum>>",
        "- IDLE / ACCEPTING",
        "- LOADING / MOVING",
        "- UNLOADING / WAITING",
    ], [
        "+ sampleNextState()",
        "+ isMoving()",
    ])

    cls(500, 745, 300, "Route", [
        "- id : int",
        "- roadType : String",
        "- distance : double",
        "- keyPoint : String(JSON)",
    ], ["+ getters / setters"])

    cls(940, 745, 320, "PolylineUtil", [
        "<<utility>>",
    ], [
        "+ totalKm(points)",
        "+ advance(points, km)",
        "+ synthetic(a, b)",
    ])

    # 关系
    arrow(d, (390, 200), (500, 200), label="管理 1..*", f=f_s, offset=(0, -24))
    arrow(d, (650, 358), (650, 450), label="指派", f=f_s, offset=(50, -6))
    arrow(d, (800, 520), (940, 520), label="使用", f=f_s, offset=(0, -24))
    arrow(d, (800, 470), (1060, 262), label="起点 / 终点", f=f_s, offset=(30, -18))
    arrow(d, (650, 700), (650, 745), label="引用 routeId", f=f_s, offset=(72, -8))
    arrow(d, (800, 845), (940, 845), label="调用", f=f_s, offset=(0, -24))
    trim(img).save(path)


# ---------------------------------------------------------------- 甘特图

GRAY_LBL = (107, 114, 128)


def draw_gantt(path):
    W, H = 1850, 900
    f_s, f_h = font(18), font(20)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    weeks = 12
    left, grid_right = 360, 1470
    col_w = (grid_right - left) / weeks
    top, row_h = 120, 56

    d.text((50, 92), "阶段 / 任务", font=f_h, fill=INK)
    d.text((grid_right + 24, 92), "参与成员", font=f_h, fill=INK)

    for i in range(weeks):
        x = left + i * col_w
        d.line([(x, top - 12), (x, top + row_h * 12)], fill=(229, 231, 235), width=1)
        tw = text_w(d, f"W{i+1}", f_s)[0]
        d.text((x + col_w / 2 - tw / 2, 72), f"W{i+1}", font=f_s, fill=GRAY_LBL)
    d.line([(grid_right, top - 12), (grid_right, top + row_h * 12)], fill=(229, 231, 235), width=1)

    tasks = [
        ("环境配置与数据库搭建", 1, 1, "陈嘉诩、邱崇翔、卢润山、王晓宇"),
        ("协作分工与项目分析", 2, 2, "陈嘉诩"),
        ("后端框架搭建", 3, 3, "陈嘉诩、邱崇翔、卢润山、王晓宇"),
        ("前端框架搭建", 4, 4, "邱崇翔、卢润山、王晓宇、张笑宇"),
        ("国庆假期", 5, 5, "—"),
        ("前后端联合调试", 6, 6, "陈嘉诩、邱崇翔、卢润山、王晓宇"),
        ("高德 API 接入与数据库连接", 7, 7, "邱崇翔、卢润山、张笑宇"),
        ("期中报告", 8, 8, "陈嘉诩、张笑宇"),
        ("状态马尔科夫表实现", 9, 9, "陈嘉诩、邱崇翔"),
        ("调试与功能补全", 10, 10, "邱崇翔、卢润山、王晓宇"),
        ("测试与缺陷修复", 11, 11, "王晓宇、张笑宇"),
        ("功能补全与验收发布", 12, 12, "卢润山、王晓宇、张笑宇"),
    ]

    for i, (name, s, e, members) in enumerate(tasks):
        y = top + i * row_h
        d.line([(50, y + row_h - 1), (W - 40, y + row_h - 1)], fill=(243, 244, 246), width=1)
        d.text((50, y + 16), name, font=f_s, fill=INK)

        x = left + (s - 1) * col_w + 5
        w = (e - s + 1) * col_w - 10
        if name == "国庆假期":
            d.rectangle([x, y + 12, x + w, y + 44], fill=(229, 231, 235), outline=(156, 163, 175), width=1)
            tw = text_w(d, "假期", f_s)[0]
            d.text((x + (w - tw) / 2, y + 19), "假期", font=f_s, fill=GRAY_LBL)
        else:
            d.rounded_rectangle([x, y + 12, x + w, y + 44], radius=8,
                                fill=(219, 234, 254), outline=(37, 99, 235), width=1)
        d.text((grid_right + 24, y + 16), members, font=f_s, fill=INK)

    d.text((50, top + row_h * 12 + 14),
           "说明：计划周次按校历周编号，W5 为国庆假期；每行任务名称为该周的主要交付目标。",
           font=font(17), fill=GRAY_LBL)
    img.crop((0, 60, img.width, img.height)).save(path)


def draw_factory_bar(path):
    W, H = 1200, 640
    f_t, f_s = font(28), font(20)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    data = [("成都", 23), ("德阳", 20), ("眉山", 19), ("资阳", 15)]
    left, top, bottom = 200, 110, 520
    max_v = 25
    bar_w = 120
    gap = (W - left - 120) / len(data)

    for i, (name, v) in enumerate(data):
        x = left + i * gap + gap / 2 - bar_w / 2
        h = (bottom - top) * v / max_v
        y = bottom - h
        d.rectangle([x, y, x + bar_w, bottom], fill=(219, 234, 254), outline=(37, 99, 235), width=2)
        tw = text_w(d, str(v), f_s)[0]
        d.text((x + bar_w / 2 - tw / 2, y - 32), str(v), font=f_s, fill=INK)
        tw2 = text_w(d, name, f_s)[0]
        d.text((x + bar_w / 2 - tw2 / 2, bottom + 14), name, font=f_s, fill=INK)

    d.line([(left - 20, bottom), (W - 60, bottom)], fill=(75, 85, 99), width=2)
    d.line([(left - 20, top - 20), (left - 20, bottom)], fill=(75, 85, 99), width=2)
    for v in range(0, 26, 5):
        y = bottom - (bottom - top) * v / max_v
        d.line([(left - 26, y), (left - 20, y)], fill=(75, 85, 99), width=1)
        tw = text_w(d, str(v), font(16))[0]
        d.text((left - 34 - tw, y - 10), str(v), font=font(16), fill=GRAY_LBL)

    d.text((50, 34), "工厂数量（家）", font=f_t, fill=INK)
    d.text((50, 566), "合计 77 家；按经纬度就近归属到四座城市统计。", font=font(17), fill=GRAY_LBL)
    trim(img).save(path)


def draw_distance_hist(path):
    W, H = 1200, 640
    f_t, f_s = font(28), font(20)
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)

    data = [("12~15", 54), ("15~20", 22), ("20~30", 1)]
    left, top, bottom = 200, 110, 520
    max_v = 60
    bar_w = 150
    gap = (W - left - 150) / len(data)

    for i, (name, v) in enumerate(data):
        x = left + i * gap + gap / 2 - bar_w / 2
        h = (bottom - top) * v / max_v
        y = bottom - h
        d.rectangle([x, y, x + bar_w, bottom], fill=(220, 252, 231), outline=(16, 185, 129), width=2)
        tw = text_w(d, str(v), f_s)[0]
        d.text((x + bar_w / 2 - tw / 2, y - 32), str(v), font=f_s, fill=INK)
        tw2 = text_w(d, name, f_s)[0]
        d.text((x + bar_w / 2 - tw2 / 2, bottom + 14), name, font=f_s, fill=INK)

    d.line([(left - 20, bottom), (W - 60, bottom)], fill=(75, 85, 99), width=2)
    d.line([(left - 20, top - 20), (left - 20, bottom)], fill=(75, 85, 99), width=2)
    for v in range(0, 61, 10):
        y = bottom - (bottom - top) * v / max_v
        d.line([(left - 26, y), (left - 20, y)], fill=(75, 85, 99), width=1)
        tw = text_w(d, str(v), font(16))[0]
        d.text((left - 34 - tw, y - 10), str(v), font=font(16), fill=GRAY_LBL)

    d.text((50, 34), "最近邻距离分布（km）", font=f_t, fill=INK)
    d.text((50, 566), "77 家工厂全部满足 ≥12 km 的间距约束，54 家的最近邻在 15 km 以内。",
           font=font(17), fill=GRAY_LBL)
    trim(img).save(path)


if __name__ == "__main__":
    draw_usecase(os.path.join(ASSETS, "usecase.png"))
    draw_activity(os.path.join(ASSETS, "activity.png"))
    draw_sequence(os.path.join(ASSETS, "sequence.png"))
    draw_package(os.path.join(ASSETS, "package.png"))
    draw_class(os.path.join(ASSETS, "class.png"))
    draw_gantt(os.path.join(ASSETS, "gantt.png"))
    draw_factory_bar(os.path.join(ASSETS, "factory_bar.png"))
    draw_distance_hist(os.path.join(ASSETS, "distance_hist.png"))
    print("done:", sorted(os.listdir(ASSETS)))