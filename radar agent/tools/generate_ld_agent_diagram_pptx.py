from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "LD智能体架构图PPT"
OUT_PPTX = OUT_DIR / "LD智能体架构流程图组.pptx"

EMU_PER_INCH = 914400
SLIDE_W = 13.333333
SLIDE_H = 7.5
SLIDE_CX = 12192000
SLIDE_CY = 6858000

FONT = "Microsoft YaHei"

COLORS = {
    "bg": "F7F9FC",
    "ink": "172033",
    "muted": "64748B",
    "line": "CBD5E1",
    "blue": "1F4E79",
    "blue2": "DBEAFE",
    "cyan": "0F766E",
    "cyan2": "CCFBF1",
    "green": "2F6B3F",
    "green2": "DCFCE7",
    "amber": "A16207",
    "amber2": "FEF3C7",
    "red": "B91C1C",
    "red2": "FEE2E2",
    "purple": "6D28D9",
    "purple2": "EDE9FE",
    "white": "FFFFFF",
    "black": "0B1220",
}


def emu(value: float) -> int:
    return int(round(value * EMU_PER_INCH))


def color(value: str) -> str:
    return value.replace("#", "").upper()


def xesc(value: str) -> str:
    return escape(str(value), {'"': "&quot;"})


class Slide:
    def __init__(self, title: str, eyebrow: str = "", subtitle: str = "") -> None:
        self.title = title
        self.eyebrow = eyebrow
        self.subtitle = subtitle
        self.items: list[str] = []
        self.shape_id = 10

    def next_id(self) -> int:
        self.shape_id += 1
        return self.shape_id

    def add(self, xml: str) -> None:
        self.items.append(xml)

    def text_box(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        text: str,
        size: int = 16,
        fill: str | None = None,
        stroke: str | None = None,
        text_color: str = COLORS["ink"],
        bold: bool = False,
        align: str = "left",
        valign: str = "mid",
        radius: bool = False,
        margin: int = 91440,
    ) -> None:
        self.add(
            shape_xml(
                self.next_id(),
                x,
                y,
                w,
                h,
                text,
                size=size,
                fill=fill,
                stroke=stroke,
                text_color=text_color,
                bold=bold,
                align=align,
                valign=valign,
                radius=radius,
                margin=margin,
            )
        )

    def box(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        label: str,
        note: str = "",
        fill: str = COLORS["white"],
        stroke: str = COLORS["line"],
        accent: str | None = None,
        dark: bool = False,
        size: int = 15,
        title_size: int = 18,
    ) -> None:
        body = label if not note else f"{label}\n{note}"
        text_color = COLORS["white"] if dark else COLORS["ink"]
        self.text_box(
            x,
            y,
            w,
            h,
            body,
            size=size,
            fill=fill,
            stroke=stroke,
            text_color=text_color,
            bold=False,
            align="center",
            radius=True,
        )
        if accent:
            self.add(line_xml(self.next_id(), x + 0.12, y + 0.13, x + 0.12, y + h - 0.13, accent, width=3, arrow=False))
        if note:
            self.text_box(
                x + 0.15,
                y + 0.15,
                w - 0.3,
                0.28,
                label,
                size=title_size,
                fill=None,
                stroke=None,
                text_color=text_color,
                bold=True,
                align="center",
                margin=0,
            )

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        stroke: str = COLORS["blue"],
        width: float = 2.0,
        arrow: bool = True,
        dash: bool = False,
    ) -> None:
        self.add(line_xml(self.next_id(), x1, y1, x2, y2, stroke, width, arrow, dash))

    def render(self, idx: int, total: int) -> str:
        header = [
            shape_xml(
                2,
                0,
                0,
                SLIDE_W,
                SLIDE_H,
                "",
                fill=COLORS["bg"],
                stroke=None,
                radius=False,
            ),
            shape_xml(
                3,
                0.42,
                0.22,
                12.5,
                0.24,
                self.eyebrow or "LD AGENT SUBSYSTEM · DIAGRAM SET",
                size=8,
                fill=None,
                stroke=None,
                text_color=COLORS["muted"],
                bold=True,
                align="left",
                margin=0,
            ),
            shape_xml(
                4,
                0.42,
                0.52,
                8.2,
                0.54,
                self.title,
                size=24,
                fill=None,
                stroke=None,
                text_color=COLORS["ink"],
                bold=True,
                align="left",
                margin=0,
            ),
            line_xml(5, 0.42, 1.16, 12.9, 1.16, COLORS["line"], width=1.0, arrow=False),
            shape_xml(
                6,
                11.5,
                0.52,
                1.4,
                0.28,
                f"{idx:02d} / {total:02d}",
                size=9,
                fill=None,
                stroke=None,
                text_color=COLORS["muted"],
                bold=True,
                align="right",
                margin=0,
            ),
        ]
        if self.subtitle:
            header.append(
                shape_xml(
                    7,
                    0.42,
                    1.22,
                    11.9,
                    0.32,
                    self.subtitle,
                    size=10,
                    fill=None,
                    stroke=None,
                    text_color=COLORS["muted"],
                    align="left",
                    margin=0,
                )
            )
        footer = [
            line_xml(8, 0.42, 7.06, 12.9, 7.06, COLORS["line"], width=0.8, arrow=False),
            shape_xml(
                9,
                0.42,
                7.12,
                12.48,
                0.18,
                "Source: 4.3.3.2 雷达智能体子系统技术方案 · editable PowerPoint shapes",
                size=7,
                fill=None,
                stroke=None,
                text_color=COLORS["muted"],
                align="right",
                margin=0,
            ),
        ]
        sp_tree = "\n".join(
            [
                '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>',
                '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>',
                *header,
                *self.items,
                *footer,
            ]
        )
        return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>{sp_tree}</p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>'''


def solid_fill(fill: str | None) -> str:
    if fill is None:
        return "<a:noFill/>"
    return f'<a:solidFill><a:srgbClr val="{color(fill)}"/></a:solidFill>'


def line_prop(stroke: str | None, width: float = 1.2, arrow: bool = False, dash: bool = False) -> str:
    if stroke is None:
        return "<a:ln><a:noFill/></a:ln>"
    tail = '<a:tailEnd type="triangle"/>' if arrow else ""
    dash_xml = '<a:prstDash val="dash"/>' if dash else ""
    return f'''<a:ln w="{int(width * 12700)}">
      <a:solidFill><a:srgbClr val="{color(stroke)}"/></a:solidFill>
      {dash_xml}{tail}
    </a:ln>'''


def text_body(text: str, size: int, text_color: str, bold: bool, align: str, valign: str, margin: int) -> str:
    anchor = {"top": "t", "mid": "mid", "bottom": "b"}.get(valign, "mid")
    algn = {"left": "l", "center": "ctr", "right": "r"}.get(align, align)
    paragraphs = []
    for i, line in enumerate(str(text).split("\n")):
        run_bold = bold or (i == 0 and len(str(text).split("\n")) > 1)
        run_size = size + 2 if i == 0 and len(str(text).split("\n")) > 1 else size
        paragraphs.append(
            f'''<a:p>
        <a:pPr algn="{algn}"/>
        <a:r>
          <a:rPr lang="zh-CN" sz="{run_size * 100}" {'b="1"' if run_bold else ''}>
            <a:solidFill><a:srgbClr val="{color(text_color)}"/></a:solidFill>
            <a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/>
          </a:rPr>
          <a:t>{xesc(line)}</a:t>
        </a:r>
      </a:p>'''
        )
    return f'''<p:txBody>
    <a:bodyPr wrap="square" anchor="{anchor}" lIns="{margin}" rIns="{margin}" tIns="{int(margin * 0.55)}" bIns="{int(margin * 0.55)}"/>
    <a:lstStyle/>
    {''.join(paragraphs)}
  </p:txBody>'''


def shape_xml(
    sid: int,
    x: float,
    y: float,
    w: float,
    h: float,
    text: str = "",
    size: int = 14,
    fill: str | None = COLORS["white"],
    stroke: str | None = COLORS["line"],
    text_color: str = COLORS["ink"],
    bold: bool = False,
    align: str = "center",
    valign: str = "mid",
    radius: bool = True,
    margin: int = 91440,
) -> str:
    geom = "roundRect" if radius else "rect"
    tx = text_body(text, size, text_color, bold, align, valign, margin) if text else ""
    return f'''<p:sp>
  <p:nvSpPr><p:cNvPr id="{sid}" name="Shape {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm><a:off x="{emu(x)}" y="{emu(y)}"/><a:ext cx="{emu(w)}" cy="{emu(h)}"/></a:xfrm>
    <a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>
    {solid_fill(fill)}
    {line_prop(stroke)}
  </p:spPr>
  {tx}
