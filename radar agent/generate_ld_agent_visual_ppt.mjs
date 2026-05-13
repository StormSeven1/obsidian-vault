import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const root = 'D:/knowledge/radar agent';
const skillRoot = `${process.env.USERPROFILE}/.codex/skills/guizang-ppt-skill`.replaceAll('\\', '/');
const templatePath = `${skillRoot}/assets/template-swiss.html`;
const outDir = join(root, 'LD智能体科研报告PPT');
const imagesDir = join(outDir, 'images');
const outPath = join(outDir, 'index.html');
mkdirSync(imagesDir, { recursive: true });

const W = 2100;
const H = 900;
const ink = '#0a0a0a';
const paper = '#fafaf8';
const grey1 = '#f0f0ee';
const grey2 = '#d4d4d2';
const grey3 = '#737373';
const accent = '#002FA7';

function esc(s) {
  return String(s).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

function text(x, y, content, size = 34, color = ink, weight = 300, attrs = '') {
  return `<text x="${x}" y="${y}" fill="${color}" font-size="${size}" font-weight="${weight}" ${attrs}>${esc(content)}</text>`;
}

function rect(x, y, w, h, fill = 'none', stroke = grey2, sw = 2, attrs = '') {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" stroke="${stroke}" stroke-width="${sw}" ${attrs}/>`;
}

function line(x1, y1, x2, y2, color = grey2, sw = 2, attrs = '') {
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="${sw}" ${attrs}/>`;
}

function arrow(x1, y1, x2, y2, color = accent) {
  return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${color}" stroke-width="4" marker-end="url(#arrow)"/>`;
}

function shell(title, subtitle, body) {
  const grid = Array.from({ length: 14 }, (_, i) => line(110 + i * 145, 0, 110 + i * 145, H, '#e8e8e5', 1)).join('');
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
<defs>
  <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="${accent}"/>
  </marker>
  <style>
    text{font-family:Inter,Helvetica Neue,Noto Sans SC,Microsoft YaHei,Arial,sans-serif}
    .mono{font-family:JetBrains Mono,Consolas,monospace;letter-spacing:.14em}
  </style>
</defs>
<rect width="${W}" height="${H}" fill="${paper}"/>
${grid}
${text(90, 86, subtitle, 22, grey3, 500, 'class="mono"')}
${text(90, 158, title, 70, ink, 200)}
${line(90, 188, 2010, 188, grey2, 2)}
${body}
</svg>`;
}

function writeImage(name, svg) {
  writeFileSync(join(imagesDir, name), svg, 'utf8');
}

writeImage('03-system-architecture.svg', shell('系统组成图', 'SYSTEM COMPOSITION / FIVE MODULES', `
${rect(105, 255, 330, 470, grey1, grey2)}
${text(140, 310, '输入与触发', 38, ink, 300)}
${['显控交互', '感知结果', '雷达状态', '数据知识'].map((v, i) => `${rect(140, 350 + i * 78, 240, 48, paper, grey2)}${text(168, 383 + i * 78, v, 26, ink, 300)}`).join('')}
${rect(570, 245, 930, 500, ink, ink)}
${text(620, 310, 'LD智能体子系统', 48, '#fff', 200)}
${text(620, 356, 'Agent Harness / Safety Gate / Trace', 24, '#89a4ff', 500, 'class="mono"')}
${[['认知核心', 620, 410], ['记忆管理', 1030, 410], ['工具执行', 620, 535], ['工作流引擎', 1030, 535], ['数据库接入', 825, 660]].map(([v, x, y]) => `${rect(x, y, 320, 74, '#171717', '#555', 1)}${text(x + 35, y + 48, v, 32, '#fff', 300)}`).join('')}
${rect(1645, 255, 330, 470, grey1, grey2)}
${text(1680, 310, '输出与联动', 38, ink, 300)}
${['研判结果', '候选参数', '流程状态', '经验资产'].map((v, i) => `${rect(1680, 350 + i * 78, 240, 48, i === 1 ? accent : paper, i === 1 ? accent : grey2)}${text(1708, 383 + i * 78, v, 26, i === 1 ? '#fff' : ink, 300)}`).join('')}
${arrow(435, 490, 570, 490)}${arrow(1500, 490, 1645, 490)}
${text(90, 820, '设计要点：智能体负责理解、研判、建议、流程请求和追溯治理；真实控制下发由控制执行链路完成。', 30, ink, 300)}
`));

writeImage('04-execution-flow.svg', shell('任务执行信息流', 'TASK LIFECYCLE / CONTROLLED COGNITION', `
${['任务触发', '任务实例', '上下文装载', '推理规划', '工具/工作流', '结果发布', '追溯记忆'].map((v, i) => {
  const x = 130 + i * 280;
  const y = 395 + (i % 2) * 118;
  return `${rect(x, y, 210, 92, i === 4 ? accent : paper, i === 4 ? accent : ink, 3)}
${text(x + 25, y + 38, String(i + 1).padStart(2, '0'), 22, i === 4 ? '#fff' : grey3, 500, 'class="mono"')}
${text(x + 25, y + 72, v, 30, i === 4 ? '#fff' : ink, 300)}
${i < 6 ? arrow(x + 210, y + 46, x + 275, 395 + ((i + 1) % 2) * 118 + 46) : ''}`;
}).join('')}
${line(130, 650, 1960, 650, grey2, 2, 'stroke-dasharray="12 12"')}
${text(130, 705, '低风险任务：动态研判与工具调用', 32, ink, 300)}
${text(930, 705, '高风险任务：参数校验、仿真评估、人工确认、检查点与回滚', 32, accent, 300)}
${text(90, 820, '任务实例贯穿显控请求、感知事件、工具结果、工作流节点、审批动作、输出结论和经验回流。', 30, ink, 300)}
`));

writeImage('05-memory-loop.svg', shell('三阶分层记忆架构', 'THREE-TIER MEMORY / TRACE TO ASSET', `
${rect(160, 320, 430, 260, paper, ink, 3)}
${text(205, 382, '短期记忆', 48, ink, 200)}
${text(205, 430, '当前任务上下文', 28, grey3, 300)}
${text(205, 485, '任务目标 / 感知证据 / 工具结果', 26, ink, 300)}
${text(205, 530, '候选方案 / 检查点 / 上下文版本', 26, ink, 300)}
${rect(835, 320, 430, 260, accent, accent, 3)}
${text(880, 382, '中期记忆', 48, '#fff', 200)}
${text(880, 430, '近期任务链', 28, '#b9c8ff', 300)}
${text(880, 485, '目标链 / 区域链 / 参数链', 26, '#fff', 300)}
${text(880, 530, '异常链 / 操作员反馈', 26, '#fff', 300)}
${rect(1510, 320, 430, 260, ink, ink, 3)}
${text(1555, 382, '长期记忆', 48, '#fff', 200)}
${text(1555, 430, '经验资产', 28, '#b9c8ff', 300)}
${text(1555, 485, '知识库 / 案例库 / 策略库', 26, '#fff', 300)}
${text(1555, 530, '经验库 / 版本与适用边界', 26, '#fff', 300)}
${arrow(590, 450, 835, 450)}${arrow(1265, 450, 1510, 450)}
${arrow(1720, 580, 1080, 760)}${arrow(1080, 760, 375, 580)}
${text(815, 805, '追溯记录：输入、上下文、推理、工具、审批、结果、效果、反馈', 30, ink, 300)}
`));

writeImage('06-control-boundary.svg', shell('控制边界与安全门控', 'CONTROL BOUNDARY / SAFETY GATE', `
${rect(135, 300, 560, 340, paper, ink, 3)}
${text(180, 365, '认知核心', 52, ink, 200)}
${text(180, 425, '生成研判结论、候选参数方案、证据缺口、风险说明和工作流触发请求。', 27, ink, 300)}
${rect(775, 300, 560, 340, accent, accent, 3)}
${text(820, 365, '安全门控 / 工作流', 52, '#fff', 200)}
${text(820, 425, '完成权限校验、参数边界、仿真评估、人工确认、检查点和异常回滚。', 27, '#fff', 300)}
${rect(1415, 300, 560, 340, paper, ink, 3)}
${text(1460, 365, '控制执行链路', 52, ink, 200)}
${text(1460, 425, '受理经确认的控制请求，执行波形、波束、门限、跟踪参数等真实下发。', 27, ink, 300)}
${arrow(695, 470, 775, 470)}${arrow(1335, 470, 1415, 470)}
${line(775, 685, 1335, 685, accent, 6)}
${text(860, 735, '高风险动作必须穿过门控，不从 LLM 直接进入控制链路', 34, accent, 300)}
`));

writeImage('07-interface-map.svg', shell('接口关系图', 'INTERFACE CONTRACTS / TASK-CENTRIC', `
${rect(790, 275, 520, 340, ink, ink, 3)}
${text(850, 345, 'LD智能体', 58, '#fff', 200)}
${text(850, 392, '任务管理 / 认知推理 / 记忆读写', 25, '#fff', 300)}
${text(850, 432, '工具代理 / 工作流代理 / 安全门控', 25, '#fff', 300)}
${text(850, 472, '数据库接入 / 追溯记录 / 结果发布', 25, '#fff', 300)}
${[
  ['显控分系统', 130, 260],
  ['感知子系统', 130, 520],
  ['雷达状态服务', 1530, 260],
  ['控制执行链路', 1530, 520],
  ['数据知识底座', 795, 690],
].map(([v, x, y], i) => `${rect(x, y, 360, 92, i === 4 ? accent : paper, i === 4 ? accent : ink, 3)}${text(x + 38, y + 58, v, 34, i === 4 ? '#fff' : ink, 300)}`).join('')}
${arrow(490, 306, 790, 350)}${arrow(490, 566, 790, 512)}${arrow(1530, 306, 1310, 350)}${arrow(1530, 566, 1310, 512)}${arrow(1055, 615, 975, 690)}
${text(95, 805, '接口类型：HTTP、消息、网络通信、数据库、文件、函数库调用；TCP/UDP 与报文细节服从总体通信协议。', 30, ink, 300)}
`));

function imageHero(n, img, title, lead, stats) {
  return `
<section class="slide" data-layout="S22" data-animate="image-hero">
  <div class="canvas-card" style="padding:0;display:flex;flex-direction:column;overflow:hidden">
    <div data-anim="img" style="position:relative;flex:0 0 62%;overflow:hidden;background:var(--paper)">
      <img src="images/${img}" alt="${title}" loading="eager" data-image-slot="s22-hero-21x9"
           style="position:absolute;inset:0;width:100%;height:100%;object-fit:contain;object-position:center center">
      <div class="chrome-min" style="position:absolute;top:0;left:0;right:0;color:var(--text-primary);padding:5.6vh 5vw 0">
        <div class="l">LD AGENT · VISUAL EVIDENCE</div>
        <div class="r">RESEARCH REPORT · ${String(n).padStart(2, '0')} / 09</div>
      </div>
      <div data-anim="title-block" style="position:absolute;left:5vw;top:10.5vh;background:var(--paper);padding:2.6vh 2.6vw;max-width:35vw;border-left:8px solid var(--accent)">
        <div style="font-family:var(--sans),var(--sans-zh);font-weight:200;font-size:min(3.9vw,7vh);line-height:1.05;letter-spacing:-.025em;color:var(--text-primary)">${title}</div>
      </div>
    </div>
    <div data-anim="kpi" class="image-hero-body" style="padding:3vh 5vw 4.4vh">
      <div style="max-width:52ch;font-family:var(--sans),var(--sans-zh);font-size:max(15px,1.25vw);line-height:1.55;font-weight:300;color:var(--text-primary);letter-spacing:0">${lead}</div>
      <div class="image-hero-stats" style="gap:4vw">
        ${stats.map((s, i) => `<div style="display:flex;flex-direction:column;gap:.6vh"><div style="height:1px;background:${i === 2 ? 'var(--accent)' : 'var(--ink)'}"></div><div class="t-meta">${s[0]}</div><div style="font-family:var(--sans),var(--sans-zh);font-weight:200;font-size:min(2.3vw,4.2vh);line-height:1.05;letter-spacing:-.02em;color:${i === 2 ? 'var(--accent)' : 'var(--text-primary)'}">${s[1]}</div><div style="height:1px;background:var(--border-subtle);margin-top:auto"></div><p class="body-sm">${s[2]}</p></div>`).join('')}
      </div>
    </div>
  </div>
</section>`;
}

const total = 9;
const slides = String.raw`
<section class="slide accent" data-layout="SWISS-COVER-ASCII" data-animate="hero">
  <div class="canvas-card">
    <canvas class="ascii-bg" aria-hidden="true"></canvas>
    <div class="chrome-min"><div class="l">LD AGENT SYSTEM · VISUAL REPORT</div><div class="r">SS · 26.05.13 · 01 / ${total}</div></div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.6vh">
      <div data-anim="kicker" class="t-meta" style="color:rgba(255,255,255,.78);letter-spacing:.22em">IMAGE-FIRST RESEARCH DECK</div>
      <h1 data-anim="title" style="align-self:center;font-family:var(--sans),var(--sans-zh);font-weight:200;font-size:min(9.2vw,16vh);line-height:.96;letter-spacing:-.025em;color:#fff">LD智能体<br/>子系统</h1>
      <div data-anim="bottom" style="display:grid;grid-template-rows:auto auto;gap:1.6vh;border-top:1px solid rgba(255,255,255,.22);padding-top:2vh">
        <div data-anim="lead" class="lead" style="max-width:62ch;color:rgba(255,255,255,.86);font-weight:300">用图像先讲清系统边界、执行链路、记忆机制、控制门控与接口关系，再用少量文字支撑科研汇报表达。</div>
        <div style="display:flex;justify-content:space-between;align-items:end"><div class="t-meta" style="color:rgba(255,255,255,.6)">SOURCE · 4.3.3.2 LD智能体子系统技术方案</div><div class="t-meta" style="color:rgba(255,255,255,.6)">→ arrow keys / swipe</div></div>
      </div>
    </div>
  </div>
</section>

<section class="slide split" data-layout="S03" data-animate="split-statement">
  <div class="canvas-card">
    <div class="split-half">
      <div class="half b-ink" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between">
        <div class="chrome-min" style="color:rgba(255,255,255,.72)"><div class="l">02 / ${total}</div><div class="r">REPORT LOGIC</div></div>
        <div data-anim="left"><div class="t-meta" style="color:rgba(255,255,255,.72);letter-spacing:.22em;margin-bottom:2vh">CORE CLAIM</div><h2 style="font-family:var(--sans),var(--sans-zh);font-weight:200;font-size:min(7.0vw,12.4vh);line-height:.98;letter-spacing:-.025em;color:#fff">不是“大模型接入”<br/>而是受控认知层</h2></div>
        <div class="t-meta" style="color:rgba(255,255,255,.55)">CONTROLLED COGNITION</div>
      </div>
      <div class="half" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between;background:var(--grey-1)">
        <div data-anim="right" style="display:flex;flex-direction:column;gap:3vh">
          <div class="t-meta" style="color:var(--text-helper);letter-spacing:.22em">THREE QUESTIONS</div>
          ${[
            ['系统边界', '智能体与显控、感知、控制执行链路、数据知识底座如何分工。'],
            ['执行机制', '目标研判、参数建议和控制请求如何从开放推理进入受控流程。'],
            ['持续演进', '任务记录如何通过三阶记忆和经验治理转化为可复用资产。']
          ].map((x, i) => `<div style="border-top:${i === 2 ? '2px solid var(--accent)' : '1px solid var(--border-subtle)'};padding-top:2vh"><div class="t-meta" style="color:${i === 2 ? 'var(--accent)' : 'var(--text-helper)'}">${String(i + 1).padStart(2, '0')}</div><h3 style="font-weight:300;font-size:max(22px,2vw);line-height:1.15;margin:.7vh 0 1vh">${x[0]}</h3><p class="body">${x[1]}</p></div>`).join('')}
        </div>
        <div class="t-meta" style="color:var(--text-helper)">THE DECK IS BUILT AROUND VISUAL PROOF OBJECTS</div>
      </div>
    </div>
  </div>
</section>

${imageHero(3, '03-system-architecture.svg', '系统组成', '五大核心模块由运行底座、安全门控和追溯记录贯穿治理，对外连接显控、感知、状态、控制和数据知识底座。', [['CORE', '5 模块', '认知、记忆、工具、工作流、数据库接入'], ['GOV', '贯穿治理', '任务实例、权限、安全、观测、追溯'], ['BOUNDARY', '控制解耦', '智能体生成建议，控制链路执行下发']])}
${imageHero(4, '04-execution-flow.svg', '执行信息流', '从任务触发到经验回流，系统以任务实例为主线，把上下文、推理、工具、工作流、显控反馈和追溯记录串成闭环。', [['TRIGGER', '多源触发', '显控请求、感知事件、状态告警'], ['PATH', '两类路径', '动态研判与受控工作流'], ['TRACE', '全程追溯', '输入、调用、审批、结果与反馈']])}
${imageHero(5, '05-memory-loop.svg', '记忆机制', '三阶分层记忆不是普通存储，而是把当前上下文、近期任务链和长期经验资产连接起来的工程化学习回路。', [['SHORT', '短期', '当前任务不断裂'], ['MID', '中期', '近期任务可连续'], ['LONG', '长期', '经验资产受控回流']])}
${imageHero(6, '06-control-boundary.svg', '安全门控', '涉及波形参数设置、工作模式切换和回滚恢复的动作必须进入工作流，经过校验、仿真、确认和检查点控制。', [['READ', '只读研判', '可动态调用工具'], ['PLAN', '候选方案', '包含适用条件和风险点'], ['ACT', '受控执行', '审批后进入控制链路']])}
${imageHero(7, '07-interface-map.svg', '接口关系', '接口设计围绕统一任务标识、目标/区域引用、证据引用和追溯引用展开，技术形态按 HTTP、消息、网络通信、数据库、文件和函数调用划分。', [['EXT', '外部接口', '显控、感知、状态、控制、数据、保障'], ['INT', '内部接口', '任务、推理、记忆、工具、工作流、门控'], ['ICD', '后续细化', '报文、端口、字段、鉴权和重试策略']])}

<section class="slide" data-layout="S08" data-animate="duo-mirror">
  <div class="canvas-card">
    <div class="chrome-min"><div class="l">DESIGN DECISIONS</div><div class="r">08 / ${total}</div></div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:3vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.2vh"><div class="t-meta">ENGINEERING POSITION · 08</div><h2 class="h-xl-zh" style="font-size:min(4.8vw,8.6vh)">科研报告中的三条设计判断</h2></div>
      <div data-anim="compare" class="duo-compare" style="width:100%">
        <div class="col"><div class="t-meta">WHAT IT IS</div><h3>智能推理分系统</h3><ul class="col-list"><li>面向调度、波形参数设置、目标研判。</li><li>统一任务实例、证据、上下文和追溯。</li><li>把工具、工作流、记忆和数据接入纳入治理。</li></ul></div>
        <div class="vrule"></div>
        <div class="col accent"><div class="t-meta">WHAT IT IS NOT</div><h3>不是控制执行替代物</h3><ul class="col-list"><li>不直接绕过控制执行链路下发指令。</li><li>不把一次任务记录直接发布为长期经验。</li><li>不把开放推理用于高风险动作自由执行。</li></ul></div>
      </div>
      <div class="foot"><span>这三条判断决定后续软件需求、概要设计和接口控制文档的边界</span><span class="nb">08</span></div>
    </div>
  </div>
</section>

<section class="slide split" data-layout="SWISS-CLOSING-ASCII" data-animate="split-statement">
  <div class="canvas-card">
    <div class="split-half">
      <div class="half b-accent" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between;position:relative;overflow:hidden"><canvas class="ascii-bg" aria-hidden="true"></canvas><div class="chrome-min" style="margin-bottom:0;position:relative;z-index:1"><div class="l">09 / ${total}</div><div class="r">CLOSING</div></div><div data-anim="manifesto" style="position:relative;z-index:1"><div class="t-meta" style="color:rgba(255,255,255,.78);letter-spacing:.22em;margin-bottom:2vh">CONCLUSION</div><h2 style="font-family:var(--sans),var(--sans-zh);font-size:min(7.2vw,12.8vh);line-height:.96;letter-spacing:-.025em;font-weight:200;color:#fff">可集成<br/>可复盘<br/>可演进</h2></div><div data-anim="signature" style="border-top:1px solid rgba(255,255,255,.22);padding-top:2vh;position:relative;z-index:1" class="t-meta">LD AGENT SYSTEM · 2026.05</div></div>
      <div class="half" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between"><div class="chrome-min"><div class="l">TAKEAWAYS</div><div class="r">03 RULES</div></div><div data-anim="rules" style="display:flex;flex-direction:column;gap:0">${[['边界清晰','智能体生成研判、建议、流程请求和追溯记录。'],['流程受控','参数设置和控制请求进入工作流、安全门控和人工确认。'],['经验治理','短期、中期、长期记忆分层流转，经验发布前评估复核。']].map((x,i)=>`<div style="display:grid;grid-template-columns:auto 1fr;gap:2vw;align-items:start;padding:2.6vh 0;border-top:1px solid var(--border-subtle);${i===2?'border-bottom:2px solid var(--accent)':''}"><div style="font-family:var(--sans);font-weight:200;font-size:min(4.4vw,7.8vh);line-height:.9;color:${i===2?'var(--accent)':'var(--text-primary)'}">${String(i+1).padStart(2,'0')}</div><div><h3 style="font-weight:400;font-size:max(18px,1.8vw);line-height:1.2;color:${i===2?'var(--accent)':'var(--text-primary)'};margin-bottom:1vh">${x[0]}</h3><p style="font-size:max(12px,.92vw);line-height:1.6;color:var(--text-secondary);font-weight:300">${x[1]}</p></div></div>`).join('')}</div><div data-anim="foot" class="t-meta" style="color:var(--text-helper);text-align:right">END OF VISUAL REPORT</div></div>
    </div>
  </div>
</section>`;

let html = readFileSync(templatePath, 'utf8');
html = html.replace('<title>[必填] 替换为 PPT 标题 · Deck Title</title>', '<title>LD智能体子系统科研报告 · 图片版</title>');
html = html.replace(/<div id="deck">[\s\S]*?<\/div>\s*<div id="nav"><\/div>/, `<div id="deck">\n${slides}\n</div>\n\n<div id="nav"></div>`);
html = html.replace(/\[必填\][^<]*/g, '');
writeFileSync(outPath, html, 'utf8');
console.log(JSON.stringify({ outPath, images: 5, slides: total }, null, 2));
