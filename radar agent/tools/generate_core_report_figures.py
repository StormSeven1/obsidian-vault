from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "核心架构图_正式版"
SVG_DIR = OUT / "svg"
PNG_DIR = OUT / "png"
PREVIEW_DIR = OUT / "preview"

W, H = 2600, 1500
SCALE = 2

FONT = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")
if not FONT.exists():
    FONT = Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")
if not FONT_BOLD.exists():
    FONT_BOLD = Path("C:/Windows/Fonts/simhei.ttf")

P = {
    "paper": "#F8FAFC",
    "white": "#FFFFFF",
    "ink": "#18263A",
    "muted": "#64748B",
    "line": "#CBD5E1",
    "line2": "#DCE4EE",
    "navy": "#12395A",
    "navy2": "#E7F0F8",
    "blue": "#245F9F",
    "blue2": "#DCEBFA",
    "teal": "#0F766E",
    "teal2": "#DDF4F0",
    "green": "#3F7636",
    "green2": "#E4F2DF",
    "amber": "#A76500",
    "amber2": "#FFF0CC",
    "red": "#B33A3A",
    "red2": "#FCE2E2",
    "purple": "#6750A4",
    "purple2": "#EEE8FF",
    "gray": "#EEF3F8",
}


def fnt(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_BOLD if bold and FONT_BOLD.exists() else FONT), size=size)


def wrap(text: str, max_chars: int) -> list[str]:
    out: list[str] = []
    for part in text.split("\n"):
        part = part.strip()
        if not part:
            out.append("")
            continue
        buf = ""
        for ch in part:
            buf += ch
            if len(buf) >= max_chars:
                out.append(buf)
                buf = ""
        if buf:
            out.append(buf)
    return out


@dataclass
class Text:
    x: int
    y: int
    w: int
    h: int
    text: str
    size: int = 24
    color: str = P["ink"]
    bold: bool = False
    align: str = "center"
    valign: str = "middle"
    max_chars: int | None = None


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int
    fill: str = P["white"]
    stroke: str = P["line"]
    radius: int = 18
    width: int = 2


@dataclass
class Line:
    x1: int
    y1: int
    x2: int
    y2: int
    color: str = P["navy"]
    width: int = 3
    arrow: bool = True
    dash: bool = False


