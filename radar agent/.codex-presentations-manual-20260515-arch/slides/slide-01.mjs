const C = {
  ink: "#0B2C69",
  blue: "#173E82",
  blue2: "#0E5CB2",
  green: "#2F7D36",
  line: "#AFC6E8",
  line2: "#D8E4F5",
  online: "#EAF3FC",
  evolution: "#EFF8F0",
  platform: "#F1ECFA",
  white: "#FFFFFF",
  text: "#10233F",
  muted: "#50617A",
  grid: "#E9EEF7",
};

function shape(slide, ctx, x, y, w, h, fill, line = C.line, width = 1, geometry = "rect", name) {
  return ctx.addShape(slide, {
    x,
    y,
    width: w,
    height: h,
    geometry,
    fill,
    line: { fill: line, width, style: "solid" },
    name,
  });
}

function text(slide, ctx, value, x, y, w, h, opts = {}) {
  return ctx.addText(slide, {
    text: value,
    x,
    y,
    width: w,
    height: h,
    fontSize: opts.size ?? 18,
    bold: opts.bold ?? false,
    color: opts.color ?? C.text,
    typeface: opts.face ?? "Microsoft YaHei",
    align: opts.align ?? "center",
    valign: opts.valign ?? "middle",
    fill: opts.fill ?? "#00000000",
    line: opts.line ?? { fill: "#00000000", width: 0, style: "solid" },
    insets: opts.insets ?? { left: 2, right: 2, top: 2, bottom: 2 },
    name: opts.name,
  });
}

async function icon(slide, ctx, name, x, y, size = 18, color = C.blue2) {
  try {
    await ctx.addLucideIcon(slide, {
      name,
      icon: name,
      x,
      y,
      width: size,
      height: size,
      color,
      strokeWidth: 2.1,
      fit: "contain",
    });
  } catch {
    shape(slide, ctx, x + 2, y + 2, size - 4, size - 4, "#00000000", color, 1.8, "ellipse");
  }
}

async function moduleBox(slide, ctx, { label, iconName, x, y, w = 128, h = 46, iconColor = C.blue2, fontSize = 15 }) {
  shape(slide, ctx, x, y, w, h, C.white, C.line, 1.15, "roundRect");
  await icon(slide, ctx, iconName, x + 16, y + 14, 18, iconColor);
  text(slide, ctx, label, x + 39, y + 6, w - 44, h - 12, {
    size: fontSize,
    color: C.text,
    align: "left",
  });
}

function rowShell(slide, ctx, y, h = 72) {
  shape(slide, ctx, 240, y, 920, h, "#FFFFFFD9", C.line, 1.1, "roundRect");
}

function domain(slide, ctx, label, x, w, fill, color) {
  shape(slide, ctx, x, 92, w, 48, fill, C.line, 1.1, "rect");
  text(slide, ctx, label, x, 102, w, 26, { size: 16, bold: true, color });
  shape(slide, ctx, x, 140, w, 372, fill + "66", "#D7E2F1", 0.75, "rect");
}

function layerLabel(slide, ctx, n, label, y) {
  shape(slide, ctx, 50, y, 132, 60, C.white, C.blue, 1.3, "rect");
  shape(slide, ctx, 50, y, 32, 60, C.blue, C.blue, 0, "rect");
  text(slide, ctx, String(n), 50, y + 14, 32, 30, { size: 17, bold: true, color: C.white });
  text(slide, ctx, label, 84, y + 8, 94, 44, { size: 15, bold: true, color: C.ink });
}

function vText(slide, ctx, value, x, y, w, h, color) {
  text(slide, ctx, value.split("").join("\n"), x, y, w, h, {
    size: 16,
    bold: true,
    color,
    insets: { left: 0, right: 0, top: 0, bottom: 0 },
  });
}

function arrowLine(slide, ctx, x1, y1, x2, y2, color, width = 3) {
  if (Math.abs(y1 - y2) < 1) {
    shape(slide, ctx, Math.min(x1, x2), y1 - width / 2, Math.abs(x2 - x1), width, color, color, 0, "rect");
  } else {
    shape(slide, ctx, x1 - width / 2, Math.min(y1, y2), width, Math.abs(y2 - y1), color, color, 0, "rect");
  }
}

function arrowHead(slide, ctx, x, y, direction, color) {
  const tri = shape(slide, ctx, x - 8, y - 8, 16, 16, color, color, 0, "triangle");
  if (direction === "right") tri.rotation = 90;
  if (direction === "left") tri.rotation = 270;
  if (direction === "up") tri.rotation = 0;
  if (direction === "down") tri.rotation = 180;
}

