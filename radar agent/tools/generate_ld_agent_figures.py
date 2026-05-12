from __future__ import annotations

import math
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "LD智能体子系统技术方案配图"
SOURCE = OUT / "source"
SVG = OUT / "svg"
PNG = OUT / "png"
PREVIEW = OUT / "preview"

FONT = Path("C:/Windows/Fonts/NotoSansSC-VF.ttf")
FONT_BOLD = Path("C:/Windows/Fonts/simhei.ttf")


PALETTE = {
    "bg": "#fbfcfe",
    "ink": "#1f2937",
    "muted": "#64748b",
    "grid": "#e6ebf2",
    "blue": "#dbeafe",
    "blue_stroke": "#1f4e79",
    "teal": "#d8f3f0",
    "teal_stroke": "#2a7f7f",
    "green": "#e5f4df",
    "green_stroke": "#4f7d4a",
    "amber": "#fff1cc",
    "amber_stroke": "#b7791f",
    "purple": "#eee7ff",
    "purple_stroke": "#7353a4",
    "gray": "#f1f5f9",
    "gray_stroke": "#7b8794",
    "red": "#fde2e2",
    "red_stroke": "#b44747",
}


@dataclass
class Shape:
    id: str
    label: str
    x: int
    y: int
    w: int
    h: int
    fill: str = "gray"
    stroke: str | None = None
    kind: str = "round"
    font_size: int = 20
    bold: bool = False
    parent: str = "1"


@dataclass
class Edge:
    source: str
    target: str
    label: str = ""
    points: list[tuple[int, int]] = field(default_factory=list)
    dashed: bool = False
    bidir: bool = False
    color: str = "#52616f"


@dataclass
class Diagram:
    slug: str
    title: str
    caption: str
    width: int
    height: int
    shapes: list[Shape]
    edges: list[Edge]
    note: str = ""


def color(name: str) -> str:
    return PALETTE.get(name, name)


def stroke_for(shape: Shape) -> str:
    return color(shape.stroke or f"{shape.fill}_stroke") if shape.stroke or f"{shape.fill}_stroke" in PALETTE else PALETTE["gray_stroke"]


def wrap_label(label: str, max_chars: int) -> list[str]:
    lines: list[str] = []
    for part in label.split("\n"):
        part = part.strip()
        if not part:
            lines.append("")
            continue
        width = max(4, max_chars)
        lines.extend(textwrap.wrap(part, width=width, break_long_words=True, replace_whitespace=False) or [part])
    return lines


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    path = FONT_BOLD if bold and FONT_BOLD.exists() else FONT
    return ImageFont.truetype(str(path), size=size)


def text_size(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0], box[3] - box[1]


def draw_wrapped_text(draw: ImageDraw.ImageDraw, shape: Shape, scale: float = 1.0) -> None:
    fnt = font(max(12, int(shape.font_size * scale)), shape.bold)
    max_chars = max(4, int(shape.w / (shape.font_size * 0.9)))
    lines = wrap_label(shape.label, max_chars)
    line_h = int(shape.font_size * 1.35 * scale)
    total_h = len(lines) * line_h
    y = shape.y * scale + (shape.h * scale - total_h) / 2
    for line in lines:
        w, _ = text_size(draw, line, fnt)
        x = shape.x * scale + (shape.w * scale - w) / 2
        draw.text((x, y), line, fill=PALETTE["ink"], font=fnt)
        y += line_h


def center(shape: Shape) -> tuple[int, int]:
    return shape.x + shape.w // 2, shape.y + shape.h // 2


