# 态势感知 AI-native Agent 系统设计 · 附录 A：Agent 最佳实践与当前架构改进建议

## 1. 文档目的

本附录用于把跨项目对标、官方最佳实践、以及对当前第 1、2 章的高价值评审结论沉淀为仓库内文档，避免关键判断只存在于会话上下文中。

本文档回答两个问题：

1. 当前优秀 Agent 项目的共同最佳实践是什么
2. 这些最佳实践映射到本系统后，暴露出哪些结构性缺口与改进方向

本文档不是新的架构骨架章节，也不替代第 2 章；它的作用是作为第 2 章和后续细化章节的外部对标依据。

---

## 2. 参考范围

本附录主要参考以下项目与官方资料：

- `awesome-agent/claude-code/`
- `awesome-agent/openclaw/`
- `awesome-agent/deer-flow/`
- `awesome-agent/langchain/deepagents/`
- `awesome-agent/hermes-agent/`
- Anthropic 官方 `Claude Code` 文档与 best practices
- OpenAI 官方 agent / eval / trace grading 文档
- LangGraph 官方 persistence / interrupts 文档

这些资料的目标领域并不完全相同，但它们在 runtime、权限边界、上下文治理、评测、恢复语义等方面提供了高价值工程参照。

---

## 3. 当前优秀 Agent 项目的共同最佳实践

### 3.1 先有可运行 runtime，再长抽象

优秀项目往往先锁定 thread / session / runtime loop / sandbox / checkpoint 等硬基础设施，再逐步长出对象模型与能力层次。

这意味着：

- 可恢复执行优先于概念完整性
- 状态快照、重入、异常恢复优先于抽象优雅
- 架构蓝图必须能落到明确的 runtime ownership

### 3.2 权限必须落到 deterministic enforcement points

最佳实践不是“模型知道不能做”，而是：

- 每个高风险动作在执行前命中明确 gate
- deny / allow / ask / override 有确定语义
- 策略决策结果可记录、可恢复、可审计

Sandbox、approval、policy engine、tool allowlist、hook 都属于 enforcement surface，而不是对模型的口头提醒。

### 3.3 上下文是第一资源，必须显式治理

优秀 Agent 项目普遍把上下文当作最稀缺资源之一，而不是无限可堆积的提示词空间。

共同做法包括：

- 长会话自动压缩 / 摘要
- 子任务使用隔离上下文
- 大结果落文件，不直接塞回主上下文
- 监控、通知、展示、审计尽量移出主推理上下文
- 长期记忆按需检索，不默认注入

### 3.4 验证必须可执行，评测必须持续化

当前最佳实践已经不满足于“系统能解释自己”，还要求：

- Agent 能在运行时验证自己的关键输出
- 工具选择、参数提取、handoff、最终结果都能被测
- trace 可以被 grader 评估
- 每次重要变更后都可以运行持续评测

也就是说，Verification 只是运行时的一部分，Evaluation 是更高层的持续质量闭环。

### 3.5 durable execution 要有硬语义

长任务与人类介入场景下，必须明确：

- checkpoint 的最小粒度
- interrupt / pause / resume 的状态语义
- fork / rewind / replay 的区别
- session / thread / mission / run 之间如何关联

“支持 continuation” 不是最佳实践；“有明确恢复合同” 才是。

### 3.6 core 要 lean，扩展能力插件化或桥接化

优秀系统通常把核心收敛在少量稳定能力：

- runtime
- permissions
- session / state
- tool execution
- observability

可选能力尽量经由 plugin、MCP、extension、gateway bridge 引入，避免核心无限膨胀。

### 3.7 subagent 的核心价值是上下文隔离与边界化委托

优秀项目使用 subagent 的主要目的不是做复杂层级管理，而是：

- 隔离探索性上下文
- 限制子任务工具权限
- 降低主线程上下文污染
- 用明确输入输出做 bounded delegation

### 3.8 监控、通知、产品表面要工程化，而不是隐含在 agent loop 中

成熟系统普遍重视：