@dataclass
class Fig:
    slug: str
    title: str
    subtitle: str = ""
    items: list[object] = field(default_factory=list)

    def rect(self, x: int, y: int, w: int, h: int, fill: str = P["white"], stroke: str = P["line"], radius: int = 18, width: int = 2) -> None:
        self.items.append(Rect(x, y, w, h, fill, stroke, radius, width))

    def text(self, x: int, y: int, w: int, h: int, text: str, size: int = 24, color: str = P["ink"], bold: bool = False, align: str = "center", valign: str = "middle", max_chars: int | None = None) -> None:
        self.items.append(Text(x, y, w, h, text, size, color, bold, align, valign, max_chars))

    def line(self, x1: int, y1: int, x2: int, y2: int, color: str = P["navy"], width: int = 3, arrow: bool = True, dash: bool = False) -> None:
        self.items.append(Line(x1, y1, x2, y2, color, width, arrow, dash))

    def base(self) -> None:
        self.rect(0, 0, W, H, P["paper"], P["paper"], radius=0, width=0)
        self.text(80, 46, 1380, 52, self.title, 34, P["navy"], True, "left")
        self.text(1530, 52, 980, 42, self.subtitle, 20, P["muted"], False, "right")
        self.line(80, 126, 2520, 126, P["line"], 2, False)

    def caption(self, text: str) -> None:
        self.line(80, 1405, 2520, 1405, P["line"], 2, False)
        self.text(80, 1420, 2440, 42, text, 21, P["muted"], False, "center")

    def group_title(self, x: int, y: int, w: int, title: str, color: str = P["navy"]) -> None:
        self.rect(x, y, w, 46, color, color, radius=12, width=0)
        self.text(x + 18, y + 5, w - 36, 34, title, 22, P["white"], True, "left")

    def box(self, x: int, y: int, w: int, h: int, title: str, body: str, fill: str, stroke: str, title_color: str | None = None, body_size: int = 20) -> None:
        self.rect(x, y, w, h, fill, stroke, 16, 2)
        self.text(x + 18, y + 16, w - 36, 30, title, 23, title_color or stroke, True, "left", max_chars=16)
        self.text(x + 18, y + 58, w - 36, h - 70, body, body_size, P["ink"], False, "left", "top", max_chars=max(8, int((w - 36) / (body_size * 0.9))))

    def pill(self, x: int, y: int, w: int, text: str, fill: str, color: str = P["white"]) -> None:
        self.rect(x, y, w, 42, fill, fill, 21, 0)
        self.text(x, y + 3, w, 34, text, 18, color, True)

    def save(self) -> None:
        self.render_png(PNG_DIR / f"{self.slug}.png")
        self.render_svg(SVG_DIR / f"{self.slug}.svg")

    def render_png(self, path: Path) -> None:
        img = Image.new("RGB", (W * SCALE, H * SCALE), P["paper"])
        draw = ImageDraw.Draw(img)
        for item in self.items:
            if isinstance(item, Rect):
                box = [item.x * SCALE, item.y * SCALE, (item.x + item.w) * SCALE, (item.y + item.h) * SCALE]
                if item.radius:
                    draw.rounded_rectangle(box, item.radius * SCALE, fill=item.fill, outline=item.stroke, width=max(1, item.width * SCALE))
                else:
                    draw.rectangle(box, fill=item.fill, outline=item.stroke, width=max(1, item.width * SCALE))
            elif isinstance(item, Line):
                draw_line(draw, item)
            elif isinstance(item, Text):
                draw_text(draw, item)
        img.save(path, quality=96)

    def render_svg(self, path: Path) -> None:
        out = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
            "<defs>",
            '<marker id="arrow" viewBox="0 0 10 10" refX="8.4" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#12395A"/></marker>',
            '<style>text{font-family:"Microsoft YaHei","Noto Sans SC",Arial,sans-serif;dominant-baseline:middle}</style>',
            "</defs>",
        ]
        for item in self.items:
            if isinstance(item, Rect):
                out.append(f'<rect x="{item.x}" y="{item.y}" width="{item.w}" height="{item.h}" rx="{item.radius}" fill="{item.fill}" stroke="{item.stroke}" stroke-width="{item.width}"/>')
            elif isinstance(item, Line):
                marker = ' marker-end="url(#arrow)"' if item.arrow else ""
                dash = ' stroke-dasharray="12 10"' if item.dash else ""
                out.append(f'<line x1="{item.x1}" y1="{item.y1}" x2="{item.x2}" y2="{item.y2}" stroke="{item.color}" stroke-width="{item.width}" stroke-linecap="round"{dash}{marker}/>')
            elif isinstance(item, Text):
                out.append(svg_text(item))
        out.append("</svg>")
        path.write_text("\n".join(out), encoding="utf-8")


def draw_text(draw: ImageDraw.ImageDraw, t: Text) -> None:
    font = fnt(t.size * SCALE, t.bold)
    max_chars = t.max_chars or max(4, int(t.w / (t.size * 0.92)))
    lines = wrap(t.text, max_chars)
    line_h = int(t.size * 1.38 * SCALE)
    total_h = line_h * len(lines)
    if t.valign == "top":
        y = t.y * SCALE
    elif t.valign == "bottom":
        y = (t.y + t.h) * SCALE - total_h
    else:
        y = t.y * SCALE + (t.h * SCALE - total_h) / 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        tw = bbox[2] - bbox[0]
        if t.align == "left":
            x = t.x * SCALE
        elif t.align == "right":
            x = (t.x + t.w) * SCALE - tw
        else:
            x = t.x * SCALE + (t.w * SCALE - tw) / 2
        draw.text((x, y), line, fill=t.color, font=font)
        y += line_h