def edge_path(src: Shape, tgt: Shape, points: list[tuple[int, int]]) -> list[tuple[int, int]]:
    sx, sy = center(src)
    tx, ty = center(tgt)
    if points:
        return [(sx, sy), *points, (tx, ty)]
    if abs(sx - tx) > abs(sy - ty):
        return [(sx, sy), ((sx + tx) // 2, sy), ((sx + tx) // 2, ty), (tx, ty)]
    return [(sx, sy), (sx, (sy + ty) // 2), (tx, (sy + ty) // 2), (tx, ty)]


def clip_to_box(a: tuple[int, int], b: tuple[int, int], shape: Shape) -> tuple[int, int]:
    cx, cy = center(shape)
    dx, dy = b[0] - a[0], b[1] - a[1]
    if dx == 0 and dy == 0:
        return cx, cy
    hw, hh = shape.w / 2, shape.h / 2
    scale = min(hw / abs(dx) if dx else math.inf, hh / abs(dy) if dy else math.inf)
    return int(cx + dx * scale), int(cy + dy * scale)


def draw_arrow(draw: ImageDraw.ImageDraw, p1: tuple[float, float], p2: tuple[float, float], fill: str, scale: float) -> None:
    angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    size = 12 * scale
    pts = [
        p2,
        (p2[0] - size * math.cos(angle - math.pi / 6), p2[1] - size * math.sin(angle - math.pi / 6)),
        (p2[0] - size * math.cos(angle + math.pi / 6), p2[1] - size * math.sin(angle + math.pi / 6)),
    ]
    draw.polygon(pts, fill=fill)


def render_png(diagram: Diagram, path: Path) -> None:
    scale = 2
    img = Image.new("RGB", (diagram.width * scale, diagram.height * scale), PALETTE["bg"])
    draw = ImageDraw.Draw(img)
    title_font = font(30 * scale, True)
    draw.text((42 * scale, 28 * scale), diagram.title, fill=PALETTE["blue_stroke"], font=title_font)
    shape_by_id = {s.id: s for s in diagram.shapes}

    for e in diagram.edges:
        src, tgt = shape_by_id[e.source], shape_by_id[e.target]
        pts = edge_path(src, tgt, e.points)
        pts[0] = clip_to_box(pts[1], pts[0], src)
        pts[-1] = clip_to_box(pts[-2], pts[-1], tgt)
        sp = [(x * scale, y * scale) for x, y in pts]
        draw.line(sp, fill=e.color, width=3 * scale, joint="curve")
        draw_arrow(draw, sp[-2], sp[-1], e.color, scale)
        if e.bidir:
            draw_arrow(draw, sp[1], sp[0], e.color, scale)
        if e.label:
            mid = sp[len(sp) // 2]
            fnt = font(15 * scale)
            tw, th = text_size(draw, e.label, fnt)
            box = [mid[0] - tw / 2 - 7 * scale, mid[1] - th / 2 - 4 * scale, mid[0] + tw / 2 + 7 * scale, mid[1] + th / 2 + 4 * scale]
            draw.rounded_rectangle(box, radius=6 * scale, fill=PALETTE["bg"], outline="#d6dee8", width=1 * scale)
            draw.text((mid[0] - tw / 2, mid[1] - th / 2 - 1 * scale), e.label, fill=PALETTE["muted"], font=fnt)

    for s in diagram.shapes:
        x, y, w, h = [v * scale for v in (s.x, s.y, s.w, s.h)]
        fill = color(s.fill)
        stroke = stroke_for(s)
        if s.kind == "lane":
            draw.rounded_rectangle([x, y, x + w, y + h], radius=10 * scale, fill=fill, outline=stroke, width=2 * scale)
            draw.rectangle([x, y, x + w, y + 36 * scale], fill=stroke)
            fnt = font(17 * scale, True)
            draw.text((x + 14 * scale, y + 7 * scale), s.label.split("\n")[0], fill="white", font=fnt)
            rest = "\n".join(s.label.split("\n")[1:])
            if rest:
                ss = Shape(s.id, rest, s.x, s.y + 42, s.w, s.h - 42, s.fill, s.stroke, "round", s.font_size, s.bold)
                draw_wrapped_text(draw, ss, scale)
        elif s.kind == "cylinder":
            draw.rounded_rectangle([x, y + 8 * scale, x + w, y + h], radius=8 * scale, fill=fill, outline=stroke, width=2 * scale)
            draw.ellipse([x, y, x + w, y + 18 * scale], fill=fill, outline=stroke, width=2 * scale)
            draw.arc([x, y + h - 20 * scale, x + w, y + h], 0, 180, fill=stroke, width=2 * scale)
            draw_wrapped_text(draw, s, scale)
        elif s.kind == "diamond":
            pts = [(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h), (x, y + h / 2)]
            draw.polygon(pts, fill=fill, outline=stroke)
            draw.line([*pts, pts[0]], fill=stroke, width=2 * scale)
            draw_wrapped_text(draw, s, scale)
        elif s.kind == "ellipse":
            draw.ellipse([x, y, x + w, y + h], fill=fill, outline=stroke, width=2 * scale)
            draw_wrapped_text(draw, s, scale)
        else:
            draw.rounded_rectangle([x, y, x + w, y + h], radius=10 * scale, fill=fill, outline=stroke, width=2 * scale)
            draw_wrapped_text(draw, s, scale)

    if diagram.note:
        fnt = font(18 * scale)
        draw.text((42 * scale, (diagram.height - 42) * scale), diagram.note, fill=PALETTE["muted"], font=fnt)
    img.save(path)


def svg_text(shape: Shape) -> str:
    max_chars = max(4, int(shape.w / (shape.font_size * 0.9)))
    lines = wrap_label(shape.label, max_chars)
    y = shape.y + (shape.h - len(lines) * shape.font_size * 1.25) / 2 + shape.font_size
    parts = []
    for line in lines:
        parts.append(f'<text x="{shape.x + shape.w / 2}" y="{y:.1f}" text-anchor="middle" font-size="{shape.font_size}" font-weight="{"700" if shape.bold else "400"}" fill="{PALETTE["ink"]}">{escape(line)}</text>')
        y += shape.font_size * 1.25
    return "\n".join(parts)


def render_svg(diagram: Diagram, path: Path) -> None:
    shape_by_id = {s.id: s for s in diagram.shapes}
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{diagram.width}" height="{diagram.height}" viewBox="0 0 {diagram.width} {diagram.height}">',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#52616f"/></marker><filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#1f2937" flood-opacity="0.12"/></filter></defs>',
        f'<rect width="100%" height="100%" fill="{PALETTE["bg"]}"/>',
        f'<text x="42" y="58" font-size="30" font-weight="700" fill="{PALETTE["blue_stroke"]}">{escape(diagram.title)}</text>',
    ]
    for e in diagram.edges:
        src, tgt = shape_by_id[e.source], shape_by_id[e.target]
        pts = edge_path(src, tgt, e.points)
        pts[0] = clip_to_box(pts[1], pts[0], src)
        pts[-1] = clip_to_box(pts[-2], pts[-1], tgt)
        d = "M " + " L ".join(f"{x},{y}" for x, y in pts)
        dash = ' stroke-dasharray="8 6"' if e.dashed else ""
        marker_start = ' marker-start="url(#arrow)"' if e.bidir else ""
        out.append(f'<path d="{d}" fill="none" stroke="{e.color}" stroke-width="3" stroke-linejoin="round" marker-end="url(#arrow)"{marker_start}{dash}/>')
        if e.label:
            mx, my = pts[len(pts) // 2]
            out.append(f'<rect x="{mx - 68}" y="{my - 16}" width="136" height="28" rx="7" fill="{PALETTE["bg"]}" stroke="#d6dee8"/>')
            out.append(f'<text x="{mx}" y="{my + 5}" text-anchor="middle" font-size="15" fill="{PALETTE["muted"]}">{escape(e.label)}</text>')
    for s in diagram.shapes:
        fill, stroke = color(s.fill), stroke_for(s)
        if s.kind == "lane":
            out.append(f'<rect x="{s.x}" y="{s.y}" width="{s.w}" height="{s.h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#shadow)"/>')
            out.append(f'<rect x="{s.x}" y="{s.y}" width="{s.w}" height="36" rx="10" fill="{stroke}"/>')
            out.append(f'<text x="{s.x + 14}" y="{s.y + 24}" font-size="17" font-weight="700" fill="#fff">{escape(s.label.split(chr(10))[0])}</text>')
            rest = "\n".join(s.label.split("\n")[1:])
            if rest:
                out.append(svg_text(Shape(s.id, rest, s.x, s.y + 42, s.w, s.h - 42, s.fill, s.stroke, "round", s.font_size, s.bold)))
        elif s.kind == "cylinder":
            out.append(f'<rect x="{s.x}" y="{s.y + 8}" width="{s.w}" height="{s.h - 8}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#shadow)"/>')
            out.append(f'<ellipse cx="{s.x + s.w / 2}" cy="{s.y + 9}" rx="{s.w / 2}" ry="9" fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
            out.append(svg_text(s))
        elif s.kind == "diamond":
            pts = f'{s.x + s.w / 2},{s.y} {s.x + s.w},{s.y + s.h / 2} {s.x + s.w / 2},{s.y + s.h} {s.x},{s.y + s.h / 2}'
            out.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#shadow)"/>')
            out.append(svg_text(s))
        elif s.kind == "ellipse":
            out.append(f'<ellipse cx="{s.x + s.w / 2}" cy="{s.y + s.h / 2}" rx="{s.w / 2}" ry="{s.h / 2}" fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#shadow)"/>')
            out.append(svg_text(s))
        else:
            out.append(f'<rect x="{s.x}" y="{s.y}" width="{s.w}" height="{s.h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#shadow)"/>')
            out.append(svg_text(s))
    if diagram.note:
        out.append(f'<text x="42" y="{diagram.height - 42}" font-size="18" fill="{PALETTE["muted"]}">{escape(diagram.note)}</text>')
    out.append("</svg>")
    path.write_text("\n".join(out), encoding="utf-8")


def drawio_style(s: Shape) -> str:
    base = "whiteSpace=wrap;html=1;fontFamily=Noto Sans SC;fontSize=14;"
    fill, stroke = color(s.fill), stroke_for(s)
    if s.kind == "lane":
        return f"swimlane;startSize=30;rounded=1;html=1;fillColor={fill};strokeColor={stroke};fontColor=#ffffff;fontStyle=1;"
    if s.kind == "cylinder":
        return f"shape=cylinder3;boundedLbl=1;backgroundOutline=1;size=15;{base}fillColor={fill};strokeColor={stroke};"
    if s.kind == "diamond":
        return f"rhombus;{base}fillColor={fill};strokeColor={stroke};"
    if s.kind == "ellipse":
        return f"ellipse;{base}fillColor={fill};strokeColor={stroke};"
    return f"rounded=1;arcSize=10;{base}fillColor={fill};strokeColor={stroke};fontStyle={'1' if s.bold else '0'};"


def render_drawio(diagram: Diagram, path: Path) -> None:
    cells = ['<mxCell id="0" />', '<mxCell id="1" parent="0" />']
    for s in diagram.shapes:
        value = escape(s.label).replace("\n", "&#xa;")
        cells.append(
            f'<mxCell id="{s.id}" value="{value}" style="{drawio_style(s)}" vertex="1" parent="{s.parent}">'
            f'<mxGeometry x="{s.x}" y="{s.y}" width="{s.w}" height="{s.h}" as="geometry" /></mxCell>'
        )
    eid = 1000
    for e in diagram.edges:
        style = f"edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor={e.color};endArrow=block;"
        if e.bidir:
            style += "startArrow=block;"
        if e.dashed:
            style += "dashed=1;"
        value = escape(e.label)
        if e.points:
            points = "".join(f'<mxPoint x="{x}" y="{y}" />' for x, y in e.points)
            geom = f'<mxGeometry relative="1" as="geometry"><Array as="points">{points}</Array></mxGeometry>'
        else:
            geom = '<mxGeometry relative="1" as="geometry" />'
        cells.append(f'<mxCell id="{eid}" value="{value}" style="{style}" edge="1" parent="1" source="{e.source}" target="{e.target}">{geom}</mxCell>')
        eid += 1
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<mxfile host="drawio" version="26.0.0">\n'
        f'  <diagram name="{escape(diagram.caption)}">\n'
        f'    <mxGraphModel dx="1600" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{diagram.width}" pageHeight="{diagram.height}" math="0" shadow="0">\n'
        "      <root>\n        "
        + "\n        ".join(cells)
        + "\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n"
    )
    path.write_text(xml, encoding="utf-8")


def diagrams() -> list[Diagram]:
    ds: list[Diagram] = []

    ds.append(Diagram(
        "00A_智能推理分系统总体闭环图",
        "图A 智能推理分系统总体闭环图",
        "图A 智能推理分系统总体闭环图",
        1600,
        980,
        [
            Shape("a1", "多源触发\n显控请求 / 感知事件 / 状态告警", 90, 220, 260, 110, "blue", bold=True),
            Shape("a2", "任务实例与上下文装载\n目标/区域/风险/证据", 420, 150, 300, 110, "teal", bold=True),
            Shape("a3", "认知推理与路径规划\nLLM + PLA/ReAct + Skills", 790, 150, 320, 110, "purple", bold=True),
            Shape("a4", "受控工具与工作流\n查询 / 仿真 / 审批 / 回滚", 1180, 220, 300, 120, "amber", bold=True),
            Shape("a5", "结果反馈与人机协同\n研判摘要 / 参数候选 / 风险提示", 1040, 560, 320, 120, "green", bold=True),
            Shape("a6", "三阶分层记忆与经验演进\n短期上下文 / 中期任务链 / 长期经验", 540, 620, 390, 130, "blue", bold=True),
            Shape("a7", "安全门控与追溯治理\n权限 / 参数边界 / 证据引用 / 审计回放", 560, 375, 450, 130, "red", bold=True),
        ],
        [
            Edge("a1", "a2"), Edge("a2", "a3"), Edge("a3", "a4"), Edge("a4", "a5"), Edge("a5", "a6"), Edge("a6", "a2"),
            Edge("a3", "a7", "约束"), Edge("a7", "a4", "门控"), Edge("a5", "a7", "追溯", dashed=True),
        ],
        "控制下发由控制执行链路完成，智能体侧输出研判、候选参数、工作流请求与追溯记录。",
    ))

    ds.append(Diagram(
        "00B_三类业务场景联动图",
        "图B 调度、波形参数设置与目标研判联动图",
        "图B 调度、波形参数设置与目标研判联动图",
        1600,
        920,
        [
            Shape("b1", "当前环境目标研判\n目标类别 / 行为特征 / 威胁等级 / 证据缺口", 110, 260, 330, 150, "blue", bold=True),
            Shape("b2", "智能雷达调度\n工作模式 / 波束资源 / 跟踪策略", 620, 150, 330, 145, "teal", bold=True),
            Shape("b3", "波形参数设置建议\n波形 / 门限 / 参数版本 / 回滚条件", 1110, 260, 330, 150, "amber", bold=True),
            Shape("b4", "LD智能体任务空间\n任务实例、上下文、证据链、能力包、追溯编号", 540, 430, 510, 150, "purple", bold=True),
            Shape("b5", "感知结果与雷达状态", 180, 620, 260, 100, "gray"),
            Shape("b6", "数据知识底座与历史经验", 650, 650, 300, 100, "green"),
            Shape("b7", "显控确认与控制执行链路", 1120, 620, 290, 100, "red"),
        ],
        [
            Edge("b1", "b4"), Edge("b2", "b4"), Edge("b3", "b4"), Edge("b4", "b1", "补证/解释"), Edge("b4", "b2", "资源约束"), Edge("b4", "b3", "候选方案"),
            Edge("b5", "b1"), Edge("b5", "b4"), Edge("b6", "b4"), Edge("b4", "b7", "审批请求"), Edge("b7", "b3", "执行回传"),
        ],
        "三类业务不是孤立能力，而是围绕同一任务实例共享证据、约束、候选方案和反馈结果。",
    ))

    ds.append(Diagram(
        "01_LD智能体子系统工作原理图",
        "图4.3.3.2-1 LD智能体子系统工作原理图",
        "图4.3.3.2-1 LD智能体子系统工作原理图",
        1700,
        980,
        [
            Shape("j1", "显控分系统\n自然语言/目标/区域/审批", 80, 180, 250, 105, "blue"),
            Shape("j2", "信息处理感知子系统\n检测/识别/跟踪/定位", 80, 330, 250, 105, "blue"),
            Shape("j3", "雷达状态与环境数据\n模式/参数/资源/环境", 80, 480, 250, 105, "blue"),
            Shape("j4", "数据知识底座\n关系/向量/图/时序", 80, 630, 250, 105, "green", kind="cylinder"),
            Shape("j5", "LD智能体子系统边界", 430, 130, 850, 690, "gray", "blue_stroke", "lane", 22, True),
            Shape("j6", "运行底座\n任务实例/上下文/能力包/追溯", 500, 210, 710, 90, "teal", bold=True),
            Shape("j7", "认知核心模块\n意图理解/推理规划/结果生成", 500, 350, 290, 105, "purple", bold=True),
            Shape("j8", "记忆管理模块\n短期/中期/长期经验", 920, 350, 290, 105, "blue", bold=True),
            Shape("j9", "工具执行模块\n工具代理/协议适配/监控", 500, 540, 290, 105, "amber", bold=True),
            Shape("j10", "工作流引擎模块\n模板/检查点/审批/回滚", 920, 540, 290, 105, "green", bold=True),
            Shape("j11", "数据库管理与接入模块\n关系/向量/图/时序统一访问", 650, 700, 410, 90, "gray", bold=True),
            Shape("j12", "控制执行链路\n波形/波束/门限/跟踪参数", 1400, 350, 250, 115, "red", bold=True),
            Shape("j13", "结果返回显控\n研判/候选方案/流程状态", 1400, 570, 250, 115, "green", bold=True),
        ],
        [
            Edge("j1", "j6"), Edge("j2", "j6"), Edge("j3", "j6"), Edge("j4", "j11"),
            Edge("j6", "j7"), Edge("j7", "j8", bidir=True), Edge("j7", "j9"), Edge("j7", "j10"), Edge("j9", "j11", bidir=True), Edge("j10", "j11", bidir=True), Edge("j8", "j11", bidir=True),
            Edge("j9", "j12", "经审批控制请求"), Edge("j12", "j9", "执行状态"), Edge("j6", "j13"), Edge("j10", "j13"), Edge("j7", "j13"),
        ],
    ))

    ds.append(Diagram(
        "02_LD智能体子系统执行信息流程图",
        "图4.3.3.2-2 LD智能体子系统执行信息流程图",
        "图4.3.3.2-2 LD智能体子系统执行信息流程图",
        1800,
        980,
        [
            Shape("p1", "任务触发\n显控/感知/状态告警", 80, 230, 230, 105, "blue", bold=True),
            Shape("p2", "创建任务实例\nID/来源/目标/风险", 380, 230, 230, 105, "teal", bold=True),
            Shape("p3", "上下文装载\n证据/状态/历史引用", 680, 230, 240, 105, "teal", bold=True),
            Shape("p4", "记忆检索与数据投影\n短期/中期/长期", 990, 230, 260, 105, "blue", bold=True),
            Shape("p5", "认知推理与路径选择", 1320, 230, 240, 105, "purple", bold=True),
            Shape("p6", "是否涉及控制\n或高风险动作", 1320, 470, 250, 130, "amber", "amber_stroke", "diamond", 22, True),
            Shape("p7", "只读研判/推荐生成\n工具调用与证据整合", 950, 650, 300, 110, "green", bold=True),
            Shape("p8", "受控执行流程\n校验/仿真/审批/回滚", 1320, 650, 300, 110, "red", bold=True),
            Shape("p9", "返回显控\n摘要/证据/方案/状态", 620, 650, 260, 110, "green", bold=True),
            Shape("p10", "追溯记录与记忆回流\n快照/工具/审批/反馈", 260, 650, 290, 110, "blue", bold=True),
        ],
        [
            Edge("p1", "p2"), Edge("p2", "p3"), Edge("p3", "p4"), Edge("p4", "p5"), Edge("p5", "p6"),
            Edge("p6", "p7", "否/低风险", [(1190, 535), (1100, 650)]), Edge("p6", "p8", "是/高风险"),
            Edge("p7", "p9"), Edge("p8", "p9"), Edge("p9", "p10"), Edge("p10", "p3", "连续任务复用", [(390, 560), (680, 560)]),
        ],
        "流程区分只读研判、推荐生成、受控执行三类模式；控制动作必须进入门控和工作流链路。",
    ))

    ds.append(Diagram(
        "03_LD智能体子系统组成图",
        "图4.3.3.2-3 LD智能体子系统组成图",
        "图4.3.3.2-3 LD智能体子系统组成图",
        1750,
        1050,
        [
            Shape("c1", "输入与触发\n显控交互 / 感知结果 / 雷达状态 / 外部知识", 80, 170, 330, 130, "blue", bold=True),
            Shape("c2", "运行底座\n任务实例管理、上下文装载、能力包调度、安全门控、运行观测、追溯记录", 500, 140, 780, 120, "teal", bold=True),
            Shape("c3", "认知核心模块\n意图理解\n任务建模\n推理规划\n结果生成", 160, 420, 250, 200, "purple", bold=True),
            Shape("c4", "记忆管理模块\n短期任务记忆\n中期任务链\n长期经验资产\n经验回流", 490, 420, 250, 200, "blue", bold=True),
            Shape("c5", "工具执行模块\n工具注册\n参数校验\n执行代理\n结果回填", 820, 420, 250, 200, "amber", bold=True),
            Shape("c6", "工作流引擎模块\n模板管理\n节点执行\n人工确认\n异常回滚", 1150, 420, 250, 200, "green", bold=True),
            Shape("c7", "数据库管理与接入模块\n关系数据 / 向量检索 / 图关系 / 时序数据 / 统一访问", 490, 730, 590, 130, "gray", bold=True),
            Shape("c8", "输出与联动\n研判结果 / 候选参数 / 审批请求 / 复盘报告 / 经验资产", 1330, 760, 330, 130, "green", bold=True),
        ],
        [
            Edge("c1", "c2"), Edge("c2", "c3"), Edge("c2", "c4"), Edge("c2", "c5"), Edge("c2", "c6"),
            Edge("c3", "c4", bidir=True), Edge("c3", "c5"), Edge("c3", "c6"), Edge("c6", "c5"),
            Edge("c4", "c7", bidir=True), Edge("c5", "c7", bidir=True), Edge("c6", "c7", bidir=True),
            Edge("c3", "c8"), Edge("c5", "c8"), Edge("c6", "c8"), Edge("c7", "c4", "经验支撑", dashed=True),
        ],
    ))

    ds.append(Diagram(
        "04_认知核心模块处理流程图",
        "图4.3.3.2-4 认知核心模块处理流程图",
        "图4.3.3.2-4 认知核心模块处理流程图",
        1650,
        860,
        [
            Shape("g1", "显控请求与感知事件", 80, 250, 240, 100, "blue", bold=True),
            Shape("g2", "意图理解\n任务类型/对象/约束", 390, 250, 230, 100, "teal", bold=True),
            Shape("g3", "任务建模\n目标/区域/时间窗口/风险", 690, 250, 260, 100, "teal", bold=True),
            Shape("g4", "上下文组织与证据链\n事实/模型判断/历史经验", 1020, 250, 300, 100, "blue", bold=True),
            Shape("g5", "执行路径规划\n动态研判 or 受控流程", 700, 480, 280, 110, "purple", bold=True),
            Shape("g6", "大语言模型推理引擎\nPLA / ReAct / 能力包约束", 1080, 480, 310, 110, "purple", bold=True),
            Shape("g7", "工具/工作流触发建议", 720, 675, 260, 95, "amber", bold=True),
            Shape("g8", "研判结论与候选方案生成", 1080, 675, 310, 95, "green", bold=True),
        ],
        [
            Edge("g1", "g2"), Edge("g2", "g3"), Edge("g3", "g4"), Edge("g4", "g6"),
            Edge("g3", "g5"), Edge("g5", "g6"), Edge("g5", "g7"), Edge("g6", "g8"), Edge("g7", "g8"),
        ],
        "认知核心负责理解、规划和建议生成，不直接承担真实控制下发。",
    ))

    ds.append(Diagram(
        "05_记忆管理模块流转图",
        "图4.3.3.2-5 记忆管理模块流转图",
        "图4.3.3.2-5 记忆管理模块流转图",
        1700,
        940,
        [
            Shape("m1", "当前任务上下文\n输入、目标、证据、工具结果", 110, 250, 310, 120, "blue", bold=True),
            Shape("m2", "短期记忆\n上下文版本/证据编号/临时状态", 520, 170, 300, 120, "teal", bold=True),
            Shape("m3", "中期任务链记忆\n连续交互/对象关联/阶段状态", 520, 380, 300, 120, "purple", bold=True),
            Shape("m4", "长期经验资产\n知识/案例/策略/经验片段", 520, 590, 300, 120, "green", bold=True),
            Shape("m5", "统一追溯记录\n输入/推理/调用/审批/反馈", 950, 380, 330, 130, "gray", bold=True),
            Shape("m6", "经验候选评估\n效果指标/冲突检查/人工确认", 1350, 290, 280, 120, "amber", bold=True),
            Shape("m7", "受控回流\n长期沉淀/版本标识/适用范围", 1350, 530, 280, 120, "red", bold=True),
        ],
        [
            Edge("m1", "m2"), Edge("m1", "m3"), Edge("m1", "m5"), Edge("m2", "m3"), Edge("m3", "m4"),
            Edge("m2", "m5"), Edge("m3", "m5"), Edge("m4", "m5"), Edge("m5", "m6"), Edge("m6", "m7"), Edge("m7", "m4"), Edge("m4", "m1", "召回支撑", [(360, 650), (260, 650)]),
        ],
        "长期经验只通过评估和受控回流形成，避免一次性任务记录被直接固化复用。",
    ))

    ds.append(Diagram(
        "06_工具执行模块时序图",
        "图4.3.3.2-6 工具执行模块时序图",
        "图4.3.3.2-6 工具执行模块时序图",
        1750,
        980,
        [
            Shape("s1", "运行底座", 80, 150, 260, 650, "teal", "teal_stroke", "lane", 22, True),
            Shape("s2", "认知核心模块", 380, 150, 260, 650, "purple", "purple_stroke", "lane", 22, True),
            Shape("s3", "安全门控组件", 680, 150, 260, 650, "red", "red_stroke", "lane", 22, True),
            Shape("s4", "工具执行模块", 980, 150, 260, 650, "amber", "amber_stroke", "lane", 22, True),
            Shape("s5", "工作流引擎", 1280, 150, 260, 650, "green", "green_stroke", "lane", 22, True),
            Shape("s6", "数据库 / 外部工具 / 控制适配", 980, 830, 560, 90, "gray", bold=True),
            Shape("t1", "1 生成执行计划", 390, 250, 230, 70, "purple", bold=True),
            Shape("t2", "2 权限、风险、参数边界检查", 690, 340, 230, 80, "red", bold=True),
            Shape("t3", "3 放行、阻断或补证", 990, 430, 230, 75, "amber", bold=True),
            Shape("t4", "4 调用查询、分析、仿真工具", 990, 560, 230, 80, "amber", bold=True),
            Shape("t5", "5 高风险任务进入流程", 1290, 430, 230, 75, "green", bold=True),
            Shape("t6", "6 流程节点调用原子工具", 1290, 560, 230, 80, "green", bold=True),
            Shape("t7", "7 标准化结果与证据编号", 390, 660, 230, 80, "blue", bold=True),
            Shape("t8", "8 结果发布与追溯写入", 90, 660, 230, 80, "teal", bold=True),
        ],
        [
            Edge("t1", "t2"), Edge("t2", "t3"), Edge("t3", "t4"), Edge("t3", "t5", "高风险"),
            Edge("t5", "t6"), Edge("t6", "t4", "节点调用"), Edge("t4", "s6", "工具执行/状态回传"),
            Edge("t4", "t7"), Edge("t7", "t8"),
        ],
        "时序图采用泳道式表达，强调工具执行模块提供原子能力，工作流引擎负责流程控制。",
    ))

    ds.append(Diagram(
        "07_LD智能体子系统接口关系图",
        "图4.3.3.2-7 LD智能体子系统接口关系图",
        "图4.3.3.2-7 LD智能体子系统接口关系图",
        1800,
        1020,
        [
            Shape("k1", "显控分系统", 80, 220, 220, 85, "blue", bold=True),
            Shape("k2", "信息处理感知子系统", 80, 350, 220, 85, "blue", bold=True),
            Shape("k3", "雷达状态与环境服务", 80, 480, 220, 85, "blue", bold=True),
            Shape("k4", "控制执行链路", 80, 610, 220, 85, "red", bold=True),
            Shape("k5", "数据知识底座", 80, 740, 220, 85, "green", kind="cylinder", bold=True),
            Shape("k6", "LD智能体子系统接口层", 420, 150, 930, 770, "gray", "blue_stroke", "lane", 21, True),
            Shape("k7", "外部接入接口", 500, 250, 230, 80, "teal", bold=True),
            Shape("k8", "任务管理接口", 820, 250, 230, 80, "teal", bold=True),
            Shape("k9", "认知核心接口", 820, 390, 230, 80, "purple", bold=True),
            Shape("k10", "记忆读写接口", 500, 530, 230, 80, "blue", bold=True),
            Shape("k11", "工具代理接口", 1140, 390, 230, 80, "amber", bold=True),
            Shape("k12", "工作流代理接口", 1140, 530, 230, 80, "green", bold=True),
            Shape("k13", "安全门控接口", 820, 660, 230, 80, "red", bold=True),
            Shape("k14", "追溯记录接口", 500, 760, 230, 80, "gray", bold=True),
            Shape("k15", "数据库接入接口", 1140, 760, 230, 80, "gray", bold=True),
            Shape("k16", "试验评估/样本/运维系统", 1460, 360, 260, 90, "green", bold=True),
        ],
        [
            Edge("k1", "k7", bidir=True), Edge("k2", "k7"), Edge("k3", "k7"), Edge("k4", "k11", bidir=True), Edge("k5", "k15", bidir=True),
            Edge("k7", "k8"), Edge("k8", "k9", bidir=True), Edge("k9", "k10", bidir=True), Edge("k9", "k11", bidir=True), Edge("k9", "k12"), Edge("k11", "k13"), Edge("k12", "k13"), Edge("k10", "k15", bidir=True), Edge("k11", "k15", bidir=True), Edge("k12", "k15", bidir=True),
            Edge("k8", "k14"), Edge("k9", "k14"), Edge("k10", "k14"), Edge("k11", "k14"), Edge("k12", "k14"), Edge("k14", "k16", bidir=True),
        ],
        "图中只表达接口关系和软件形态，端口、完整字段、错误码和报文结构留到接口控制文件细化。",
    ))
    return ds


def write_readme(ds: Iterable[Diagram]) -> None:
    rows = "\n".join(f"| {d.caption} | `{d.slug}.drawio` | `{d.slug}.svg` | `{d.slug}.png` |" for d in ds)
    readme = f"""# LD智能体子系统技术方案配图

本目录为 `4.3.3.2 LD智能体子系统技术方案.md` 配套生成可编辑工程图资产。

## 目录

- `source/`：draw.io 源文件，可在 diagrams.net/draw.io 中二次编辑。
- `svg/`：Word 推荐插入格式，缩放清晰。
- `png/`：Word 兼容格式，按 2 倍分辨率导出。
- `preview/`：预留给后续人工预览、批注或拼图检查使用。

## 文件清单

| 图名 | draw.io源文件 | SVG | PNG |
| --- | --- | --- | --- |
{rows}

## 插入建议

- `图A` 建议放在 4.3.3.2.1 概述之后，作为智能推理分系统总览图。
- `图B` 建议放在业务能力描述之后，支撑“当前环境目标研判、智能雷达调度、波形参数设置”三类能力说明。
- `图4.3.3.2-1` 至 `图4.3.3.2-7` 可替换正文中同编号 Mermaid 图。

## 后续编辑与 Visio 转换

1. 使用 diagrams.net/draw.io 打开 `source/*.drawio`，文本、节点和连线均可编辑。
2. Word 中优先插入 `svg/*.svg`；如目标环境对 SVG 支持不好，插入 `png/*.png`。
3. 转 Visio 时优先从 draw.io 打开 `.drawio` 后导出 SVG/PDF，再在 Visio 中插入或重构；复杂接口图建议保留 `.drawio` 作为主源文件。

## 生成说明

当前本机未检测到 draw.io Desktop CLI，因此本批次未使用 draw.io CLI 导出。`.drawio`、`.svg`、`.png` 由同一套图元数据生成，内容保持一致。
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    for d in [OUT, SOURCE, SVG, PNG, PREVIEW]:
        d.mkdir(parents=True, exist_ok=True)
    ds = diagrams()
    for d in ds:
        render_drawio(d, SOURCE / f"{d.slug}.drawio")
        render_svg(d, SVG / f"{d.slug}.svg")
        render_png(d, PNG / f"{d.slug}.png")
    write_readme(ds)


if __name__ == "__main__":
    main()