</p:sp>'''


def line_xml(
    sid: int,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stroke: str = COLORS["blue"],
    width: float = 2.0,
    arrow: bool = True,
    dash: bool = False,
) -> str:
    left, top = min(x1, x2), min(y1, y2)
    w, h = abs(x2 - x1), abs(y2 - y1)
    flip_h = ' flipH="1"' if x2 < x1 else ""
    flip_v = ' flipV="1"' if y2 < y1 else ""
    return f'''<p:sp>
  <p:nvSpPr><p:cNvPr id="{sid}" name="Line {sid}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
  <p:spPr>
    <a:xfrm{flip_h}{flip_v}><a:off x="{emu(left)}" y="{emu(top)}"/><a:ext cx="{max(1, emu(w))}" cy="{max(1, emu(h))}"/></a:xfrm>
    <a:prstGeom prst="line"><a:avLst/></a:prstGeom>
    <a:noFill/>
    {line_prop(stroke, width=width, arrow=arrow, dash=dash)}
  </p:spPr>
</p:sp>'''


def pill(slide: Slide, x: float, y: float, text: str, fill: str, text_color: str = COLORS["white"]) -> None:
    slide.text_box(x, y, 1.34, 0.28, text, size=8, fill=fill, stroke=fill, text_color=text_color, bold=True, align="center", radius=True)


def add_cover() -> Slide:
    s = Slide("雷达智能体子系统图组", "ARCHITECTURE · FLOW · SEQUENCE · COMPOSITION", "面向方案文档和汇报复用的可编辑 PowerPoint 原生图形")
    s.text_box(0, 0, SLIDE_W, SLIDE_H, "", fill=COLORS["black"], stroke=None, radius=False)
    s.text_box(0.62, 0.52, 5.2, 0.25, "LD AGENT SUBSYSTEM · 2026.05", size=9, fill=None, stroke=None, text_color="B9C7E6", bold=True, align="left", margin=0)
    s.text_box(0.62, 1.28, 7.5, 1.2, "雷达智能体\n架构流程图组", size=32, fill=None, stroke=None, text_color=COLORS["white"], bold=True, align="left", margin=0)
    s.text_box(0.7, 3.05, 4.9, 0.6, "用于 PPT 汇报，也可复制到 Word 方案文档。图形由原生形状、线条和文本组成，后续可直接编辑。", size=15, fill=None, stroke=None, text_color="D7DEEE", align="left", margin=0)
    cards = [
        ("01", "总体架构", "外部系统、智能体核心与输出联动"),
        ("02", "功能组成", "五大模块与贯穿治理机制"),
        ("03", "执行流程", "从任务触发到追溯记忆"),
        ("04", "时序交互", "低风险工具与高风险工作流"),
    ]
    for i, (num, title, note) in enumerate(cards):
        x = 0.78 + i * 3.05
        s.text_box(x, 5.25, 2.55, 1.05, f"{num}\n{title}\n{note}", size=10, fill="111C32", stroke="2E436C", text_color=COLORS["white"], align="left", radius=True)
    s.line(8.6, 1.0, 12.45, 6.45, "355B96", width=2.0, arrow=False, dash=True)
    s.line(9.2, 0.75, 12.65, 5.2, "1D4ED8", width=4.0, arrow=False)
    s.line(8.95, 5.75, 12.55, 1.95, "14B8A6", width=3.0, arrow=False)
    return s


def add_architecture() -> Slide:
    s = Slide("总体架构图", "SYSTEM ARCHITECTURE", "以雷达智能体为智能决策中枢，连接显控、感知、状态、控制执行链路和数据知识底座。")
    # External input side
    left_items = [
        ("显控分系统", "自然语言 / 目标选择\n区域选择 / 审批确认", COLORS["blue2"], COLORS["blue"]),
        ("信息处理感知子系统", "检测 / 识别 / 跟踪 / 定位\n模型结果与置信度", COLORS["cyan2"], COLORS["cyan"]),
        ("雷达状态与环境数据", "工作模式 / 参数 / 资源\n设备健康 / 环境条件", COLORS["green2"], COLORS["green"]),
    ]
    for i, (title, note, fill, stroke) in enumerate(left_items):
        y = 1.72 + i * 1.15
        s.box(0.48, y, 2.35, 0.78, title, note, fill=fill, stroke=stroke, accent=stroke, size=9, title_size=12)
        s.line(2.83, y + 0.39, 3.42, 3.18, stroke, width=1.8)
    s.box(4.0, 1.55, 5.15, 3.4, "雷达智能体子系统", "Agent Harness / Safety Gate / Trace", fill=COLORS["black"], stroke=COLORS["black"], dark=True, size=12, title_size=19)
    modules = [
        ("认知核心", 4.32, 2.25, COLORS["blue"]),
        ("记忆管理", 6.18, 2.25, COLORS["purple"]),
        ("工具执行", 7.84, 2.25, COLORS["cyan"]),
        ("工作流引擎", 4.95, 3.38, COLORS["amber"]),
        ("数据库接入", 6.98, 3.38, COLORS["green"]),
    ]
    for label, x, y, c in modules:
        s.text_box(x, y, 1.42, 0.58, label, size=12, fill="16243C", stroke="44546A", text_color=COLORS["white"], bold=True, align="center", radius=True)
    s.text_box(4.35, 4.35, 4.45, 0.34, "贯穿治理：任务实例 · 权限校验 · 参数边界 · 追溯记录 · 经验回流", size=9, fill="243B64", stroke="243B64", text_color="D7E7FF", align="center", radius=True)
    right_items = [
        ("研判结果与证据链", "目标类别 / 行为 / 威胁等级", COLORS["blue"]),
        ("候选参数方案", "波形 / 波束 / 门限 / 跟踪参数", COLORS["amber"]),
        ("工作流状态与审批", "检查点 / 回滚 / 状态同步", COLORS["red"]),
        ("复盘报告与经验资产", "短中长期记忆与经验候选", COLORS["green"]),
    ]
    for i, (title, note, stroke) in enumerate(right_items):
        y = 1.62 + i * 0.92
        s.box(10.05, y, 2.65, 0.62, title, note, fill=COLORS["white"], stroke=stroke, accent=stroke, size=8, title_size=11)
        s.line(9.15, 3.18, 10.05, y + 0.31, stroke, width=1.7)
    s.box(4.72, 5.55, 3.7, 0.58, "数据知识底座", "关系库 / 向量库 / 图数据库 / 时序库", fill=COLORS["green2"], stroke=COLORS["green"], accent=COLORS["green"], size=9, title_size=12)
    s.line(6.55, 4.95, 6.55, 5.55, COLORS["green"], width=1.8)
    s.box(9.88, 5.48, 2.86, 0.7, "控制执行链路", "真实控制下发由控制链路完成", fill=COLORS["red2"], stroke=COLORS["red"], accent=COLORS["red"], size=9, title_size=12)
    s.line(8.72, 4.18, 9.88, 5.83, COLORS["red"], width=1.8)
    return s


def add_composition() -> Slide:
    s = Slide("功能组成图", "FUNCTION COMPOSITION", "五大核心功能模块支撑任务理解、智能研判、参数建议、流程执行和经验沉淀。")
    s.text_box(0.62, 1.55, 12.1, 0.42, "贯穿式运行治理：任务实例管理 / 能力包调度 / 安全门控机制 / 追溯记录 / 运行观测", size=13, fill=COLORS["black"], stroke=COLORS["black"], text_color=COLORS["white"], bold=True, align="center", radius=True)
    items = [
        ("认知核心模块", "意图理解、任务建模、上下文组织、执行路径规划、研判结论和候选方案生成", COLORS["blue2"], COLORS["blue"]),
        ("记忆管理模块", "短期任务记忆、中期任务链、长期知识/案例/策略/经验与追溯回流", COLORS["purple2"], COLORS["purple"]),
        ("工具执行模块", "感知解释、数据查询、目标分析、参数仿真、控制请求适配和报告生成", COLORS["cyan2"], COLORS["cyan"]),
        ("工作流引擎模块", "模板编排、节点执行、审批、检查点、回滚和流程追溯", COLORS["amber2"], COLORS["amber"]),
        ("数据库管理与接入模块", "关系、向量、图关系、时序数据访问，检索路由、质量标识和追溯写入", COLORS["green2"], COLORS["green"]),
    ]
    positions = [(0.72, 2.38), (5.0, 2.38), (9.28, 2.38), (2.72, 4.28), (7.12, 4.28)]
    for (title, note, fill, stroke), (x, y) in zip(items, positions):
        s.box(x, y, 3.36, 1.18, title, note, fill=fill, stroke=stroke, accent=stroke, size=9, title_size=14)
    center = (6.66, 3.77)
    for x, y in positions:
        s.line(center[0], center[1], x + 1.68, y + 0.59, COLORS["line"], width=1.3, arrow=False)
    s.text_box(5.35, 3.34, 2.62, 0.86, "统一任务实例\n统一证据引用\n统一追溯引用", size=13, fill=COLORS["black"], stroke=COLORS["black"], text_color=COLORS["white"], bold=True, align="center", radius=True)
    s.text_box(0.82, 6.05, 11.72, 0.5, "设计要点：运行底座、安全门控和追溯记录是贯穿机制，不作为替代五大核心模块的独立业务孤岛。", size=12, fill="EEF2F7", stroke=COLORS["line"], text_color=COLORS["ink"], align="center", radius=True)
    return s


def add_layered() -> Slide:
    s = Slide("软件分层架构图", "SOFTWARE LAYERING", "同一套智能体能力可以从应用层、服务层、组件层和资源层四个实现视角组织。")
    layers = [
        ("应用层", "态势问答 | 目标研判 | 波形参数建议 | 流程状态展示 | 复盘报告生成", COLORS["blue2"], COLORS["blue"]),
        ("服务层", "任务运行管理 | 认知推理 | 工作流编排 | 记忆管理 | 安全门控 | 追溯记录", COLORS["purple2"], COLORS["purple"]),
        ("组件层", "大语言模型推理引擎 | 雷达专业能力包 | 工具执行适配 | 数据库访问适配 | 语义检索 | 图关系与时序查询", COLORS["cyan2"], COLORS["cyan"]),
        ("资源层", "模型算力 | 关系/向量/图/时序数据 | 感知结果 | 雷达状态 | 控制执行接口 | 雷达知识与历史案例", COLORS["green2"], COLORS["green"]),
    ]
    for i, (title, note, fill, stroke) in enumerate(layers):
        y = 1.6 + i * 1.22
        s.text_box(0.76, y, 1.55, 0.68, title, size=17, fill=stroke, stroke=stroke, text_color=COLORS["white"], bold=True, align="center", radius=True)
        s.text_box(2.55, y, 9.9, 0.68, note, size=13, fill=fill, stroke=stroke, text_color=COLORS["ink"], align="center", radius=True)
        if i < len(layers) - 1:
            s.line(6.65, y + 0.72, 6.65, y + 1.18, stroke, width=1.8)
    s.text_box(0.85, 6.56, 11.55, 0.34, "映射关系：认知核心主要承接应用层和服务层；记忆、工具、工作流位于服务层/组件层；数据库接入连接组件层和资源层。", size=10, fill=None, stroke=None, text_color=COLORS["muted"], align="center", margin=0)
    return s


def add_execution_flow() -> Slide:
    s = Slide("系统执行信息流程图", "TASK EXECUTION FLOW", "任务实例贯穿显控请求、感知事件、上下文、推理、工具、工作流、追溯和记忆回流。")
    steps = [
        ("任务触发", "显控请求\n感知事件\n状态告警", COLORS["blue"]),
        ("创建任务实例", "任务编号\n对象引用\n风险等级", COLORS["blue"]),
        ("上下文装载", "感知证据\n雷达状态\n历史引用", COLORS["purple"]),
        ("意图理解", "任务目标\n约束条件\n输出要求", COLORS["purple"]),
        ("路径选择", "能力包\n工具清单\n风险分级", COLORS["amber"]),
        ("结果发布", "研判摘要\n证据链\n流程状态", COLORS["green"]),
        ("追溯记忆", "上下文快照\n工具/审批\n经验候选", COLORS["green"]),
    ]
    xs = [0.55, 2.35, 4.15, 5.95, 7.75, 10.15, 11.75]
    for i, ((title, note, stroke), x) in enumerate(zip(steps, xs)):
        y = 2.3 if i % 2 == 0 else 3.45
        s.box(x, y, 1.32, 0.86, title, note, fill=COLORS["white"], stroke=stroke, accent=stroke, size=8, title_size=10)
        if i < len(steps) - 1:
            nx, ny = xs[i + 1], (2.3 if (i + 1) % 2 == 0 else 3.45)
            s.line(x + 1.32, y + 0.43, nx, ny + 0.43, COLORS["blue"], width=1.6)
    s.text_box(7.55, 4.92, 2.05, 0.68, "低风险路径\nReAct 工具调用", size=11, fill=COLORS["cyan2"], stroke=COLORS["cyan"], text_color=COLORS["ink"], align="center", radius=True)
    s.text_box(7.55, 5.82, 2.05, 0.68, "高风险路径\n受控工作流编排", size=11, fill=COLORS["red2"], stroke=COLORS["red"], text_color=COLORS["ink"], align="center", radius=True)
    s.line(8.43, 4.31, 8.58, 4.92, COLORS["cyan"], width=1.4)
    s.line(8.43, 4.31, 8.58, 5.82, COLORS["red"], width=1.4)
    s.text_box(0.8, 5.35, 5.75, 0.78, "核心分流规则：目标解释、异常归因、报告生成等只读任务可动态调用工具；波形参数设置、工作模式切换、回滚恢复进入工作流模板。", size=12, fill="EEF2F7", stroke=COLORS["line"], text_color=COLORS["ink"], align="left", radius=True)
    return s


def add_waveform_workflow() -> Slide:
    s = Slide("波形参数设置受控流程图", "CONTROLLED WAVEFORM WORKFLOW", "候选参数方案不直接下发，需经过校验、仿真、审批、控制请求适配、状态跟踪和回滚检查点。")
    steps = [
        ("候选方案生成", "任务目标、目标状态、资源约束、历史效果"),
        ("参数边界校验", "频段、功率、波束、门限、跟踪参数"),
        ("仿真评估", "预期效果、风险点、适用条件、回滚条件"),
        ("人工确认", "显控审批、待确认事项、风险提示"),
        ("控制请求适配", "按控制链路协议组织经审批请求"),
        ("状态跟踪与回滚", "受理、执行、异常、效果指标、回滚结果"),
    ]
    for i, (title, note) in enumerate(steps):
        x = 0.72 + (i % 3) * 4.15
        y = 1.8 + (i // 3) * 2.25
        stroke = [COLORS["blue"], COLORS["amber"], COLORS["purple"], COLORS["red"], COLORS["cyan"], COLORS["green"]][i]
        fill = [COLORS["blue2"], COLORS["amber2"], COLORS["purple2"], COLORS["red2"], COLORS["cyan2"], COLORS["green2"]][i]
        s.box(x, y, 3.25, 1.05, f"{i + 1}. {title}", note, fill=fill, stroke=stroke, accent=stroke, size=9, title_size=12)
        if i in (0, 1, 3, 4):
            s.line(x + 3.25, y + 0.53, x + 4.15, y + 0.53, stroke, width=1.8)
        if i == 2:
            s.line(x + 1.62, y + 1.05, x + 1.62, y + 1.52, stroke, width=1.8)
            s.line(x + 1.62, y + 1.52, 0.72 + 1.62, 4.05, stroke, width=1.8)
        if i == 5:
            s.line(x + 1.62, y + 1.05, 1.05, 6.35, COLORS["green"], width=1.6, dash=True)
    s.text_box(1.05, 6.2, 4.25, 0.46, "效果指标、异常信息和操作员反馈进入追溯记录与记忆回流", size=11, fill=COLORS["green2"], stroke=COLORS["green"], text_color=COLORS["ink"], align="center", radius=True)
    s.text_box(7.0, 6.2, 4.9, 0.46, "控制请求由控制执行链路真实下发，智能体保留建议、流程状态和追溯引用", size=11, fill=COLORS["red2"], stroke=COLORS["red"], text_color=COLORS["ink"], align="center", radius=True)
    return s


def add_sequence() -> Slide:
    s = Slide("高风险任务时序交互图", "SEQUENCE DIAGRAM", "展示认知核心提交方案后，任务运行管理、安全门控、工作流、工具执行和外部控制链路之间的关键交互。")
    lanes = [
        ("认知核心", 0.72, COLORS["blue"]),
        ("任务运行管理", 2.62, COLORS["purple"]),
        ("安全门控", 4.52, COLORS["red"]),
        ("工作流引擎", 6.42, COLORS["amber"]),
        ("工具执行", 8.32, COLORS["cyan"]),
        ("外部服务/控制链路", 10.22, COLORS["green"]),
    ]
    for name, x, stroke in lanes:
        s.text_box(x, 1.56, 1.42, 0.42, name, size=10, fill=stroke, stroke=stroke, text_color=COLORS["white"], bold=True, align="center", radius=True)
        s.line(x + 0.71, 2.0, x + 0.71, 6.55, "AAB6C5", width=1.0, arrow=False, dash=True)
    arrows = [
        (0, 1, 2.25, "提交执行计划/工具建议/流程触发建议", COLORS["blue"]),
        (1, 2, 2.8, "组织风险分级并提交门控校验", COLORS["purple"]),
        (2, 2, 3.32, "权限、参数边界、雷达状态、审批状态校验", COLORS["red"]),
        (2, 1, 3.84, "要求进入受控工作流", COLORS["red"]),
        (1, 3, 4.35, "触发工作流实例", COLORS["amber"]),
        (3, 2, 4.86, "参数边界/审批/检查点", COLORS["amber"]),
        (3, 4, 5.37, "调用控制请求适配工具", COLORS["cyan"]),
        (4, 5, 5.88, "发送经审批的控制请求", COLORS["green"]),
        (5, 4, 6.38, "返回受理与执行状态", COLORS["green"]),
    ]
    for src, dst, y, label, stroke in arrows:
        x1 = lanes[src][1] + 0.71
        x2 = lanes[dst][1] + 0.71
        s.line(x1, y, x2, y, stroke, width=1.4, arrow=True, dash=src == dst)
        if src == dst:
            s.text_box(x1 + 0.12, y - 0.2, 2.6, 0.22, label, size=7, fill=COLORS["bg"], stroke=None, text_color=COLORS["muted"], align="left", margin=0)
        else:
            s.text_box(min(x1, x2) + 0.08, y - 0.19, abs(x2 - x1) - 0.16, 0.22, label, size=7, fill=COLORS["bg"], stroke=None, text_color=COLORS["muted"], align="center", margin=0)
    s.text_box(0.78, 6.62, 11.6, 0.28, "只读或低风险任务可由安全门控放行动态工具调用；高风险或控制请求进入工作流模板并绑定追溯引用。", size=9, fill=None, stroke=None, text_color=COLORS["muted"], align="center", margin=0)
    return s


def add_memory_loop() -> Slide:
    s = Slide("三阶分层记忆闭环图", "THREE-TIER MEMORY LOOP", "短期记忆支撑当前任务，中期记忆组织近期任务链，长期记忆沉淀知识、案例、策略和经验资产。")
    nodes = [
        ("当前任务上下文", "任务目标 / 感知证据\n雷达状态 / 工具结果", 0.82, 3.02, COLORS["blue2"], COLORS["blue"]),
        ("短期记忆", "上下文版本\n证据编号\n任务状态", 3.18, 1.82, COLORS["cyan2"], COLORS["cyan"]),
        ("追溯记录", "输入 / 推理 / 调用\n审批 / 结果 / 反馈", 5.65, 3.02, COLORS["purple2"], COLORS["purple"]),
        ("中期任务链", "目标链 / 区域链\n参数链 / 异常链", 8.15, 1.82, COLORS["amber2"], COLORS["amber"]),
        ("长期经验资产", "知识库 / 案例库\n策略库 / 经验库", 10.12, 3.02, COLORS["green2"], COLORS["green"]),
    ]
    for title, note, x, y, fill, stroke in nodes:
        s.box(x, y, 2.0, 1.12, title, note, fill=fill, stroke=stroke, accent=stroke, size=9, title_size=12)
    s.line(2.82, 3.58, 3.18, 2.38, COLORS["blue"], width=1.8)
    s.line(5.18, 2.38, 5.65, 3.58, COLORS["cyan"], width=1.8)
    s.line(7.65, 3.58, 8.15, 2.38, COLORS["purple"], width=1.8)
    s.line(10.15, 2.38, 10.12, 3.58, COLORS["amber"], width=1.8)
    s.line(11.12, 4.14, 1.82, 4.14, COLORS["green"], width=1.6, arrow=True, dash=True)
    s.text_box(4.75, 5.15, 3.85, 0.74, "质量评估与复核\n冲突检查 / 适用边界 / 版本管理 / 影子运行", size=11, fill=COLORS["red2"], stroke=COLORS["red"], text_color=COLORS["ink"], align="center", radius=True)
    s.line(6.65, 4.14, 6.65, 5.15, COLORS["red"], width=1.6)
    s.text_box(0.9, 6.35, 11.45, 0.35, "记忆回流原则：不是把一次任务记录直接变成长期经验，而是先形成经验候选，再经过质量评估、复核和版本治理。", size=10, fill=None, stroke=None, text_color=COLORS["muted"], align="center", margin=0)
    return s


def add_interface_map() -> Slide:
    s = Slide("接口关系图", "INTERFACE MAP", "接口围绕统一任务标识、目标/区域引用、证据引用和追溯引用展开，技术类型按实现形态划分。")
    s.box(4.62, 2.2, 4.05, 2.35, "雷达智能体子系统", "外部接入 / 任务运行 / 认知推理\n记忆读写 / 工具代理 / 工作流代理\n门控判定 / 数据库接入 / 追溯记录", fill=COLORS["black"], stroke=COLORS["black"], dark=True, size=10, title_size=15)
    externals = [
        ("显控分系统", "HTTP / 消息\n任务提交、状态、结果", 0.62, 1.65, COLORS["blue2"], COLORS["blue"]),
        ("信息处理感知子系统", "消息接口\n检测、识别、跟踪、定位", 0.62, 4.12, COLORS["cyan2"], COLORS["cyan"]),
        ("雷达状态与环境服务", "网络通信 / 消息\n状态、参数、告警", 9.95, 1.65, COLORS["green2"], COLORS["green"]),
        ("控制执行链路", "网络通信\n经审批控制请求", 9.95, 4.12, COLORS["red2"], COLORS["red"]),
        ("数据知识底座", "HTTP / 数据库\n知识、案例、时序、图关系", 4.72, 5.55, COLORS["purple2"], COLORS["purple"]),
    ]
    for title, note, x, y, fill, stroke in externals:
        s.box(x, y, 2.65, 0.9, title, note, fill=fill, stroke=stroke, accent=stroke, size=8, title_size=11)
    s.line(3.27, 2.1, 4.62, 2.75, COLORS["blue"], width=1.6)
    s.line(3.27, 4.57, 4.62, 4.02, COLORS["cyan"], width=1.6)
    s.line(9.95, 2.1, 8.67, 2.75, COLORS["green"], width=1.6)
    s.line(9.95, 4.57, 8.67, 4.02, COLORS["red"], width=1.6)
    s.line(6.74, 4.55, 6.74, 5.55, COLORS["purple"], width=1.6)
    chips = [
        ("HTTP", COLORS["blue"]),
        ("消息", COLORS["cyan"]),
        ("网络通信", COLORS["green"]),
        ("数据库", COLORS["purple"]),
        ("文件", COLORS["amber"]),
        ("函数库调用", COLORS["red"]),
    ]
    for i, (txt, c) in enumerate(chips):
        pill(s, 1.05 + i * 1.87, 6.58, txt, c)
    return s


def build_slides() -> list[Slide]:
    return [
        add_cover(),
        add_architecture(),
        add_composition(),
        add_layered(),
        add_execution_flow(),
        add_waveform_workflow(),
        add_sequence(),
        add_memory_loop(),
        add_interface_map(),
    ]


def presentation_xml(slide_count: int) -> str:
    slide_ids = "\n".join(
        f'<p:sldId id="{256 + i}" r:id="rId{i + 2}"/>' for i in range(1, slide_count + 1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>{slide_ids}</p:sldIdLst>
  <p:sldSz cx="{SLIDE_CX}" cy="{SLIDE_CY}" type="wide"/>
  <p:notesSz cx="6858000" cy="9144000"/>
  <p:defaultTextStyle><a:defPPr><a:defRPr lang="zh-CN"><a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/></a:defRPr></a:defPPr></p:defaultTextStyle>
</p:presentation>'''


