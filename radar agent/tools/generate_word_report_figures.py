from __future__ import annotations

import math
from dataclasses import dataclass, field
from pathlib import Path
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Word方案配图"
SVG_DIR = OUT / "svg"
PNG_DIR = OUT / "png"
PREVIEW_DIR = OUT / "preview"

W, H = 2200, 1300
SCALE = 2

FONT_REG = Path("C:/Windows/Fonts/msyh.ttc")
FONT_BOLD = Path("C:/Windows/Fonts/msyhbd.ttc")
if not FONT_REG.exists():
    FONT_REG = Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")
if not FONT_BOLD.exists():
    FONT_BOLD = Path("C:/Windows/Fonts/simhei.ttf")

PALETTE = {
    "paper": "#F7FAFC",
    "white": "#FFFFFF",
    "ink": "#142033",
    "muted": "#607085",
    "line": "#C8D3DF",
    "navy": "#173A5E",
    "navy2": "#E6F0FA",
    "blue": "#2563A6",
    "blue2": "#DDEBFA",
    "cyan": "#0F766E",
    "cyan2": "#D9F2EE",
    "green": "#477A36",
    "green2": "#E3F3DC",
    "amber": "#B06A00",
    "amber2": "#FFF0CC",
    "red": "#B43A3A",
    "red2": "#FDE2E2",
    "purple": "#6950A1",
    "purple2": "#EEE8FF",
    "gray": "#EDF2F7",
    "gray2": "#D8E0EA",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT_REG
    return ImageFont.truetype(str(path), size)


def wrap_text(text: str, max_chars: int) -> list[str]:
    lines: list[str] = []
    for raw in text.split("\n"):
        raw = raw.strip()
        if not raw:
            lines.append("")
            continue
        buf = ""
        for ch in raw:
            buf += ch
            if len(buf) >= max_chars:
                lines.append(buf)
                buf = ""
        if buf:
            lines.append(buf)
    return lines


def text_bbox(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


@dataclass
class TextItem:
    x: int
    y: int
    w: int
    h: int
    text: str
    size: int = 26
    color: str = PALETTE["ink"]
    bold: bool = False
    align: str = "center"
    valign: str = "middle"
    max_chars: int | None = None


@dataclass
class RectItem:
    x: int
    y: int
    w: int
    h: int
    fill: str = PALETTE["white"]
    stroke: str = PALETTE["line"]
    radius: int = 18
    width: int = 3


@dataclass
class LineItem:
    x1: int
    y1: int
    x2: int
    y2: int
    color: str = PALETTE["navy"]
    width: int = 4
    arrow: bool = True
    dash: bool = False


@dataclass
class Canvas:
    slug: str
    title: str
    subtitle: str = ""
    items: list[object] = field(default_factory=list)

    def rect(self, x: int, y: int, w: int, h: int, fill: str = PALETTE["white"], stroke: str = PALETTE["line"], radius: int = 18, width: int = 3) -> None:
        self.items.append(RectItem(x, y, w, h, fill, stroke, radius, width))

    def text(self, x: int, y: int, w: int, h: int, text: str, size: int = 26, color: str = PALETTE["ink"], bold: bool = False, align: str = "center", valign: str = "middle", max_chars: int | None = None) -> None:
        self.items.append(TextItem(x, y, w, h, text, size, color, bold, align, valign, max_chars))

    def line(self, x1: int, y1: int, x2: int, y2: int, color: str = PALETTE["navy"], width: int = 4, arrow: bool = True, dash: bool = False) -> None:
        self.items.append(LineItem(x1, y1, x2, y2, color, width, arrow, dash))

    def card(self, x: int, y: int, w: int, h: int, title: str, body: str, fill: str, stroke: str, title_color: str | None = None, compact: bool = False) -> None:
        self.rect(x, y, w, h, fill, stroke, radius=20, width=3)
        self.rect(x, y, w, 54 if compact else 62, stroke, stroke, radius=20, width=0)
        self.text(x + 22, y + 7, w - 44, 42, title, size=24 if not compact else 21, color=title_color or PALETTE["white"], bold=True, align="left", max_chars=18)
        self.text(x + 24, y + (68 if not compact else 58), w - 48, h - (82 if not compact else 68), body, size=22 if not compact else 19, color=PALETTE["ink"], align="left", valign="top", max_chars=max(8, int((w - 48) / (22 if not compact else 19))))

    def pill(self, x: int, y: int, w: int, text: str, fill: str, color: str = PALETTE["white"]) -> None:
        self.rect(x, y, w, 42, fill, fill, radius=21, width=0)
        self.text(x, y + 1, w, 40, text, size=18, color=color, bold=True, align="center")

    def header(self) -> None:
        self.rect(0, 0, W, H, PALETTE["paper"], PALETTE["paper"], radius=0, width=0)
        self.rect(0, 0, W, 112, PALETTE["navy"], PALETTE["navy"], radius=0, width=0)
        self.text(54, 26, 1320, 52, self.title, size=34, color=PALETTE["white"], bold=True, align="left")
        if self.subtitle:
            self.text(1500, 32, 640, 42, self.subtitle, size=20, color="#D9E7F5", bold=False, align="right")
        self.line(54, 1190, 2146, 1190, PALETTE["line"], width=2, arrow=False)

    def note(self, text: str) -> None:
        self.text(58, 1205, 2084, 52, text, size=22, color=PALETTE["muted"], align="center")

    def render_png(self, path: Path) -> None:
        img = Image.new("RGB", (W * SCALE, H * SCALE), PALETTE["paper"])
        draw = ImageDraw.Draw(img)
        for item in self.items:
            if isinstance(item, RectItem):
                box = [item.x * SCALE, item.y * SCALE, (item.x + item.w) * SCALE, (item.y + item.h) * SCALE]
                if item.radius:
                    draw.rounded_rectangle(box, radius=item.radius * SCALE, fill=item.fill, outline=item.stroke, width=max(1, item.width * SCALE))
                else:
                    draw.rectangle(box, fill=item.fill, outline=item.stroke, width=max(1, item.width * SCALE))
            elif isinstance(item, LineItem):
                draw_line(draw, item, SCALE)
            elif isinstance(item, TextItem):
                draw_text(draw, item, SCALE)
        img.save(path, quality=95)

    def render_svg(self, path: Path) -> None:
        parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
            "<defs>",
            '<marker id="arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#173A5E"/></marker>',
            '<style>text{font-family:"Microsoft YaHei","Noto Sans SC",Arial,sans-serif;dominant-baseline:middle}</style>',
            "</defs>",
        ]
        for item in self.items:
            if isinstance(item, RectItem):
                parts.append(f'<rect x="{item.x}" y="{item.y}" width="{item.w}" height="{item.h}" rx="{item.radius}" fill="{item.fill}" stroke="{item.stroke}" stroke-width="{item.width}"/>')
            elif isinstance(item, LineItem):
                dash = ' stroke-dasharray="12 10"' if item.dash else ""
                marker = ' marker-end="url(#arrow)"' if item.arrow else ""
                parts.append(f'<line x1="{item.x1}" y1="{item.y1}" x2="{item.x2}" y2="{item.y2}" stroke="{item.color}" stroke-width="{item.width}" stroke-linecap="round"{dash}{marker}/>')
            elif isinstance(item, TextItem):
                parts.append(svg_text(item))
        parts.append("</svg>")
        path.write_text("\n".join(parts), encoding="utf-8")


def draw_text(draw: ImageDraw.ImageDraw, item: TextItem, scale: int) -> None:
    fnt = font(item.size * scale, item.bold)
    max_chars = item.max_chars or max(4, int(item.w / (item.size * 0.92)))
    lines = wrap_text(item.text, max_chars)
    line_h = int(item.size * 1.42 * scale)
    total_h = line_h * len(lines)
    if item.valign == "top":
        y = item.y * scale
    elif item.valign == "bottom":
        y = (item.y + item.h) * scale - total_h
    else:
        y = item.y * scale + (item.h * scale - total_h) / 2
    for line in lines:
        tw, _ = text_bbox(draw, line, fnt)
        if item.align == "left":
            x = item.x * scale
        elif item.align == "right":
            x = (item.x + item.w) * scale - tw
        else:
            x = item.x * scale + (item.w * scale - tw) / 2
        draw.text((x, y), line, fill=item.color, font=fnt)
        y += line_h


def svg_text(item: TextItem) -> str:
    max_chars = item.max_chars or max(4, int(item.w / (item.size * 0.92)))
    lines = wrap_text(item.text, max_chars)
    line_h = item.size * 1.42
    total_h = line_h * len(lines)
    if item.valign == "top":
        y = item.y + line_h / 2
    elif item.valign == "bottom":
        y = item.y + item.h - total_h + line_h / 2
    else:
        y = item.y + (item.h - total_h) / 2 + line_h / 2
    if item.align == "left":
        x, anchor = item.x, "start"
    elif item.align == "right":
        x, anchor = item.x + item.w, "end"
    else:
        x, anchor = item.x + item.w / 2, "middle"
    spans = []
    for i, line in enumerate(lines):
        spans.append(f'<tspan x="{x}" y="{y + i * line_h:.1f}">{escape(line)}</tspan>')
    weight = "700" if item.bold else "400"
    return f'<text text-anchor="{anchor}" font-size="{item.size}" font-weight="{weight}" fill="{item.color}">{"".join(spans)}</text>'


def draw_line(draw: ImageDraw.ImageDraw, item: LineItem, scale: int) -> None:
    p1 = (item.x1 * scale, item.y1 * scale)
    p2 = (item.x2 * scale, item.y2 * scale)
    if item.dash:
        draw_dashed_line(draw, p1, p2, item.color, item.width * scale)
    else:
        draw.line([p1, p2], fill=item.color, width=item.width * scale)
    if item.arrow:
        draw_arrowhead(draw, p1, p2, item.color, scale)


def draw_dashed_line(draw: ImageDraw.ImageDraw, p1: tuple[int, int], p2: tuple[int, int], color: str, width: int) -> None:
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    dash, gap = 24, 18
    ux, uy = dx / dist, dy / dist
    t = 0
    while t < dist:
        end = min(t + dash, dist)
        draw.line([(p1[0] + ux * t, p1[1] + uy * t), (p1[0] + ux * end, p1[1] + uy * end)], fill=color, width=width)
        t += dash + gap


def draw_arrowhead(draw: ImageDraw.ImageDraw, p1: tuple[int, int], p2: tuple[int, int], color: str, scale: int) -> None:
    angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    size = 15 * scale
    a1 = angle + math.pi * 0.82
    a2 = angle - math.pi * 0.82
    pts = [
        p2,
        (p2[0] + size * math.cos(a1), p2[1] + size * math.sin(a1)),
        (p2[0] + size * math.cos(a2), p2[1] + size * math.sin(a2)),
    ]
    draw.polygon(pts, fill=color)


def add_step(c: Canvas, n: int, x: int, y: int, title: str, body: str, stroke: str, fill: str) -> None:
    c.rect(x, y, 265, 150, fill, stroke, radius=20, width=3)
    c.rect(x + 18, y + 20, 44, 44, stroke, stroke, radius=22, width=0)
    c.text(x + 18, y + 20, 44, 44, f"{n}", size=20, color=PALETTE["white"], bold=True)
    c.text(x + 78, y + 18, 165, 38, title, size=23, color=stroke, bold=True, align="left")
    c.text(x + 28, y + 72, 210, 62, body, size=20, color=PALETTE["ink"], align="left", valign="top", max_chars=9)


def fig01_architecture() -> Canvas:
    c = Canvas("01_雷达智能体子系统总体架构图", "图 4.3.3.2-1 雷达智能体子系统总体架构图", "系统边界 / 核心模块 / 外部联动")
    c.header()
    left = [
        ("显控分系统", "自然语言、目标选择、区域选择、审批确认"),
        ("信息处理感知子系统", "检测、识别、跟踪、定位与置信度"),
        ("雷达状态与环境数据", "工作模式、参数、资源、设备健康与环境"),
    ]
    for i, (t, b) in enumerate(left):
        y = 230 + i * 210
        c.card(70, y, 330, 145, t, b, PALETTE["blue2"] if i == 0 else PALETTE["cyan2"] if i == 1 else PALETTE["green2"], PALETTE["blue"] if i == 0 else PALETTE["cyan"] if i == 1 else PALETTE["green"], compact=True)
        c.line(400, y + 72, 640, 510, PALETTE["line"], width=4)
    c.rect(610, 215, 950, 690, PALETTE["white"], PALETTE["navy"], radius=24, width=4)
    c.rect(610, 215, 950, 70, PALETTE["navy"], PALETTE["navy"], radius=24, width=0)
    c.text(650, 226, 850, 48, "雷达智能体子系统：智能决策与人机协同中枢", size=27, color=PALETTE["white"], bold=True, align="left")
    c.card(665, 330, 250, 145, "认知核心模块", "意图理解、任务建模、推理规划、结果生成", PALETTE["blue2"], PALETTE["blue"], compact=True)
    c.card(965, 330, 250, 145, "记忆管理模块", "短期上下文、中期任务链、长期经验资产", PALETTE["purple2"], PALETTE["purple"], compact=True)
    c.card(1265, 330, 250, 145, "工具执行模块", "工具代理、协议适配、结果标准化", PALETTE["cyan2"], PALETTE["cyan"], compact=True)
    c.card(810, 570, 250, 145, "工作流引擎", "模板编排、审批、检查点、回滚", PALETTE["amber2"], PALETTE["amber"], compact=True)
    c.card(1110, 570, 250, 145, "数据库接入", "关系、向量、图、时序统一访问", PALETTE["green2"], PALETTE["green"], compact=True)
    c.rect(700, 780, 770, 55, PALETTE["gray"], PALETTE["line"], radius=18, width=2)
    c.text(720, 790, 730, 35, "贯穿治理：任务实例 · 能力包调度 · 安全门控 · 追溯记录", size=22, color=PALETTE["ink"], bold=True)
    right = [
        ("研判结果与证据链", "目标类别、行为特征、威胁等级、不确定性"),
        ("候选参数方案", "波形、波束、门限、跟踪参数与风险说明"),
        ("工作流状态与审批", "流程节点、待确认事项、检查点与回滚状态"),
        ("经验资产与复盘报告", "任务样例、效果指标、长期经验候选"),
    ]
    for i, (t, b) in enumerate(right):
        y = 185 + i * 168
        stroke = [PALETTE["blue"], PALETTE["amber"], PALETTE["red"], PALETTE["green"]][i]
        fill = [PALETTE["blue2"], PALETTE["amber2"], PALETTE["red2"], PALETTE["green2"]][i]
        c.card(1730, y, 380, 122, t, b, fill, stroke, compact=True)
        c.line(1560, 560, 1730, y + 61, stroke, width=4)
    c.card(760, 980, 650, 115, "数据知识底座", "关系库、向量库、图数据库、时序库、雷达知识与历史案例", PALETTE["green2"], PALETTE["green"], compact=True)
    c.line(1085, 905, 1085, 980, PALETTE["green"], width=5)
    c.card(1615, 865, 420, 120, "控制执行链路", "经审批的控制请求由控制链路完成真实下发", PALETTE["red2"], PALETTE["red"], compact=True)
    c.line(1360, 642, 1615, 925, PALETTE["red"], width=5)
    c.note("设计重点：智能体输出研判、建议、工作流请求和追溯记录；真实控制下发由控制执行链路完成。")
    return c


def fig02_composition() -> Canvas:
    c = Canvas("02_五大核心模块功能组成图", "图 4.3.3.2-2 五大核心模块功能组成图", "功能定位 / 流程作用 / 贯穿治理")
    c.header()
    c.rect(90, 180, 2020, 78, PALETTE["navy"], PALETTE["navy"], radius=20, width=0)
    c.text(115, 194, 1970, 48, "统一任务实例贯穿：任务理解 → 智能研判 → 参数建议 → 流程执行 → 经验沉淀", size=28, color=PALETTE["white"], bold=True)
    cards = [
        ("认知核心模块", "智能推理、任务规划与运行协调中心\n\n主要承担意图理解、任务建模、上下文组织、执行路径规划、研判结论与候选方案生成。", PALETTE["blue2"], PALETTE["blue"]),
        ("记忆管理模块", "面向智能体任务的上下文与经验管理中心\n\n管理短期任务记忆、中期任务链、长期经验资产，支撑检索增强与经验回流。", PALETTE["purple2"], PALETTE["purple"]),
        ("工具执行模块", "雷达专业能力的统一执行代理\n\n封装感知解释、数据查询、目标分析、参数仿真、控制适配和报告生成工具。", PALETTE["cyan2"], PALETTE["cyan"]),
        ("工作流引擎模块", "标准流程与高风险动作的受控执行引擎\n\n管理模板、节点、审批、检查点、回滚和流程追溯。", PALETTE["amber2"], PALETTE["amber"]),
        ("数据库管理与接入模块", "智能体侧数据访问、记忆支撑和追溯写入适配中心\n\n提供关系、向量、图关系和时序数据统一访问。", PALETTE["green2"], PALETTE["green"]),
    ]
    xs = [90, 505, 920, 1335, 1750]
    for x, item in zip(xs, cards):
        c.card(x, 345, 360, 430, item[0], item[1], item[2], item[3])
    for i in range(4):
        c.line(xs[i] + 360, 560, xs[i + 1], 560, PALETTE["line"], width=4, arrow=False)
    c.rect(245, 880, 1710, 120, PALETTE["gray"], PALETTE["line"], radius=22, width=3)
    c.text(290, 897, 1620, 38, "贯穿式治理机制", size=28, color=PALETTE["navy"], bold=True)
    c.text(300, 942, 1600, 38, "运行底座、安全门控、追溯记录和运行观测贯穿五大模块，不改变核心功能模块划分。", size=24, color=PALETTE["ink"])
    c.note("图中模块强调功能和流程协同，避免把运行治理机制写成彼此割裂的职责边界。")
    return c


def fig03_layering() -> Canvas:
    c = Canvas("03_软件实现分层架构图", "图 4.3.3.2-3 软件实现分层架构图", "应用层 / 服务层 / 组件层 / 资源层")
    c.header()
    layers = [
        ("应用层", "态势问答、目标研判、波形参数建议、流程状态展示、复盘报告生成", PALETTE["blue2"], PALETTE["blue"]),
        ("服务层", "任务运行管理、认知推理、工作流编排、记忆管理、安全门控机制、追溯记录", PALETTE["purple2"], PALETTE["purple"]),
        ("组件层", "大语言模型推理引擎、雷达专业能力包、工具执行适配、数据库访问适配、语义检索、图关系与时序查询", PALETTE["cyan2"], PALETTE["cyan"]),
        ("资源层", "模型算力、关系库/向量库/图数据库/时序库、感知结果、雷达状态、控制执行接口、雷达知识与历史案例", PALETTE["green2"], PALETTE["green"]),
    ]
    for i, (title, body, fill, stroke) in enumerate(layers):
        y = 210 + i * 210
        c.rect(145, y, 280, 130, stroke, stroke, radius=22, width=0)
        c.text(145, y, 280, 130, title, size=34, color=PALETTE["white"], bold=True)
        c.rect(480, y, 1520, 130, fill, stroke, radius=22, width=3)
        c.text(520, y + 12, 1440, 104, body, size=30, color=PALETTE["ink"], bold=False, max_chars=31)
        if i < 3:
            c.line(1090, y + 130, 1090, y + 205, stroke, width=5)
    c.rect(530, 1075, 1140, 72, PALETTE["gray"], PALETTE["line"], radius=18, width=3)
    c.text(560, 1085, 1080, 42, "五大核心模块用于说明功能组成；四层架构用于说明软件实现组织方式。", size=25, color=PALETTE["ink"], bold=True)
    c.note("映射关系：认知核心承接应用层与服务层，记忆/工具/工作流位于服务层和组件层，数据库接入连接组件层与资源层。")
    return c


def fig04_execution_flow() -> Canvas:
    c = Canvas("04_任务执行信息流程图", "图 4.3.3.2-4 雷达智能体子系统执行信息流程图", "任务实例主线 / 风险分流 / 追溯回流")
    c.header()
    steps = [
        ("任务触发", "显控请求\n感知事件\n状态告警", PALETTE["blue"], PALETTE["blue2"]),
        ("任务实例", "任务编号\n对象引用\n风险等级", PALETTE["blue"], PALETTE["blue2"]),
        ("上下文装载", "感知证据\n雷达状态\n历史引用", PALETTE["purple"], PALETTE["purple2"]),
        ("意图建模", "任务目标\n约束条件\n输出要求", PALETTE["purple"], PALETTE["purple2"]),
        ("路径选择", "能力包\n工具清单\n门控校验", PALETTE["amber"], PALETTE["amber2"]),
        ("结果发布", "摘要\n证据链\n流程状态", PALETTE["green"], PALETTE["green2"]),
        ("追溯记忆", "上下文快照\n工具/审批\n经验候选", PALETTE["green"], PALETTE["green2"]),
    ]
    positions = [(95, 285), (375, 285), (655, 285), (935, 285), (1215, 285), (1770, 285), (1770, 565)]
    for i, ((title, body, stroke, fill), (x, y)) in enumerate(zip(steps, positions), start=1):
        add_step(c, i, x, y, title, body, stroke, fill)
    for i in range(4):
        c.line(positions[i][0] + 265, positions[i][1] + 75, positions[i + 1][0], positions[i + 1][1] + 75, PALETTE["navy"], width=4)
    c.rect(1180, 555, 320, 155, PALETTE["cyan2"], PALETTE["cyan"], radius=20, width=3)
    c.text(1205, 580, 270, 35, "低风险路径", size=27, color=PALETTE["cyan"], bold=True)
    c.text(1220, 635, 240, 45, "动态研判与\nReAct工具调用", size=23, color=PALETTE["ink"])
    c.rect(1180, 805, 320, 155, PALETTE["red2"], PALETTE["red"], radius=20, width=3)
    c.text(1205, 830, 270, 35, "高风险路径", size=27, color=PALETTE["red"], bold=True)
    c.text(1220, 885, 240, 45, "受控工作流编排\n校验、审批、回滚", size=23, color=PALETTE["ink"])
    c.line(1480, 360, 1770, 360, PALETTE["green"], width=4)
    c.line(1340, 435, 1340, 555, PALETTE["cyan"], width=4)
    c.line(1340, 435, 1340, 805, PALETTE["red"], width=4)
    c.line(1500, 635, 1770, 360, PALETTE["cyan"], width=4)
    c.line(1500, 885, 1770, 640, PALETTE["red"], width=4)
    c.line(1902, 565, 1902, 435, PALETTE["green"], width=4)
    c.line(1770, 640, 1498, 885, PALETTE["red"], width=3, arrow=False, dash=True)
    c.note("只读研判和推荐生成可动态调用工具；涉及参数设置、模式切换和回滚恢复时进入受控工作流。")
    return c


def fig05_cognition() -> Canvas:
    c = Canvas("05_认知核心模块处理流程图", "图 4.3.3.2-5 认知核心模块处理流程图", "任务理解 / 能力选择 / 推理规划 / 质量控制")
    c.header()
    steps = [
        ("任务运行管理", "创建任务实例\n绑定来源、对象、风险等级"),
        ("意图理解", "解析自然语言和显控上下文\n抽取任务目标与约束"),
        ("上下文与证据组织", "装载感知证据、雷达状态\n历史任务链与知识片段"),
        ("能力包选择", "匹配目标研判、参数优化\n异常归因或工作流能力"),
        ("执行路径规划", "选择动态工具调用\n或受控工作流模板"),
        ("推理与结果生成", "形成研判结论、候选方案\n风险说明和补证要求"),
        ("响应质量控制", "检查事实依据、证据引用\n不确定性和安全表达"),
    ]
    xs = [90, 385, 680, 975, 1270, 1565, 1860]
    for i, (title, body) in enumerate(steps):
        fill = PALETTE["blue2"] if i < 3 else PALETTE["purple2"] if i < 5 else PALETTE["green2"]
        stroke = PALETTE["blue"] if i < 3 else PALETTE["purple"] if i < 5 else PALETTE["green"]
        add_step(c, i + 1, xs[i], 420, title, body, stroke, fill)
        if i < len(steps) - 1:
            c.line(xs[i] + 265, 495, xs[i + 1], 495, PALETTE["navy"], width=4)
    c.rect(610, 225, 980, 85, PALETTE["gray"], PALETTE["line"], radius=22, width=3)
    c.text(640, 244, 920, 42, "大语言模型推理引擎 + 雷达专业能力包 + 受控工具/工作流", size=27, color=PALETTE["navy"], bold=True)
    c.line(1100, 310, 1100, 420, PALETTE["line"], width=4, arrow=False)
    c.rect(660, 760, 880, 105, PALETTE["amber2"], PALETTE["amber"], radius=22, width=3)
    c.text(690, 784, 820, 45, "输出：研判摘要、证据链、候选参数方案、流程触发建议、风险提示", size=25, color=PALETTE["ink"], bold=True)
    c.line(1992, 570, 1992, 812, PALETTE["green"], width=4)
    c.line(1992, 812, 1540, 812, PALETTE["green"], width=4)
    c.note("认知核心的工程价值在于把开放推理纳入任务实例、能力包、证据引用和质量控制约束。")
    return c


def fig06_memory() -> Canvas:
    c = Canvas("06_三阶分层记忆与经验回流图", "图 4.3.3.2-6 三阶分层记忆与经验回流图", "短期上下文 / 中期任务链 / 长期经验资产")
    c.header()
    c.card(100, 450, 330, 190, "当前任务上下文", "任务目标、感知证据、雷达状态、工具结果、候选方案、检查点", PALETTE["blue2"], PALETTE["blue"], compact=True)
    c.card(520, 240, 360, 190, "短期记忆", "上下文版本、证据编号、工具结果、流程状态，用于当前任务不断裂。", PALETTE["cyan2"], PALETTE["cyan"], compact=True)
    c.card(960, 450, 360, 190, "追溯记录", "输入、推理、工具调用、工作流节点、审批动作、输出结果和反馈。", PALETTE["purple2"], PALETTE["purple"], compact=True)
    c.card(1400, 240, 360, 190, "中期任务链", "目标链、区域链、参数链、异常链，用于近期连续任务关联。", PALETTE["amber2"], PALETTE["amber"], compact=True)
    c.card(1770, 450, 330, 190, "长期经验资产", "知识库、案例库、策略库、经验库，带版本、来源和适用边界。", PALETTE["green2"], PALETTE["green"], compact=True)
    c.line(430, 545, 520, 335, PALETTE["blue"], width=5)
    c.line(880, 335, 960, 545, PALETTE["cyan"], width=5)
    c.line(1320, 545, 1400, 335, PALETTE["purple"], width=5)
    c.line(1760, 335, 1770, 545, PALETTE["amber"], width=5)
    c.rect(760, 780, 690, 125, PALETTE["red2"], PALETTE["red"], radius=24, width=3)
    c.text(805, 800, 600, 42, "质量评估与复核", size=30, color=PALETTE["red"], bold=True)
    c.text(820, 850, 570, 34, "冲突检查 / 适用条件 / 版本管理 / 影子运行 / 人工复核", size=23, color=PALETTE["ink"])
    c.line(1140, 640, 1140, 780, PALETTE["red"], width=5)
    c.line(1935, 640, 1935, 1010, PALETTE["green"], width=4, dash=True)
    c.line(1935, 1010, 265, 1010, PALETTE["green"], width=4, dash=True)
    c.line(265, 1010, 265, 640, PALETTE["green"], width=4, dash=True)
    c.text(770, 1030, 650, 40, "受控回流：相似案例、策略推荐、工具匹配、流程优化", size=25, color=PALETTE["green"], bold=True)
    c.note("经验回流不是简单归档：任务记录先成为经验候选，再经质量评估和复核后进入长期资产。")
    return c


def fig07_workflow_sequence() -> Canvas:
    c = Canvas("07_高风险任务时序交互图", "图 4.3.3.2-7 高风险任务时序交互图", "门控判定 / 受控工作流 / 控制请求适配")
    c.header()
    lanes = [
        ("认知核心", 120, PALETTE["blue"]),
        ("任务运行管理", 430, PALETTE["purple"]),
        ("安全门控", 740, PALETTE["red"]),
        ("工作流引擎", 1050, PALETTE["amber"]),
        ("工具执行", 1360, PALETTE["cyan"]),
        ("外部服务/控制链路", 1670, PALETTE["green"]),
    ]
    for title, x, stroke in lanes:
        c.rect(x, 190, 230, 58, stroke, stroke, radius=16, width=0)
        c.text(x, 199, 230, 36, title, size=22, color=PALETTE["white"], bold=True)
        c.line(x + 115, 248, x + 115, 1090, PALETTE["gray2"], width=3, arrow=False, dash=True)
    events = [
        (0, 1, 310, "提交执行计划、工具建议或工作流触发建议", PALETTE["blue"]),
        (1, 2, 400, "组织风险分级并提交门控校验", PALETTE["purple"]),
        (2, 2, 490, "权限、参数边界、雷达状态、审批状态校验", PALETTE["red"]),
        (2, 1, 580, "要求进入受控工作流", PALETTE["red"]),
        (1, 3, 670, "触发工作流实例", PALETTE["amber"]),
        (3, 2, 760, "参数边界校验、审批确认、检查点", PALETTE["amber"]),
        (3, 4, 850, "调用控制请求适配工具", PALETTE["cyan"]),
        (4, 5, 940, "发送经审批的控制请求", PALETTE["green"]),
        (5, 4, 1030, "返回受理结果、执行状态、异常信息", PALETTE["green"]),
    ]
    for src, dst, y, label, stroke in events:
        x1 = lanes[src][1] + 115
        x2 = lanes[dst][1] + 115
        if src == dst:
            c.line(x1, y, x1 + 170, y, stroke, width=4, arrow=True)
            c.line(x1 + 170, y, x1 + 170, y + 42, stroke, width=4, arrow=False)
            c.line(x1 + 170, y + 42, x1, y + 42, stroke, width=4, arrow=True)
            c.text(x1 + 190, y + 5, 310, 45, label, size=20, color=PALETTE["muted"], align="left", max_chars=15)
        else:
            c.line(x1, y, x2, y, stroke, width=4, arrow=True)
            c.text(min(x1, x2) + 12, y - 38, abs(x2 - x1) - 24, 32, label, size=19, color=PALETTE["muted"], max_chars=22)
    c.note("低风险任务可由门控放行动态工具调用；高风险或控制请求必须进入工作流模板并绑定追溯引用。")
    return c


def fig08_waveform() -> Canvas:
    c = Canvas("08_波形参数设置受控流程图", "图 4.3.3.2-8 波形参数设置受控流程图", "候选方案 / 校验仿真 / 人工确认 / 状态回传")
    c.header()
    data = [
        ("候选方案生成", "认知核心结合任务目标、目标状态、雷达资源和历史效果形成候选参数。", PALETTE["blue"], PALETTE["blue2"]),
        ("参数边界校验", "检查频段、功率、波束资源、检测门限和跟踪参数边界。", PALETTE["purple"], PALETTE["purple2"]),
        ("仿真评估", "评估预期效果、风险点、适用条件和回滚条件。", PALETTE["amber"], PALETTE["amber2"]),
        ("人工确认", "显控分系统展示风险提示、待确认事项和审批回调。", PALETTE["red"], PALETTE["red2"]),
        ("控制请求适配", "按控制链路接口组织经审批的控制请求和检查点信息。", PALETTE["cyan"], PALETTE["cyan2"]),
        ("状态跟踪与回滚", "跟踪受理、执行、异常、效果指标和回滚结果。", PALETTE["green"], PALETTE["green2"]),
    ]
    pos = [(110, 265), (745, 265), (1380, 265), (1380, 665), (745, 665), (110, 665)]
    for i, ((title, body, stroke, fill), (x, y)) in enumerate(zip(data, pos), start=1):
        c.rect(x, y, 520, 170, fill, stroke, radius=22, width=3)
        c.rect(x + 26, y + 28, 50, 50, stroke, stroke, radius=25, width=0)
        c.text(x + 26, y + 28, 50, 50, str(i), size=22, color=PALETTE["white"], bold=True)
        c.text(x + 95, y + 22, 380, 42, title, size=29, color=stroke, bold=True, align="left")
        c.text(x + 95, y + 78, 380, 58, body, size=22, color=PALETTE["ink"], align="left", valign="top", max_chars=18)
    c.line(630, 350, 745, 350, PALETTE["navy"], width=5)
    c.line(1265, 350, 1380, 350, PALETTE["navy"], width=5)
    c.line(1640, 435, 1640, 665, PALETTE["navy"], width=5)
    c.line(1380, 750, 1265, 750, PALETTE["navy"], width=5)
    c.line(745, 750, 630, 750, PALETTE["navy"], width=5)
    c.line(370, 665, 370, 435, PALETTE["green"], width=4, dash=True)
    c.rect(790, 1040, 620, 74, PALETTE["gray"], PALETTE["line"], radius=20, width=3)
    c.text(820, 1056, 560, 38, "效果指标、异常信息和操作员反馈进入追溯记录与记忆回流", size=24, color=PALETTE["ink"], bold=True)
    c.note("该流程用于说明控制链路安全边界：智能体生成候选方案，工作流完成校验审批，控制执行链路完成真实下发。")
    return c


def fig09_interface() -> Canvas:
    c = Canvas("09_接口关系与数据流向图", "图 4.3.3.2-9 雷达智能体子系统接口关系图", "外部接口 / 内部接口 / 统一引用")
    c.header()
    c.rect(730, 235, 740, 560, PALETTE["white"], PALETTE["navy"], radius=24, width=4)
    c.rect(730, 235, 740, 68, PALETTE["navy"], PALETTE["navy"], radius=24, width=0)
    c.text(760, 246, 680, 42, "雷达智能体子系统接口域", size=28, color=PALETTE["white"], bold=True)
    internal = [
        ("外部接入接口", 790, 350, PALETTE["blue"]),
        ("任务运行管理接口", 1030, 350, PALETTE["purple"]),
        ("认知推理接口", 1270, 350, PALETTE["purple"]),
        ("记忆读写接口", 790, 500, PALETTE["green"]),
        ("工具代理接口", 1030, 500, PALETTE["cyan"]),
        ("工作流代理接口", 1270, 500, PALETTE["amber"]),
        ("门控判定接口", 790, 650, PALETTE["red"]),
        ("数据库接入接口", 1030, 650, PALETTE["green"]),
        ("追溯记录接口", 1270, 650, PALETTE["blue"]),
    ]
    for text, x, y, stroke in internal:
        c.rect(x, y, 170, 68, PALETTE["gray"], stroke, radius=15, width=3)
        c.text(x + 8, y + 8, 154, 48, text, size=18, color=PALETTE["ink"], bold=True)
    ext = [
        ("显控分系统", "HTTP / 消息\n任务提交、状态、结果", 80, 230, PALETTE["blue"], PALETTE["blue2"]),
        ("信息处理感知子系统", "消息接口\n感知结果接入", 80, 470, PALETTE["cyan"], PALETTE["cyan2"]),
        ("试验评估/样本/运维", "HTTP / 文件\n评估导出、样本沉淀", 80, 710, PALETTE["amber"], PALETTE["amber2"]),
        ("雷达状态与环境服务", "网络通信 / 消息\n状态、参数、告警", 1635, 230, PALETTE["green"], PALETTE["green2"]),
        ("控制执行链路", "网络通信\n经审批控制请求", 1635, 470, PALETTE["red"], PALETTE["red2"]),
        ("数据知识底座", "HTTP / 数据库\n知识、案例、图、时序", 1635, 710, PALETTE["purple"], PALETTE["purple2"]),
    ]
    for title, body, x, y, stroke, fill in ext:
        c.card(x, y, 390, 120, title, body, fill, stroke, compact=True)
    c.line(470, 290, 730, 385, PALETTE["blue"], width=5)
    c.line(470, 530, 730, 385, PALETTE["cyan"], width=5)
    c.line(470, 770, 730, 690, PALETTE["amber"], width=5)
    c.line(1635, 290, 1470, 385, PALETTE["green"], width=5)
    c.line(1635, 530, 1470, 690, PALETTE["red"], width=5)
    c.line(1635, 770, 1470, 690, PALETTE["purple"], width=5)
    c.rect(370, 1000, 1460, 78, PALETTE["gray"], PALETTE["line"], radius=20, width=3)
    c.text(400, 1015, 1400, 40, "统一引用：任务标识 · 目标/区域引用 · 证据引用 · 追溯引用", size=27, color=PALETTE["navy"], bold=True)
    for i, (txt, fill) in enumerate([("HTTP", PALETTE["blue"]), ("消息", PALETTE["cyan"]), ("网络通信", PALETTE["green"]), ("数据库", PALETTE["purple"]), ("文件", PALETTE["amber"]), ("函数库调用", PALETTE["red"])]):
        c.pill(500 + i * 205, 1105, 155, txt, fill)
    c.note("接口类型按软件实现形态描述；TCP/UDP、端口、报文和字段细节在后续接口控制文档中细化。")
    return c


def figures() -> list[Canvas]:
    return [
        fig01_architecture(),
        fig02_composition(),
        fig03_layering(),
        fig04_execution_flow(),
        fig05_cognition(),
        fig06_memory(),
        fig07_workflow_sequence(),
        fig08_waveform(),
        fig09_interface(),
    ]


def write_readme(figs: list[Canvas]) -> None:
    rows = "\n".join(
        f"| {i:02d} | {f.title} | `svg/{f.slug}.svg` | `png/{f.slug}.png` |"
        for i, f in enumerate(figs, start=1)
    )
    text = f"""# Word方案配图

本目录用于替换技术方案 Markdown 中的 Mermaid 图，面向正式 Word 报告插图使用。

## 使用建议

- Word 中优先插入 `png/` 下的高清 PNG，版式最稳定。
- 如需矢量缩放或后续精修，可使用 `svg/` 下的 SVG。
- 每张图已经按报告正文横向插图比例设计，不要求一页只放一张图；可按章节逐张插入。
- 图内保留标题编号，Word 中也可另加正式图注。

## 文件清单

| 序号 | 图名 | SVG | PNG |
| --- | --- | --- | --- |
{rows}

## 生成方式

运行：

```powershell
& 'C:\\Users\\sunbf\\.cache\\codex-runtimes\\codex-primary-runtime\\dependencies\\python\\python.exe' 'D:\\knowledge\\radar agent\\tools\\generate_word_report_figures.py'
```

脚本会重新生成 `svg/`、`png/` 和 `preview/配图总览.png`。
"""
    (OUT / "README.md").write_text(text, encoding="utf-8")


def write_contact_sheet(figs: list[Canvas]) -> None:
    thumbs: list[tuple[str, Image.Image]] = []
    for f in figs:
        img = Image.open(PNG_DIR / f"{f.slug}.png").convert("RGB")
        img.thumbnail((620, 365))
        thumbs.append((f.slug, img.copy()))
    cols = 3
    cell_w, cell_h = 700, 455
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * cell_w + 80, rows * cell_h + 120), "white")
    draw = ImageDraw.Draw(sheet)
    draw.text((40, 30), "Word方案配图总览", fill=PALETTE["navy"], font=font(36, True))
    label_font = font(20)
    for idx, (name, img) in enumerate(thumbs):
        col, row = idx % cols, idx // cols
        x, y = 40 + col * cell_w, 95 + row * cell_h
        sheet.paste(img, (x, y))
        draw.text((x, y + 375), name, fill=PALETTE["muted"], font=label_font)
    sheet.save(PREVIEW_DIR / "配图总览.png", quality=95)


def main() -> None:
    for d in (OUT, SVG_DIR, PNG_DIR, PREVIEW_DIR):
        d.mkdir(parents=True, exist_ok=True)
    figs = figures()
    for f in figs:
        f.render_svg(SVG_DIR / f"{f.slug}.svg")
        f.render_png(PNG_DIR / f"{f.slug}.png")
    write_contact_sheet(figs)
    write_readme(figs)
    print(OUT)
    print(f"figures={len(figs)}")


if __name__ == "__main__":
    main()