def svg_text(t: Text) -> str:
    max_chars = t.max_chars or max(4, int(t.w / (t.size * 0.92)))
    lines = wrap(t.text, max_chars)
    line_h = t.size * 1.38
    total_h = line_h * len(lines)
    if t.valign == "top":
        y = t.y + line_h / 2
    elif t.valign == "bottom":
        y = t.y + t.h - total_h + line_h / 2
    else:
        y = t.y + (t.h - total_h) / 2 + line_h / 2
    if t.align == "left":
        x, anchor = t.x, "start"
    elif t.align == "right":
        x, anchor = t.x + t.w, "end"
    else:
        x, anchor = t.x + t.w / 2, "middle"
    spans = "".join(f'<tspan x="{x}" y="{y + i * line_h:.1f}">{escape(line)}</tspan>' for i, line in enumerate(lines))
    return f'<text text-anchor="{anchor}" font-size="{t.size}" font-weight="{"700" if t.bold else "400"}" fill="{t.color}">{spans}</text>'


def draw_line(draw: ImageDraw.ImageDraw, line: Line) -> None:
    p1 = (line.x1 * SCALE, line.y1 * SCALE)
    p2 = (line.x2 * SCALE, line.y2 * SCALE)
    if line.dash:
        dashed(draw, p1, p2, line.color, line.width * SCALE)
    else:
        draw.line([p1, p2], fill=line.color, width=line.width * SCALE)
    if line.arrow:
        arrowhead(draw, p1, p2, line.color)


def dashed(draw: ImageDraw.ImageDraw, p1: tuple[int, int], p2: tuple[int, int], color: str, width: int) -> None:
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    ux, uy = dx / dist, dy / dist
    step, gap = 28, 18
    t = 0
    while t < dist:
        e = min(t + step, dist)
        draw.line([(p1[0] + ux * t, p1[1] + uy * t), (p1[0] + ux * e, p1[1] + uy * e)], fill=color, width=width)
        t += step + gap


def arrowhead(draw: ImageDraw.ImageDraw, p1: tuple[int, int], p2: tuple[int, int], color: str) -> None:
    angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    size = 15 * SCALE
    pts = [
        p2,
        (p2[0] + size * math.cos(angle + 2.55), p2[1] + size * math.sin(angle + 2.55)),
        (p2[0] + size * math.cos(angle - 2.55), p2[1] + size * math.sin(angle - 2.55)),
    ]
    draw.polygon(pts, fill=color)