- `doctor` / health check
- `status` / usage / session management
- setup / onboarding
- 可恢复会话
- 审批与权限 UX

这说明“可用性”本身是架构能力，不只是 UI 包装。

### 3.9 安全关键场景需要 defense-in-depth

在涉及物理资产或高风险执行时，最佳实践不是单押某一层，而是多层叠加：

- sandbox / isolation
- policy gate
- approval / override
- lease / lock / arbitration
- audit / replay
- 独立安全联锁或执行保护层

### 3.10 渐进采用比一次性完备更优雅

优秀项目通常允许团队先获得一个可工作的窄版本，再逐步增加：

- 更强模型
- 更多工具
- 更复杂的记忆
- 更细的评测
- 更自动的演进

最佳实践不是一开始把所有抽象都实现出来，而是确保架构终态正确、实现路径渐进。

---

## 4. 当前系统架构的主要问题

以下问题针对第 1、2 章当前版本，不意味着总体方向错误；它们主要说明“蓝图强于 runtime 合同”。

### 4.1 Checkpoint / Resume 被放在 P1，削弱了 Mission 架构的可落地性

第 1 章当前把长生命周期任务的 `checkpoint / resume` 放在 P1。对于以 Mission Continuation 为核心能力的系统，这个优先级偏低。

问题在于：

- 没有 durable execution，Mission 很容易退化成“逻辑存在、运行时脆弱”
- 人工接管、暂停恢复、长任务重入都缺硬基础设施
- 后续第 7 章很难在没有 P0 合同的前提下稳定展开

### 4.2 第 1 章与第 2 章对象术语仍未完全收敛

第 1 章仍使用 `State / Review` 这样的简化表达，而第 2 章已经锁定为 `Committed State / Review Record / Asset Lease`。

问题在于：

- 上游愿景文档仍可能成为术语漂移来源
- 后续章节引用第 1 章时，容易重新引入旧称呼

### 4.3 Boundary 有 gate，但还没有完整 rule contract

第 2 章已经把 Runtime Boundary 映射到多个 enforcement surface，这是重要进步；但最佳实践要求更进一步明确：

- 规则表达形态
- 决策输入 payload
- 决策输出模型
- deny 后的恢复路径
- gate 决策是否进入 Trace / Review Record

当前的问题不是“没有 Boundary”，而是“Boundary 仍偏概念，缺执行合同”。

### 4.4 Context Discipline 仍是原则，不是 contract

当前第 2 章只明确了“系统状态不等于模型上下文”“长期记忆按需检索”等原则，但还没有回答：

- 什么对象允许进入 prompt
- 什么对象只能通过查询读取
- 何时 summarize / compact
- worker / subagent 如何交接
- 何种信息必须从主上下文剥离

### 4.5 Verification 仍未上升为 Evaluation 体系

当前架构有运行时 Verification，但还缺：

- trace grading
- tool selection eval
- argument extraction eval
- promotion eval
- continuous evaluation

这会导致系统“可验证”，但不一定“可持续优化、可比较回归”。

### 4.6 Fast Run 可跳过 Verification 的边界仍偏松

当前设计允许 Fast Run 跳过 `6.7 Verification`。这对只读查询成立，但对任何有副作用动作都偏危险。

问题在于：

- 容易在快路径上形成治理豁免
- 后续产品迭代时，低风险动作的边界容易被不断放宽

### 4.7 Audit and Replay 过早绑定外部语义标准

当前第 2 章倾向把 OpenTelemetry GenAI 语义直接作为基础要求。外部标准很有价值，但仍在演化。

风险在于：

- 内部审计契约被外部语义变更牵动
- 系统内部真相模式与外部导出格式混淆

### 4.8 Consolidation Run 缺完整 promotion pipeline

当前设计已经要求人工复核，这是对的；但还缺：

- offline eval
- graded trace review
- shadow / canary
- 分阶段 promotion

否则演进链仍然偏人工经验驱动。

### 4.9 Runtime Budget / Backpressure 还不是一等约束

虽然第 2 章已经引入 `Model Routing`，但还没有把以下 runtime 现实上升为骨架级约束：