function divider(slide, ctx, x) {
  shape(slide, ctx, x, 552, 1, 42, C.line2, C.line2, 0, "rect");
}

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();

  shape(slide, ctx, 0, 0, 1280, 720, "#FCFDFF", "#FCFDFF", 0);

  text(slide, ctx, "系统软件总体架构设计", 340, 24, 600, 48, {
    size: 32,
    bold: true,
    color: C.ink,
  });

  domain(slide, ctx, "在线运行域", 240, 310, C.online, C.ink);
  domain(slide, ctx, "能力生成演进域", 550, 310, C.evolution, "#1F6B2A");
  domain(slide, ctx, "平台协同保障域", 860, 300, C.platform, "#24146E");

  [160, 256, 352, 448].forEach((y) => rowShell(slide, ctx, y));
  layerLabel(slide, ctx, 4, "应用交互层", 166);
  layerLabel(slide, ctx, 3, "业务能力\n服务层", 262);
  layerLabel(slide, ctx, 2, "数据与通信\n支撑层", 358);
  layerLabel(slide, ctx, 1, "基础资源层", 454);

  await moduleBox(slide, ctx, { label: "态势显示", iconName: "monitor", x: 258, y: 174 });
  await moduleBox(slide, ctx, { label: "任务提交", iconName: "clipboard-list", x: 406, y: 174, iconColor: "#D98224" });
  await moduleBox(slide, ctx, { label: "智能研判", iconName: "brain", x: 572, y: 174, iconColor: "#E449A7" });
  await moduleBox(slide, ctx, { label: "处置确认", iconName: "check", x: 720, y: 174, iconColor: "#745BC6" });
  await moduleBox(slide, ctx, { label: "运维诊断", iconName: "stethoscope", x: 960, y: 174, w: 142, iconColor: C.blue2 });

  await moduleBox(slide, ctx, { label: "阵面控制", iconName: "radio-tower", x: 258, y: 270 });
  await moduleBox(slide, ctx, { label: "信息处理感知", iconName: "activity", x: 398, y: 270, w: 144, iconColor: "#FF7A21" });
  await moduleBox(slide, ctx, { label: "LD智能体", iconName: "bot", x: 572, y: 270 });
  await moduleBox(slide, ctx, { label: "智能显控", iconName: "panel-top", x: 720, y: 270 });
  await moduleBox(slide, ctx, { label: "能力生成演进", iconName: "chart-no-axes-combined", x: 858, y: 270, w: 144, iconColor: "#7F7BEA", fontSize: 14 });
  await moduleBox(slide, ctx, { label: "平台协同保障", iconName: "shield-check", x: 1012, y: 270, w: 142, fontSize: 14 });

  await moduleBox(slide, ctx, { label: "DDS/消息总线", iconName: "link", x: 258, y: 366, w: 160, iconColor: "#8A96A8" });
  await moduleBox(slide, ctx, { label: "HTTP/gRPC", iconName: "cloud", x: 438, y: 366, w: 140, iconColor: "#8A96A8" });
  await moduleBox(slide, ctx, { label: "WebSocket", iconName: "refresh-cw", x: 635, y: 366, w: 138, iconColor: C.blue });
  await moduleBox(slide, ctx, { label: "数据库", iconName: "database", x: 875, y: 366, w: 122, iconColor: "#008EC3" });
  await moduleBox(slide, ctx, { label: "文件/对象存储", iconName: "folder", x: 1008, y: 366, w: 146, iconColor: "#F4B51F" });

  await moduleBox(slide, ctx, { label: "计算资源", iconName: "server", x: 258, y: 462, w: 128, iconColor: "#42306B" });
  await moduleBox(slide, ctx, { label: "存储资源", iconName: "hard-drive", x: 412, y: 462, w: 128, iconColor: "#42306B" });
  await moduleBox(slide, ctx, { label: "网络资源", iconName: "globe-2", x: 635, y: 462, w: 138, iconColor: "#61B5FF" });
  await moduleBox(slide, ctx, { label: "时统资源", iconName: "clock", x: 960, y: 462, w: 142, iconColor: "#8A344B" });

  arrowLine(slide, ctx, 240, 194, 194, 194, C.blue, 3);
  arrowLine(slide, ctx, 194, 194, 194, 488, C.blue, 3);
  arrowLine(slide, ctx, 194, 488, 240, 488, C.blue, 3);
  arrowHead(slide, ctx, 240, 488, "right", C.blue);
  vText(slide, ctx, "在线运行闭环", 180, 292, 26, 140, C.blue);

  arrowLine(slide, ctx, 1160, 194, 1208, 194, "#245C24", 3);
  arrowHead(slide, ctx, 1160, 194, "left", "#245C24");
  arrowLine(slide, ctx, 1208, 194, 1208, 488, "#245C24", 3);
  arrowLine(slide, ctx, 1160, 488, 1208, 488, "#245C24", 3);
  arrowHead(slide, ctx, 1160, 488, "left", "#245C24");
  vText(slide, ctx, "能力生成演进闭环", 1213, 282, 32, 180, "#245C24");

  shape(slide, ctx, 134, 552, 1026, 70, C.white, C.line, 1.1, "roundRect");
  shape(slide, ctx, 50, 552, 74, 70, C.blue, C.blue, 0, "roundRect");
  text(slide, ctx, "横向\n治理", 55, 558, 46, 48, { size: 17, bold: true, color: C.white });
  await icon(slide, ctx, "shield", 88, 596, 16, "#6CCBFF");
  await icon(slide, ctx, "lock-keyhole", 252, 580, 18, "#F1B81B");
  text(slide, ctx, "安全门控", 280, 573, 100, 30, { size: 16, bold: true, color: C.text, align: "left" });
  divider(slide, ctx, 382);
  await icon(slide, ctx, "layers", 482, 580, 18, "#3DBD45");
  text(slide, ctx, "版本治理", 510, 573, 100, 30, { size: 16, bold: true, color: C.text, align: "left" });
  divider(slide, ctx, 608);
  await icon(slide, ctx, "search", 730, 580, 18, "#0976D8");
  text(slide, ctx, "观测审计", 758, 573, 100, 30, { size: 16, bold: true, color: C.text, align: "left" });
  divider(slide, ctx, 876);
  await icon(slide, ctx, "file-pen-line", 960, 580, 18, "#EB7D34");
  text(slide, ctx, "追溯记录", 988, 573, 100, 30, { size: 16, bold: true, color: C.text, align: "left" });

  return slide;
}