def architecture() -> Fig:
    g = Fig("01_总体架构图_正式版", "雷达智能体子系统总体架构图", "系统定位 / 能力分层 / 受控执行边界")
    g.base()

    g.group_title(88, 190, 370, "外部输入与支撑")
    left = [
        ("显控分系统", "自然语言、目标/区域选择、告警卡片、审批回调", P["blue2"], P["blue"]),
        ("信息处理感知子系统", "检测、识别、跟踪、定位结果与置信度", P["teal2"], P["teal"]),
        ("雷达状态与环境", "工作模式、当前参数、资源占用、设备健康、环境条件", P["green2"], P["green"]),
        ("数据知识底座", "知识、案例、策略、关系、向量、图、时序数据", P["purple2"], P["purple"]),
    ]
    for i, (t, b, fill, stroke) in enumerate(left):
        y = 270 + i * 145
        g.box(88, y, 370, 108, t, b, fill, stroke, body_size=18)
        g.line(458, y + 54, 620, 620, P["line"], 3, False)

    g.rect(610, 190, 1280, 780, P["white"], P["navy"], 20, 3)
    g.rect(610, 190, 1280, 66, P["navy"], P["navy"], 20, 0)
    g.text(642, 202, 1215, 42, "雷达智能体子系统：智能决策与人机协同中枢", 27, P["white"], True, "left")

    # Layer 1
    g.text(650, 292, 190, 34, "认知推理层", 23, P["blue"], True, "left")
    cog = [
        ("LLM推理引擎", "意图理解 / 推理规划"),
        ("雷达Skills能力包", "目标研判 / 参数优化"),
        ("结果生成", "研判摘要 / 候选方案"),
    ]
    for i, (t, b) in enumerate(cog):
        g.box(845 + i * 310, 275, 260, 105, t, b, P["blue2"], P["blue"], body_size=18)

    # Layer 2
    g.text(650, 468, 230, 34, "任务运行与治理层", 23, P["navy"], True, "left")
    gov = [
        ("Agent Harness运行底座", "任务实例、上下文、能力调度、状态管理"),
        ("安全门控", "权限、风险、参数边界、人工确认"),
        ("追溯治理", "输入、证据、调用、审批、输出全程记录"),
    ]
    for i, (t, b) in enumerate(gov):
        fill, stroke = [(P["gray"], P["navy"]), (P["red2"], P["red"]), (P["purple2"], P["purple"])][i]
        g.box(845 + i * 310, 450, 260, 116, t, b, fill, stroke, body_size=17)

    # Layer 3
    g.text(650, 662, 250, 34, "能力与数据支撑层", 23, P["teal"], True, "left")
    support = [
        ("三阶分层记忆", "短期上下文 / 中期任务链 / 长期经验资产"),
        ("工具执行", "查询、分析、仿真、报告、控制请求适配"),
        ("工作流引擎", "模板、节点、审批、检查点、回滚"),
        ("数据库接入", "关系、向量、图、时序统一访问"),
    ]
    for i, (t, b) in enumerate(support):
        colors = [(P["green2"], P["green"]), (P["teal2"], P["teal"]), (P["amber2"], P["amber"]), (P["purple2"], P["purple"])][i]
        g.box(708 + i * 285, 645, 238, 116, t, b, colors[0], colors[1], body_size=16)

    g.rect(755, 820, 990, 70, P["gray"], P["line"], 15, 2)
    g.text(790, 836, 920, 36, "统一对象：任务实例 · 目标/区域引用 · 证据引用 · 追溯引用", 22, P["ink"], True)

    g.group_title(2040, 190, 380, "智能体输出")
    outs = [
        ("目标研判结果", "目标类别、行为特征、威胁等级、证据缺口"),
        ("候选参数方案", "工作模式、波形、波束、门限、跟踪参数"),
        ("工作流请求", "流程模板、审批事项、检查点、回滚条件"),
        ("追溯记录与经验候选", "上下文快照、工具记录、执行效果、反馈"),
    ]
    for i, (t, b) in enumerate(outs):
        y = 270 + i * 145
        fill, stroke = [(P["blue2"], P["blue"]), (P["amber2"], P["amber"]), (P["red2"], P["red"]), (P["green2"], P["green"])][i]
        g.box(2040, y, 380, 108, t, b, fill, stroke, body_size=18)
        g.line(1890, 620, 2040, y + 54, stroke, 4)

    # Controlled execution boundary
    g.rect(350, 1060, 1900, 215, P["white"], P["red"], 20, 3)
    g.text(388, 1080, 380, 34, "受控执行边界", 24, P["red"], True, "left")
    chain = [
        ("候选方案", P["amber2"], P["amber"]),
        ("安全门控", P["red2"], P["red"]),
        ("工作流校验/审批", P["amber2"], P["amber"]),
        ("控制请求适配", P["teal2"], P["teal"]),
        ("控制执行链路", P["red2"], P["red"]),
    ]
    x0 = 520
    for i, (t, fill, stroke) in enumerate(chain):
        x = x0 + i * 330
        g.rect(x, 1140, 230, 64, fill, stroke, 13, 2)
        g.text(x, 1152, 230, 36, t, 21, stroke, True)
        if i < len(chain) - 1:
            g.line(x + 230, 1172, x + 330, 1172, P["navy"], 4)
    g.text(700, 1230, 1190, 34, "智能体生成建议和流程请求；真实控制下发由控制执行链路完成", 22, P["muted"], False)
    g.line(1250, 890, 1250, 1060, P["red"], 4, True, True)

    g.caption("架构表达重点：将大语言模型推理纳入任务运行、能力调用、安全门控、追溯治理和控制执行边界之内。")
    return g


