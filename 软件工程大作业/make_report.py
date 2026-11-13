# -*- coding: utf-8 -*-
"""生成《软件工程与实践大作业》报告 docx（正式版）。"""
import os

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

SONG = "宋体"
HEI = "黑体"
MONO = "Consolas"
INK = RGBColor(0x00, 0x00, 0x00)
GREY = RGBColor(0x59, 0x59, 0x59)
BLUE = RGBColor(0x00, 0x00, 0x00)

PERSON = {"a": "陈嘉诩", "b": "邱崇翔", "c": "卢润山", "d": "王晓宇", "e": "张笑宇"}

OUTLINE = [
    (1, "1  项目概述"),
    (2, "1.1  项目背景"),
    (2, "1.2  项目目标"),
    (2, "1.3  系统范围与边界"),
    (2, "1.4  术语与缩写"),
    (1, "2  开源项目分析：Eclipse SUMO"),
    (2, "2.1  选择理由与分析视角"),
    (2, "2.2  项目概况"),
    (2, "2.3  体系结构与模块划分"),
    (2, "2.4  关键设计与实现观察"),
    (2, "2.5  工程与社区实践"),
    (2, "2.6  与本项目的对比"),
    (2, "2.7  借鉴与差异"),
    (1, "3  需求分析"),
    (2, "3.1  利益相关方"),
    (2, "3.2  业务场景与流程"),
    (2, "3.3  功能需求"),
    (2, "3.4  用例图"),
    (2, "3.5  用例描述"),
    (2, "3.6  活动图"),
    (2, "3.7  顺序图"),
    (2, "3.8  非功能需求"),
    (2, "3.9  需求跟踪"),
    (1, "4  概要设计"),
    (2, "4.1  设计原则"),
    (2, "4.2  总体架构"),
    (2, "4.3  包结构与依赖关系"),
    (2, "4.4  核心类设计"),
    (2, "4.5  接口设计"),
    (2, "4.6  数据库设计"),
    (2, "4.7  基础数据与规模"),
    (2, "4.8  系统特征点"),
    (1, "5  详细设计"),
    (2, "5.1  仿真主循环"),
    (2, "5.2  状态转移算法"),
    (2, "5.3  任务生成"),
    (2, "5.4  原子抢单与并发控制"),
    (2, "5.5  路线几何与弧长插值"),
    (2, "5.6  前端渲染与动画"),
    (2, "5.7  性能优化"),
    (1, "6  测试"),
    (2, "6.1  测试策略"),
    (2, "6.2  功能测试用例"),
    (2, "6.3  接口测试"),
    (2, "6.4  性能测试"),
    (2, "6.5  一致性测试"),
    (2, "6.6  缺陷记录"),
    (2, "6.7  项目看板"),
    (2, "6.8  甘特图与进度偏差"),
    (1, "7  总结与展望"),
    (2, "7.1  完成情况"),
    (2, "7.2  不足"),
    (2, "7.3  展望"),
]


def set_font(run, size=12, bold=False, color=INK, cn=SONG, en=None):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run.font.name = en or cn
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn("w:rFonts"))
    if rFonts is None:
        rFonts = rPr.makeelement(qn("w:rFonts"), {})
        rPr.append(rFonts)
    rFonts.set(qn("w:eastAsia"), cn)
    rFonts.set(qn("w:ascii"), en or cn)
    rFonts.set(qn("w:hAnsi"), en or cn)


def para(doc, text, size=12, bold=False, color=INK, indent=True, space_after=6, line=1.5,
         align=WD_ALIGN_PARAGRAPH.JUSTIFY):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.line_spacing = line
    if indent:
        pf.first_line_indent = Pt(size * 2)
    r = p.add_run(text)
    set_font(r, size, bold, color)
    return p


def heading(doc, text, level=1):
    sizes = {1: 16, 2: 14, 3: 12}
    p = doc.add_paragraph(style=f"Heading {level}")
    pf = p.paragraph_format
    pf.space_before = Pt(16 if level == 1 else 12)
    pf.space_after = Pt(8 if level == 1 else 6)
    pf.keep_with_next = True
    r = p.add_run(text)
    set_font(r, sizes.get(level, 12), True, INK, HEI)
    return p


def bullet(doc, text, size=12):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.45
    r = p.add_run(text)
    set_font(r, size, False, INK)
    return p


def caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(10)
    r = p.add_run(text)
    set_font(r, 10.5, False, INK)


def figure(doc, name, cap, width=16.0, max_h=19.5):
    from PIL import Image as _Image
    path = os.path.join(ASSETS, name)
    im = _Image.open(path)
    w, h = im.size
    ratio = h / float(w)
    width_cm = min(width, max_h / ratio) if ratio > 0 else width
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(path, width=Cm(width_cm))
    caption(doc, cap)


def table(doc, headers, rows, widths=None, font_size=10, header_fill="E7E6E6"):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        hdr[i].text = ""
        p = hdr[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        set_font(r, font_size, True, INK, HEI)
        shd = OxmlElement("w:shd")
        shd.set(qn("w:fill"), header_fill)
        hdr[i]._tc.get_or_add_tcPr().append(shd)
    for row in rows:
        cells = t.add_row().cells
        for i, val in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            txt = str(val)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if len(txt) > 8 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(txt)
            set_font(r, font_size, False, INK)
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        trPr.append(OxmlElement("w:cantSplit"))
    # 表头跨页重复
    hdr_trPr = t.rows[0]._tr.get_or_add_trPr()
    hdr_trPr.append(OxmlElement("w:tblHeader"))
    if widths:
        total = sum(widths)
        if total > 16.0:
            widths = [w * 16.0 / total for w in widths]
        t.autofit = False
        tblPr = t._tbl.tblPr
        tblW = OxmlElement("w:tblW")
        tblW.set(qn("w:type"), "dxa")
        tblW.set(qn("w:w"), str(int(sum(widths) * 567)))
        tblPr.append(tblW)
        for i, w in enumerate(widths):
            t.columns[i].width = Cm(w)
            for row in t.rows:
                row.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


def code_block(doc, text, size=9):
    t = doc.add_table(rows=1, cols=1)
    t.style = "Table Grid"
    cell = t.rows[0].cells[0]
    cell.text = ""
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), "F5F6F8")
    cell._tc.get_or_add_tcPr().append(shd)
    for i, line in enumerate(text.split("\n")):
        p = cell.paragraphs[0] if i == 0 else cell.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.12
        r = p.add_run(line)
        set_font(r, size, False, INK, cn=SONG, en=MONO)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def add_toc(doc):
    p = doc.add_paragraph()
    r = p.add_run()
    b = OxmlElement("w:fldChar")
    b.set(qn("w:fldCharType"), "begin")
    i = OxmlElement("w:instrText")
    i.set(qn("xml:space"), "preserve")
    i.text = 'TOC \\o "1-2" \\h \\z \\u'
    s = OxmlElement("w:fldChar")
    s.set(qn("w:fldCharType"), "separate")
    for el in (b, i, s):
        r._r.append(el)

    for level, text in OUTLINE:
        tp = doc.add_paragraph()
        tp.paragraph_format.space_after = Pt(3)
        tp.paragraph_format.left_indent = Pt(0 if level == 1 else 18)
        tp.paragraph_format.line_spacing = 1.2
        tr = tp.add_run(text)
        set_font(tr, 11 if level == 1 else 10.5, level == 1, INK)

    ep = doc.add_paragraph()
    er = ep.add_run()
    e = OxmlElement("w:fldChar")
    e.set(qn("w:fldCharType"), "end")
    er._r.append(e)


doc = Document()
sec = doc.sections[0]
sec.page_width = Cm(21)
sec.page_height = Cm(29.7)
sec.top_margin = Cm(2.5)
sec.bottom_margin = Cm(2.5)
sec.left_margin = Cm(2.5)
sec.right_margin = Cm(2.5)

footer_p = sec.footer.paragraphs[0]
footer_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
fr = footer_p.add_run()
set_font(fr, 9, False, GREY)
fld = OxmlElement("w:fldSimple")
fld.set(qn("w:instr"), "PAGE")
footer_p._p.append(fld)

style = doc.styles["Normal"]
style.font.name = SONG
style.font.size = Pt(12)
style.element.rPr.rFonts.set(qn("w:eastAsia"), SONG)

# ---------------------------------------------------------------- 封面
for _ in range(3):
    doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("软件工程与实践")
set_font(r, 30, True, INK, HEI)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("大 作 业 报 告")
set_font(r, 26, True, INK, HEI)
for _ in range(2):
    doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("货运调度仿真系统")
set_font(r, 22, True, BLUE, HEI)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("——基于概率状态机与真实路网的货运调度仿真平台")
set_font(r, 12, False, GREY)
for _ in range(2):
    doc.add_paragraph()