- deadline budget
- queue backlog
- concurrency caps
- approval backlog
- degraded-mode fallback
- priority inversion control

### 4.10 Tool / ACI 契约没有被提升到架构级

当前架构对平面、对象、主循环约束很强，但对工具契约本身还不够强调。

问题包括：

- tool 的副作用等级分类未显式建模
- tool 的 verifier 可用性未成为准入要求
- tool 错误面与恢复面没有统一合同

### 4.11 Control Kernel 虽已分组，但仍需更强的实现纪律

当前已经引入五个子职责组，这是正确方向；但最佳实践还会继续要求：

- 每组可独立观测
- 每组可单独降级
- 每组可单独替换
- 分组不只是文档结构，而要成为实现边界

---

## 5. 建议的修改方向

### 5.1 将 durable execution 提升为 P0 基础设施

建议把以下能力从“应预留”提升为“首版基础设施”：

- checkpoint
- interrupt / pause
- resume
- mission / run 重入
- 审批挂起后的恢复

### 5.2 在第 1 章显式声明对象术语以第 2 章为准

建议在第 1 章对象列表后增加一句说明：

> 完整的一等运行对象与正式命名以第 2 章 §4 为准；本章只保留前提层简化描述。

### 5.3 为 Runtime Boundary 增补明确的 rule contract

建议在第 4 章至少锁定：

- Rule 的声明式表达
- Gate 输入输出模型
- `allow / deny / ask / override` 语义
- 决策记录如何进入 Review / Trace
- deny 后的 retry / edit / escalate 机制

### 5.4 为 Context Discipline 增补上下文合同

建议新增 `Context Contract`，明确：

- 对象到上下文的投影规则
- compact / summarize 触发条件
- subagent / worker 的交接格式
- 主推理上下文与监控/通知上下文的隔离纪律

### 5.5 将 Evaluation 提升为独立质量闭环

建议不要让 Evaluation 只隐含在 Verification 里，而应单独锁定：

- 运行时 verifier
- 离线 eval
- trace grading
- regression suite
- promotion gate

### 5.6 收紧 Fast Run 的治理豁免

建议把当前规则改为：

- 只读 fast path 可跳过重验证
- 任何副作用动作必须经过至少 lightweight verification 或显式白名单检查

### 5.7 内部 audit schema 与外部 telemetry 标准解耦

建议采用：

- 内部稳定审计对象模型
- 外部 OTel / vendor telemetry adapter

不要让外部标准直接成为内部真相模式。

### 5.8 为 Consolidation Run 增补 promotion pipeline

建议把产出升级链补成：

1. candidate generation
2. offline eval
3. trace grading
4. shadow / canary
5. operator review
6. promotion

### 5.9 新增 Runtime Budget / Backpressure 约束

建议在第 2 章或后续 runtime 章节明确：

- latency / cost budget
- queue depth limits
- worker concurrency limits
- approval backlog policy
- degrade policy

### 5.10 为 Tool / ACI 增补统一契约

建议锁定：

- tool schema discipline
- side-effect classification
- verifier availability
- human-readable error surface
- 恢复 / 重试 / 回退语义

### 5.11 继续把 Control Kernel 分组落实到实现边界

建议后续章节和实现路线都围绕五个子职责组展开，而不是重新回到“单一总控类”。

---

## 6. 总结判断

当前第 1、2 章已经具备以下明显优势：

- 治理强度高
- 状态链清晰
- 正交维度设计优秀
- 演进回路与实时路径分离

但距离“Agent 领域最佳实践”还有几个必须补上的硬合同：

- Checkpoint / Resume / Fork Contract
- Boundary Rule Contract
- Context Contract
- Verification + Evaluation Contract
- Promotion Pipeline Contract
- Runtime Budget / Backpressure Contract
- Tool / ACI Contract

因此，更准确的判断不是“架构需要推翻重做”，而是：

> **当前架构骨架成立，但必须把强蓝图继续编译成强 runtime 合同，才能真正接近该领域的最佳实践。**
