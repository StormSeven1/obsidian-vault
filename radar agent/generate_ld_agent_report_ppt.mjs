import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const root = 'D:/knowledge/radar agent';
const skillRoot = `${process.env.USERPROFILE}/.codex/skills/guizang-ppt-skill`.replaceAll('\\', '/');
const templatePath = `${skillRoot}/assets/template-swiss.html`;
const outDir = join(root, 'LD智能体科研报告PPT');
const imagesDir = join(outDir, 'images');
const outPath = join(outDir, 'index.html');

mkdirSync(imagesDir, { recursive: true });

const title = 'LD智能体子系统科研报告 · Swiss Web PPT';
const total = 13;
const page = (n) => String(n).padStart(2, '0');
const chrome = (n, left = 'LD AGENT SYSTEM') => `
    <div class="chrome-min">
      <div class="l">${left}</div>
      <div class="r">RESEARCH REPORT · 26.05.12 · ${page(n)} / ${total}</div>
    </div>`;

const slides = String.raw`
<section class="slide accent" data-layout="SWISS-COVER-ASCII" data-animate="hero">
  <div class="canvas-card">
    <canvas class="ascii-bg" aria-hidden="true"></canvas>
    <div class="chrome-min">
      <div class="l">LD AGENT SYSTEM · RESEARCH REPORT</div>
      <div class="r">SS · 26.05.12 · 01 / ${total}</div>
    </div>
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.6vh">
      <div data-anim="kicker" class="t-meta" style="color:rgba(255,255,255,.78);letter-spacing:.22em">INTELLIGENT RADAR · CONTROLLED COGNITION</div>
      <h1 data-anim="title" style="align-self:center;font-family:var(--sans),var(--sans-zh);font-weight:200;font-size:min(9.2vw,16vh);line-height:.96;letter-spacing:-.025em;color:#fff">LD智能体<br/>子系统技术方案</h1>
      <div data-anim="bottom" style="display:grid;grid-template-rows:auto auto;gap:1.6vh;border-top:1px solid rgba(255,255,255,.22);padding-top:2vh">
        <div data-anim="lead" class="lead" style="max-width:58ch;color:rgba(255,255,255,.86);font-weight:300">面向智能雷达调度、波形参数设置与当前环境目标研判的智能决策和人机协同子系统。</div>
        <div style="display:flex;justify-content:space-between;align-items:end">
          <div class="t-meta" style="color:rgba(255,255,255,.6)">SOURCE · 4.3.3.2 LD智能体子系统技术方案</div>
          <div class="t-meta" style="color:rgba(255,255,255,.6)">→ arrow keys / swipe</div>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="slide split" data-layout="S03" data-animate="split-statement">
  <div class="canvas-card">
    <div class="split-half">
      <div class="half b-ink" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between">
        <div class="chrome-min" style="color:rgba(255,255,255,.72)"><div class="l">SYSTEM SHIFT</div><div class="r">02 / ${total}</div></div>
        <div data-anim="left" style="display:flex;flex-direction:column;gap:2vh">
          <div class="t-meta" style="color:rgba(255,255,255,.72);letter-spacing:.22em">FROM PASSIVE TO ACTIVE</div>
          <h2 style="font-family:var(--sans),var(--sans-zh);font-weight:200;font-size:min(7.2vw,12.8vh);line-height:.98;letter-spacing:-.025em;color:#fff">从被动感知<br/>到主动理解</h2>
        </div>
        <div class="t-meta" style="color:rgba(255,255,255,.55)">INTELLIGENT DECISION LOOP</div>
      </div>
      <div class="half" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between;background:var(--grey-1)">
        <div data-anim="right" style="display:flex;flex-direction:column;gap:3vh">
          <div class="t-meta" style="color:var(--text-helper);letter-spacing:.22em">THESIS</div>
          <div class="lead" style="max-width:38ch;color:var(--text-primary)">LD智能体不是替代雷达处理链路，而是在现有处理、控制与显控体系之上增加受控的认知增强层。</div>
          <div style="display:grid;gap:1.4vh">
            <div style="border-top:1px solid var(--border-subtle);padding-top:1.6vh"><span class="t-cat">01</span><div class="body">智能推理与真实控制链路解耦。</div></div>
            <div style="border-top:1px solid var(--border-subtle);padding-top:1.6vh"><span class="t-cat">02</span><div class="body">开放研判与标准流程分治。</div></div>
            <div style="border-top:1px solid var(--accent);padding-top:1.6vh"><span class="t-cat" style="color:var(--accent)">03</span><div class="body">全流程证据化、追溯化和经验回流。</div></div>
          </div>
        </div>
        <div class="t-meta" style="color:var(--text-helper)">BOUNDARY · ADVICE / WORKFLOW REQUEST / TRACE</div>
      </div>
    </div>
  </div>
</section>

<section class="slide" data-layout="S05" data-animate="stack-build">
  <div class="canvas-card">
${chrome(3, 'ARCHITECTURE POSITION')}
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:3vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.4vh">
        <div class="t-meta">SYSTEM POSITION · 03</div>
        <h2 class="h-xl-zh" style="font-size:min(5.4vw,9.6vh)">智能决策与人机协同中枢</h2>
      </div>
      <div data-anim="stack" class="stack-row" style="width:100%">
        <div class="stack-block">
          <div class="layer-tag">INPUT LAYER</div>
          <div class="layer-ttl">多源任务触发</div>
          <div class="layer-desc">显控自然语言、目标/区域选择、感知结果事件、雷达状态告警与环境数据共同形成任务入口。</div>
        </div>
        <div class="stack-block accent">
          <div class="layer-tag">COGNITION LAYER</div>
          <div class="layer-ttl">LLM + Agent Harness</div>
          <div class="layer-desc">认知核心完成意图理解、上下文组织、执行路径规划；运行底座提供任务实例、权限、安全门控和追溯治理。</div>
        </div>
        <div class="stack-block">
          <div class="layer-tag">ACTION LAYER</div>
          <div class="layer-ttl">受控工具与工作流</div>
          <div class="layer-desc">工具执行模块提供专业能力，工作流引擎承接高风险流程，真实控制下发由控制执行链路完成。</div>
        </div>
      </div>
      <div class="foot"><span>核心边界：智能体输出研判结果、候选参数方案、补证请求、工作流请求和追溯记录</span><span class="nb">03</span></div>
    </div>
  </div>
</section>

<section class="slide grey" data-layout="S17" data-animate="system-diagram">
  <div class="canvas-card">
${chrome(4, 'SYSTEM COMPOSITION')}
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.8vh">
      <div data-anim="head" style="display:grid;grid-template-columns:1fr .82fr;gap:4vw;align-items:end">
        <div style="display:flex;flex-direction:column;gap:1.2vh">
          <div class="t-meta">COMPOSITION · 04</div>
          <h2 class="h-xl-zh" style="font-size:min(4.8vw,8.8vh)">系统组成与输入输出</h2>
        </div>
        <p class="body">五大核心模块由运行底座贯穿治理，面向显控、感知、状态、控制链路和数据知识底座形成闭环。</p>
      </div>
      <div data-anim="diagram" style="display:grid;grid-template-columns:1fr 1.35fr 1fr;gap:2vw;align-items:stretch">
        <div style="display:grid;gap:1.2vh">
          <div class="card-fill" style="padding:1.7vh 1.4vw"><div class="t-cat">INPUT</div><div class="body">显控交互输入</div></div>
          <div class="card-fill" style="padding:1.7vh 1.4vw"><div class="t-cat">SENSING</div><div class="body">检测/识别/跟踪/定位</div></div>
          <div class="card-fill" style="padding:1.7vh 1.4vw"><div class="t-cat">STATUS</div><div class="body">雷达状态与环境数据</div></div>
          <div class="card-fill" style="padding:1.7vh 1.4vw"><div class="t-cat">KNOWLEDGE</div><div class="body">关系/向量/图/时序底座</div></div>
        </div>
        <div class="card-ink" style="padding:2.4vh 2vw;display:grid;grid-template-rows:auto 1fr auto;gap:2vh">
          <div class="t-meta" style="color:rgba(255,255,255,.66)">LD AGENT SUBSYSTEM</div>
          <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:1.2vh 1vw">
            <div style="border-top:1px solid rgba(255,255,255,.3);padding-top:1vh">认知核心模块</div>
            <div style="border-top:1px solid rgba(255,255,255,.3);padding-top:1vh">记忆管理模块</div>
            <div style="border-top:1px solid rgba(255,255,255,.3);padding-top:1vh">工具执行模块</div>
            <div style="border-top:1px solid rgba(255,255,255,.3);padding-top:1vh">工作流引擎模块</div>
            <div style="border-top:1px solid rgba(255,255,255,.3);padding-top:1vh;grid-column:1 / span 2">数据库管理与接入模块</div>
          </div>
          <div class="t-meta" style="color:var(--accent-bright)">Agent Harness · Safety Gate · Trace</div>
        </div>
        <div style="display:grid;gap:1.2vh">
          <div class="card-accent" style="padding:1.7vh 1.4vw"><div class="t-cat">RESULT</div><div class="body">目标研判与证据链</div></div>
          <div class="card-fill" style="padding:1.7vh 1.4vw"><div class="t-cat">PLAN</div><div class="body">候选参数方案</div></div>
          <div class="card-fill" style="padding:1.7vh 1.4vw"><div class="t-cat">FLOW</div><div class="body">工作流状态与审批请求</div></div>
          <div class="card-fill" style="padding:1.7vh 1.4vw"><div class="t-cat">LEARN</div><div class="body">复盘报告与经验资产</div></div>
        </div>
      </div>
      <div class="foot"><span>信息流从任务触发进入智能体，控制类动作转入受控工作流与控制执行链路</span><span class="nb">04</span></div>
    </div>
  </div>
</section>

<section class="slide" data-layout="S11" data-animate="timeline-walk">
  <div class="canvas-card">
${chrome(5, 'EXECUTION FLOW')}
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:3vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.2vh">
        <div class="t-meta">TASK LIFECYCLE · 05</div>
        <h2 class="h-xl-zh" style="font-size:min(5vw,9vh)">从任务触发到经验回流</h2>
      </div>
      <div data-anim="timeline" class="timeline-h" style="width:100%">
        <div class="tl-h-axis"></div>
        ${['任务触发','任务实例','上下文装载','推理规划','工具/工作流','结果发布','追溯记忆'].map((t, i) => `
        <div class="tl-h-node">
          <div class="dot"></div>
          <div class="t-meta">${page(i + 1)}</div>
          <div style="font-size:max(17px,1.45vw);font-weight:400;margin-top:1vh">${t}</div>
          <div class="body-sm">${[
            '显控请求、感知事件或状态告警进入系统。',
            '绑定任务ID、来源、对象、风险等级和上下文版本。',
            '短期上下文、中期任务链和长期经验共同投影。',
            '认知核心选择能力包、工具和执行路径。',
            '低风险动态调用，高风险进入模板化受控流程。',
            '返回摘要、证据、建议、风险与流程状态。',
            '固化上下文、工具、审批、效果和反馈。'
          ][i]}</div>
        </div>`).join('')}
      </div>
      <div class="foot"><span>任务实例是贯穿推理、工具、工作流、接口和追溯的共同对象</span><span class="nb">05</span></div>
    </div>
  </div>
</section>

<section class="slide grey" data-layout="S04" data-animate="grid-reveal">
  <div class="canvas-card">
${chrome(6, 'FUNCTION MODULES')}
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.8vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.2vh">
        <div class="t-meta">MODULE MAP · 06</div>
        <h2 class="h-xl-zh" style="font-size:min(4.8vw,8.6vh)">五大模块，一条治理主线</h2>
      </div>
      <div data-anim="grid" class="sub-grid-3-2">
        ${[
          ['认知核心','意图理解、任务建模、上下文组织、执行路径规划和结果生成。'],
          ['记忆管理','短期任务、中期任务链、长期经验资产与追溯回流。'],
          ['工具执行','封装查询、分析、仿真、控制适配和报告生成等专业工具。'],
          ['工作流引擎','模板、节点、审批、检查点、回滚和状态追溯。'],
          ['数据库接入','关系、向量、图、时序数据的统一访问与质量标识。'],
          ['运行治理','任务实例、能力包调度、安全门控、观测和追溯贯穿全程。']
        ].map((x, i) => `
        <div class="sub-card ${i === 1 || i === 5 ? 'accent' : ''}">
          <div class="t-meta">${page(i + 1)}</div>
          <div class="title">${x[0]}</div>
          <div class="desc">${x[1]}</div>
        </div>`).join('')}
      </div>
      <div class="foot"><span>Agent Harness 是贯穿式运行治理机制，不改变五大核心模块划分</span><span class="nb">06</span></div>
    </div>
  </div>
</section>

<section class="slide" data-layout="S08" data-animate="duo-mirror">
  <div class="canvas-card">
${chrome(7, 'ROUTING LOGIC')}
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:3vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.2vh">
        <div class="t-meta">DUAL EXECUTION · 07</div>
        <h2 class="h-xl-zh" style="font-size:min(4.6vw,8.2vh)">开放式研判与受控流程分治</h2>
      </div>
      <div data-anim="compare" class="duo-compare" style="width:100%">
        <div class="col">
          <div class="t-meta">DYNAMIC REASONING</div>
          <h3>只读研判 / 推荐生成</h3>
          <ul class="col-list">
            <li>目标解释、异常归因、跟踪质量评估。</li>
            <li>通过 ReAct 式工具调用补充证据。</li>
            <li>输出事实、判断、建议、风险和证据引用。</li>
            <li>证据不足时返回补证或人工复核提示。</li>
          </ul>
        </div>
        <div class="vrule"></div>
        <div class="col accent">
          <div class="t-meta">CONTROLLED WORKFLOW</div>
          <h3>参数设置 / 控制请求</h3>
          <ul class="col-list">
            <li>候选参数方案进入工作流模板。</li>
            <li>执行边界校验、仿真评估和人工确认。</li>
            <li>控制请求由控制执行链路受理并回传状态。</li>
            <li>检查点与回滚条件进入追溯记录。</li>
          </ul>
        </div>
      </div>
      <div class="foot"><span>路径选择由任务标准化程度、风险等级、系统状态和资源负载共同决定</span><span class="nb">07</span></div>
    </div>
  </div>
</section>

<section class="slide grey" data-layout="S14" data-animate="loop-form">
  <div class="canvas-card">
${chrome(8, 'COGNITIVE LOOP')}
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.8vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.2vh">
        <div class="t-meta">PLA + REACT · 08</div>
        <h2 class="h-xl-zh" style="font-size:min(4.7vw,8.4vh)">感知、理解、行动的认知循环</h2>
      </div>
      <div style="display:grid;grid-template-columns:.9fr 1.1fr;gap:3vw;align-items:center">
        <div data-anim="steps" style="display:grid;gap:1.5vh">
          ${[
            ['感知接入','显控输入、感知结果、雷达状态和历史任务进入任务工作空间。'],
            ['语言理解','识别意图、绑定对象、抽取约束并选择雷达能力包。'],
            ['执行规划','根据风险和标准化程度选择动态工具调用或受控工作流。'],
            ['观察回流','工具结果、流程状态、审批反馈和效果指标更新上下文。']
          ].map((x, i) => `
          <div class="ledger-row" style="display:grid;grid-template-columns:auto 1fr;gap:1.4vw;align-items:start">
            <div class="num" style="font-size:min(3.6vw,6.5vh);font-weight:200;color:${i === 2 ? 'var(--accent)' : 'var(--text-primary)'}">${page(i + 1)}</div>
            <div style="border-top:1px solid var(--border-subtle);padding-top:1.3vh">
              <div style="font-size:max(17px,1.5vw);font-weight:400">${x[0]}</div>
              <div class="body-sm">${x[1]}</div>
            </div>
          </div>`).join('')}
        </div>
        <div data-anim="loop" class="card-ink" style="min-height:48vh;padding:3vh 2.2vw;display:grid;place-items:center">
          <div style="width:min(32vw,54vh);height:min(32vw,54vh);border:1px solid rgba(255,255,255,.28);display:grid;grid-template:repeat(2,1fr)/repeat(2,1fr);gap:1px;background:rgba(255,255,255,.18)">
            ${['PERCEIVE','LANGUAGE','ACT','OBSERVE'].map((x, i) => `<div style="background:var(--ink);display:flex;align-items:center;justify-content:${i % 2 ? 'flex-start' : 'flex-end'};padding:2vw;color:${i === 2 ? 'var(--accent-bright)' : '#fff'};font-family:var(--mono);letter-spacing:.18em">${x}</div>`).join('')}
          </div>
        </div>
      </div>
      <div class="foot"><span>认知核心的价值不在于自由生成，而在于将大语言模型推理纳入雷达工程约束</span><span class="nb">08</span></div>
    </div>
  </div>
</section>

<section class="slide" data-layout="S15" data-animate="matrix-fill">
  <div class="canvas-card">
${chrome(9, 'THREE-TIER MEMORY')}
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.8vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.2vh">
        <div class="t-meta">MEMORY ARCHITECTURE · 09</div>
        <h2 class="h-xl-zh" style="font-size:min(4.8vw,8.6vh)">三阶分层记忆把记录变成资产</h2>
      </div>
      <div data-anim="matrix" class="matrix-fill" style="grid-template-columns:repeat(4,1fr);grid-auto-rows:minmax(8vh,1fr)">
        ${[
          ['短期记忆','当前任务上下文','一次研判、一次参数调度、一次流程执行。'],
          ['中期记忆','近期任务链','目标链、区域链、参数链、异常链。'],
          ['长期记忆','经验资产','知识、案例、策略和发布后的经验。'],
          ['追溯记录','统一贯通','输入、工具、审批、结果、效果和反馈。'],
          ['上下文版本','防止污染','关键状态变化可回看、可恢复。'],
          ['证据编号','支撑结论','事实、工具结果、历史案例和知识来源可引用。'],
          ['质量评估','控制回流','冲突检查、适用条件、版本和复核。'],
          ['受控复用','不绕边界','长期经验只作为建议和依据，不越过审批。']
        ].map((x, i) => `
        <div class="matrix-cell ${i === 2 || i === 6 ? 'accent' : ''}">
          <div class="t-meta">${x[0]}</div>
          <div style="font-size:max(17px,1.45vw);font-weight:400;margin-top:.9vh">${x[1]}</div>
          <div class="body-sm" style="margin-top:.8vh">${x[2]}</div>
        </div>`).join('')}
      </div>
      <div class="foot"><span>检索策略：当前任务优先，近期任务补充，长期经验参考</span><span class="nb">09</span></div>
    </div>
  </div>
</section>

<section class="slide grey" data-layout="S16" data-animate="field-notes">
  <div class="canvas-card">
${chrome(10, 'TOOL GOVERNANCE')}
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.8vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.2vh">
        <div class="t-meta">TOOLS · 10</div>
        <h2 class="h-xl-zh" style="font-size:min(4.7vw,8.3vh)">工具执行模块连接专业能力</h2>
      </div>
      <div data-anim="cards" class="brief-grid">
        ${[
          ['数据查询','目标、航迹、历史任务、环境数据，为研判和参数优化提供事实依据。'],
          ['感知解释','检测、识别、置信度和异常评分解释，记录模型版本和证据编号。'],
          ['分析算法','目标行为、跟踪质量、异常归因，输出适用边界和不确定性。'],
          ['参数仿真','波形、门限、资源调度评估，支撑执行前效果判断。'],
          ['控制适配','经审批的模式切换、参数设置和回滚请求进入控制链路。'],
          ['报告生成','研判报告、复盘报告和执行记录导出，绑定追溯引用。']
        ].map((x, i) => `
        <div class="brief-card ${i === 4 ? 'accent' : ''}">
          <div class="t-meta">${page(i + 1)}</div>
          <div class="title">${x[0]}</div>
          <div class="desc">${x[1]}</div>
        </div>`).join('')}
      </div>
      <div class="foot"><span>工具接入按只读、分析、仿真评估、控制请求适配分级治理</span><span class="nb">10</span></div>
    </div>
  </div>
</section>

<section class="slide" data-layout="S02" data-animate="progression">
  <div class="canvas-card">
${chrome(11, 'WAVEFORM PARAMETER WORKFLOW')}
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.8vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.2vh">
        <div class="t-meta">CONTROLLED PROCESS · 11</div>
        <h2 class="h-xl-zh" style="font-size:min(4.5vw,8vh)">波形参数设置进入受控工作流</h2>
      </div>
      <div style="display:grid;grid-template-columns:.86fr 1.14fr;gap:3vw;align-items:stretch">
        <div data-anim="timeline" class="timeline-v">
          <div class="tl-axis"></div>
          ${[
            ['候选方案生成','认知核心根据任务目标、目标状态、资源和历史效果生成候选参数。'],
            ['边界与仿真','工作流完成参数边界校验、仿真评估和风险说明。'],
            ['人工确认','涉及控制请求的节点等待显控确认和审批反馈。'],
            ['提交与回滚','控制请求适配工具提交请求，状态回传并保留检查点。']
          ].map((x, i) => `
          <div class="tl-node">
            <div class="dot"></div>
            <div class="t-meta">${page(i + 1)}</div>
            <div style="font-size:max(17px,1.45vw);font-weight:400">${x[0]}</div>
            <div class="body-sm">${x[1]}</div>
          </div>`).join('')}
        </div>
        <div data-anim="kpi" class="kpi-row-4" style="width:100%">
          ${[
            ['READ', '只读研判', '查询与解释可动态调用'],
            ['PLAN', '推荐生成', '输出候选方案和风险边界'],
            ['CHECK', '受控校验', '仿真、审批、检查点'],
            ['ACT', '控制链路', '真实下发与状态回传']
          ].map((x, i) => `
          <div class="kpi-cell">
            <div class="t-meta">${x[0]}</div>
            <div class="kpi-hero" style="font-size:min(2.6vw,4.8vh);color:${i === 2 ? 'var(--accent)' : 'var(--text-primary)'}">${x[1]}</div>
            <div class="body-sm">${x[2]}</div>
          </div>`).join('')}
        </div>
      </div>
      <div class="foot"><span>高风险动作的可靠性来自模板、检查点、人工确认、状态回传和异常回滚</span><span class="nb">11</span></div>
    </div>
  </div>
</section>

<section class="slide grey" data-layout="S21" data-animate="tech-spec">
  <div class="canvas-card">
${chrome(12, 'DATA AND INTERFACE CONTRACTS')}
    <div style="flex:1;padding:0;display:grid;grid-template-rows:auto 1fr auto;gap:2.8vh">
      <div data-anim="head" style="display:flex;flex-direction:column;gap:1.2vh">
        <div class="t-meta">INTERFACE SPEC · 12</div>
        <h2 class="h-xl-zh" style="font-size:min(4.6vw,8.2vh)">接口围绕统一引用与追溯展开</h2>
      </div>
      <div data-anim="spec" class="tech-spec" style="display:grid;grid-template-columns:1fr .95fr;gap:3vw;align-items:stretch">
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:1vw">
          <div class="card-ink" style="padding:2.2vh 1.5vw"><div class="t-meta" style="color:rgba(255,255,255,.65)">CORE</div><div class="kpi-hero" style="color:#fff">5</div><div class="body-sm" style="color:rgba(255,255,255,.72)">核心功能模块</div></div>
          <div class="card-accent" style="padding:2.2vh 1.5vw"><div class="t-meta">EXT</div><div class="kpi-hero">10</div><div class="body-sm">外部接口</div></div>
          <div class="card-fill" style="padding:2.2vh 1.5vw"><div class="t-meta">INT</div><div class="kpi-hero">12</div><div class="body-sm">内部接口</div></div>
          <div style="grid-column:1 / span 3;display:grid;grid-template-columns:repeat(2,1fr);gap:1vw;margin-top:1vh">
            ${[
              ['统一任务标识','任务编号贯穿触发、推理、工具、工作流和结果发布。'],
              ['统一目标/区域引用','显控选择、感知结果、时序数据和经验检索指向同一对象。'],
              ['统一证据引用','观测事实、工具结果、历史案例和专业知识可追溯。'],
              ['统一追溯引用','任务输入、上下文版本、工具、审批、输出和反馈形成回放索引。']
            ].map((x) => `<div class="card-fill" style="padding:1.6vh 1.2vw"><div class="t-cat">${x[0]}</div><div class="body-sm">${x[1]}</div></div>`).join('')}
          </div>
        </div>
        <div style="display:grid;gap:1.2vh">
          ${[
            ['HTTP / 消息','显控任务提交、状态订阅和智能研判结果发布。'],
            ['网络通信','雷达状态接入和控制请求适配，TCP/UDP按总体协议确定。'],
            ['数据库 / 文件','数据知识访问、试验评估、样本沉淀和运维保障。'],
            ['函数库调用','内部任务管理、认知推理、记忆读写、工具代理、工作流代理和安全门控。']
          ].map((x, i) => `<div style="border-top:${i === 1 ? '2px solid var(--accent)' : '1px solid var(--border-subtle)'};padding-top:1.6vh"><div class="t-meta">${x[0]}</div><div class="body">${x[1]}</div></div>`).join('')}
        </div>
      </div>
      <div class="foot"><span>本阶段确定接口名称、类型、提供方、调用方、输入和输出；报文与字段在后续 ICD 细化</span><span class="nb">12</span></div>
    </div>
  </div>
</section>

<section class="slide split" data-layout="SWISS-CLOSING-ASCII" data-animate="split-statement">
  <div class="canvas-card">
    <div class="split-half">
      <div class="half b-accent" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between;position:relative;overflow:hidden">
        <canvas class="ascii-bg" aria-hidden="true"></canvas>
        <div class="chrome-min" style="margin-bottom:0;position:relative;z-index:1">
          <div class="l">13 / ${total}</div>
          <div class="r">CLOSING</div>
        </div>
        <div data-anim="manifesto" style="display:flex;flex-direction:column;gap:2vh;position:relative;z-index:1">
          <div class="t-meta" style="color:rgba(255,255,255,.78);letter-spacing:.22em;margin-bottom:1.6vh">CONCLUSION</div>
          <h2 style="font-family:var(--sans),var(--sans-zh);font-size:min(7.2vw,12.8vh);line-height:.96;letter-spacing:-.025em;font-weight:200;color:#fff">受控认知<br/>持续进化</h2>
          <div style="font-family:var(--sans),var(--sans-zh);font-size:max(13px,1vw);line-height:1.6;color:rgba(255,255,255,.82);font-weight:300;max-width:38ch;margin-top:1.4vh">LD智能体的工程价值，是把智能研判、参数建议、工具执行、工作流治理和经验沉淀组织成可集成、可复盘、可演进的闭环。</div>
        </div>
        <div data-anim="signature" style="display:flex;justify-content:space-between;align-items:end;border-top:1px solid rgba(255,255,255,.22);padding-top:2vh;position:relative;z-index:1">
          <div class="t-meta" style="color:rgba(255,255,255,.62)">LD AGENT SYSTEM</div>
          <div class="t-meta" style="color:rgba(255,255,255,.62)">2026.05</div>
        </div>
      </div>
      <div class="half" style="padding:5.6vh 3.6vw 4.4vh;justify-content:space-between">
        <div class="chrome-min">
          <div class="l">TAKEAWAYS</div>
          <div class="r">03 RULES</div>
        </div>
        <div data-anim="rules" style="display:flex;flex-direction:column;gap:0">
          ${[
            ['边界清晰','智能体负责研判、建议、补证、流程请求和追溯；控制下发由控制执行链路完成。'],
            ['路径受控','只读研判动态处理，推荐生成带风险边界，高风险动作进入工作流。'],
            ['经验治理','短期、中期、长期记忆分层流转，经验进入长期资产前经过评估和复核。']
          ].map((x, i) => `
          <div style="display:grid;grid-template-columns:auto 1fr;gap:2vw;align-items:start;padding:2.6vh 0;border-top:1px solid var(--border-subtle);${i === 2 ? 'border-bottom:2px solid var(--accent)' : ''}">
            <div style="font-family:var(--sans);font-weight:200;font-size:min(4.4vw,7.8vh);line-height:.9;color:${i === 2 ? 'var(--accent)' : 'var(--text-primary)'}">${page(i + 1)}</div>
            <div>
              <h3 style="font-family:var(--sans),var(--sans-zh);font-weight:400;font-size:max(18px,1.8vw);line-height:1.2;letter-spacing:-.015em;color:${i === 2 ? 'var(--accent)' : 'var(--text-primary)'};margin-bottom:1vh">${x[0]}</h3>
              <p style="font-family:var(--sans),var(--sans-zh);font-size:max(12px,.92vw);line-height:1.6;color:var(--text-secondary);font-weight:300">${x[1]}</p>
            </div>
          </div>`).join('')}
        </div>
        <div data-anim="foot" class="t-meta" style="color:var(--text-helper);text-align:right">END OF RESEARCH REPORT</div>
      </div>
    </div>
  </div>
</section>
`;

let html = readFileSync(templatePath, 'utf8');
html = html.replace('<title>[必填] 替换为 PPT 标题 · Deck Title</title>', `<title>${title}</title>`);
html = html.replace(/<div id="deck">[\s\S]*?<\/div>\s*<div id="nav"><\/div>/, `<div id="deck">\n${slides}\n</div>\n\n<div id="nav"></div>`);
html = html.replace(/\[必填\][^<]*/g, '');

writeFileSync(outPath, html, 'utf8');
console.log(outPath);