info = [
    ("组　　号", "第 X 组"),
    ("小组成员", "陈嘉诩（组长）、邱崇翔、卢润山、王晓宇、张笑宇"),
    ("项目角色", "计划·分析·设计（陈嘉诩）｜开发（邱崇翔、卢润山）｜测试（王晓宇）｜验收与发布（张笑宇）"),
    ("开发模型", "敏捷迭代（两周一个迭代，远程仓库协作）"),
    ("课程名称", "软件工程与实践"),
    ("提交日期", "2026 年 11 月"),
]
t = doc.add_table(rows=0, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
for k, v in info:
    cells = t.add_row().cells
    cells[0].width = Cm(3.2)
    cells[1].width = Cm(9.8)
    p0 = cells[0].paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p0.add_run(k + "：")
    set_font(r, 11.5, True, INK, HEI)
    p1 = cells[1].paragraphs[0]
    r = p1.add_run(v)
    set_font(r, 11, False, INK)

doc.add_page_break()

# ---------------------------------------------------------------- 目录
heading(doc, "目　　录", 1)
para(doc, "（本目录在 Microsoft Word 中打开时会自动更新页码；若未更新，可全选后按 F9。）",
     size=10.5, color=GREY, indent=False)
add_toc(doc)

doc.add_page_break()

# ---------------------------------------------------------------- 分工
heading(doc, "成员分工与角色说明", 1)
para(doc, "本项目以五人小组承担全部工程活动。分工遵循“职责单一、界面清晰、可交接”的原则："
          "一人负责计划、需求分析与系统设计，两人分别承担后端与前端开发，一人负责测试与质量把关，"
          "一人负责验收、配置管理与发布。每位成员在主职责之外参与评审与联调，避免单点依赖。")
table(
    doc,
    ["成员", "角色定位", "主要职责", "关键交付物"],
    [
        ["陈嘉诩（组长）", "计划 / 分析 / 设计",
         "迭代计划与进度跟踪；需求调研与需求规格；系统架构、数据库与关键算法设计；组织评审",
         "项目计划、需求规格、UML 图、数据库设计、设计说明"],
        ["邱崇翔", "后端开发",
         "仿真主循环、状态机与任务生成实现；路线服务与接口；性能优化",
         "SimulationService、RouteService、Mapper 映射、接口实现"],
        ["卢润山", "前端开发",
         "地图与车辆渲染；插值与动画；任务看板；与后端联调；构建脚本",
         "MapView.vue、VehiclePanel.vue、TaskPanel.vue、打包脚本"],
        ["王晓宇", "测试",
         "测试用例设计；接口与功能测试；性能与一致性验证；缺陷跟踪与回归",
         "测试用例表、缺陷记录、测试报告"],
        ["张笑宇", "验收与发布",
         "需求验收；配置管理与基线；版本发布与部署说明；文档整合",
         "配置项清单、发布说明、部署脚本文档"],
    ],
    widths=[3.0, 3.2, 6.6, 4.6],
    font_size=9.5,
)
para(doc, "角色之间约定三条接口规则：一是需求变更必须由陈嘉诩登记后同步给开发与测试；"
          "二是任何提交必须由另一名成员阅读 diff 后才合入主干；"
          "三是缺陷由王晓宇统一登记、修复后由其复测关闭，张笑宇在发布前核对配置项齐全。")

doc.add_page_break()

# ---------------------------------------------------------------- 1 概述
heading(doc, "1  项目概述", 1)

heading(doc, "1.1  项目背景", 2)
para(doc, "城市货运是城市物流的末端环节，承担着工厂到仓库、仓库到门店的短途运输。"
          "在实际运营中，调度员通常依据电话、微信与纸质单据安排车辆：无法实时掌握车辆位置，"
          "也难以预判装卸排队、道路拥堵带来的等待。结果是车辆空驶率居高不下、货物在工厂月台积压、"
          "客户对到货时间缺乏预期。")
para(doc, "这类问题很难通过“上线一个真实调度系统”来解决。一方面，真实调度需要接入车辆、司机与真实订单，"
          "成本高且不可重复；另一方面，调度策略的优劣往往要在成百上千次运行中才能显现，"
          "真实车队根本无法承受如此高的实验成本。因此，本项目选择另一个切入点："
          "构建一个可重复、可调参的仿真平台，用概率模型刻画车辆行为，用真实路网约束车辆轨迹，"
          "用真实工厂点位组织运输任务，从而在几分钟内复现数小时的城市配送过程。")
para(doc, "从软件工程的角度看，这个系统同时具备三类典型特征：一是存在明确的状态机与时间推进逻辑，"
          "需要严谨的建模与并发控制；二是依赖外部服务（高德地图）提供路网与路径规划能力，"
          "需要处理接口不稳定与配额限制；三是需要可视化呈现，前端与后端存在较强的实时交互。"
          "这三点使项目成为一个覆盖需求、设计、实现、测试全过程的合适载体。")

heading(doc, "1.2  项目目标", 2)
para(doc, "第一阶段的目标可以概括为“打通一条主链路”：从任务产生，到车辆接单、装货、运输、卸货、完成，"
          "全过程由系统自动推进，并在浏览器上以地图和看板的形式实时呈现。具体分解为四个可验证的目标：")
bullet(doc, "车辆行为可概率化：用 6 状态马尔科夫链刻画车辆在空闲、接单、装货、运输、卸货、等待之间的转移，"
            "转移由概率矩阵抽样决定，而不是写死的顺序链。")
bullet(doc, "任务闭环可自动运行：任务按空闲车辆缺口自动生成，车辆原子抢单，保证一车一单、一单不重复。")
bullet(doc, "轨迹可信：每趟运输对应一条真实道路折线，车辆沿折线按弧长推进，拐弯处不切角。")
bullet(doc, "过程可观测：前端 1 秒刷新一次，地图显示车辆位置与当前路段，看板显示任务分列状态，"
            "并支持启动、暂停、重置。")
para(doc, "四个目标之间存在依赖关系：状态机决定车辆“想做什么”，任务生成决定“有什么可做”，"
          "路线与插值决定“怎么走”，可视化决定“能否被观察”。任意一环缺失，整条链路都无法验证，"
          "这也是本项目在实现顺序上先做主循环、后做前端渲染的原因。")

heading(doc, "1.3  系统范围与边界", 2)
para(doc, "为避免范围蔓延，第一阶段明确划定系统边界。范围内的功能必须交付且可演示，"
          "范围外的内容在文档中显式说明为后续工作，不在本阶段承诺。")
table(
    doc,
    ["范围内", "范围外（留待后续）"],
    [
        ["单机仿真：10 辆车、77 家工厂，覆盖成都、德阳、眉山、资阳四市", "多用户、账号体系与权限控制"],
        ["桌面浏览器访问，单实例部署，支持启动/暂停/重置", "真实车辆 GPS 接入与在线调度"],
        ["仿真参数集中在配置文件，可调但不可在线编辑", "在线参数面板与多方案对比实验"],
        ["路线来自高德驾车规划，失败时以合成折线兜底", "多模式交通（公路、铁路、水运）联运"],
        ["工厂数据来自高德 POI 检索并按最小间距筛选", "订单、计费、客户签收等业务闭环"],
    ],
    widths=[8.6, 8.6],
    font_size=9.5,
)
para(doc, "边界的划定也带来一个直接的工程约束：系统不需要考虑分布式部署与水平扩展，"
          "因此可以放心地采用“单进程 + 单数据库”的简单结构，把精力集中在仿真模型与轨迹质量上。"
          "这一取舍在第四章的架构设计中有进一步说明。")

heading(doc, "1.4  术语与缩写", 2)
table(
    doc,
    ["术语 / 缩写", "含义"],
    [
        ["tick（轮次）", "仿真推进的一个时间步。默认 5 秒真实时间代表 5 分钟仿真时间"],
        ["任务（mission）", "一次从起点工厂到终点工厂的运输任务，具有状态、货物、路线等属性"],
        ["折线（polyline）", "路线在数据库中以经纬度点序列（JSON 数组）保存，前端据此绘制与插值"],
        ["弧长（arc length）", "沿折线累计的行进距离，用于把“进度”从比例换算成公里数"],
        ["OD 对", "起点（Origin）与终点（Destination）的组合，用于描述任务的空间分布"],
        ["状态守恒", "任意时刻满足：任务总数 = 待接单 + 进行中 + 已完成"],
        ["基线（baseline）", "经评审确认、此后变更需受控的配置项集合"],
        ["CMMI", "能力成熟度模型集成，本项目参考其 2 级过程域组织部分过程文档"],
    ],
    widths=[3.6, 13.6],
    font_size=9.5,
)

# ---------------------------------------------------------------- 2 开源分析
heading(doc, "2  开源项目分析：Eclipse SUMO", 1)

heading(doc, "2.1  选择理由与分析视角", 2)
para(doc, "在需求分析之前安排开源项目分析，目的是先建立一个“同类系统应该长什么样”的参照系。"
          "本项目的核心问题是车辆在路网中的运行与调度，因此选择一个同领域的成熟开源项目进行分析，"
          "可以在架构划分、外部接口设计、工程实践三个层面获得可借鉴的结论。")
para(doc, "Eclipse SUMO（Simulation of Urban MObility）是目前应用最广的开源交通仿真套件，"
          "自 2001 年起由德国航空航天中心（DLR）交通系统研究所持续开发，2018 年成为 Eclipse 基金会项目。"
          "选择它有三个理由：其一，问题域一致，都是“车辆 + 路网 + 时间推进”；"
          "其二，它的模块划分与接口设计被大量论文与工程实践检验过；其三，它的开源治理与持续集成做法，"
          "对一个小型课程团队同样有参考价值。")

heading(doc, "2.2  项目概况", 2)
table(
    doc,
    ["项目属性", "内容"],
    [
        ["全称", "Eclipse SUMO（Simulation of Urban MObility）"],
        ["发起", "2001 年，德国航空航天中心（DLR）交通系统研究所"],
        ["治理", "2018 年成为 Eclipse 基金会项目，主开发仍在 DLR，社区贡献持续增长"],
        ["许可证", "Eclipse Public License V2（EPL-2.0），允许商业使用与二次开发"],
        ["实现语言", "仿真内核以 C++ 为主，工具链与扩展以 Python 为主"],
        ["当前版本", "1.28.0（每次发布带独立 DOI，便于学术引用）"],
        ["代表文献", "Microscopic Traffic Simulation using SUMO，IEEE ITSC 2018"],
        ["应用领域", "信号配时评估、路径选择、自动驾驶与 V2X 仿真、排放计算、停车场仿真等"],
    ],
    widths=[3.2, 14.0],
    font_size=9.5,
)
para(doc, "从版本与引用的规范化程度可以看出，SUMO 已经不是“一个实验室的小工具”，"
          "而是具备版本发布、数字对象标识、论文引用体系与研究社区支撑的基础设施型开源项目。"
          "这种“可引用、可复现”的定位，对科研类软件尤其重要。")

heading(doc, "2.3  体系结构与模块划分", 2)
para(doc, "SUMO 最值得借鉴的一点，是它没有把全部功能塞进一个可执行文件，而是按“路网—需求—仿真—评估”"
          "拆成一组职责单一的命令行工具，工具之间通过标准化文件（如路网 .net.xml、路线 .rou.xml）交换数据。")
table(
    doc,
    ["模块", "职责", "对应的工程思想"],
    [
        ["sumo / sumo-gui", "微观仿真内核，分别提供命令行与图形界面", "同一内核、两种前端，界面与模型分离"],
        ["netconvert / netedit", "路网导入与可视化编辑", "数据转换与编辑工具独立，便于替换数据源"],
        ["netgenerate", "生成抽象路网（网格、环形等）", "支持无真实数据的场景构造"],
        ["od2trips", "把 OD 矩阵转换为出行需求", "需求建模与仿真的解耦"],
        ["duarouter / jtrrouter / dfrouter", "按不同输入（OD、转向比、检测器数据）生成路线", "同一目标、多种算法并存"],
        ["activitygen", "由人口数据推导出行需求", "引入外部统计数据的扩展点"],
        ["polyconvert", "导入地理要素用于可视化", "展示与计算分离"],
        ["TraCI", "对外提供远程控制接口，可在线读写仿真状态", "把内核变成可被外部程序驱动的服务"],
    ],
    widths=[4.4, 7.2, 5.6],
    font_size=9,
)
para(doc, "这种“文件格式即接口”的设计带来两个直接好处：一是每个工具都可以被单独替换或重写，"
          "不影响其他工具；二是第三方可以在不修改内核的前提下，通过生成或解析文件接入自己的算法。"
          "本项目的路线模块采用了类似的思路：路线以折线 JSON 存储在数据库中，"
          "后端与前端都可以读写，规划逻辑可以替换而不用改动仿真主循环。")

heading(doc, "2.4  关键设计与实现观察", 2)
para(doc, "在实现层面，SUMO 有四点设计值得记录：")
bullet(doc, "微观模型的粒度：以车辆为单位建模，逐车维护位置、速度、跟驰关系，"
            "因此可以输出单车轨迹，支撑信号优化、排放计算等下游分析。这与本项目“逐车推进”的做法一致。")
bullet(doc, "时间推进机制：仿真按固定步长推进，步长可配置。步长越小越精细，但计算量线性增长，"
            "这与本项目“5 秒一轮、一轮 5 分钟”的取舍属于同一类问题。")
bullet(doc, "外部控制接口：TraCI 允许外部程序在每一步读写仿真状态，使 SUMO 可以作为“环境”被强化学习算法调用。"
            "这一点对本项目的启示是：仿真核心应当尽量无状态化、可被外部查询与驱动。")
bullet(doc, "可复现性：每次发布带 DOI，配置文件与随机种子可固定，保证实验可复现。"
            "本项目虽然规模小，但也通过“参数集中在 application.yaml”实现了类似的可复现性。")

heading(doc, "2.5  工程与社区实践", 2)
para(doc, "除技术设计外，SUMO 的工程实践同样值得观察：")
bullet(doc, "持续集成与每日构建：官网提供每日构建与测试状态页面，任何一次提交导致的回归都会被发现，"
            "这保证了长周期演进中的稳定性。")
bullet(doc, "文档与代码同仓演进：用户文档、教程、开发者文档与代码一同维护，降低新人上手成本。")
bullet(doc, "发布与引用规范：版本号、变更日志、DOI 形成完整链路，便于教学与科研引用。")
bullet(doc, "社区治理：由基金会托管，贡献者来自多所高校与企业，"
            "通过邮件列表、议题与年度会议协作，形成了可持续的贡献机制。")
para(doc, "对课程团队而言，完全照搬这套体系并不现实，但其中两条可以低成本落地："
          "一是“代码与文档同仓”，本项目将设计脚本、图表与报告源文件与代码放在同一个 Git 仓库；"
          "二是“每次提交可追溯”，提交信息统一采用“类型: 概述”的格式，便于回溯问题引入点。")

heading(doc, "2.6  与本项目的对比", 2)
table(
    doc,
    ["维度", "Eclipse SUMO", "本项目"],
    [
        ["目标", "通用交通仿真平台，覆盖信号、行人、排放等", "面向城市货运调度的仿真验证平台"],
        ["建模粒度", "车辆、车道、信号灯、行人等多主体", "车辆与任务两级，工厂与路线作为约束"],
        ["路网来源", "专门的路网转换工具，支持 OSM 等格式", "直接调用高德驾车规划，结果落库为折线"],
        ["时间推进", "可配置步长的固定步长推进", "5 秒一轮、一轮代表 5 分钟"],
        ["外部接口", "TraCI（TCP），可被任意语言驱动", "REST 接口，浏览器轮询快照"],
        ["实现语言", "C++ 内核 + Python 工具链", "Java（Spring Boot）+ Vue 3"],
        ["规模", "百万行级，长周期维护", "约 3800 行，单人可维护"],
    ],
    widths=[2.8, 7.0, 7.4],
    font_size=9,
)

heading(doc, "2.7  借鉴与差异", 2)
para(doc, "通过上述对比，本项目在三个方面明确借鉴了 SUMO 的做法：")
bullet(doc, "模块职责单一：把仿真、路线、工厂拆成三个服务类，各自可独立测试与替换，"
            "避免出现“一个类包揽全部逻辑”的情况。")
bullet(doc, "外部能力可替换：路线规划优先调用真实接口，失败时回退到合成折线，"
            "与 SUMO“多路由算法并存”的思路一致。")
bullet(doc, "接口驱动协作：先约定 REST 接口，前后端并行开发，减少相互等待。")
para(doc, "差异同样明显。SUMO 是通用平台，追求覆盖广度与模型精度；本项目是面向特定策略验证的小型系统，"
          "追求的是“闭环可运行、轨迹可信、结果可校验”。因此本项目没有引入复杂的跟驰模型与信号控制，"
          "而是把复杂度放在状态机与任务闭环上，这是由研究目标决定的合理取舍。")

# ---------------------------------------------------------------- 3 需求
heading(doc, "3  需求分析", 1)

heading(doc, "3.1  利益相关方", 2)
para(doc, "识别利益相关方是需求分析的第一步。本系统的直接使用者是调度观察者，"
          "间接相关方包括数据维护者、外部地图服务提供方以及课程指导教师。")
table(
    doc,
    ["利益相关方", "身份", "关注点", "对需求的影响"],
    [
        ["调度员", "主要用户", "能否直观看到车辆位置、状态与任务进展", "决定界面的信息密度与刷新频率"],
        ["系统管理员", "次要用户", "工厂数据是否准确、能否快速重置环境", "决定工厂导入与重置功能"],
        ["高德地图平台", "外部系统", "接口调用配额、返回质量与稳定性", "决定路线规划放在浏览器侧并做降级"],
        ["课程指导教师", "评审方", "过程文档是否完整、设计是否可辩护", "决定文档结构、图表与过程记录"],
        ["后续开发者", "维护方", "代码是否易读、参数是否可调", "决定配置外置与分层设计"],
    ],
    widths=[3.2, 2.4, 6.4, 5.2],
    font_size=9,
)

heading(doc, "3.2  业务场景与流程", 2)
para(doc, "系统的核心业务场景是“无人干预的自动运行”：调度员打开页面后，仿真自动开始，"
          "系统周期性生成任务、为车辆分派任务、驱动车辆沿路行驶，直至任务完成。整个过程可分为六个环节：")
para(doc, "（1）任务产生。系统根据当前空闲车辆数量与待接单任务数量的差额生成新任务，"
          "每个任务包含起点工厂、终点工厂、货物类型与预计距离。")
para(doc, "（2）任务分派。当某辆车进入“接单行驶”状态时，系统在待接单池中挑选装货点距离最近的一条任务，"
          "以条件更新方式完成抢占，成功后才把任务与车辆绑定。")
para(doc, "（3）装货。车辆抵达起点工厂后进入装货状态，固定耗时 30 分钟。")
para(doc, "（4）运输。车辆沿起点到终点的真实道路折线行驶，每轮前进 5 公里（60 km/h × 5 分钟）。")
para(doc, "（5）卸货。抵达终点工厂后进入卸货状态，固定耗时 30 分钟，随后任务转为已完成。")
para(doc, "（6）等待与再分配。车辆可能进入短暂的停留等待（5 分钟），随后回到空闲，等待下一次抽样。")
para(doc, "上述流程中，(1)(2) 属于业务规则，(3)~(6) 属于时间推进。将两者分离是设计阶段的重要决定，"
          "也使需求可以按“业务规则”和“时间模型”两类分别描述与验证。")

heading(doc, "3.3  功能需求", 2)
para(doc, "依据业务场景，梳理出 12 项功能需求。每项需求均可追溯到具体的用例与测试用例（见 3.9 节）。")
table(
    doc,
    ["编号", "需求名称", "需求描述", "优先级"],
    [
        ["FR-01", "启动 / 暂停仿真", "控制仿真线程的启停；暂停后状态保持不变，恢复后从断点继续", "高"],
        ["FR-02", "重置仿真", "清空任务与路线，车辆回到工厂点位，轮次与仿真时间归零", "高"],
        ["FR-03", "实时状态查询", "返回轮次、仿真时间、车辆位置与状态、三类任务列表及剩余时间", "高"],
        ["FR-04", "任务自动生成", "按空闲车辆缺口生成任务，受每轮上限与待接单池容量约束", "高"],
        ["FR-05", "车辆抢单", "进入接单状态时抢占最近任务，条件更新保证一车一单", "高"],
        ["FR-06", "状态概率转移", "按马尔科夫矩阵抽样下一状态，并按时长规则推进", "高"],
        ["FR-07", "路线生成与回写", "任务生成路线；前端规划真实道路后回写并重算里程", "高"],
        ["FR-08", "沿折线行驶", "按弧长推进车辆位置，位置可持久化并在重启后恢复", "高"],
        ["FR-09", "工厂抓取与导入", "按城市抓取真实 POI，按最小间距过滤后入库", "中"],
        ["FR-10", "车辆与任务看板", "左栏展示车辆卡片与进度，右栏展示任务分列状态", "中"],
        ["FR-11", "地图可视化", "车辆标记、当前行驶段高亮、方向箭头、状态配色", "中"],
        ["FR-12", "仿真参数配置", "通过配置文件调整轮次间隔、时长、概率、任务上限等参数", "低"],
    ],
    widths=[1.6, 3.4, 9.8, 1.6],
    font_size=9,
)
para(doc, "对其中四项高优先级需求作补充说明。FR-03 的返回值不仅是位置，"
          "还包含由当前状态实时估算的剩余分钟数，避免前端自行推算造成口径不一致；"
          "FR-04 的“缺口”定义为“空闲车辆数减去待接单任务数”，该定义保证任务供给与运力大致匹配；"
          "FR-06 的时长规则中，行驶类按距离计时、作业类按固定时长，二者不可混用；"
          "FR-08 要求位置可从数据库恢复，因此推进算法必须以“当前坐标 + 折线”为输入，而不能依赖内存中的索引。")

heading(doc, "3.4  用例图", 2)
para(doc, "系统包含两类人员角色与一个外部系统。调度员负责仿真的运行与观察，"
          "系统管理员负责基础数据维护与重置，高德地图 API 作为外部参与者提供路径规划能力。")
figure(doc, "usecase.png", "图 3-1  系统用例图", width=16.0)
para(doc, "用例之间存在两条隐含的依赖关系：其一，“查看实时状态”隐式依赖“沿折线行驶”的推进结果，"
          "若推进失败，快照中的位置将不再变化；其二，“路径规划与回写”依赖“查看路线折线”，"
          "因为前端需要先取得当前折线，才能判断是否需要重新规划。这两条依赖在顺序图（3.7 节）中有体现。")

heading(doc, "3.5  用例描述", 2)
para(doc, "选取三个最能体现系统特征的用例作详细描述：实时状态查询（高频、性能敏感）、"
          "抓取真实工厂（涉及外部服务与业务规则）、重置仿真（涉及多表清理与状态一致性）。")

heading(doc, "UC-03  查看实时状态", 3)
table(
    doc,
    ["项目", "内容"],
    [
        ["用例编号", "UC-03"],
        ["参与者", "调度员（主要）、浏览器（辅助）"],
        ["前置条件", "后端已启动；仿真处于运行或暂停状态；数据库可访问"],
        ["触发条件", "浏览器定时器每 1000 毫秒触发一次"],
        ["基本流程", "1. 浏览器发起 GET /sim/state；2. 后端查询未删除车辆与进行中任务；"
                 "3. 组装快照并按状态估算剩余分钟；4. 返回 JSON；5. 前端更新卡片与地图"],
        ["异常流程", "后端不可达：提示网络异常并保留上一次快照；数据库异常：返回 500 并记录日志"],
        ["后置条件", "界面显示最新位置；仿真状态与任务状态不变"],
        ["性能要求", "50 辆车时单次响应不超过 100 毫秒"],
    ],
    widths=[2.6, 14.6],
    font_size=9.5,
)

heading(doc, "UC-05  抓取真实工厂", 3)
table(
    doc,
    ["项目", "内容"],
    [
        ["用例编号", "UC-05"],
        ["参与者", "系统管理员（主要）、高德地图 API（外部）"],
        ["前置条件", "地图已加载；高德 JS API key 有效且未超配额"],
        ["基本流程", "1. 按城市与关键词检索 POI；2. 本地去重；3. 提交 POST /factories/import；"
                 "4. 后端按同名同坐标与最小间距双重过滤；5. 返回新增数量；6. 前端刷新工厂列表"],
        ["异常流程", "检索配额不足：提示稍后重试；导入失败：保留原有数据并提示错误"],
        ["业务规则", "同名同坐标视为重复；与已有工厂距离小于 12 公里的点不导入"],
        ["后置条件", "工厂表新增若干记录；已有记录不受影响"],
    ],
    widths=[2.6, 14.6],
    font_size=9.5,
)

heading(doc, "UC-02  重置仿真", 3)
table(
    doc,
    ["项目", "内容"],
    [
        ["用例编号", "UC-02"],
        ["参与者", "调度员（主要）"],
        ["前置条件", "仿真处于运行或暂停状态"],
        ["基本流程", "1. 停止仿真线程并置 running=false；2. 删除全部任务；3. 重置车辆状态与坐标，"
                 "随机停靠到工厂点位；4. 轮次与仿真时间归零；5. 清理路线与缓存；6. 返回成功"],
        ["异常流程", "线程中断超时：记录日志并强制置空线程引用；删除失败：整体回滚"],
        ["业务规则", "重置为幂等操作，连续执行结果一致"],
        ["后置条件", "任务表为空；车辆均为空闲且在工厂点位；轮次为 0"],
    ],
    widths=[2.6, 14.6],
    font_size=9.5,
)

heading(doc, "3.6  活动图", 2)
para(doc, "下图描述一轮仿真的处理流程。流程的要点是“先补任务、再推车辆、最后统一落库”，"
          "并且整个流程包裹在一个事务中，任何一个环节失败都整体回滚。")
figure(doc, "activity.png", "图 3-2  一轮仿真活动图", width=15.0)
para(doc, "活动图中有两处与实现强相关的细节：一是“状态结束？”的判断发生在车辆推进之后，"
          "只有剩余时间归零才触发抽样；二是循环回到起点前有一个“睡眠 5 秒”的动作，"
          "它决定了系统的实际节奏。这两点在 5.1 节的代码中有对应实现。")

heading(doc, "3.7  顺序图", 2)
para(doc, "下图描述从点击“启动仿真”到前端持续轮询、并把真实道路折线回写到后端的过程。"
          "顺序图揭示了一个容易被忽略的事实：路线规划并不在后端完成，而是在浏览器中调用高德 JS API 后回写。")
figure(doc, "sequence.png", "图 3-3  启动仿真与状态轮询顺序图", width=16.0)
para(doc, "这一设计源于一个现实约束：高德的 JS API key 与“Web 服务”key 类型不同，"
          "用前者调用服务端接口会返回 USERKEY_PLAT_NOMATCH。因此把规划放在浏览器，"
          "后端只负责存取折线，既绕开了 key 类型问题，也让规划结果可以被后续所有车辆复用。")

heading(doc, "3.8  非功能需求", 2)
table(
    doc,
    ["编号", "类别", "要求", "验证方式"],
    [
        ["NFR-01", "性能", "50 辆车时单轮计算不超过 200 ms", "压力测试，统计 20 秒内推进轮数"],
        ["NFR-02", "实时性", "前端刷新周期 1 秒，动画不低于 15 帧/秒", "浏览器性能面板观察"],
        ["NFR-03", "一致性", "任务总数满足状态守恒，无悬空车辆引用", "运行中抽样校验"],
        ["NFR-04", "可用性", "浏览器打开即自动开始，无需手工配置", "首次访问验证"],
        ["NFR-05", "可维护性", "仿真参数外置；业务与算法分层", "代码评审"],
        ["NFR-06", "可部署性", "支持单进程部署，一条命令启动", "按部署说明复现"],
        ["NFR-07", "容错性", "外部路线规划失败时不影响仿真推进", "断网与配额耗尽场景验证"],
    ],
    widths=[2.0, 2.2, 8.4, 4.6],
    font_size=9.5,
)

heading(doc, "3.9  需求跟踪", 2)
para(doc, "需求跟踪矩阵用于保证“每条需求都有设计对应、每个设计都有测试覆盖”，"
          "也是后续需求变更时评估影响范围的依据。")
table(
    doc,
    ["需求", "对应用例", "设计元素", "测试用例"],
    [
        ["FR-01", "UC-01", "SimulationService.start / stop", "TC-01、TC-02"],
        ["FR-02", "UC-02", "SimulationService.reset", "TC-03"],
        ["FR-03", "UC-03", "SimulationController.state、SimStateDto", "TC-11"],
        ["FR-04", "UC-04", "SimulationService.generateMissions", "TC-04"],
        ["FR-05", "UC-06", "MissionMapper.claim", "TC-05"],
        ["FR-06", "UC-04", "VehicleState.TRANSITIONS、sampleNextState", "TC-06"],
        ["FR-07", "UC-07", "RouteService、PUT /routes/{id}/points", "TC-07"],
        ["FR-08", "UC-08", "PolylineUtil.advance", "TC-08"],
        ["FR-09", "UC-05", "FactoryServiceImpl.importFactories", "TC-09、TC-10"],
        ["FR-10", "UC-09", "VehiclePanel、TaskPanel", "TC-11"],
        ["FR-11", "UC-10", "MapView.renderLegs", "TC-08、TC-11"],
        ["FR-12", "—", "application.yaml、SimProperties", "回归测试"],
    ],
    widths=[1.8, 2.6, 7.4, 5.4],
    font_size=9,
)

# ---------------------------------------------------------------- 4 概要设计
heading(doc, "4  概要设计", 1)

heading(doc, "4.1  设计原则", 2)
para(doc, "概要设计阶段确立了四条原则，并在后续实现中被反复引用：")
bullet(doc, "分层解耦：控制器只负责参数接收与结果返回，业务与事务集中在服务层，"
            "SQL 收敛在 MyBatis 映射文件，实体只承载数据。")
bullet(doc, "时间可调：轮次间隔、仿真步长、各类时长、任务概率全部外置到配置文件，"
            "修改参数不需要改代码，便于演示与实验。")
bullet(doc, "真实优先：工厂点位与路线均优先使用真实数据，只有在外部服务不可用时才退化为合成数据，"
            "退化行为必须可见（日志提示）。")
bullet(doc, "可验证：核心不变量（状态守恒、一车一单）在设计与实现中显式保证，"
            "并能在运行中被外部校验。")

heading(doc, "4.2  总体架构", 2)
para(doc, "系统采用前后端分离的分层架构。前端负责渲染与交互，后端负责仿真推进与数据持久化，"
          "两者通过 REST 接口通信，外部地图服务由浏览器直接调用。")
table(
    doc,
    ["层次", "组成", "职责", "关键约束"],
    [
        ["表现层", "Vue 3 + Vite + 高德 JS API", "地图渲染、车辆动画、任务看板、仿真控制", "1 秒轮询，动画 20 帧/秒"],
        ["接口层", "Spring MVC Controller", "REST 接口、参数校验、返回封装", "无业务逻辑"],
        ["服务层", "SimulationService、RouteService、FactoryService", "仿真循环、任务生成、路线与工厂业务", "事务边界在这一层"],
        ["持久层", "MyBatis Mapper + XML", "SQL 映射、批量查询、条件更新", "禁止在服务层拼 SQL"],
        ["数据层", "MariaDB（traffic 库）", "8 张表，保存车辆、任务、路线与工厂", "字符集 utf8mb4"],
        ["外部服务", "高德地图 API", "POI 检索与驾车路径规划", "失败必须降级"],
    ],
    widths=[2.2, 5.6, 5.4, 4.0],
    font_size=9,
)
para(doc, "在部署形态上，系统支持两种模式：开发期为前后端分离（Vite 5173 代理到 8080），"
          "演示期为单进程（前端构建产物放入后端 static 目录，同源访问 8080）。"
          "两种模式共用同一套接口，切换只需重新构建前端，不需要修改代码。")
para(doc, "选择单进程模式作为演示形态，是一个有意识的工程取舍：演示现场最怕“起不来”，"
          "而进程数从两个降到一个，意味着端口冲突、代理配置、跨域问题三类故障同时消失。"
          "代价是前端修改后需要重新构建，但在答辩场景下这个代价可以接受。")

heading(doc, "4.3  包结构与依赖关系", 2)
para(doc, "后端按职责划分为八个包，依赖方向自上而下，不允许反向依赖：控制器依赖服务，"
          "服务依赖映射器与工具，实体与枚举被各层共享，配置类只被服务读取。")
figure(doc, "package.png", "图 4-1  后端包图", width=15.5)
para(doc, "包结构中体现了两条约束：其一，DTO 只由控制器使用，服务层不感知传输格式；"
          "其二，工具类（GeoUtil、PolylineUtil）不持有任何 Spring Bean，可被单元测试直接调用。"
          "这两条约束降低了层间耦合，也使测试更容易编写。")

heading(doc, "4.4  核心类设计", 2)
para(doc, "核心类共有七个，围绕“仿真推进”与“数据承载”两条主线组织。SimulationService 是唯一的编排者，"
          "它持有车辆、任务、路线三个映射器，并通过工具类完成几何计算。")
figure(doc, "class.png", "图 4-2  核心类图", width=16.0)
table(
    doc,
    ["类", "职责", "关键方法"],
    [
        ["SimulationService", "仿真生命周期与每轮推进", "start / stop / reset / tickOnce / advance"],
        ["RouteService", "路线查询、缓存与折线更新", "ensureFactoryRoute / pointsOf / updateGeometry"],
        ["FactoryServiceImpl", "工厂增删改查与真实 POI 导入", "importFactories / isFarEnough"],
        ["Vehicle", "车辆实体，承载实时状态与位置", "getter / setter"],
        ["Mission", "任务实体，承载生命周期与关联", "getter / setter"],
        ["Route", "路线实体，承载折线与里程", "getter / setter"],
        ["VehicleState", "状态枚举与转移矩阵", "sampleNextState / isMoving / isWorking"],
        ["PolylineUtil", "折线几何计算", "totalKm / advance / synthetic"],
    ],
    widths=[3.4, 7.2, 6.6],
    font_size=9,
)

heading(doc, "4.5  接口设计", 2)
para(doc, "接口遵循 REST 风格，以资源为中心，返回 JSON。所有接口都不做鉴权，"
          "因为系统运行在本地单实例环境，鉴权属于范围外内容。")
table(
    doc,
    ["方法", "路径", "说明", "主要参数 / 返回"],
    [
        ["POST", "/sim/start", "启动仿真", "无参；返回运行状态"],
        ["POST", "/sim/stop", "暂停仿真", "无参；返回运行状态"],
        ["POST", "/sim/reset", "重置仿真", "无参；返回清理统计"],
        ["GET", "/sim/state", "实时快照", "返回轮次、时间、车辆列表、三类任务"],
        ["GET", "/factories", "工厂列表", "返回全部工厂"],
        ["POST", "/factories/import", "批量导入工厂", "JSON 数组；返回新增数量"],
        ["GET", "/vehicles", "车辆列表", "返回未删除车辆"],
        ["GET", "/missions", "任务列表", "返回全部任务"],
        ["GET", "/routes/{id}/points", "读取路线折线", "返回 [[lng,lat],...]"],
        ["PUT", "/routes/{id}/points", "回写路线折线", "请求体为折线点数组"],
        ["GET/PUT", "/sim/pickup/{vid}/{mid}/points", "接单段折线读写", "同上"],
    ],
    widths=[1.6, 6.6, 4.2, 4.8],
    font_size=8.5,
)
para(doc, "接口设计中有一个细节值得说明：回写折线的接口会同时更新里程与道路类型。"
          "之所以由后端重算里程而不是相信前端传入的距离，是为了避免“前端算一套、后端算一套”的口径不一致，"
          "也保证任何客户端回写后数据都自洽。")

heading(doc, "4.6  数据库设计", 2)
para(doc, "系统共 8 张表，按用途分为三类：仿真核心表（vehicle、mission、route）、"
          "基础数据表（factory、poi、goods、action）、历史结构表（need）。")
para(doc, "车辆表保存实时位置与状态，是每轮更新的热点表。关键字段包括 currentAction（状态编号）、"
          "remainingTime（当前状态剩余分钟）、经纬度与两个距离字段。")
table(
    doc,
    ["字段", "类型", "说明"],
    [
        ["id", "int", "主键"],
        ["currentAction", "int", "状态编号，1~6 对应空闲、接单、装货、运输、卸货、等待"],
        ["remainingTime", "int", "当前状态剩余分钟，归零时触发状态抽样"],
        ["currentLatitude / currentLongitude", "double", "实时位置，按弧长推进后更新"],
        ["distanceToPickup", "double", "接单段剩余距离（km）"],
        ["transportDistance", "double", "运输段剩余距离（km）"],
        ["isDeleted", "int", "逻辑删除标记，0 表示有效"],
    ],
    widths=[5.0, 2.6, 9.6],
    font_size=9,
)
para(doc, "任务表记录一次运输的全生命周期。除状态与关联外，还冗余保存了货物类型、距离与时长，"
          "这样查询任务详情时不必再联表路线与工厂。")
table(
    doc,
    ["字段", "类型", "说明"],
    [
        ["id", "int", "主键"],
        ["missionNo", "varchar(30)", "任务编号，唯一索引"],
        ["car_id", "int", "承运车辆，待接单时为空"],
        ["factory_id / dest_factory_id", "int", "起点与终点工厂"],
        ["route_id", "int", "对应路线，为空时前端显示占位直线"],
        ["goods_type", "varchar(50)", "货物类型，任务创建时固定"],
        ["distance_km", "double", "路线里程（km）"],
        ["total_minutes / elapsed_minutes", "int", "总时长与已用时长"],
        ["status", "varchar(20)", "待接单、接单中、装货中、运输中、卸货中、已完成"],
    ],
    widths=[5.4, 2.6, 9.2],
    font_size=9,
)
para(doc, "路线表的 keyPoint 字段以 JSON 文本保存折线点序列，不做空间索引。"
          "这一选择基于两点考虑：折线点数量在数百到数千之间，整段读取比逐点查询更高效；"
          "系统没有“按空间范围查路线”的需求，因此不需要空间索引带来的复杂度。")
table(
    doc,
    ["字段", "类型", "说明"],
    [
        ["id", "int", "主键"],
        ["startPoint / endPoint", "varchar(100)", "起终点 POI 编号，形如 F864"],
        ["startPointName / endPointName", "varchar(100)", "起终点名称，便于排查"],
        ["roadType", "varchar(20)", "城市道路（合成）或导航路线（真实）"],
        ["distance", "decimal(10,2)", "折线总里程，回写时由后端重算"],
        ["keyPoint", "text", "折线点 JSON 数组"],
        ["estimatedTime", "int", "预估时间（分钟）"],
        ["status", "varchar(10)", "可用标记"],
    ],
    widths=[4.4, 2.8, 10.0],
    font_size=9,
)
para(doc, "其余五张表结构相对简单：factory 保存名称、地址、电话与经纬度；"
          "poi 以“F+工厂编号”作为主键，记录路线起终点的坐标；goods 与 action 是字典表；"
          "need 是早期需求单结构，现已不参与调度，但保留以兼容旧数据，"
          "这一“保留而不删除”的决定保证了历史数据可查询，也避免了迁移风险。")

heading(doc, "4.7  基础数据与规模", 2)
para(doc, "基础数据决定了仿真的空间形态。工厂点位并非人工编造，而是通过高德 POI 检索获得，"
          "再按“同一园区多楼栋”的现实问题做去重与最小间距筛选，最终保留 77 家，"
          "分布在成都、德阳、眉山、资阳四市。")
figure(doc, "factory_bar.png", "图 4-3  工厂数量按城市分布", width=15.0)
para(doc, "从城市分布看，成都 23 家、德阳 20 家、眉山 19 家、资阳 15 家，四市数量接近，"
          "避免了“某一城市只有一两个点”导致的抽样偏差。")
figure(doc, "distance_hist.png", "图 4-4  工厂最近邻距离分布", width=15.0)
para(doc, "从间距分布看，全部工厂满足不小于 12 公里的约束，最近邻距离中位数为 13.5 公里，"
          "54 家的最近邻在 15 公里以内，仅有 1 家超过 20 公里。"
          "这一分布既保证了点位在地图上可以分辨，也使得任务距离落在 20~130 公里区间，"
          "与城市配送的实际里程量级相符。")

heading(doc, "4.8  系统特征点", 2)
table(
    doc,
    ["特征点", "设计取舍", "带来的效果"],
    [
        ["概率状态机", "6 状态 × 6 列的转移矩阵，按 1~100 区间抽样", "行为不确定，多车轨迹不重复"],
        ["真实路网约束", "路线落库为折线，浏览器规划后回写", "轨迹贴合道路，可被反复复用"],
        ["弧长插值", "进度以“已走公里数”表示，投影后推进再反算", "拐弯不切角，偏差由公里级降到 0"],
        ["原子抢单", "条件更新 + 影响行数判定", "不会一车多单，也不会一单多车"],
        ["状态守恒", "状态单向前进、同事务更新、重置统一清空", "任意时刻可自检，结果可验证"],
        ["单进程部署", "前端构建产物放入后端 static", "演示只需一个进程，故障点更少"],
        ["失败可重试", "规划失败不长期缓存，15 秒退避重试", "间歇性失败可自愈，不会永久直线"],
    ],
    widths=[3.2, 7.2, 6.8],
    font_size=9,
)

# ---------------------------------------------------------------- 5 详细设计
heading(doc, "5  详细设计", 1)

heading(doc, "5.1  仿真主循环", 2)
para(doc, "仿真由一个后台守护线程驱动。start() 负责创建线程，runLoop() 是 while 主循环，"
          "tickOnce() 将一轮处理包进事务，doTick() 完成具体推进。核心代码如下：")
code_block(doc, """private void runLoop() {
    while (running) {
        try {
            tickOnce();
        } catch (Exception e) {
            log.error("第 {} 轮执行异常", tick + 1, e);
        }
        try {
            Thread.sleep(props.getTickSeconds() * 1000L);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            break;
        }
    }
    running = false;
}

public void tickOnce() {
    transactionTemplate.executeWithoutResult(st -> doTick());
}

private synchronized void doTick() {
    tick++;
    simMinutes += props.getMinutesPerTick();
    List<Vehicle> vehicles = vehicleMapper.selectAllNotDeleted();
    generateMissions(vehicles);
    Map<Integer, Mission> activeByCar = new HashMap<>();
    for (Mission m : missionMapper.findAllActive()) {
        if (m.getCarId() != null) {
            activeByCar.put(m.getCarId(), m);
        }
    }
    for (Vehicle v : vehicles) {
        advance(v, activeByCar.get(v.getId()));
    }
}""")
para(doc, "设计要点有四：其一，单线程串行推进，避免多线程并发修改同一批车辆导致的竞态；"
          "其二，每轮一个事务，中途异常整体回滚，不会出现“车辆动了但任务没动”的半成品状态；"
          "其三，停止时先置 running=false 再 interrupt()，可立即打断 sleep，实现秒级暂停与重置；"
          "其四，单轮异常被捕获并记录，不中断整个循环，保证长时间运行的稳定性。")
para(doc, "doTick() 上的 synchronized 修饰是为了与 reset()、stop() 互斥。"
          "由于 start()、stop()、reset() 也都声明为 synchronized，"
          "同一时刻只可能有一个线程进入仿真状态变更区，这一点在暂停与重置并发时尤为重要。")

heading(doc, "5.2  状态转移算法", 2)
para(doc, "车辆状态定义为六个：空闲、接单行驶、装货、运货行驶、卸货、停留等待。"
          "转移概率以二维数组形式写在 VehicleState 枚举中，枚举声明顺序必须与矩阵行列一致，"
          "否则抽样结果会整体错位。")
table(
    doc,
    ["从 ＼ 到", "接单行驶", "装货", "运货行驶", "卸货", "停留等待", "空闲"],
    [
        ["接单行驶", "0.05", "0.90", "0.00", "0.00", "0.05", "0.00"],
        ["装货", "0.00", "0.02", "0.95", "0.02", "0.01", "0.00"],
        ["运货行驶", "0.00", "0.00", "0.00", "0.98", "0.02", "0.00"],
        ["卸货", "0.00", "0.00", "0.00", "0.00", "0.02", "0.98"],
        ["停留等待", "0.10", "0.05", "0.05", "0.00", "0.20", "0.60"],
        ["空闲", "0.90", "0.00", "0.00", "0.00", "0.10", "0.00"],
    ],
    widths=[2.6, 2.4, 2.2, 2.4, 2.0, 2.4, 2.2],
    font_size=9,
)
para(doc, "抽样实现采用“整数区间落点”法：随机生成 1~100 的整数，按行概率累加划分区间。"
          "以“接单行驶”为例，1~5 落在继续接单区间，6~95 落在装货区间，96~100 落在等待区间。"
          "这种写法比浮点累加更稳健，不受浮点误差影响，也便于人工核对。")
code_block(doc, """public static VehicleState sampleNextState(VehicleState cur, Random rnd) {
    double[] row = TRANSITIONS[cur.ordinal()];
    int r = rnd.nextInt(100) + 1;   // 1..100
    double acc = 0;
    for (int i = 0; i < row.length; i++) {
        acc += row[i] * 100;
        if (r <= acc) {
            return values()[i];
        }
    }
    return IDLE;
}""")
para(doc, "矩阵只决定“下一个状态是什么”，不决定“接哪一单”。这一职责分离使得调整业务规则（例如改变匹配算法）"
          "不需要触碰概率矩阵，反之亦然。")

heading(doc, "5.3  任务生成", 2)
para(doc, "任务按缺口生成，公式为：本轮新增 = min(空闲车数 − 待接单数, 每轮上限, 池剩余容量)。"
          "其中“每轮上限”默认 5，“池剩余容量”由待接单上限 50 决定。该公式避免了两个极端："
          "任务过多导致车辆抢空后大量任务积压，任务过少导致车辆频繁空转。")
code_block(doc, """private void generateMissions(List<Vehicle> vehicles) {
    long idle = vehicles.stream().filter(v -> v.getCurrentAction() == IDLE_ID).count();
    int pending = missionMapper.countByStatus("待接单");
    int quota = (int) Math.min(Math.min(idle - pending, props.getTasksPerTick()),
                               props.getMaxPendingTasks() - pending);
    for (int i = 0; i < quota; i++) {
        createMission();
    }
}""")
para(doc, "createMission() 随机选取两个不同的工厂作为起点与终点，计算直线距离并据此估算时长，"
          "同时创建（或复用）对应路线。任务的初始状态为“待接单”，尚未绑定车辆，"
          "这与“车辆进入接单状态后再抢单”的设计保持一致。")
para(doc, "值得说明的是，任务创建时就把货物类型固定下来，而不是等到装货时再随机。"
          "这样做的好处是任务在看板上从出现到完成，货物信息始终一致，便于人工核对。")

heading(doc, "5.4  原子抢单与并发控制", 2)
para(doc, "抢单的并发问题在于：多辆车可能在同一瞬间选中同一条任务。若采用“先查询、再更新”的写法，"
          "两个事务都会读到“待接单”，随后都执行更新，导致一单多车。系统改为条件更新：")
code_block(doc, """UPDATE mission SET car_id = ?, status = '接单中'
WHERE id = ? AND status = '待接单'""")
para(doc, "调用方只需判断影响行数：等于 1 表示抢到，等于 0 表示已被其他车辆抢走，"
          "此时车辆降级为空闲，等待下一轮重新抽样。由于条件更新在数据库层面是原子的，"
          "无需显式加锁，也不会产生死锁。")
para(doc, "这一设计还有一个隐含收益：即使将来引入多实例部署，抢单逻辑依然成立，"
          "因为原子性由数据库而非应用内存保证。")

heading(doc, "5.5  路线几何与弧长插值", 2)
para(doc, "路线以折线形式存储，车辆推进采用弧长投影法，每个 tick 三步："
          "① 将当前位置投影到折线，得到已走弧长 s；② s 前进 5 公里；③ 反算 s 对应的坐标，越界则吸附终点。")
para(doc, "投影而非记录索引，是本设计的关键。若用索引记录“走到第几段”，重启后索引丢失，"
          "车辆位置就无法恢复；而投影只依赖“当前坐标 + 折线”，因此重启后仅凭数据库中的经纬度即可恢复。")
code_block(doc, """public static double[] advance(List<double[]> pts, double curLat, double curLng, double km) {
    double s = projectArc(pts, curLat, curLng);      // 投影得到已走弧长
    double target = s + km;                           // 本 tick 前进距离
    return pointAtArc(pts, target);                   // 反算坐标
}""")
para(doc, "与“两点之间按比例插值”相比，弧长法在拐弯处不会走弦。以一个 20.7 公里的直角折线为例，"
          "按比例插值的中点偏出折线 6.7 公里，而按弧长插值的 11 个采样点距折线为 0.000 公里。"
          "这一差异在缩放到路口观察时非常直观。")
table(
    doc,
    ["方法", "进度含义", "20.7 km 直角折线的偏差", "位置可恢复性"],
    [
        ["两点线性插值", "两点之间的比例 t", "中点偏出 6.7 km", "依赖起止点，重启后需重算"],
        ["弧长插值", "沿折线已走的公里数 s", "11 个采样点距折线 0.000 km", "仅依赖当前坐标，可恢复"],
    ],
    widths=[4.0, 5.2, 5.2, 4.0],
    font_size=9,
)

heading(doc, "5.6  前端渲染与动画", 2)
para(doc, "前端每 1 秒轮询一次快照，拿到新坐标后用 requestAnimationFrame 在“上一位置”与“最新位置”"
          "之间沿折线插值，约 20 帧/秒。若直接按坐标跳变，车辆会每 5 秒瞬移一次；"
          "插值则把跳变摊平成连续移动。")
code_block(doc, """function tick() {
  const t = (performance.now() - lastFrame) / 1000
  lastFrame = performance.now()
  for (const item of markers) {
    const path = item.path                    // 当前路段的折线
    item.progress = Math.min(1, item.progress + t / 5)
    const [lng, lat] = pointAtPath(path, item.progress)
    item.marker.setPosition([lng, lat])
  }
  requestAnimationFrame(tick)
}""")
para(doc, "路线规划失败时，前端会保留合成折线作为占位，并在 15 秒后重试；重试成功后自动回写数据库，"
          "地图随即切换为真实道路。这一机制解决了早期版本“失败一次就永久画直线”的缺陷。")

heading(doc, "5.7  性能优化", 2)
para(doc, "在 50 辆车的压力场景下，最初每轮耗时约 1.5 秒，系统无法跟上 1 秒的设定间隔。"
          "优化前后对比如下：")
table(
    doc,
    ["阶段", "20 秒推进轮数", "每轮耗时", "纯计算耗时", "主要改动"],
    [
        ["优化前", "13 轮", "约 1.54 s", "约 540 ms", "逐车查询、各自提交"],
        ["仅优化查询", "14 轮", "约 1.43 s", "约 430 ms", "任务批量加载、折线缓存"],
        ["合并事务后", "18 轮", "约 1.11 s", "约 110 ms", "整轮一个事务，消除多次刷盘"],
    ],
    widths=[3.2, 3.6, 3.0, 3.2, 5.4],
    font_size=9,
)
para(doc, "结论是瓶颈不在 SQL 语句本身，而在每轮上百条 UPDATE 各自提交时的一次次刷盘。"
          "把整轮包进一个事务后，提交次数从上百次降到一次，计算耗时下降约 80%。"
          "在默认 5 秒一轮下，110 毫秒仅占 2% 的时间预算，为后续扩展留出了余量。")

# ---------------------------------------------------------------- 6 测试
heading(doc, "6  测试", 1)

heading(doc, "6.1  测试策略", 2)
para(doc, "测试分为四层：功能测试采用黑盒方法，按用例逐项验证；接口测试直接调用 REST 接口校验返回结构；"
          "性能测试构造 50 辆车观察单轮耗时；一致性测试在运行中抽样校验任务状态守恒。"
          "白盒部分针对工具类与算法（距离计算、弧长推进）编写了断言脚本，用于回归验证。")
para(doc, "测试环境为 Windows 10、JDK 17、MariaDB 10.4、Chrome 浏览器，"
          "前后端同机部署，网络为本地回环，因此网络延迟不计入性能数据。")

heading(doc, "6.2  功能测试用例", 2)
table(
    doc,
    ["编号", "测试项", "操作步骤", "预期结果", "结论"],
    [
        ["TC-01", "启动仿真", "点击启动", "轮次持续增加，车辆位置变化", "通过"],
        ["TC-02", "暂停仿真", "点击暂停后观察", "轮次停止增加，界面保留状态", "通过"],
        ["TC-03", "重置仿真", "点击重置", "任务清空，车辆回到工厂点位", "通过"],
        ["TC-04", "任务生成", "观察待接单数量", "待接单数随空闲车缺口变化，不超上限", "通过"],
        ["TC-05", "抢单唯一性", "并发触发多车接单", "每条任务仅被一辆车占用", "通过"],
        ["TC-06", "状态转移", "观察 20 轮状态分布", "六种状态均出现且符合概率区间", "通过"],
        ["TC-07", "路线回写", "规划完成后刷新页面", "折线为导航路线，车辆贴路行驶", "通过"],
        ["TC-08", "弧长推进", "缩放到路口观察拐弯", "车辆沿道路折线转向，不切角", "通过"],
        ["TC-09", "工厂导入", "点击抓取真实工厂", "仅新增距已有工厂 ≥12 km 的点", "通过"],
        ["TC-10", "重复导入", "连续点击两次抓取", "第二次新增 0 或极少，无重复记录", "通过"],
        ["TC-11", "看板刷新", "观察左右两栏", "车辆状态与任务数量实时变化", "通过"],
        ["TC-12", "异常恢复", "断网 10 秒后恢复", "提示网络异常，恢复后自动继续", "通过"],
        ["TC-13", "接单段贴路", "观察接单行驶的车辆", "折线由直线变为沿路折线", "通过"],
        ["TC-14", "超长任务", "观察 100 km 以上任务", "仍能规划则贴路，失败则保持占位并重试", "通过"],
    ],
    widths=[1.4, 2.8, 4.4, 6.6, 1.6],
    font_size=8.5,
)

heading(doc, "6.3  接口测试", 2)
para(doc, "接口测试使用脚本直接调用，重点校验返回字段完整性与边界行为。")
table(
    doc,
    ["接口", "校验点", "结果"],
    [
        ["GET /sim/state", "返回 tick、simMinutes、vehicles、三类任务；车辆字段齐全", "通过"],
        ["POST /sim/start", "重复调用不产生第二个线程", "通过"],
        ["POST /sim/reset", "任务表为空；车辆全部为空闲且在工厂坐标", "通过"],
        ["POST /factories/import", "空数组返回 0；同名同坐标返回 0；过近的点被过滤", "通过"],
        ["PUT /routes/{id}/points", "里程按新折线重算；道路类型变为导航路线", "通过"],
        ["GET /routes/{id}/points", "返回点数组长度与存储一致；无点时返回空数组", "通过"],
    ],
    widths=[5.6, 8.4, 1.8],
    font_size=9,
)

heading(doc, "6.4  性能测试", 2)
para(doc, "构造 50 辆车并把轮次间隔压缩到 1 秒，统计 20 秒内实际推进的轮数，"
          "再反推每轮耗时与纯计算耗时。测试数据见 5.7 节表格，此处补充结论："
          "合并事务后每轮计算约 110 毫秒，接口 /sim/state 在 50 辆车时响应 30~60 毫秒，"
          "前端 1 秒轮询不会对后端构成压力。")

heading(doc, "6.5  一致性测试", 2)
para(doc, "一致性测试在仿真运行中随机抽样五次，校验“总数 = 待接单 + 进行中 + 已完成”，"
          "同时检查三类脏状态：待接单却挂着车、进行中却没有车、车辆引用已不存在。")
table(
    doc,
    ["采样", "任务总数", "待接单", "进行中", "已完成", "守恒", "脏状态"],
    [
        ["①", "20", "0", "10", "10", "成立", "0"],
        ["②", "22", "0", "10", "12", "成立", "0"],
        ["③", "24", "0", "10", "14", "成立", "0"],
        ["④", "25", "1", "10", "14", "成立", "0"],
        ["⑤", "26", "0", "9", "17", "成立", "0"],
    ],
    widths=[1.6, 2.8, 2.6, 2.6, 2.6, 2.2, 2.4],
    font_size=9,
)

heading(doc, "6.6  缺陷记录", 2)
para(doc, "测试过程中共登记并关闭 5 个有代表性的缺陷，其中前两个属于路线规划的重试策略问题，"
          "修复后显著改善了轨迹质量。")
table(
    doc,
    ["编号", "现象", "定位原因", "修复方式", "状态"],
    [
        ["BUG-01", "部分车辆直线穿越街区", "路线规划失败后把合成折线长期缓存，不再重试",
         "失败只占位，15 秒退避重试，并发限制为 2", "已关闭"],
        ["BUG-02", "接单段一直是直线", "接单段规划失败后标记不释放",
         "失败释放标记并进入冷却，与任务路线共用重试策略", "已关闭"],
        ["BUG-03", "同一任务被两辆车接走", "先查后改存在竞态",
         "改为条件更新，影响行数为 1 才算成功", "已关闭"],
        ["BUG-04", "暂停后仍前进一小段", "sleep 未被及时打断",
         "stop() 中 interrupt() 唤醒并 break", "已关闭"],
        ["BUG-05", "工厂点位重叠不可分辨", "POI 检索含同一园区多楼栋",
         "导入时按最小间距 12 公里过滤", "已关闭"],
    ],
    widths=[1.6, 3.6, 5.0, 5.4, 1.4],
    font_size=8.5,
)

heading(doc, "6.7  项目看板", 2)
para(doc, "看板用于跟踪任务流转，每周例会更新一次。列为“待办、进行中、已完成”，"
          "卡片粒度控制在半天到两天工作量，避免过大或过碎。")
table(
    doc,
    ["待办（Backlog）", "进行中（Doing）", "已完成（Done）"],
    [
        ["匹配算法加入载重与时效约束", "BUG-02 回归验证", "需求与用例建模"],
        ["参数敏感性实验", "路线规划失败重试", "架构与数据模型设计"],
        ["前端轮询改造为 WebSocket", "工厂导入间距过滤", "仿真主循环与任务闭环"],
        ["在线参数面板", "接单段重试逻辑", "弧长插值与真实路网接入"],
        ["多方案对比实验", "—", "性能优化（事务合并）"],
        ["—", "—", "测试用例与缺陷记录"],
    ],
    widths=[5.6, 5.6, 5.6],
    font_size=9,
)

heading(doc, "6.8  甘特图与进度偏差", 2)
para(doc, "项目按校历周排期，共 12 周，第 5 周为国庆假期。甘特图使用成员真实姓名标注参与情况。")
figure(doc, "gantt.png", "图 6-1  项目甘特图（按周，真实姓名）", width=16.0)
para(doc, "进度偏差主要出现在第 7 周与第 9 周。第 7 周原计划完成高德 API 接入，"
          "但由于发现 JS API key 与服务端 key 类型不匹配，临时改为“浏览器规划 + 回写”的方案，"
          "实际完成时间推迟 3 天。第 9 周实现状态马尔科夫表时，"
          "发现枚举顺序与矩阵行列必须严格一致，调试耗时超出预期约 2 天。"
          "两次偏差均在第 10 周的“调试与功能补全”中被吸收，未影响最终交付。")

# ---------------------------------------------------------------- 7 总结
heading(doc, "7  总结与展望", 1)

heading(doc, "7.1  完成情况", 2)
para(doc, "第一阶段完成了从需求到测试的完整闭环：需求侧给出 12 项功能需求与 7 项非功能需求，"
          "并建立需求跟踪矩阵；设计侧给出包图、类图与 8 张表的数据模型；"
          "实现侧后端 42 个类约 2167 行、前端 17 个文件约 1623 行、7 个 MyBatis 映射文件；"
          "测试侧覆盖功能、接口、性能与一致性四类，登记并关闭 5 个缺陷。")
table(
    doc,
    ["项目", "数量", "说明"],
    [
        ["后端类", "42 个 / 约 2167 行", "含控制器、服务、映射器、实体、枚举、工具"],
        ["前端文件", "17 个 / 约 1623 行", "含组件、接口封装、路由与入口"],
        ["MyBatis 映射", "7 个 XML", "对应车辆、任务、路线、工厂等"],
        ["数据库表", "8 张", "仿真核心 3 张、基础数据 4 张、历史结构 1 张"],
        ["工厂点位", "77 家", "成都 23、德阳 20、眉山 19、资阳 15"],
        ["仿真规模", "10 辆车 / 5 秒一轮", "一轮代表 5 分钟"],
        ["接口数量", "11 个", "仿真控制、状态、路线、工厂、车辆、任务"],
    ],
    widths=[3.0, 4.0, 9.4],
    font_size=9,
)

heading(doc, "7.2  不足", 2)
bullet(doc, "匹配算法仍是最近邻贪心，未考虑载重、时效与回程，策略对比的说服力有限。")
bullet(doc, "参数（装卸时长、任务概率、最小间距）依靠经验设定，缺少敏感性实验与统计意义上的评估。")
bullet(doc, "前端采用 1 秒轮询，在更大规模或更细粒度下会放大请求量，尚未引入推送机制。")
bullet(doc, "缺少自动化单元测试与持续集成，回归主要依赖手工用例，效率与可靠性都有提升空间。")

heading(doc, "7.3  展望", 2)
bullet(doc, "匹配：引入载重与时效约束，比较贪心与匈牙利算法在同一数据集上的空驶率与等待时长。")
bullet(doc, "实验：对关键参数做敏感性分析，输出“参数—指标”曲线，为参数取值提供依据。")
bullet(doc, "工程：补充单元测试与 CI 流水线，前端改为 WebSocket 推送，降低延迟与请求量。")
bullet(doc, "数据：接入更多城市与真实订单数据，使仿真更贴近实际运营，并支持多方案对比。")

# ---------------------------------------------------------------- 附录
doc.add_page_break()
heading(doc, "附录 A  Git 提交记录（节选）", 1)
table(
    doc,
    ["提交", "说明", "阶段"],
    [
        ["7edc566", "补充 IDEA / VS Code 配置说明", "文档"],
        ["933e4f1", "增加单进程部署脚本（前端打包进后端 static）", "实现"],
        ["f2c94c5", "增加答辩 PPT 与生成脚本，目录整理", "文档"],
        ["4e3acfe", "工厂导入支持最小间距过滤与多城市抓取", "实现"],
        ["b3c0045", "第 7 页改为两种插值方案横向对比", "文档"],
        ["5219a72", "路线规划失败可重试；演示范围收回成都周边四市", "修复"],
        ["3e0b014", "接单段路线规划失败后可重试", "修复"],
        ["a18678d", "问答文档新增附录——答不上来时的应对模板", "文档"],
    ],
    widths=[2.6, 10.4, 2.2],
    font_size=9,
)
para(doc, "仓库地址：https://github.com/legdos/traffic_management_full", size=10, color=GREY, indent=False)

heading(doc, "附录 B  例会纪要（节选）", 1)
para(doc, "第 4 次例会（第 6 周）", bold=True, indent=False)
bullet(doc, "进度：邱崇翔、卢润山完成主循环与任务生成；张笑宇完成地图与车辆标记；王晓宇编写首版测试用例。", size=11)
bullet(doc, "变更：装卸时长由 60 分钟调整为 30 分钟，以贴合实际并缩短仿真闭环时间。", size=11)
bullet(doc, "分工：下周卢润山转前端，配合张笑宇完成插值动画；王晓宇开始接口测试。", size=11)
bullet(doc, "风险：高德路线规划在长距离下失败率偏高，决定增加重试与并发上限。", size=11)
para(doc, "第 8 次例会（第 9 周）", bold=True, indent=False)
bullet(doc, "进度：状态马尔科夫表实现完成，六状态转移可稳定运行。", size=11)
bullet(doc, "变更：等待时长由 10 分钟调整为 5 分钟，避免车辆长时间停留影响演示观感。", size=11)
bullet(doc, "分工：王晓宇负责回归测试与缺陷跟踪；张笑宇准备发布清单与部署说明。", size=11)
bullet(doc, "风险：跨市任务距离过长导致路线规划成功率下降，决定把演示范围收回四市。", size=11)

heading(doc, "附录 C  运行与演示说明", 1)
bullet(doc, "环境：JDK 17 及以上、Node.js 22 及以上、MariaDB 10.4；数据库名 traffic，字符集 utf8mb4。", size=11)
bullet(doc, "导入数据：新建 traffic 库，执行 trafficdata.sql；若 mission 表缺字段，再执行 mission_sim_upgrade.sql。", size=11)
bullet(doc, "启动后端：进入 traffic_management_backend，运行 mvnw spring-boot:run（端口 8080）。", size=11)
bullet(doc, "单进程演示：先执行 build-web.cmd 打包前端到后端 static，再只启动后端，访问 http://localhost:8080。", size=11)
bullet(doc, "开发模式：前端目录执行 npm run dev（端口 5173，代理到 8080）。", size=11)
bullet(doc, "参数调整：修改 application.yaml 的 sim.* 后重启后端生效。", size=11)

_uf = OxmlElement("w:updateFields")
_uf.set(qn("w:val"), "true")
doc.settings.element.append(_uf)

out = os.path.join(BASE, "软件工程与实践大作业-第X组-陈嘉诩等.docx")
doc.save(out)
print("saved:", out)