def presentation_rels(slide_count: int) -> str:
    rels = [
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
    ]
    for i in range(1, slide_count + 1):
        rels.append(
            f'<Relationship Id="rId{i + 2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  {''.join(rels)}
</Relationships>'''


def content_types(slide_count: int) -> str:
    slide_overrides = "\n".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, slide_count + 1)
    )
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
  {slide_overrides}
</Types>'''


def static_parts(slide_count: int) -> dict[str, str]:
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    return {
        "[Content_Types].xml": content_types(slide_count),
        "_rels/.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>''',
        "docProps/core.xml": f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>LD智能体架构流程图组</dc:title>
  <dc:creator>Codex</dc:creator>
  <cp:lastModifiedBy>Codex</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
  <dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>''',
        "docProps/app.xml": f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>Microsoft PowerPoint</Application>
  <PresentationFormat>On-screen Show (16:9)</PresentationFormat>
  <Slides>{slide_count}</Slides>
  <Company></Company>
</Properties>''',
        "ppt/presentation.xml": presentation_xml(slide_count),
        "ppt/_rels/presentation.xml.rels": presentation_rels(slide_count),
        "ppt/slideMasters/slideMaster1.xml": f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
  <p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>''',
        "ppt/slideMasters/_rels/slideMaster1.xml.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>''',
        "ppt/slideLayouts/slideLayout1.xml": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr></p:spTree></p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>''',
        "ppt/slideLayouts/_rels/slideLayout1.xml.rels": '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>''',
        "ppt/theme/theme1.xml": f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="LD Agent Theme">
  <a:themeElements>
    <a:clrScheme name="LD Agent">
      <a:dk1><a:srgbClr val="{COLORS['ink']}"/></a:dk1><a:lt1><a:srgbClr val="{COLORS['white']}"/></a:lt1>
      <a:dk2><a:srgbClr val="{COLORS['black']}"/></a:dk2><a:lt2><a:srgbClr val="{COLORS['bg']}"/></a:lt2>
      <a:accent1><a:srgbClr val="{COLORS['blue']}"/></a:accent1><a:accent2><a:srgbClr val="{COLORS['cyan']}"/></a:accent2>
      <a:accent3><a:srgbClr val="{COLORS['green']}"/></a:accent3><a:accent4><a:srgbClr val="{COLORS['amber']}"/></a:accent4>
      <a:accent5><a:srgbClr val="{COLORS['purple']}"/></a:accent5><a:accent6><a:srgbClr val="{COLORS['red']}"/></a:accent6>
      <a:hlink><a:srgbClr val="{COLORS['blue']}"/></a:hlink><a:folHlink><a:srgbClr val="{COLORS['purple']}"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="LD Agent Fonts"><a:majorFont><a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/><a:cs typeface="{FONT}"/></a:majorFont><a:minorFont><a:latin typeface="{FONT}"/><a:ea typeface="{FONT}"/><a:cs typeface="{FONT}"/></a:minorFont></a:fontScheme>
    <a:fmtScheme name="LD Agent Format"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
  </a:themeElements>
</a:theme>''',
    }


def write_pptx(slides: list[Slide]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUT_PPTX, "w", ZIP_DEFLATED) as z:
        for path, content in static_parts(len(slides)).items():
            z.writestr(path, content)
        for i, slide in enumerate(slides, start=1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide.render(i, len(slides)))
            z.writestr(
                f"ppt/slides/_rels/slide{i}.xml.rels",
                '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
</Relationships>''',
            )


def main() -> None:
    slides = build_slides()
    write_pptx(slides)
    print(OUT_PPTX)
    print(f"slides={len(slides)}")


if __name__ == "__main__":
    main()
