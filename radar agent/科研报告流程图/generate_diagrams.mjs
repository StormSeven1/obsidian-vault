import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { writeFileSync } from "node:fs";

const outDir = dirname(fileURLToPath(import.meta.url));

const palette = {
  bg: "#f8fbff",
  grid: "#e6f0ff",
  blue50: "#eff6ff",
  blue100: "#dbeafe",
  blue200: "#bfdbfe",
  blue500: "#2563eb",
  blue700: "#1d4ed8",
  blue900: "#17376b",
  cyan50: "#ecfeff",
  cyan200: "#a5f3fc",
  slate: "#334155",
  gray: "#64748b",
  white: "#ffffff",
};

const diagrams = [
  {
    key: "01_agent整体架构设计图",
    width: 1600,
    height: 940,
    boxes: [
      { id: "in1", x: 70, y: 120, w: 230, h: 92, text: "显控任务\n人机交互输入", fill: palette.white },
      { id: "in2", x: 70, y: 250, w: 230, h: 92, text: "感知结果\n目标状态/异常评分", fill: palette.white },
      { id: "in3", x: 70, y: 380, w: 230, h: 92, text: "雷达状态\n资源/模式/参数版本", fill: palette.white },
      { id: "in4", x: 70, y: 510, w: 230, h: 92, text: "数据知识底座\n历史案例/专业知识", fill: palette.white },
      { id: "harness", x: 400, y: 90, w: 620, h: 560, text: "Agent Harness 运行底座\n任务生命周期、状态管理、能力路由、异常恢复、结果发布", fill: palette.blue50, group: true },
      { id: "task", x: 455, y: 185, w: 225, h: 72, text: "任务实例与状态机\n编号/对象/风险等级", fill: palette.white, parent: "harness" },
      { id: "ctx", x: 740, y: 185, w: 225, h: 72, text: "上下文工程\n证据选择/版本固化", fill: palette.white, parent: "harness" },
      { id: "llm", x: 455, y: 300, w: 225, h: 86, text: "LLM 推理引擎\n任务理解/证据解释/方案生成", fill: palette.cyan50, parent: "harness" },
      { id: "skills", x: 740, y: 300, w: 225, h: 86, text: "雷达 Skills 能力包\n研判/调度/波形/复盘", fill: palette.cyan50, parent: "harness" },
      { id: "tool", x: 455, y: 435, w: 225, h: 82, text: "工具调用\n查询/计算/仿真/校验", fill: palette.white, parent: "harness" },
      { id: "flow", x: 740, y: 435, w: 225, h: 82, text: "工作流门控\n边界校验/人工确认/回滚", fill: palette.white, parent: "harness" },
      { id: "trace", x: 510, y: 555, w: 400, h: 62, text: "追溯记录与评估治理\n输入、上下文、工具、流程、输出全链路记录", fill: palette.blue100, parent: "harness" },
      { id: "out1", x: 1130, y: 125, w: 260, h: 72, text: "当前环境目标研判\n证据链/置信度/不确定性", fill: palette.white },
      { id: "out2", x: 1130, y: 230, w: 260, h: 72, text: "调度与波形候选方案\n依据/约束/预期效果", fill: palette.white },
      { id: "out3", x: 1130, y: 335, w: 260, h: 72, text: "补证与仿真请求\n只读分析/效果估计", fill: palette.white },
      { id: "out4", x: 1130, y: 440, w: 260, h: 72, text: "受控流程请求\n参数设置/请求适配", fill: palette.white },
      { id: "out5", x: 1130, y: 545, w: 260, h: 72, text: "经验回流\n复盘结论/长期资产", fill: palette.white },
      { id: "ctrl", x: 720, y: 735, w: 360, h: 78, text: "控制执行链路\n真实控制下发与执行反馈", fill: palette.blue100 },
      { id: "display", x: 1120, y: 735, w: 260, h: 78, text: "显控展示\n解释、确认、反馈", fill: palette.blue100 },
    ],
    arrows: [
      ["in1", "task"], ["in2", "task"], ["in3", "ctx"], ["in4", "ctx"],
      ["task", "llm"], ["ctx", "llm"], ["llm", "skills"], ["skills", "tool"], ["skills", "flow"],
      ["tool", "trace"], ["flow", "trace"], ["trace", "ctx"],
      ["llm", "out1"], ["skills", "out2"], ["tool", "out3"], ["flow", "out4"], ["trace", "out5"],
      ["out4", "ctrl"], ["ctrl", "display"], ["display", "in1"],
    ],
  },
  {
    key: "02_harness任务运行机制图",
    width: 1600,
    height: 760,
    boxes: [
      { id: "a", x: 70, y: 270, w: 150, h: 84, text: "触发接入\n指令/事件/告警", fill: palette.white },
      { id: "b", x: 265, y: 270, w: 170, h: 84, text: "任务实例化\n编号/对象/窗口", fill: palette.white },
      { id: "c", x: 480, y: 270, w: 170, h: 84, text: "上下文装载\n证据/约束/版本", fill: palette.white },
      { id: "d", x: 695, y: 270, w: 170, h: 84, text: "能力路由\n只读/工具/工作流", fill: palette.white },
      { id: "e", x: 910, y: 270, w: 170, h: 84, text: "模型与 Skills\n推理/生成/校验", fill: palette.cyan50 },
      { id: "f", x: 1125, y: 270, w: 170, h: 84, text: "工具/流程执行\n查询/仿真/确认", fill: palette.white },
      { id: "g", x: 1340, y: 270, w: 170, h: 84, text: "结果发布\n展示/请求/记录", fill: palette.white },
      { id: "s1", x: 250, y: 110, w: 1080, h: 70, text: "横向运行治理：状态管理、上下文版本控制、权限约束、超时重试、异常恢复", fill: palette.blue50 },
      { id: "s2", x: 250, y: 500, w: 1080, h: 70, text: "全过程观测追溯：模型输入输出、工具结果、工作流节点、人工反馈、评估指标", fill: palette.blue50 },
      { id: "loop", x: 655, y: 610, w: 260, h: 58, text: "归档复盘与记忆回流\n短期 -> 中期 -> 长期", fill: palette.blue100 },
    ],
    arrows: [
      ["a", "b"], ["b", "c"], ["c", "d"], ["d", "e"], ["e", "f"], ["f", "g"],
      ["g", "loop"], ["loop", "c"],
      ["s1", "d"], ["e", "s2"], ["f", "s2"],
    ],
  },
  {
    key: "03_上下文工程证据组织图",
    width: 1600,
    height: 900,
    boxes: [
      { id: "src1", x: 80, y: 95, w: 230, h: 76, text: "当前任务上下文\n目标/区域/时间窗口", fill: palette.white },
      { id: "src2", x: 80, y: 205, w: 230, h: 76, text: "感知证据\n检测/识别/跟踪/定位", fill: palette.white },
      { id: "src3", x: 80, y: 315, w: 230, h: 76, text: "状态与约束\n模式/资源/参数边界", fill: palette.white },
      { id: "src4", x: 80, y: 425, w: 230, h: 76, text: "知识与经验\n案例/策略/专业规则", fill: palette.white },
      { id: "src5", x: 80, y: 535, w: 230, h: 76, text: "输出约束\n结论/方案/补证/流程", fill: palette.white },
      { id: "asm", x: 460, y: 190, w: 300, h: 330, text: "上下文装配器\n\n证据选择\n质量标识\n约束注入\n版本固化", fill: palette.blue50 },
      { id: "q", x: 455, y: 590, w: 310, h: 75, text: "质量标签\n缺失 / 冲突 / 过期 / 低置信 / 版本不一致", fill: palette.blue100 },
      { id: "pkg", x: 915, y: 125, w: 330, h: 420, text: "任务上下文包\n\n1 当前任务层\n2 状态约束层\n3 知识经验层\n4 输出约束层", fill: palette.white },
      { id: "llm", x: 1010, y: 650, w: 245, h: 88, text: "LLM + 雷达 Skills\n基于证据推理", fill: palette.cyan50 },
      { id: "out", x: 1340, y: 640, w: 205, h: 108, text: "结构化输出\n事实 / 判断 / 依据\n风险 / 不确定性", fill: palette.white },
    ],
    arrows: [
      ["src1", "asm"], ["src2", "asm"], ["src3", "asm"], ["src4", "asm"], ["src5", "asm"],
      ["asm", "q"], ["asm", "pkg"], ["q", "pkg"], ["pkg", "llm"], ["llm", "out"], ["out", "q"],
    ],
  },
  {
    key: "04_skills工作流记忆演进图",
    width: 1600,
    height: 960,
    boxes: [
      { id: "skill", x: 110, y: 120, w: 280, h: 250, text: "雷达 Skills 能力包\n\n目标研判 Skill\n波形参数推荐 Skill\n智能调度 Skill\n复盘生成 Skill\n质量检查规则", fill: palette.blue50 },
      { id: "reason", x: 520, y: 145, w: 250, h: 92, text: "推理\n任务理解/证据解释", fill: palette.cyan50 },
      { id: "tool", x: 860, y: 145, w: 250, h: 92, text: "工具调用\n查询/计算/仿真/校验", fill: palette.white },
      { id: "observe", x: 690, y: 300, w: 250, h: 92, text: "观察反馈\n工具结果/证据补充", fill: palette.white },
      { id: "plan", x: 520, y: 475, w: 250, h: 96, text: "候选方案包\n参数/依据/风险/回滚", fill: palette.cyan50 },
      { id: "wf1", x: 860, y: 465, w: 190, h: 82, text: "边界校验\n约束检查", fill: palette.white },
      { id: "wf2", x: 1090, y: 465, w: 190, h: 82, text: "仿真评估\n效果估计", fill: palette.white },
      { id: "wf3", x: 1320, y: 465, w: 190, h: 82, text: "人工确认\n请求适配", fill: palette.white },
      { id: "trace", x: 705, y: 665, w: 295, h: 76, text: "追溯与评估\n任务轨迹/工具轨迹/质量评分", fill: palette.blue100 },
      { id: "m1", x: 180, y: 770, w: 240, h: 72, text: "短期记忆\n当前任务上下文", fill: palette.white },
      { id: "m2", x: 550, y: 770, w: 240, h: 72, text: "中期记忆\n近期任务链/目标状态", fill: palette.white },
      { id: "m3", x: 920, y: 770, w: 240, h: 72, text: "长期经验资产\n案例/策略/复盘结论", fill: palette.white },
      { id: "gov", x: 1230, y: 750, w: 240, h: 112, text: "经验治理\n记录-评估-抽取\n确认-复用", fill: palette.blue50 },
    ],
    arrows: [
      ["skill", "reason"], ["reason", "tool"], ["tool", "observe"], ["observe", "reason"],
      ["reason", "plan"], ["plan", "wf1"], ["wf1", "wf2"], ["wf2", "wf3"], ["wf3", "trace"],
      ["tool", "trace"], ["plan", "trace"], ["trace", "m1"], ["m1", "m2"], ["m2", "m3"], ["m3", "gov"], ["gov", "skill"],
    ],
  },
];