def work_principle() -> Fig:
    g = Fig("02_工作原理图_正式版", "雷达智能体子系统工作原理图", "认知循环 / 双路径执行 / 三阶记忆回流")
    g.base()

    # Main loop frame
    g.rect(115, 200, 2370, 720, P["white"], P["navy"], 22, 3)
    g.text(150, 220, 560, 36, "主运行闭环", 26, P["navy"], True, "left")

    loop = [
        ("多源触发", "显控请求\n感知事件\n状态告警", 190, 360, P["blue2"], P["blue"]),
        ("任务实例", "来源、对象、风险\n上下文版本、追溯编号", 500, 360, P["blue2"], P["blue"]),
        ("任务工作空间", "当前上下文\n证据链\n历史经验投影", 830, 330, P["purple2"], P["purple"]),
        ("LLM + Skills推理", "意图理解\n任务建模\n执行规划", 1195, 360, P["blue2"], P["blue"]),
        ("执行路径选择", "只读研判\n推荐生成\n受控执行", 1535, 360, P["amber2"], P["amber"]),
        ("结果反馈", "摘要、证据、建议\n风险与流程状态", 1875, 360, P["green2"], P["green"]),
        ("追溯与记忆回流", "工具记录、审批记录\n效果指标、反馈", 1875, 635, P["green2"], P["green"]),
        ("经验候选评估", "冲突检查\n适用边界\n版本治理", 1195, 635, P["red2"], P["red"]),
        ("上下文更新", "短期归档\n任务链更新\n长期经验候选", 500, 635, P["teal2"], P["teal"]),
    ]
    for t, b, x, y, fill, stroke in loop:
        g.box(x, y, 245, 116, t, b, fill, stroke, body_size=17)
    arrows = [
        (435, 418, 500, 418), (745, 418, 830, 398), (1075, 398, 1195, 418),
        (1440, 418, 1535, 418), (1780, 418, 1875, 418), (1998, 476, 1998, 635),
        (1875, 693, 1440, 693), (1195, 693, 745, 693), (500, 693, 315, 476),
    ]
    for x1, y1, x2, y2 in arrows:
        g.line(x1, y1, x2, y2, P["navy"], 4)

    # Memory side support
    g.rect(170, 775, 730, 95, P["gray"], P["line"], 14, 2)
    g.text(200, 792, 670, 28, "三阶分层记忆支撑任务工作空间", 22, P["green"], True)
    for i, (txt, col) in enumerate([("短期上下文", P["teal"]), ("中期任务链", P["amber"]), ("长期经验资产", P["green"])]):
        g.pill(225 + i * 205, 830, 165, txt, col)
    g.line(830, 776, 950, 446, P["green"], 3, True, True)

    # Execution paths
    g.text(150, 970, 520, 34, "执行路径分治", 26, P["navy"], True, "left")
    g.rect(145, 1020, 1045, 250, P["teal2"], P["teal"], 18, 3)
    g.text(190, 1042, 320, 34, "动态研判路径", 25, P["teal"], True, "left")
    dyn = [("ReAct工具调用", 245), ("查询/分析/解释", 525), ("报告与证据整理", 805)]
    for title, x in dyn:
        g.rect(x, 1125, 210, 58, P["white"], P["teal"], 12, 2)
        g.text(x, 1137, 210, 34, title, 19, P["ink"], True)
    g.line(455, 1154, 525, 1154, P["teal"], 3)
    g.line(735, 1154, 805, 1154, P["teal"], 3)
    g.text(190, 1205, 910, 32, "适用：目标解释、异常归因、跟踪质量评估、报告生成等只读或低风险任务。", 20, P["muted"], False)

    g.rect(1410, 1020, 1045, 250, P["red2"], P["red"], 18, 3)
    g.text(1455, 1042, 340, 34, "受控流程路径", 25, P["red"], True, "left")
    ctrl = [("参数边界校验", 1505), ("仿真评估", 1765), ("人工确认", 2025), ("状态跟踪/回滚", 2250)]
    for title, x in ctrl:
        w = 180 if x != 2250 else 160
        g.rect(x, 1125, w, 58, P["white"], P["red"], 12, 2)
        g.text(x, 1137, w, 34, title, 18, P["ink"], True)
    for x1, x2 in [(1685, 1765), (1945, 2025), (2205, 2250)]:
        g.line(x1, 1154, x2, 1154, P["red"], 3)
    g.text(1455, 1205, 910, 32, "适用：波形参数调整、工作模式切换、控制请求适配和回滚恢复等高风险任务。", 20, P["muted"], False)

    g.rect(980, 948, 640, 46, P["gray"], P["line"], 14, 2)
    g.text(1005, 956, 590, 28, "执行路径按风险等级与标准化程度分治", 21, P["ink"], True)

    # Time classes
    g.rect(520, 1320, 1560, 58, P["gray"], P["line"], 14, 2)
    labels = [("实时事件接入", P["blue"]), ("准实时智能研判", P["teal"]), ("受控流程任务", P["red"]), ("离线后台任务", P["green"])]
    for i, (txt, col) in enumerate(labels):
        g.pill(590 + i * 365, 1328, 225, txt, col)

    g.caption("工作原理表达重点：以任务实例组织上下文、推理、工具、工作流、结果反馈和记忆回流；按风险与标准化程度选择执行路径。")
    return g


def contact_sheet(figs: list[Fig]) -> None:
    thumbs = []
    for fig in figs:
        img = Image.open(PNG_DIR / f"{fig.slug}.png").convert("RGB")
        img.thumbnail((980, 565))
        thumbs.append((fig.title, img.copy()))
    sheet = Image.new("RGB", (2100, 720), "white")
    draw = ImageDraw.Draw(sheet)
    draw.text((50, 32), "核心架构图正式版预览", fill=P["navy"], font=fnt(34, True))
    for i, (title, img) in enumerate(thumbs):
        x = 50 + i * 1010
        y = 100
        sheet.paste(img, (x, y))
        draw.text((x, y + 585), title, fill=P["muted"], font=fnt(24))
    sheet.save(PREVIEW_DIR / "核心图预览.png", quality=96)


def readme(figs: list[Fig]) -> None:
    rows = "\n".join(f"| {fig.title} | `svg/{fig.slug}.svg` | `png/{fig.slug}.png` |" for fig in figs)
    text = f"""# 核心架构图正式版

本目录先生成两张用于正式 Word 方案文档的核心配图：

| 图名 | SVG | PNG |
| --- | --- | --- |
{rows}

设计原则：

- 不照搬 Mermaid 节点结构，而是按正文方案重新抽象。
- 总体架构图强调系统定位、能力分层、输出关系和受控执行边界。
- 工作原理图强调任务实例主线、双路径执行、三阶记忆支撑和经验回流。
- Word 中建议优先插入 `png/` 下的高清 PNG；需要精修时使用 `svg/`。
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")


def main() -> None:
    for d in (OUT, SVG_DIR, PNG_DIR, PREVIEW_DIR):
        d.mkdir(parents=True, exist_ok=True)
    figs = [architecture(), work_principle()]
    for fig in figs:
        fig.save()
    contact_sheet(figs)
    readme(figs)
    print(OUT)
    print(f"figures={len(figs)}")


if __name__ == "__main__":
    main()