function esc(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function center(box) {
  return { x: box.x + box.w / 2, y: box.y + box.h / 2 };
}

function edgePoints(from, to) {
  const a = center(from);
  const b = center(to);
  const dx = b.x - a.x;
  const dy = b.y - a.y;
  if (Math.abs(dx) >= Math.abs(dy)) {
    return dx >= 0
      ? { x1: from.x + from.w, y1: a.y, x2: to.x, y2: b.y }
      : { x1: from.x, y1: a.y, x2: to.x + to.w, y2: b.y };
  }
  return dy >= 0
    ? { x1: a.x, y1: from.y + from.h, x2: b.x, y2: to.y }
    : { x1: a.x, y1: from.y, x2: b.x, y2: to.y + to.h };
}

function svgText(text, x, y, w, h, color = palette.blue900, size = 25) {
  const lines = String(text).split("\n");
  const lineHeight = size + 8;
  const total = (lines.length - 1) * lineHeight;
  const startY = y + h / 2 - total / 2;
  return `<text x="${x + w / 2}" y="${startY}" text-anchor="middle" dominant-baseline="middle" fill="${color}" font-size="${size}" font-family="Microsoft YaHei, SimHei, Arial, sans-serif" font-weight="600">${lines
    .map((line, idx) => `<tspan x="${x + w / 2}" dy="${idx === 0 ? 0 : lineHeight}">${esc(line)}</tspan>`)
    .join("")}</text>`;
}

function renderSvg(diagram) {
  const boxMap = Object.fromEntries(diagram.boxes.map((box) => [box.id, box]));
  const grid = [];
  for (let x = 0; x <= diagram.width; x += 80) {
    grid.push(`<line x1="${x}" y1="0" x2="${x}" y2="${diagram.height}" stroke="${palette.grid}" stroke-width="1" opacity="0.45"/>`);
  }
  for (let y = 0; y <= diagram.height; y += 80) {
    grid.push(`<line x1="0" y1="${y}" x2="${diagram.width}" y2="${y}" stroke="${palette.grid}" stroke-width="1" opacity="0.45"/>`);
  }
  const arrows = diagram.arrows.map(([fromId, toId]) => {
    const p = edgePoints(boxMap[fromId], boxMap[toId]);
    const midX = Math.abs(p.x1 - p.x2) > 180 ? (p.x1 + p.x2) / 2 : undefined;
    if (midX) {
      return `<path d="M ${p.x1} ${p.y1} L ${midX} ${p.y1} L ${midX} ${p.y2} L ${p.x2} ${p.y2}" fill="none" stroke="${palette.blue500}" stroke-width="3" marker-end="url(#arrow)" stroke-linejoin="round" opacity="0.9"/>`;
    }
    return `<line x1="${p.x1}" y1="${p.y1}" x2="${p.x2}" y2="${p.y2}" stroke="${palette.blue500}" stroke-width="3" marker-end="url(#arrow)" opacity="0.9"/>`;
  });
  const boxes = diagram.boxes.map((box) => {
    const strokeWidth = box.group ? 3 : 2.4;
    const labelSize = box.group ? 24 : box.w < 200 ? 21 : 23;
    return `<rect x="${box.x}" y="${box.y}" width="${box.w}" height="${box.h}" rx="${box.group ? 22 : 14}" fill="${box.fill}" stroke="${palette.blue500}" stroke-width="${strokeWidth}" filter="url(#softShadow)"/>
${svgText(box.text, box.x, box.y, box.w, box.h, palette.blue900, labelSize)}`;
  });
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${diagram.width}" height="${diagram.height}" viewBox="0 0 ${diagram.width} ${diagram.height}">
  <defs>
    <marker id="arrow" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto" markerUnits="strokeWidth">
      <path d="M2,2 L10,6 L2,10 Z" fill="${palette.blue500}"/>
    </marker>
    <filter id="softShadow" x="-8%" y="-12%" width="116%" height="128%">
      <feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1d4ed8" flood-opacity="0.13"/>
    </filter>
  </defs>
  <rect x="0" y="0" width="${diagram.width}" height="${diagram.height}" fill="${palette.bg}"/>
  ${grid.join("\n  ")}
  <rect x="30" y="30" width="${diagram.width - 60}" height="${diagram.height - 60}" rx="26" fill="none" stroke="${palette.blue200}" stroke-width="2"/>
  ${arrows.join("\n  ")}
  ${boxes.join("\n  ")}
</svg>
`;
}

function drawioStyle(box) {
  const base = [
    "rounded=1",
    "whiteSpace=wrap",
    "html=1",
    `fillColor=${box.fill}`,
    `strokeColor=${palette.blue500}`,
    `fontColor=${palette.blue900}`,
    "fontStyle=1",
    "fontSize=14",
    "shadow=1",
    "arcSize=8",
  ];
  if (box.group) base.push("container=1");
  return base.join(";");
}

function renderDrawioPage(diagram, index) {
  const ids = Object.fromEntries(diagram.boxes.map((box, i) => [box.id, `${index}_${i + 2}`]));
  const cells = [
    '<mxCell id="0"/>',
    '<mxCell id="1" parent="0"/>',
    ...diagram.boxes.map((box) => `<mxCell id="${ids[box.id]}" value="${esc(box.text).replaceAll("\n", "&#xa;")}" style="${drawioStyle(box)}" vertex="1" parent="1"><mxGeometry x="${box.x}" y="${box.y}" width="${box.w}" height="${box.h}" as="geometry"/></mxCell>`),
    ...diagram.arrows.map(([from, to], i) => `<mxCell id="${index}_e${i + 1}" value="" style="edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=${palette.blue500};strokeWidth=2;endArrow=block;endFill=1;" edge="1" parent="1" source="${ids[from]}" target="${ids[to]}"><mxGeometry relative="1" as="geometry"/></mxCell>`),
  ];
  return `<diagram name="${esc(diagram.key)}"><mxGraphModel dx="${diagram.width}" dy="${diagram.height}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="${diagram.width}" pageHeight="${diagram.height}" math="0" shadow="0"><root>${cells.join("")}</root></mxGraphModel></diagram>`;
}

for (const diagram of diagrams) {
  writeFileSync(join(outDir, `${diagram.key}.svg`), renderSvg(diagram), "utf8");
}

const drawio = `<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="drawio" version="26.0.0">${diagrams.map(renderDrawioPage).join("")}</mxfile>
`;
writeFileSync(join(outDir, "雷达智能体科研报告流程图.drawio"), drawio, "utf8");
