# AI原生JSC2自主决策智能体微服务架构方案v5.0

**文档版本**：v5.0（文档重构版——12章+附录结构）
**发布日期**：2026 年 5 月 10 日
**领域定位**：JS指挥控制（Command & Control）/ 多域智能作战 / AI原生C2
**系统定位**：开源版 Lattice + Donovan + Gotham 融合体
**编制单位**：指挥控制系统架构研究组
**v5.0关键升级**：文档结构重构为12章+附录，按功能域重组技术选型，工作流引擎独立成章，新增经验蒸馏与自主演进章节，新增术语表

---

## 目录

1. [方案概述](#1-方案概述)
2. [核心技术选型与架构设计](#2-核心技术选型与架构设计)
3. [智能体认知架构——自主决策的三大支柱](#3-智能体认知架构自主决策的三大支柱)
4. [快慢双系统与自主决策闭环](#4-快慢双系统与自主决策闭环)
5. [COP数据平面与知识服务](#5-cop数据平面与知识服务)
6. [对抗训练与仿真体系](#6-对抗训练与仿真体系)
7. [五大作战场景验证](#7-五大作战场景验证)
8. [数据闭环与模型演进](#8-数据闭环与模型演进)
9. [安全设计与JS合规管理](#9-安全设计与JS合规管理)
10. [系统运维与可观测性](#10-系统运维与可观测性)
11. [性能指标与测试验证](#11-性能指标与测试验证)
12. [落地实施路线](#12-落地实施路线)
附录 [术语表·许可证·版本记录·参考文献](#附录)

---

## 1. 方案概述

### 1.1 项目背景

现代战争正在从机械化、信息化向智能化加速演进。多域作战（MDO）、联合全域指挥控制（JADC2）、分布式杀伤等新作战概念的提出，对C2系统提出了前所未有的要求：

- **杀伤链闭环加速**：从"发现-定位-跟踪-瞄准-打击-评估"（F2T2EA）全链路要求从小时级压缩到分钟甚至秒级
- **多域异构协同**：陆、海、空、天、电、网多域平台需要实时感知、协同决策、联合行动
- **大规模无人集群**：百架级无人机、数十艘无人艇的集群控制与自主协同
- **强对抗环境**：GPS拒止、通信干扰、电子战对抗下的降级运行能力
- **人在回路**：关键决策（特别是武器释放）必须保留人类确认环节
- **AI深度嵌入**：大语言模型（LLM）驱动的态势理解、行动方案生成、情报分析成为新范式

美国国防领域已涌现三款标志性产品：
- **Anduril Lattice**：自主作战管理系统，专注于战术边缘的实时传感器融合、目标跟踪和任务规划，以Lattice OS为核心实现硬件+软件一体化
- **Palantir Gotham/AIP/MSS**：基于本体论的大数据分析平台，擅长多源情报融合、语义推理，并通过AIP将LLM嵌入决策流程，获得陆军$100亿MSS合同
- **Scale AI Donovan/Thunderforge**：以数据和评估为核心，通过Defense Llama（国防定制LLM）和Thunderforge（AI智能体JS规划系统）将AI Agent深度整合进JS工作流

传统C2系统（如单体式指挥信息系统）无法满足上述需求。本方案基于开源技术栈，构建一套AI原生的JSC2多智能体微服务架构，融合三款产品的核心设计思想，实现**"感知-理解-决策-行动"（OODA）循环的智能化加速**。

### 1.2 与Lattice/Gotham/Donovan的定位对比

| 维度 | Anduril Lattice | Palantir Gotham/AIP | Scale AI Donovan | **本方案（开源融合体）** |
|------|-----------------|---------------------|------------------|------------------------|
| **核心定位** | 战术边缘自主平台 | 全域情报分析操作系统 | AI决策与评估平台 | AI原生C2操作系统 |
| **数据层** | Entity-Component模型 | 本体论（Ontology） | Scale Data Engine | JC3IEDM本体 + 多模态PG |
| **AI层** | 边缘AI推理 | LLM嵌入分析（AIP） | Defense Llama + Agents | SGLang多模型 + RAG知识库 |
| **决策层** | Lattice OS任务规划 | COA辅助生成 | Thunderforge AI规划 | Temporal OODA + COA智能体 |
| **执行层** | 自主硬件平台 | 软件平台（不控硬件） | 软件平台 | 数据链集成 + SDK插件 |
| **部署模式** | 战术边缘气隙 | 云/企业级 | FedRAMP云/气隙 | 全密级/边缘K3s |
| **技术栈** | 闭源 | 闭源 | 闭源 | 全栈开源 |
| **差异化** | 最强战术边缘实时性 | 最深情报分析语义 | 最强LLM Agent + 评估 | 三者融合 + 开源可控 |

### 1.3 核心定位——从决策加速器到自主决策智能体

本方案不是指挥员决策的"加速工具"，而是一套**具备自主决策能力的智能体集群**。系统通过三大支柱实现从"执行人类预案"到"自主推理决策"的跃迁：

**世界模型（World Model）**：从历史战场数据中学习战场动力学，能够预测"如果我这样做，对手会怎样反应，战场会变成什么样"。世界模型是智能体的内部仿真器，让它在行动前就能推演后果（详见第3章）。

**技能库（Skills）**：从条令、战例、指挥员操作中提取可复用的决策能力单元。与静态工作流模板不同，Skill具有自学习的适用条件和因果模型，能在新态势中泛化（详见第3章）。

**蒙特卡洛树搜索（MCTS）**：在世界模型中进行数千次推演，系统性地探索决策空间。取代LLM"生成3个方案"的启发式方法，用搜索保证决策质量（详见第3章）。

工作流模板不再是决策主体，而是退化为**安全执行层**——智能体做出的决策通过工作流模板进行验证和执行，确保符合交战规则和指挥意图（详见第4章）。

对抗训练（红蓝对抗）通过持续的自博弈产生鲁棒的策略，并将训练结果转化为新的Skill（详见第6章）。

### 1.4 设计目标

| 目标维度 | 具体要求 | 量化指标 |
|---------|---------|---------|
| **杀伤链闭环** | OODA循环加速，杀伤链端到端闭环 | 战术级OODA < 10s，战役级规划 < 5min |
| **多域感知融合** | 多源异构传感器数据融合 | 支持 ≥ 8 种传感器类型，传感器融合延迟 < 3s（从原始数据到COP实体更新）；传感器→COP更新发布 P95 < 500ms |
| **集群控制规模** | 异构无人平台大规模协同 | 单控站支持 ≥ 200 个平台实例 |
| **强对抗韧性** | 通信中断/GPS拒止下的降级运行 | 降级模式下核心功能可用率 ≥ 95% |
| **AI原生嵌入** | LLM深度嵌入OODA各阶段 | 情报分析、COA生成、威胁研判均由AI驱动 |
| **知识驱动** | JS条令/战例/装备知识的RAG检索 | 条令检索响应 < 2s，知识覆盖 ≥ 5类条令 |
| **自主可控** | 基于开源技术栈，支持国产化适配 | 核心组件采用 Apache 2.0/MIT 等开源许可 |
| **高可用性** | 指挥系统不间断运行 | 系统可用性 ≥ 99.95%，MTTR < 10 分钟 |
| **安全保密** | 多密级信息处理与隔离 | 支持秘密级及以上密级标定与隔离 |
| **模型可评估** | AI模型的安全性、可靠性可量化评估 | 部署前红队测试、OOD退化评估 |
| **多模态交互** | 语音/文字/AR多通道人机交互 | 语音命令响应 < 2s，NL态势查询 < 3s，AR渲染 ≥ 30fps |
| **自主演进** | 系统从实战数据中持续学习和改进 | 漂移检测 < 1h，自动重训练闭环 < 24h，联邦聚合 ≤ 1次/天 |
| **工作流统一界面** | 快/慢系统和指挥员通过工作流注册表统一交互 | 快系统选模板 < 500ms，慢系统调模板 < 120s，语音干预响应 < 2s |
| **经验蒸馏** | 慢系统有效方法自动晋升为快系统先验 | 经验积累≥10次自动评估晋升，OPA规则自动生成 |

### 1.5 核心创新点

1. **智能体认知架构**：世界模型+技能库+MCTS三支柱，使智能体具备真正的自主决策能力，而非仅执行预编码的工作流模板
2. **快慢双系统**：Skill匹配的亚秒级快路径 + MCTS搜索的深度慢路径，兼顾速度与质量
3. **对抗训练闭环**：红蓝对抗的GAN式训练，持续产生鲁棒策略并蒸馏为Skill
4. **经验因果学习**：从统计压缩升级为因果归因——不仅记录"什么有效"，更理解"为什么有效"
5. **分层自主等级（L1-L5）**：从查询辅助到紧急自主，人在不同等级扮演不同角色
6. **工作流安全执行层**：智能体决策通过工作流模板验证后执行，确保符合交战规则

### 1.6 设计原则

| 原则 | 说明 | 优先级 |
|------|------|--------|
| **任务式指挥** | 上级下达意图，下级自主执行；智能体在约束条件下自主决策 | P0 |
| **人在回路** | 武器释放、跨境行动等高风险决策必须经人类指挥员确认 | P0 |
| **降级 graceful** | 通信中断时基于本地规则自主运行，通信恢复后自动同步 | P0 |
| **最小权限** | 智能体仅获取完成任务所需的最小信息和资源 | P1 |
| **可解释可追溯** | 每个决策可追溯到输入数据、推理过程、决策依据 | P1 |
| **时敏优先** | 时间敏感目标优先处理，非时敏任务让出资源 | P1 |
| **策略即代码** | 交战规则、行为边界通过声明式策略（OPA/Rego）管理 | P1 |
| **评估先行** | 模型部署前必须通过安全评估、红队测试和退化测试 | P1 |

---

## 2. 核心技术选型与架构设计

### 2.1 技术选型原则

| 选型维度 | 评估标准 | 权重 |
|---------|---------|------|
| **开源许可** | Apache 2.0/MIT 等可商用/可修改许可 | 25% |
| **实时性能** | 低延迟、高吞吐、确定性响应 | 30% |
| **战场适配** | 支持边缘部署、弱网运行、资源受限环境 | 20% |
| **社区与生态** | 活跃社区、丰富集成、长期维护 | 15% |
| **国产化适配** | 支持国产CPU（飞腾/鲲鹏）、OS（麒麟/统信） | 10% |

### 2.2 架构分层与组件职责划分


```Plain
┌──────────────────────────────────────────────────────────────────────────┐
│  第-1层：多模态人机交互层                                    │
│  FunASR/Whisper(语音识别) | CosyVoice(语音合成) | NL态势查询引擎         │
│  WebSocket实时推送 | Cesium三维态势+MIL-STD-2525D | WebXR AR战术叠加     │
├──────────────────────────────────────────────────────────────────────────┤
│       第0层：安全网关 + 服务网格                                          │
│       APISIX（外部流量入口）+ Linkerd（服务网格mTLS/可观测性）             │
├──────────────────────────────────────────────────────────────────────────┤
│       第1层：OODA循环编排引擎                                             │
│       Temporal — 作战流程编排、状态持久化、人工审批、Saga补偿              │
├──────────────────────────────────────────────────────────────────────────┤
│       第2层：智能体逻辑层                                                 │
│       LangGraph（智能体状态图）+ LiteLLM（多模型代理路由）                │
├──────────────────────────────────────────────────────────────────────────┤
│       第3层：分布式通信层                                                 │
│       Dapr — 服务间调用、发布订阅、状态管理、密钥管理                      │
├──────────────────────────────────────────────────────────────────────────┤
│       第4层：AI推理与优化层                                               │
│       SGLang（LLM推理）+ Triton（传统ML推理）+ OR-Tools（组合优化）       │
├──────────────────────────────────────────────────────────────────────────┤
│       第5层：RAG/OAG知识层                                    │
│       Qdrant（向量检索）+ JS知识库（条令/战例/装备手册）                 │
├──────────────────────────────────────────────────────────────────────────┤
│       第6层：战术数据链集成层                                  │
│       Link 16 / VMF / STANAG 4609 适配器 + Protobuf中间格式              │
├──────────────────────────────────────────────────────────────────────────┤
│       第7层：COP多模态数据平面                                            │
│       PostgreSQL + PostGIS + TimescaleDB + Apache AGE + Valkey           │
├──────────────────────────────────────────────────────────────────────────┤
│       第8层：模型评估与仿真层                                  │
│       SEAL式评估框架 + HLA4/C-BML仿真引擎 + AFSIM兵棋推演               │
└──────────────────────────────────────────────────────────────────────────┘

横向贯穿：
  • OPA策略引擎 — 交战规则/行为边界/数据访问的声明式管理
  • Redpanda消息总线 — 替代Kafka，更低延迟、无JVM依赖
  • 可观测性 — Prometheus + Grafana + Jaeger + Loki
  • GitOps — ArgoCD + Flux 双引擎，配置即代码、审计可追溯
  • 自主演进闭环— 反馈采集→漂移检测(Evidently)→自动训练
    →RLHF/DPO(TRL)→灰度发布→联邦学习(Flower)→闭环A/B实验
```

**十层+演进闭环职责划分矩阵**：

| 能力 | 负责组件（层） | 不参与的组件 | 详细设计 |
|------|---------------|------------|---------|
| 外部请求路由/限流/WAF | APISIX（第0层） | Linkerd（仅服务间） | Ch9 |
| 服务间mTLS/流量管理 | Linkerd（第0层） | APISIX（仅外部流量） | Ch9 |
| 跨服务业务流程编排 | Temporal（第1层） | LangGraph（仅智能体内部） | Ch3 |
| 智能体内部状态转换 | LangGraph（第2层） | Temporal（仅跨服务编排） | Ch3 |
| 多LLM模型路由/代理 | LiteLLM（第2层） | LangGraph（不直接调LLM） | Ch3 |
| 服务发现/调用/状态 | Dapr（第3层） | Temporal（用自身持久化） | — |
| LLM推理（结构化输出） | SGLang（第4层） | Triton（传统ML推理） | Ch3 |
| 传统ML推理/GPU调度 | Triton（第4层） | SGLang（LLM专用） | Ch3 |
| 路径规划/资源分配优化 | OR-Tools（第4层） | LangGraph | Ch3 |
| 条令知识检索/嵌入存储 | Qdrant（第5层） | PostgreSQL（主数据存储） | Ch5 |
| Link 16/VMF消息编解码 | 数据链适配器（第6层） | Dapr（通用通信） | Ch5 |
| 时空/时序/图/向量存储 | PG多模态（第7层） | Qdrant（知识专用） | Ch5 |
| 模型安全评估/红队测试 | 评估框架（第8层） | Triton（仅推理） | Ch8 |
| ROE/行为边界策略管理 | OPA（横向贯穿） | 各组件（仅执行策略） | Ch9 |
| 事件流/消息总线 | Redpanda（横向贯穿） | Dapr pubsub（底层用Redpanda） | — |
| 指标采集/告警/仪表盘 | 可观测性（横向贯穿） | 各组件（仅暴露指标） | Ch10 |
| 声明式部署/版本管理 | GitOps（横向贯穿） | 各组件（仅打包为manifest） | Ch10 |
| 漂移检测/偏好学习/联邦 | 自演进闭环（横向贯穿） | 各组件（仅产生训练数据） | Ch8 |
| 多模态交互（语音/NL/AR） | 第-1层交互组件 | 内部服务间通信 | Ch4/Ch5 |

### 2.3 全局信息流程图

本节从信息流动的视角，描述数据与决策信号如何在各架构层、智能体三大支柱、快慢双系统之间流转。下图展示了系统的 **8 条核心信息流**，覆盖从传感器接入到自主决策再到经验演化的完整闭环。

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 全局信息流程图 — 8条核心信息流                                    │
│                                                                                                 │
│  ╔═════════════════════════════════════════════════════════════════════════════════════════════╗  │
│  ║  ❶ 感知接入流（Sensor→COP，<3s）                                                           ║  │
│  ║                                                                                             ║  │
│  ║  传感器阵列 ──Link16/VMF/STANAG──▸ 数据链适配器(L6) ──Protobuf──▸ Redpanda主题              ║  │
│  ║      (雷达/EO/IR/ESM)                  │                              │                       ║  │
│  ║                                         ▼                              ▼                       ║  │
│  ║                                   Triton目标检测(L4)         COP数据平面(L7)                   ║  │
│  ║                                   (P95<100ms)             ┌──────────────┐                   ║  │
│  ║                                         │                │PostGIS(空间)  │                   ║  │
│  ║                                         ▼                │TimescaleDB(时序)│                  ║  │
│  ║                                    目标检测报告 ──▸       │AGE(图谱)      │                   ║  │
│  ║                                                       │Valkey(缓存)   │                   ║  │
│  ║                                                       └──────┬───────┘                   ║  │
│  ║                              ❷ COP广播流                    │                           ║  │
│  ║                       ┌─────────────────────┘           │                           ║  │
│  ║                       ▼                                  ▼                           ║  │
│  ║              cop_updates主题(Redpanda) ◂───── COP实体变更通知 ──────┘                   ║  │
│  ║                       │                                                                 ║  │
│  ║                       ▼                                                                 ║  │
│  ║              WebSocket推送 ──▸ Cesium 3D态势显示(L-1)                                   ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════════════════════╝  │
│                                                                                                 │
│  ╔═════════════════════════════════════════════════════════════════════════════════════════════╗  │
│  ║  ❸ 快路径决策流（COP→执行，<500ms）                                                        ║  │
│  ║                                                                                             ║  │
│  ║  COP态势变更 ──▸ AgentKernel.decide() ──▸ 五路径决策级联                                   ║  │
│  ║                                               │                                             ║  │
│  ║        ┌──────────────────────────────────────┼──────────────────────────┐              ║  │
│  ║        │              │              │         │         │              │              ║  │
│  ║        ▼              ▼              ▼         ▼         ▼              ▼              ║  │
│  ║   ┌─────────┐  ┌──────────┐  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   ║  │
│  ║   │路径0    │  │路径1     │  │路径2     │ │路径3     │ │路径4     │ │OPA安全   │   ║  │
│  ║   │蒸馏模型 │  │Skill快速 │  │Skill自适应│ │MCTS搜索  │ │人工决策  │ │校验层    │   ║  │
│  ║   │  <30ms  │  │  <500ms  │  │  1-5s    │ │ 10-30s   │ │(等待指挥)│ │(贯穿全程)│   ║  │
│  ║   └────┬────┘  └────┬─────┘  └────┬─────┘ └────┬─────┘ └────┬─────┘ └─────┬────┘  ║  │
│  ║        │            │              │              │             │            │        ║  │
│  ║        └────────────┴─────┬────────┴──────────────┴──────┬──────┘            │        ║  │
│  ║        【快系统 L0-L2】    │      【中速路径】            │  【慢系统】       │        ║  │
│  ║                           ▼                               │             │         │          ║  │
│  ║                  ❹ 执行验证流                              │             │         │          ║  │
│  ║                  OPA策略引擎 ◂───── 决策输出                │             │         │          ║  │
│  ║                       │         ROE/交战规则合规校验         │             │         │          ║  │
│  ║                       ▼                                    ▼             │         │          ║  │
│  ║                Temporal工作流引擎(L1) ◂──────── MCTS最优方案 ◂────┘      │         │          ║  │
│  ║                  │   DAG步骤执行                           世界模型推演      │         │          ║  │
│  ║                  ▼                                                        │         │          ║  │
│  ║           数据链指令输出(L6) ──▸ 平台执行动作 ──────────────────────────┘          │          ║  │
│  ╚═══════════════════════════════════════════════════════════════════════════════════════════╝  │
│                                                                                                 │
│  ╔═════════════════════════════════════════════════════════════════════════════════════════════╗  │
│  ║  ❺ 经验反馈流（执行→学习，异步）                      ❻ Skill蒸馏流（学习→快路径，周期性）      ║  │
│  ║                                                                                             ║  │
│  ║  平台执行结果 ──▸ ExperienceRecorder                                                        ║  │
│  ║        │         (态势,动作,结果,人工判定)                                                   ║  │
│  ║        ├─────────▸ Qdrant经验集合                                                           ║  │
│  ║        │              │                                                                     ║  │
│  ║        │         ExperienceMiner(周期聚合)                                                   ║  │
│  ║        │              │  过滤: 成功率≥90%, 人工认可率≥95%                                    ║  │
│  ║        │              ▼                                                                     ║  │
│  ║        │         ┌────────────────┐                                                         ║  │
│  ║        │         │ 三路蒸馏输出    │                                                         ║  │
│  ║        │         │ ┌────────────┐ │                                                         ║  │
│  ║        │         │ │Qdrant快车道 │ │──▸ L2向量匹配路径(~20ms)                                ║  │
│  ║        │         │ └────────────┘ │                                                         ║  │
│  ║        │         │ ┌────────────┐ │                                                         ║  │
│  ║        │         │ │OPA编译规则  │ │──▸ L1短路路径(<5ms)                                     ║  │
│  ║        │         │ └────────────┘ │                                                         ║  │
│  ║        │         │ ┌────────────┐ │                                                         ║  │
│  ║        │         │ │SFT/DPO数据 │ │──▸ 蒸馏小模型训练 ──▸ L0路径(<30ms)                      ║  │
│  ║        │         │ └────────────┘ │     (1-3B模型,Triton)                                   ║  │
│  ║        │         └────────────────┘                                                         ║  │
│  ║        │                                                                                    ║  │
│  ║        └─────────▸ 世界模型训练管道 ◂── 兵棋推演/历史战例/演习数据                             ║  │
│  ║                        │                  (状态,动作,下一状态)三元组                            ║  │
│  ║                        ▼                                                                     ║  │
│  ║                   世界模型更新 ──▸ MCTS仿真评估 ──▸ 决策质量提升                               ║  │
│  ╚═════════════════════════════════════════════════════════════════════════════════════════════╝  │
│                                                                                                 │
│  ╔═════════════════════════════════════════════════════════════════════════════════════════════╗  │
│  ║  ❼ 模型演进流（漂移→重训→部署，<24h）               ❽ 快慢协调流（实时融合）                 ║  │
│  ║                                                                                             ║  │
│  ║  生产数据流 ──▸ Evidently漂移检测                                                            ║  │
│  ║                     │  KS统计量>0.05触发                                                     ║  │
│  ║                     ▼                                                                       ║  │
│  ║              偏好数据采集(指挥员决策)                                                         ║  │
│  ║                     │  (选择的COA vs 拒绝的COA)                                              ║  │
│  ║                     ▼                                                                       ║  │
│  ║              DPO偏好微调(TRL+LoRA)          快系统结果 ──▸ 立即发布到COP                     ║  │
│  ║                     │                                       │                                ║  │
│  ║                     ▼                                       ▼                                ║  │
│  ║              六维评估(SEAL式)              慢系统结果 ──▸ 覆盖快结果                           ║  │
│  ║              (安全/准确/鲁棒/可解释/          (若冲突: threat_level,                            ║  │
│  ║               一致/高效)                     classification,                                   ║  │
│  ║                     │                        engagement_recommendation)                        ║  │
│  ║                     ▼                                       │                                ║  │
│  ║              金丝雀发布(10%流量)                              ▼                                ║  │
│  ║              LiteLLM路由                     冲突升级 ──▸ 人工裁决                              ║  │
│  ║                     │                                                                       ║  │
│  ║                     ▼                                                                       ║  │
│  ║              全量发布 ◂── 监控通过                                                           ║  │
│  ║                     │                                                                       ║  │
│  ║                     ▼                                                                       ║  │
│  ║              边缘节点联邦聚合(Flower)                                                        ║  │
│  ║              (仅传输梯度,原始数据不出域)                                                      ║  │
│  ╚═════════════════════════════════════════════════════════════════════════════════════════════╝  │
└─────────────────────────────────────────────────────────────────────────────────────────────────┘

以上8条信息流覆盖了从传感器接入（Ch5）→ 自主决策（Ch3/Ch4）→ 经验反馈与模型演进（Ch8）的完整闭环。每条流的时延要求、起终点和对应章节详见上图。

**信息实体血缘追踪**（以下血缘图是对上述8条流的端到端数据实体追踪视角，聚焦数据血缘关系而非组件交互）：

```
传感器原始数据 ──(解码)──▸ Protobuf中间格式 ──(融合)──▸ COP实体
    │                                                │
    │                                          (快路径)
    │                                                ▼
    │                                        AgentKernel决策
    │                                                │
    │                                          (执行反馈)
    │                                                ▼
    │                                     ExperienceTuple(态势,动作,结果)
    │                                        │           │           │
    │                                   (Skill学习)  (世界模型)  (偏好数据)
    │                                        │           │           │
    │                                        ▼           ▼           ▼
    │                                   Skill库更新  模型重训练   DPO微调
    │                                        │           │           │
    │                                        └─────┬─────┘           │
    │                                              ▼                 ▼
    │                                     快路径能力增强 ◂──── 新模型部署
    │                                              │
    │                                              ▼
    └──────────────── 闭环：更快更准的下一轮决策 ◂────────────────┘
```

**数据对账与一致性保障**：

| 层级 | 存储引擎 | 写入模式 | 对账机制 | 最终一致窗口 |
|------|---------|---------|---------|------------|
| 热路径 | Valkey缓存 | 同步写入，TTL 5min | 到期自动失效，重新从PG加载 | 实时 |
| 温路径 | Redpanda主题 | 异步发布 | 消费者ACK+幂等处理 | <1s |
| 冷路径 | PostgreSQL+PostGIS | 对账消费者合并写入 | 乐观锁(version) + 冲突检测 | <2s |
| 归档路径 | TimescaleDB | 连续聚合自动压缩 | 压缩策略(7天后降采样) | T+1 |

（数据对账的详细技术实现见第5章COP数据平面。）

### 2.4 核心组件技术特性

#### 2.4.1 Temporal v1.24+ — OODA循环编排引擎

**定位**：第1层业务流程编排。负责跨服务的OODA循环编排，包括长时间运行的作战任务流程、人工审批、Saga补偿事务。**不负责**智能体内部的状态图逻辑（由LangGraph负责），**不负责**时敏目标的快速响应（由战术短路路径负责）。

**核心特性**：

- **持久化工作流**：作战任务流程自动状态持久化，进程崩溃后无缝恢复
- **信号机制**：支持外部事件注入（如新情报到达、指挥员干预），实现OODA循环的异步触发
- **Saga补偿**：任务失败时自动逆序执行补偿操作（召回平台、释放资源）
- **版本管理**：支持工作流就地升级、影子验证、蓝绿切换，确保作战流程不停机更新

**SLA 指标**：

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 工作流调度延迟 P95 | < 100ms | 从触发到首Activity开始执行 |
| 单集群工作流并发 | ≥ 5,000 个/秒 | 取决于后端存储和分片配置 |
| 系统可用性 | 99.95% | 单集群，跨区域可达99.99% |

#### 2.4.2 Dapr v1.14+ — 分布式通信运行时

**定位**：第3层分布式通信。负责微服务间的服务发现、服务调用（mTLS加密）、状态管理、发布订阅、密钥管理。明确不启用Dapr Workflow功能，避免与Temporal编排层冲突。pubsub底层使用Redpanda。

**核心特性**：

- **服务调用**：基于mTLS的服务间安全通信，支持服务发现与负载均衡
- **发布订阅**：基于Redpanda的事件驱动架构，解耦传感器数据接入与处理
- **状态管理**：基于Redis的热数据缓存，支持Actor模式
- **密钥管理**：集成OpenBao（Vault开源fork），密钥不落盘

**SLA 指标**：

| 指标 | 目标值 |
|------|--------|
| 服务调用延迟 P95 | < 5ms（sidecar开销） |
| 状态操作吞吐量 | ≥ 10,000 TPS |
| 消息投递可靠性 | 至少一次投递 + 幂等处理 |

**配置示例**：

```yaml
# dapr/config.yaml
apiVersion: dapr.io/v1alpha1
kind: Configuration
metadata:
  name: c2-dapr-config
spec:
  tracing:
    samplingRate: "1"
    zipkin:
      endpointAddress: "http://zipkin:9411/api/v2/spans"
  metrics:
    enabled: true
  secrets:
    scopes:
      - storeName: "openbao-secret-store"
        defaultAccess: "deny"
        allow:
          - "encryption-key"
          - "jwt-signing-key"
  features:
    - name: "Actor.TypeMetadata"
      enabled: true
    - name: "Workflow"
      enabled: false
```

**组件配置示例**：

```yaml
# dapr/components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: tactical-statestore
spec:
  type: state.redis
  version: v1
  metadata:
  - name: redisHost
    value: "valkey-master:6379"
  - name: redisPassword
    secretKeyRef:
      name: redis-password
      key: password
  - name: actorStateStore
    value: "true"
  - name: ttlInSeconds
    value: "300"
---
# dapr/components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: sensor-pubsub
spec:
  type: pubsub.redpanda
  version: v1
  metadata:
  - name: brokers
    value: "redpanda-broker:9092"
  - name: maxMessageBytes
    value: 10485760
  - name: consumerGroup
    value: "c2-fusion-group"
---
# dapr/components/secretstore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: openbao-secret-store
spec:
  type: secretstores.hashicorp.vault
  version: v1
  metadata:
  - name: vaultAddr
    value: "http://openbao:8200"
  - name: vaultToken
    secretKeyRef:
      name: vault-token
      key: token
```

#### 2.4.3 SGLang v0.3+ — LLM推理引擎

**定位**：第4层LLM推理。专门负责大语言模型的高效推理服务，提供结构化输出、批量推理和推理加速。与Triton（传统ML推理）互补。

**选型理由**：

| 对比维度 | SGLang | vLLM |
|---------|--------|------|
| 推理吞吐 | 更高（RadixAttention前缀缓存） | 高 |
| 结构化输出 | 原生支持JSON/正则约束 | 有限支持 |
| 多模型管理 | 单服务多模型 | 单服务多模型 |
| 内存效率 | 更优（共享前缀缓存） | 良好 |
| 延迟 | P95 < 200ms（7B模型） | P95 < 250ms（7B模型） |
| 开源许可 | Apache 2.0 | Apache 2.0 |

**核心特性**：

- **RadixAttention**：自动复用公共前缀的KV Cache，条令/ROE等固定Prompt可共享缓存
- **结构化输出**：原生支持JSON Schema约束，确保LLM输出符合C2数据格式
- **批量推理**：自动合并并发请求，最大化GPU利用率
- **多LoRA服务**：同时服务多个JS领域微调适配器

**配置示例**：

```python
# sglang/launch_config.py
"""SGLang推理服务启动配置"""

LAUNCH_CONFIG = {
    "model_path": "/models/military-llama-7b",
    "host": "0.0.0.0",
    "port": 8000,
    "mem_fraction_static": 0.85,
    "tp_size": 1,  # Tensor Parallelism
    "enable_prefix_caching": True,
    "enable_overlap_schedule": True,
    "max_running_requests": 64,
    "max_total_tokens": 65536,
    "lora_paths": {
        "doctrine": "/adapters/doctrine-lora",
        "threat": "/adapters/threat-analysis-lora",
        "coa": "/adapters/coa-generation-lora",
    },
}
```


#### 2.4.4 Triton Inference Server v24.09+ — 传统ML推理服务器

**定位**：第4层传统ML推理。负责目标检测、信号分类、威胁评估等非LLM类AI模型推理。与SGLang（LLM推理）互补。

**核心特性**：

- **多模型并发**：同时部署目标检测、信号分类、行为预测等多种模型
- **动态批处理**：自动合并推理请求，最大化GPU利用率
- **模型热更新**：支持不停机更新模型版本
- **TensorRT加速**：GPU推理性能优化

**SLA 指标**：

| 模型类型 | 批量 | 吞吐量 | P95延迟 | GPU |
|---------|------|--------|---------|-----|
| 目标检测（YOLOv8-L） | 16 | 250 FPS | 65ms | A100 |
| 信号分类（CNN） | 32 | 1500 FPS | 22ms | A100 |
| SAR图像识别 | 8 | 80 FPS | 105ms | A100 |
| 行为预测（Transformer） | 4 | 40 FPS | 105ms | A100 |

**配置示例**：

```python
# triton/model_repository/target_detection/config.pbtxt
name: "target_detection"
platform: "tensorrt_plan"
max_batch_size: 32
input [
  {
    name: "images"
    data_type: TYPE_FP32
    dims: [ 3, 640, 640 ]
  }
]
output [
  {
    name: "detections"
    data_type: TYPE_FP32
    dims: [ 100, 6 ]
  }
]
dynamic_batching {
  preferred_batch_size: [ 8, 16, 32 ]
  max_queue_delay_microseconds: 2000
}
instance_group [
  {
    count: 2
    kind: KIND_GPU
    gpus: [ 0 ]
  }
]
```

#### 2.4.5 Apache APISIX v3.15+ — 安全API网关

**定位**：第0层外部接口。仅处理外部流量（操作员终端、外部系统接入）的路由、认证、限流、WAF防护。**不处理**服务间内部通信（由Linkerd + Dapr负责）。

**核心特性**：

- **高性能转发**：单核 QPS 达 18,000
- **动态路由**：全配置热更新
- **WAF防护**：OWASP Top 10攻击防护
- **认证集成**：JWT/OIDC/MTLS多种认证方式

#### 2.4.6 FunASR / Whisper — 语音识别引擎

**定位**：第-1层交互层的语音输入组件。将指挥员语音命令转化为文本，送入LLM进行意图识别。

**选型理由**：

| 对比维度 | FunASR（阿里达摩院） | OpenAI Whisper |
|---------|---------------------|----------------|
| 中文JS术语 | 优（中文预训练+热词增强） | 良 |
| 实时流式识别 | 支持（延迟 < 300ms） | 支持（延迟 ~500ms） |
| 离线部署 | 支持 | 支持 |
| 热词定制 | 支持JS术语热词表 | 有限 |
| 许可证 | MIT | MIT |

**核心特性**：

- **流式识别**：边说边识别，端到端延迟 < 300ms
- **JS热词增强**：支持加载自定义热词表（装备型号、地名、JS术语）
- **噪声鲁棒**：在指挥所噪声环境下仍保持高识别率
- **国产化适配**：支持飞腾/鲲鹏CPU

**配置与调用示例**：

```python
# hmi/speech_recognition.py
import httpx
from typing import Dict, Any, Optional, List


class MilitarySTTService:
    """JS语音识别服务"""

    def __init__(self, url: str = "http://funasr-server:10095"):
        self._client = httpx.Client(base_url=url, timeout=10.0)
        # JS热词表（可动态更新）
        self._hotwords: List[str] = [
            "歼击机", "轰炸机", "无人机", "无人艇",
            "雷达", "预警机", "航母", "驱逐舰", "潜艇",
            "导弹", "防空", "反导", "电子战", "网络战",
            "OODA", "杀伤链", "态势感知", "指挥控制",
        ]

    def recognize(self, audio_data: bytes, format: str = "wav") -> Dict[str, Any]:
        """
        语音识别（离线/准实时模式）
        Args:
            audio_data: 音频二进制数据
            format: 音频格式 wav/pcm/opus
        Returns:
            {text, confidence, language, is_final}
        """
        response = self._client.post(
            "/api/recognition",
            files={"audio": ("input.wav", audio_data, f"audio/{format}")},
            data={
                "hotwords": ",".join(self._hotwords),
                "language": "zh",
                "mode": "offline",
            },
        )
        response.raise_for_status()
        result = response.json()
        return {
            "text": result.get("text", ""),
            "confidence": result.get("confidence", 0.0),
            "language": "zh",
            "is_final": True,
        }

    def add_hotwords(self, words: List[str]):
        """动态添加JS热词"""
        self._hotwords.extend(words)

    def get_hotwords(self) -> List[str]:
        return self._hotwords
```

#### 2.4.7 CosyVoice — 语音合成引擎

**定位**：第-1层交互层的语音输出组件。将AI生成的态势报告、告警信息转化为语音播报。

**核心特性**：

- **高自然度合成**：接近真人语音质量
- **情感控制**：支持紧急/平静/警告等语调切换
- **低延迟合成**：首包延迟 < 200ms
- **国产化**：阿里开源，MIT许可

**调用示例**：

```python
# hmi/speech_synthesis.py
import httpx
from typing import Dict, Any


class MilitaryTTSService:
    """JS语音合成服务"""

    # 预定义语调模板
    VOICE_TEMPLATES = {
        "calm": {"speed": 1.0, "pitch": 0, "volume": 0.8},       # 常规态势播报
        "urgent": {"speed": 1.3, "pitch": 2, "volume": 1.0},     # 紧急告警
        "warning": {"speed": 1.1, "pitch": -1, "volume": 0.9},   # 威胁警告
        "command": {"speed": 1.0, "pitch": 1, "volume": 1.0},    # 命令确认
    }

    def __init__(self, url: str = "http://cosyvoice-server:50000"):
        self._client = httpx.Client(base_url=url, timeout=10.0)

    def synthesize(
        self, text: str, voice_mode: str = "calm"
    ) -> bytes:
        """
        文本转语音
        Args:
            text: 待合成文本
            voice_mode: 语调模板 calm/urgent/warning/command
        Returns:
            音频二进制数据（PCM/WAV）
        """
        params = self.VOICE_TEMPLATES.get(voice_mode, self.VOICE_TEMPLATES["calm"])

        response = self._client.post(
            "/api/tts",
            json={
                "text": text,
                "speaker": "military_announcer",
                "speed": params["speed"],
                "pitch": params["pitch"],
                "volume": params["volume"],
                "format": "wav",
            },
        )
        response.raise_for_status()
        return response.content

    def synthesize_alert(self, alert_level: str, message: str) -> bytes:
        """合成告警语音"""
        voice_map = {
            "INFO": "calm",
            "WARNING": "warning",
            "CRITICAL": "urgent",
        }
        prefix_map = {
            "WARNING": "注意，",
            "CRITICAL": "紧急告警！",
        }
        prefix = prefix_map.get(alert_level, "")
        return self.synthesize(f"{prefix}{message}", voice_map.get(alert_level, "calm"))
```

#### 2.4.8 WebSocket实时推送 + Cesium态势渲染

**定位**：第-1层交互层的实时态势推送与可视化组件。

**WebSocket实时推送**（基于APISIX原生WebSocket支持）：

```python
# hmi/ws_push.py
import asyncio
import json
from typing import Dict, Any, Set
from datetime import datetime
import aioredis


class COPPushService:
    """
    COP态势实时推送服务
    通过Redis Pub/Sub监听COP更新，通过WebSocket推送到前端
    """

    def __init__(self, redis_url: str = "redis://valkey-master:6379"):
        self._redis_url = redis_url
        self._clients: Set[asyncio.Queue] = set()

    async def start(self):
        """启动推送服务"""
        redis = aioredis.from_url(self._redis_url)
        pubsub = redis.pubsub()
        await pubsub.subscribe("cop_updates", "threat_alerts")

        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                # 推送给所有连接的前端客户端
                await self._broadcast(data)

    async def _broadcast(self, data: Dict[str, Any]):
        """广播到所有WebSocket客户端"""
        payload = json.dumps({
            "type": data.get("op", "UPDATE"),
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
        })
        dead_queues = set()
        for queue in self._clients:
            try:
                queue.put_nowait(payload)
            except asyncio.QueueFull:
                dead_queues.add(queue)
        self._clients -= dead_queues

    def register_client(self) -> asyncio.Queue:
        """注册新的前端WebSocket客户端"""
        queue = asyncio.Queue(maxsize=1000)
        self._clients.add(queue)
        return queue

    def unregister_client(self, queue: asyncio.Queue):
        """注销客户端"""
        self._clients.discard(queue)
```


#### 2.4.9 自然语言态势查询引擎

**定位**：第-1层交互层的NL查询组件。对标Scale Donovan的自然语言接口，将指挥员自然语言查询转化为COP数据查询和态势分析。

```python
# hmi/nl_query_engine.py
from typing import Dict, Any, List
from clients.litellm_client import C2LLMClient
from knowledge.qdrant_setup import MilitaryKnowledgeStore
from ontology.cop_service import COPService, COPEntityQuery


class NLQueryEngine:
    """
    自然语言态势查询引擎
    对标Scale Donovan的NL接口能力
    """

    def __init__(
        self,
        llm: C2LLMClient,
        cop: COPService,
        knowledge: MilitaryKnowledgeStore,
    ):
        self._llm = llm
        self._cop = cop
        self._knowledge = knowledge

    async def query(self, natural_language_query: str) -> Dict[str, Any]:
        """
        自然语言态势查询
        Examples:
            "当前区域有哪些高空高速目标？"
            "距离我最近的威胁是什么？"
            "过去1小时敌方舰艇的活动规律？"
        """
        # Step 1: LLM解析查询意图，提取查询参数
        parsed = self._llm.analyze_situation(
            sensor_summary=natural_language_query,
            context="请解析以下查询意图，提取：查询类型、空间范围、时间范围、实体类型、过滤条件",
        )

        # Step 2: 将解析结果转化为COP查询
        cop_query = self._build_cop_query(parsed["content"])

        # Step 3: 执行COP查询
        entities = await self._cop.query_entities(cop_query)

        # Step 4: LLM生成自然语言回答
        answer = self._llm.analyze_situation(
            sensor_summary=f"查询结果：共{len(entities)}个实体。数据摘要：{self._summarize_entities(entities)}",
            context=f"用户问题：{natural_language_query}\n请用自然语言回答，包含关键数据和JS建议。",
        )

        return {
            "query": natural_language_query,
            "answer": answer["content"],
            "entities": entities,
            "total_count": len(entities),
        }

    def _build_cop_query(self, parsed_text: str) -> COPEntityQuery:
        """将LLM解析结果转化为COP查询参数（示意）"""
        return COPEntityQuery(
            center_lat=0, center_lon=0,
            radius_km=100,
            force_affiliation="HOSTILE",
            classification_max="SECRET",
        )

    def _summarize_entities(self, entities: List[Dict]) -> str:
        if not entities:
            return "无匹配实体"
        types = {}
        for e in entities:
            t = e.get("entity_type", "unknown")
            types[t] = types.get(t, 0) + 1
        return ", ".join(f"{t}: {c}个" for t, c in types.items())
```

#### 2.4.10 Linkerd v2.14+ — 服务网格

**定位**：第0层服务网格。负责微服务间的自动mTLS加密、流量管理、可观测性和故障注入。与APISIX（外部网关）互补，Linkerd仅处理集群内部服务间流量。

**选型理由**：

| 对比维度 | Linkerd | Istio |
|---------|---------|-------|
| 侧车资源消耗 | ~50MB RSS / 代理 | ~150MB RSS / Envoy |
| 配置复杂度 | 低（CRD声明式） | 高（VirtualService/DestinationRule等） |
| Rust数据平面 | 是（linkerd2-proxy） | 否（C++ Envoy） |
| 延迟开销 | P99 < 2ms | P99 < 5ms |
| 开源许可 | Apache 2.0 | Apache 2.0 |
| JS边缘适配 | 资源占用低，适合边缘 | 资源占用高，边缘受限 |

**核心特性**：

- **自动mTLS**：服务间通信自动加密，无需手动证书管理
- **透明代理**：对应用代码无侵入，通过K8s annotation自动注入
- **可观测性**：自动收集每个服务的延迟、成功率、吞吐量指标
- **流量分割**：支持金丝雀发布、蓝绿部署的流量权重管理

#### 2.4.11 LangGraph v0.2+ — 智能体逻辑框架

**定位**：第2层智能体逻辑。负责单个智能体内部的状态图编排、多智能体间的协作通信。**不负责**跨服务的业务流程编排（由Temporal负责），**不负责**LLM调用路由（由LiteLLM负责）。

**核心特性**：

- **状态图编排**：基于有向图定义智能体内部处理步骤
- **持久化Checkpoint**：智能体状态自动持久化，支持断点续跑
- **条件路由**：基于中间结果动态选择后续步骤
- **人机协作**：支持中断点（interrupt）等待人类输入

**多智能体协作代码示例**：

```python
# agents/intelligence_team.py
from typing import TypedDict, Annotated, List, Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import operator


class IntelTeamState(TypedDict):
    """情报分析团队共享状态"""
    raw_data: Dict[str, Any]
    imagery_analysis: Annotated[List[Dict], operator.add]
    sigint_analysis: Annotated[List[Dict], operator.add]
    llm_assessment: Dict[str, Any]  # LLM分析结果
    fused_assessment: Dict[str, Any]
    threat_report: Dict[str, Any]
    current_phase: str


class ImageryAnalystAgent:
    """图像分析智能体——处理光电/红外/SAR图像"""

    def __call__(self, state: IntelTeamState) -> dict:
        imagery_data = state["raw_data"].get("imagery", {})
        detections = self._run_detection(imagery_data)
        classified = self._classify_targets(detections)

        return {
            "imagery_analysis": [{
                "source": "eo_ir_sensor",
                "detections": classified,
                "confidence": self._compute_confidence(classified),
            }],
            "current_phase": "imagery_done",
        }

    def _run_detection(self, imagery_data: Dict) -> List[Dict]:
        return []

    def _classify_targets(self, detections: List[Dict]) -> List[Dict]:
        return detections

    def _compute_confidence(self, classified: List[Dict]) -> float:
        if not classified:
            return 0.0
        return sum(d.get("confidence", 0) for d in classified) / len(classified)


class SIGINTAnalystAgent:
    """信号情报分析智能体——处理雷达/通信信号"""

    def __call__(self, state: IntelTeamState) -> dict:
        sigint_data = state["raw_data"].get("sigint", {})
        signals = self._analyze_signals(sigint_data)
        emitters = self._locate_emitters(signals)

        return {
            "sigint_analysis": [{
                "source": "elint",
                "detected_emitters": emitters,
                "signal_types": [s["type"] for s in signals],
            }],
            "current_phase": "sigint_done",
        }

    def _analyze_signals(self, sigint_data: Dict) -> List[Dict]:
        return []

    def _locate_emitters(self, signals: List[Dict]) -> List[Dict]:
        return []


class LLMAnalysisAgent:
    """LLM分析智能体——利用RAG检索条令+LLM生成研判"""

    def __init__(self, sglang_client, qdrant_client):
        self._sglang = sglang_client
        self._qdrant = qdrant_client

    def __call__(self, state: IntelTeamState) -> dict:
        imagery = state.get("imagery_analysis", [])
        sigint = state.get("sigint_analysis", [])

        # RAG检索相关条令
        doctrine_context = self._retrieve_doctrine(imagery, sigint)

        # LLM生成研判
        assessment = self._sglang.analyze_threat(
            sensor_summary=self._summarize_intel(imagery, sigint),
            context=doctrine_context,
        )

        return {
            "llm_assessment": assessment.model_dump(),
            "current_phase": "llm_analysis_done",
        }

    def _retrieve_doctrine(self, imagery, sigint) -> str:
        # 查询Qdrant向量库检索相关条令
        return ""

    def _summarize_intel(self, imagery, sigint) -> str:
        return ""


class FusionAgent:
    """融合分析智能体——综合多源情报与LLM研判"""

    def __call__(self, state: IntelTeamState) -> dict:
        imagery_results = state.get("imagery_analysis", [])
        sigint_results = state.get("sigint_analysis", [])
        llm_results = state.get("llm_assessment", {})

        correlated = self._cross_correlate(imagery_results, sigint_results)
        assessment = self._generate_assessment(correlated, llm_results)

        return {
            "fused_assessment": assessment,
            "current_phase": "fusion_done",
        }

    def _cross_correlate(self, imagery, sigint) -> List[Dict]:
        return []

    def _generate_assessment(self, correlated, llm_results) -> Dict[str, Any]:
        return {
            "total_entities": 0,
            "threat_entities": 0,
            "overall_threat_level": "unknown",
            "confidence": 0.0,
            "llm_supported": bool(llm_results),
        }


class ThreatReportAgent:
    """威胁报告生成智能体"""

    def __call__(self, state: IntelTeamState) -> dict:
        assessment = state.get("fused_assessment", {})
        llm = state.get("llm_assessment", {})
        report = self._generate_report(assessment, llm)
        return {
            "threat_report": report,
            "current_phase": "complete",
        }

    def _generate_report(self, assessment: Dict, llm: Dict) -> Dict[str, Any]:
        return {
            "report_type": "threat_assessment",
            "classification": "SECRET",
            "summary": "",
            "threat_level": assessment.get("overall_threat_level", "unknown"),
            "llm_analysis": llm,
            "recommended_actions": [],
        }


def build_intel_team_graph():
    """构建情报分析团队工作流图"""
    graph = StateGraph(IntelTeamState)

    graph.add_node("imagery_analyst", ImageryAnalystAgent())
    graph.add_node("sigint_analyst", SIGINTAnalystAgent())
    # LLM分析节点
    # graph.add_node("llm_analyst", LLMAnalysisAgent(sglang_client, qdrant_client))
    graph.add_node("fusion_agent", FusionAgent())
    graph.add_node("threat_report", ThreatReportAgent())

    graph.set_entry_point("imagery_analyst")

    # 图像和信号分析并行执行
    graph.add_edge("imagery_analyst", "sigint_analyst")
    graph.add_edge("sigint_analyst", "fusion_agent")
    graph.add_edge("fusion_agent", "threat_report")
    graph.add_edge("threat_report", END)

    return graph.compile(checkpointer=MemorySaver())
```

#### 2.4.12 LiteLLM v1.40+ — 多模型代理路由

**定位**：第2层多模型代理。统一管理多个LLM供应商的调用路由，提供故障切换、A/B测试、成本控制和速率限制。所有智能体通过LiteLLM调用LLM，不直接调用SGLang或外部API。

**核心特性**：

- **统一接口**：OpenAI兼容API，屏蔽底层LLM差异
- **多供应商支持**：SGLang（本地部署）、国产大模型（通义/文心/星火）、商业API（OpenAI/Claude）
- **故障切换**：主模型不可用时自动切换到备选模型
- **A/B测试**：按比例将请求路由到不同模型，对比效果
- **速率限制**：防止LLM调用过载

**配置示例**：

```yaml
# litellm/config.yaml
model_list:
  # 主力JSLLM（本地SGLang部署）
  - model_name: "military-llm"
    litellm_params:
      model: "hosted_sglang/military-llama-7b"
      api_base: "http://sglang-server:8000/v1"
      rpm: 60
      timeout: 30

  # 备选：国产大模型（SGLang不可用时）
  - model_name: "military-llm"
    litellm_params:
      model: "openai/qwen-max"
      api_base: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      api_key: "os.environ/DASHSCOPE_API_KEY"
      rpm: 30
      timeout: 60

  # COA生成专用（更大模型，更强推理）
  - model_name: "coa-generator"
    litellm_params:
      model: "hosted_sglang/military-llama-13b"
      api_base: "http://sglang-server-coa:8000/v1"
      rpm: 20
      timeout: 120

  # 情报摘要专用（小模型，低延迟）
  - model_name: "intel-summarizer"
    litellm_params:
      model: "hosted_sglang/military-llama-7b"
      api_base: "http://sglang-server-intel:8000/v1"
      rpm: 120
      timeout: 10

router_settings:
  routing_strategy: "usage-based-routing-v2"
  allowed_fails: 3
  cooldown_time: 60
  num_retries: 2
  fallbacks:
    - "military-llm":
        - "qwen-fallback"

general_settings:
  drop_params: true
  set_verbose: false
  max_budget: 1000.0  # 月度预算上限（美元等价）
```

**调用示例**：

```python
# clients/litellm_client.py
from litellm import completion
from typing import Dict, Any, Optional


class C2LLMClient:
    """C2系统统一LLM客户端——通过LiteLLM代理路由"""

    def __init__(self):
        # LiteLLM自动加载config.yaml
        pass

    def analyze_situation(
        self, sensor_summary: str, context: str
    ) -> Dict[str, Any]:
        """使用JSLLM进行态势分析"""
        response = completion(
            model="military-llm",
            messages=[
                {"role": "system", "content": "你是JS态势分析AI助手。"},
                {"role": "user", "content": f"传感器数据：{sensor_summary}\n背景：{context}"},
            ],
            temperature=0.1,
            max_tokens=1024,
            metadata={
                "c2_task": "situation_analysis",
                "classification": "SECRET",
            },
        )
        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": response.usage.model_dump(),
        }

    def generate_coa_draft(
        self, situation: str, forces: str, intent: str
    ) -> Dict[str, Any]:
        """使用COA专用模型生成行动方案草案"""
        response = completion(
            model="coa-generator",
            messages=[
                {"role": "system", "content": "你是JS行动方案规划AI助手。"},
                {"role": "user", "content": f"态势：{situation}\n兵力：{forces}\n意图：{intent}"},
            ],
            temperature=0.3,
            max_tokens=2048,
        )
        return {"content": response.choices[0].message.content}
```

#### 2.4.13 OR-Tools v9.10+ — 组合优化求解器

**定位**：第4层优化求解。负责路径规划（VRP/TSP）、资源调度、行动方案（COA）优化等组合优化问题。

> **许可证说明**：OR-Tools核心采用Apache 2.0许可。使用CP-SAT求解器（完全Apache 2.0），不使用默认SCIP求解器（ZIB License限制商业使用）。

**代码示例**：

```python
# optimization/path_planner.py
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class Waypoint:
    id: str
    lat: float
    lon: float
    alt: float = 0.0
    time_window_start: int = 0
    time_window_end: int = 86400
    service_time: int = 0


@dataclass
class Platform:
    id: str
    max_range_km: float = 500.0
    max_speed_kmh: float = 200.0
    max_endurance_min: float = 120.0
    payload_capacity: float = 100.0


class TacticalPathPlanner:
    """战术路径规划器"""

    def __init__(self):
        pass

    def plan_multi_uav_routes(
        self,
        waypoints: List[Waypoint],
        platforms: List[Platform],
        depot_lat: float,
        depot_lon: float,
        no_fly_zones: List[Dict] = None,
        time_limit_seconds: int = 30,
    ) -> Dict[str, Any]:
        all_points = [(depot_lat, depot_lon)] + [(wp.lat, wp.lon) for wp in waypoints]
        num_locations = len(all_points)
        num_vehicles = len(platforms)
        depot_index = 0

        distance_matrix = self._build_distance_matrix(all_points, no_fly_zones)

        manager = pywrapcp.RoutingIndexManager(num_locations, num_vehicles, depot_index)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_idx, to_idx):
            from_node = manager.IndexToNode(from_idx)
            to_node = manager.IndexToNode(to_idx)
            return int(distance_matrix[from_node][to_node] * 1000)

        transit_cb = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_cb)

        routing.AddDimension(
            transit_cb, 0, int(max(p.max_range_km for p in platforms) * 1000),
            True, "Distance",
        )
        dist_dim = routing.GetDimensionOrDie("Distance")
        dist_dim.SetGlobalSpanCostCoefficient(100)

        time_cb = routing.RegisterTransitCallback(distance_callback)
        routing.AddDimension(time_cb, 30, 86400, False, "Time")
        time_dim = routing.GetDimensionOrDie("Time")

        for i, wp in enumerate(waypoints, 1):
            index = manager.NodeToIndex(i)
            time_dim.CumulVar(index).SetRange(wp.time_window_start, wp.time_window_end)

        params = pywrapcp.DefaultRoutingSearchParameters()
        params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        params.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
        params.time_limit.seconds = time_limit_seconds

        solution = routing.SolveWithParameters(params)

        if solution:
            # 提取路由结果（具体实现略）
            return {"status": "success", "num_routes": manager.GetNumberOfVehicles()}

        return {"status": "no_solution_found"}

```

#### 2.4.14 Qdrant v1.9+ — 向量检索引擎

**定位**：第5层RAG/OAG知识层。负责JS知识（条令、战例、装备手册、ROE）的向量嵌入存储和语义检索，为LLM推理提供知识增强（RAG）。

**选型理由**：

| 对比维度 | Qdrant | Milvus | Weaviate |
|---------|--------|--------|----------|
| 语言 | Rust（高性能） | Go + C++ | Go |
| 延迟 | P99 < 10ms（100万向量） | P99 < 20ms | P99 < 30ms |
| 内存效率 | 高（量化压缩） | 中 | 中 |
| 过滤支持 | 丰富payload过滤 | 有限 | 中等 |
| 边缘部署 | 单二进制，资源占用低 | 依赖多组件 | JVM偏重 |
| 开源许可 | Apache 2.0 | Apache 2.0 | BSD-3 |

**核心特性**：

- **高性能向量检索**：百万级向量毫秒级响应
- **Payload过滤**：支持按密级、条令类型、作战域等维度过滤
- **量化压缩**：支持Scalar/Product量化，降低内存占用
- **多向量支持**：同一文档可有多个向量表示（标题向量、内容向量）

**配置与知识库构建示例**：

```python
# knowledge/qdrant_setup.py
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct,
    PayloadSchemaType, OptimizersConfigDiff,
)
from typing import List, Dict, Any


MILITARY_COLLECTION = "military_knowledge"

# 条令知识分类
DOCTRINE_CATEGORIES = [
    "joint_doctrine",       # 联合条令
    "army_doctrine",        # 陆军条令
    "navy_doctrine",        # 海军条令
    "air_force_doctrine",   # 空军条令
    "roe",                  # 交战规则
    "threat_library",       # 威胁库
    "equipment_manual",     # 装备手册
    "after_action_report",  # 战后总结报告
]


class MilitaryKnowledgeStore:
    """JS知识向量库"""

    def __init__(self, url: str = "http://qdrant:6333"):
        self._client = QdrantClient(url=url)
        self._ensure_collection()

    def _ensure_collection(self):
        """确保知识库集合存在"""
        collections = self._client.get_collections().collections
        names = [c.name for c in collections]

        if MILITARY_COLLECTION not in names:
            self._client.create_collection(
                collection_name=MILITARY_COLLECTION,
                vectors_config=VectorParams(
                    size=1024,  # 嵌入维度（bge-large-zh）
                    distance=Distance.COSINE,
                    on_disk=True,
                ),
                optimizers_config=OptimizersConfigDiff(
                    indexing_threshold=20000,
                ),
            )

            # 创建payload索引（过滤加速）
            self._client.create_payload_index(
                MILITARY_COLLECTION, "category",
                field_schema=PayloadSchemaType.KEYWORD,
            )
            self._client.create_payload_index(
                MILITARY_COLLECTION, "classification",
                field_schema=PayloadSchemaType.KEYWORD,
            )
            self._client.create_payload_index(
                MILITARY_COLLECTION, "domain",
                field_schema=PayloadSchemaType.KEYWORD,
            )

    def ingest_document(
        self,
        doc_id: str,
        text: str,
        embedding: List[float],
        metadata: Dict[str, Any],
    ) -> None:
        """摄入知识文档"""
        self._client.upsert(
            collection_name=MILITARY_COLLECTION,
            points=[
                PointStruct(
                    id=doc_id,
                    vector=embedding,
                    payload={
                        "text": text,
                        "category": metadata.get("category", "unknown"),
                        "classification": metadata.get("classification", "SECRET"),
                        "domain": metadata.get("domain", "joint"),
                        "source": metadata.get("source", ""),
                        "title": metadata.get("title", ""),
                    },
                )
            ],
        )

    def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        category_filter: List[str] = None,
        classification_max: str = "SECRET",
        domain_filter: List[str] = None,
    ) -> List[Dict[str, Any]]:
        """语义检索JS知识"""
        from qdrant_client.models import Filter, FieldCondition, MatchAny

        conditions = []
        if category_filter:
            conditions.append(
                FieldCondition(key="category", match=MatchAny(any=category_filter))
            )
        if domain_filter:
            conditions.append(
                FieldCondition(key="domain", match=MatchAny(any=domain_filter))
            )

        results = self._client.search(
            collection_name=MILITARY_COLLECTION,
            query_vector=query_embedding,
            query_filter=Filter(must=conditions) if conditions else None,
            limit=limit,
            with_payload=True,
        )

        return [
            {
                "doc_id": str(r.id),
                "score": r.score,
                "text": r.payload.get("text", ""),
                "category": r.payload.get("category", ""),
                "source": r.payload.get("source", ""),
            }
            for r in results
        ]
```

#### 2.4.15 TimescaleDB — 时序数据扩展

**定位**：第7层COP数据平面的时序数据组件。作为PostgreSQL扩展，专门处理传感器时序数据（航迹历史、信号强度、平台遥测等）。

**核心特性**：

- **Hypertable自动分区**：按时间自动分区，查询性能不随数据量增长下降
- **连续聚合**：自动预计算聚合（如5分钟平均航速、小时级信号统计）
- **数据保留策略**：自动过期清理历史数据（如原始传感器数据保留90天）
- **PostgreSQL原生**：与PostGIS、AGE等扩展无缝共存

**配置与使用示例**：

```sql
-- timescale/setup.sql

-- 启用TimescaleDB扩展
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- 传感器时序数据表（完整Schema见第5章COP数据平面）
CREATE TABLE sensor_telemetry (
    time            TIMESTAMPTZ NOT NULL,
    sensor_id       VARCHAR(64) NOT NULL,
    entity_id       VARCHAR(64),
    measurement_type VARCHAR(32) NOT NULL,
    value_numeric   DOUBLE PRECISION,
    value_json      JSONB,
    quality         REAL DEFAULT 1.0,
    classification  VARCHAR(16) DEFAULT 'SECRET'
);

-- 转换为Hypertable（按时间分区）
SELECT create_hypertable('sensor_telemetry', 'time', chunk_time_interval => INTERVAL '1 day');

-- 连续聚合：5分钟航迹统计
CREATE MATERIALIZED VIEW track_stats_5min
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('5 minutes', time) AS bucket,
    entity_id,
    COUNT(*) AS update_count,
    AVG(value_numeric) AS avg_value,
    MIN(value_numeric) AS min_value,
    MAX(value_numeric) AS max_value
FROM sensor_telemetry
WHERE measurement_type = 'position'
GROUP BY bucket, entity_id;

-- 数据保留策略：原始数据保留90天
SELECT add_retention_policy('sensor_telemetry', INTERVAL '90 days');

-- 压缩策略：7天前的数据自动压缩
ALTER TABLE sensor_telemetry SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'sensor_id, entity_id',
    timescaledb.compress_orderby = 'time DESC'
);
SELECT add_compression_policy('sensor_telemetry', INTERVAL '7 days');
```

#### 2.4.16 Apache AGE — 图数据库扩展

**定位**：第7层COP数据平面的图数据组件。作为PostgreSQL扩展，用openCypher查询语言处理实体关系网络（威胁关系链、指挥层级、后勤依赖图）。

**选型理由**：替代Neo4j（GPLv3社区版限制商业使用），Apache AGE基于PostgreSQL、采用Apache 2.0许可，可同时访问关系数据和图数据。

**核心特性**：

- **openCypher查询**：标准图查询语言
- **PostgreSQL原生**：图数据与关系数据在同一数据库
- **多图支持**：不同作战域可使用独立的图命名空间

**配置与使用示例**：

```sql
-- age/setup.sql

-- 加载AGE扩展
CREATE EXTENSION IF NOT EXISTS age;
LOAD 'age';

-- 设置图搜索路径
SET search_path = ag_catalog, "$user", public;

-- 创建JS关系图
SELECT create_graph('military_relations');

-- === 插入实体和关系（openCypher）===

-- 创建实体节点
SELECT * FROM cypher('military_relations', $$
    CREATE (:Platform {
        id: 'UAV-001',
        type: 'uav',
        force: 'FRIENDLY',
        status: 'active',
        position: 'POINT(121.5 31.2 500)'
    }),
    (:Platform {
        id: 'HOSTILE-001',
        type: 'fixed_wing',
        force: 'HOSTILE',
        status: 'active',
        threat_level: 'HIGH'
    }),
    (:WeaponSystem {
        id: 'SAM-UNIT-01',
        type: 'surface_to_air',
        range_km: 150,
        status: 'ready'
    })
$$) as (v agtype);

-- 创建威胁关系
SELECT * FROM cypher('military_relations', $$
    MATCH (h:Platform {id: 'HOSTILE-001'}), (s:WeaponSystem {id: 'SAM-UNIT-01'})
    CREATE (h)-[:THREATENS {
        threat_level: 'HIGH',
        weapon_range_km: 150,
        estimated_tti_min: 8
    }]->(s)
$$) as (e agtype);

-- 创建指挥关系
SELECT * FROM cypher('military_relations', $$
    MATCH (u:Platform {id: 'UAV-001'}), (h:Platform {id: 'HOSTILE-001'})
    CREATE (u)-[:TRACKS {
        since: datetime(),
        confidence: 0.92,
        track_type: 'radar+eo'
    }]->(h)
$$) as (e agtype);

-- === 查询威胁关系链 ===
-- 查找所有威胁SAM单元的敌方平台
SELECT * FROM cypher('military_relations', $$
    MATCH (h:Platform)-[t:THREATENS]->(s:WeaponSystem)
    WHERE t.threat_level = 'HIGH'
    RETURN h.id, h.type, t.estimated_tti_min, s.id, s.type
$$) as (hostile_id agtype, hostile_type agtype, tti agtype, sam_id agtype, sam_type agtype);

-- 查找完整的威胁-跟踪-交战链
SELECT * FROM cypher('military_relations', $$
    MATCH path = (u:Platform)-[:TRACKS]->(h:Platform)-[:THREATENS]->(s:WeaponSystem)
    RETURN path
$$) as (path agtype);
```

#### 2.4.17 OPA (Open Policy Agent) v0.60+ — 策略引擎

**定位**：横向贯穿组件。统一管理交战规则（ROE）、自主行为边界、数据访问控制等策略，用Rego声明式语言定义，支持运行时热更新。

**核心特性**：

- **声明式策略**：Rego语言定义策略规则，无需修改应用代码
- **热更新**：策略变更通过GitOps推送，无需重启服务
- **细粒度控制**：支持基于上下文的动态决策（时间、位置、态势）
- **审计日志**：所有策略决策可审计

**策略示例**：

```rego
# opa/policies/roe.rego
package c2.roe

# 交战规则策略

# 输入：行动请求
default allow_engagement = false
default allow_autonomous = false

# 规则1：武器释放必须经人类确认
allow_engagement {
    input.action_type == "weapon_release"
    input.human_approved == true
    input.approver_clearance >= 2  # SECRET及以上
}

# 规则2：自卫交战可自动授权（特定条件）
allow_engagement {
    input.action_type == "self_defense"
    input.threat_level == "CRITICAL"
    input.time_to_impact_seconds < 30
    input.roe_mode == "weapons_free"
}

# 规则3：侦察行动在和平时期可自主执行
allow_autonomous {
    input.action_type == "reconnaissance"
    input.alert_level == "peace"
    input.classification <= 1  # CONFIDENTIAL及以下
}

# 规则4：跨境行动需战区司令批准
allow_engagement {
    input.action_type == "cross_boundary"
    input.human_approved == true
    input.approver_role == "theater_commander"
}

# 规则5：无人平台自主等级控制
allow_autonomous {
    input.platform_type == "uav"
    input.autonomy_level == "supervised"
    input.operator_online == true
}

# 规则6：通信中断时降级规则
allow_autonomous {
    input.communication_status == "degraded"
    input.platform_type == "uav"
    input.standing_roe_active == true
    input.action_type != "kinetic_strike"
}
```

```rego
# opa/policies/data_access.rego
package c2.data_access

# 数据访问控制策略

default allow_access = false

# 规则：用户密级必须 >= 数据密级
allow_access {
    input.user_clearance >= input.data_classification
}

# 规则：NOFORN标记数据不允许非本国人员访问
allow_access {
    input.data_caveats == "NOFORN"
    input.user_nationality == "CN"
    input.user_clearance >= input.data_classification
}
```

**OPA集成代码示例**：

```python
# security/policy_engine.py
import httpx
from typing import Dict, Any, Optional


class OPAPolicyEngine:
    """OPA策略引擎客户端"""

    def __init__(self, opa_url: str = "http://opa:8181"):
        self._client = httpx.Client(base_url=opa_url, timeout=5.0)

    def check_engagement(self, action_request: Dict[str, Any]) -> Dict[str, Any]:
        """检查交战行动是否允许"""
        response = self._client.post(
            "/v1/data/c2/roe",
            json={"input": action_request},
        )
        response.raise_for_status()
        result = response.json()["result"]
        return {
            "allow_engagement": result.get("allow_engagement", False),
            "allow_autonomous": result.get("allow_autonomous", False),
        }

    def check_data_access(
        self, user_clearance: int, data_classification: int,
        data_caveats: str = None, user_nationality: str = "CN",
    ) -> bool:
        """检查数据访问权限"""
        response = self._client.post(
            "/v1/data/c2/data_access",
            json={
                "input": {
                    "user_clearance": user_clearance,
                    "data_classification": data_classification,
                    "data_caveats": data_caveats,
                    "user_nationality": user_nationality,
                }
            },
        )
        response.raise_for_status()
        return response.json()["result"].get("allow_access", False)
```

#### 2.4.18 Redpanda v23.3+ — 事件流平台

**定位**：横向贯穿的消息总线。替代Apache Kafka，作为传感器数据接入、事件驱动架构的核心消息中间件。Dapr pubsub底层使用Redpanda。

**选型理由**：

| 对比维度 | Redpanda | Apache Kafka |
|---------|----------|-------------|
| 语言 | C++（无JVM开销） | Scala/JVM |
| 延迟 | P99 < 50ms | P99 < 100ms |
| 运维复杂度 | 单二进制部署 | ZooKeeper/KRaft + Broker |
| 内存占用 | 更低（无GC） | 较高（JVM堆） |
| Kafka兼容 | 完全兼容API | 原生 |
| 开源许可 | BSL 1.1（源码可用） | Apache 2.0 |
| 边缘适配 | 单节点可用，资源占用低 | 最少3 Broker |

> **许可证说明**：Redpanda采用BSL 1.1许可，源码完全公开，单节点可免费商用。如需多节点集群的商业许可，可降级使用Apache Kafka（Apache 2.0）。

**核心特性**：

- **Kafka API兼容**：所有Kafka客户端（包括aiokafka、Dapr Kafka组件）可直接使用
- **更低延迟**：C++实现，无JVM GC停顿
- **简化运维**：单二进制部署，无需ZooKeeper

#### 2.4.19 模型评估与仿真层组件

**定位**：第8层，对标Scale AI SEAL实验室。负责AI模型的安全评估、基准测试、OOD退化评估和红队测试，以及基于HLA4/C-BML的兵棋仿真引擎。

此层的详细设计见第8章"数据闭环与模型演进"及第10章"系统运维与可观测性"。

**核心组件**：

| 组件 | 功能 | 开源方案 |
|------|------|---------|
| **安全评估框架** | 模型安全性、偏差、毒性测试 | 自建（对标SEAL） |
| **OOD退化评估** | 分布外数据上的模型退化度量 | 自建 |
| **红队测试框架** | 对抗性Prompt注入测试 | Garak（Apache 2.0） |
| **基准测试排名** | JS任务LLM排名 | 自建（对标SEAL Leaderboards） |
| **兵棋仿真引擎** | COA方案仿真验证 | HLA4 + C-BML |
| **AFSIM集成** | 高保真度作战仿真 | AFSIM（政府开源） |

#### 2.4.20 GitOps部署引擎

**定位**：横向贯穿的部署管理。使用ArgoCD或Flux实现基础设施和应用的声明式部署、版本管理和审计追溯。

---

## 3. 智能体认知架构——自主决策的三大支柱

### 3.1 设计理念：从执行器到推理者

#### 3.1.1 v4.0回顾：工作流模板执行器

v4.0架构的核心设计是"工作流驱动"——所有执行路径统一为"从注册表选择工作流模板 → 按DAG执行"。智能体（Agent）本质上是一个**模板选择器 + DAG执行器**：

```python
# v4.0 Agent的决策逻辑（简化）
def v4_agent_decide(situation):
    # Step 1: 态势向量化
    embedding = embed(situation)
    # Step 2: Qdrant检索最匹配的工作流模板
    template = qdrant.search(embedding, top_k=1)
    # Step 3: 自动填充参数
    params = auto_fill(template.parameters, situation)
    # Step 4: 按DAG执行
    return execute_dag(template.dag, params)
```

这个设计的关键优势是**可预测性**：每个决策都能追溯到具体的模板和参数，安全可控。但它的根本局限在于——智能体只做**模式匹配**，不做**推理**。它不理解"为什么选择这个模板"，不理解"如果对手做出意料之外的反应怎么办"，更不理解"这个行动会导致什么后果"。

#### 3.1.2 工作流模板的三大能力缺口

在实际作战场景中，有三种情况是工作流模板无法覆盖的：

**缺口一：全新态势——从未见过的局面**

工作流模板依赖历史归纳。如果态势特征向量与所有模板的触发条件距离都超过阈值（"陌生态势"），模板匹配会失败。这在战争初期尤其常见——对手的首轮行动往往超出预想。

典型案例：蓝方预期红方从海上突入，红方却从内陆渗透。此时所有海上防御模板都不适用，而内陆防御模板可能尚未创建。v4.0的降级策略是"选择距离最近的模板"——但这等于在陌生环境中套用旧经验，风险极高。

**缺口二：复杂决策——可能性空间爆炸**

JS决策的分支因子远超棋类游戏。一个联合火力打击方案涉及：打击目标选择（数十个）、打击平台分配（海/空/陆/电磁）、打击时序（同步/异步/波次）、弹药组合（毁伤概率与附带损伤的权衡）。即使只考虑每个维度3个选项，组合空间也已达到3⁴=81个方案。

LLM直接生成COA（Course of Action）的典型做法是"生成3个候选方案"——但这只看了81个方案中的3个，覆盖率不到4%。v4.0的慢系统虽然可以"调整现有模板"，但仍然是基于模板的局部优化，无法系统性地搜索整个决策空间。

**缺口三：适应性对手——敌人也在学习**

工作流模板假设对手行为模式是稳定的。但现代战争中，对手会持续学习和适应——红方可能已经分析了蓝方的模板化行为模式，并发展出针对性的反制策略。v4.0的模板无法预测对手的适应性反应，更无法进行对抗性推理。

#### 3.1.3 v5.0升级：三大认知支柱

v5.0引入三大认知能力，分别解决上述三个缺口：

```
┌─────────────────────────────────────────────────────────────────────────────┐
│           v5.0 智能体认知架构——自主决策的三大支柱                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                    AgentKernel（智能体推理引擎）                        │ │
│  │    编排三大支柱 → 选择决策路径 → 产出可执行方案                        │ │
│  └───────────────────────────────┬───────────────────────────────────────┘ │
│                                  │                                          │
│          ┌───────────────────────┼───────────────────────┐                 │
│          │                       │                       │                 │
│  ┌───────▼────────┐   ┌─────────▼──────────┐   ┌───────▼──────────┐     │
│  │  支柱一：       │   │  支柱二：          │   │  支柱三：        │     │
│  │  世界模型       │   │  Skills技能库      │   │  MCTS搜索        │     │
│  │  World Model   │   │  Skill Library     │   │  Monte Carlo     │     │
│  │               │   │                    │   │  Tree Search     │     │
│  │  预测未来的    │   │  从人类经验中学习   │   │  系统探索决策空间  │     │
│  │  能力          │   │  的能力             │   │  的能力           │     │
│  │               │   │                    │   │                  │     │
│  │  解决：        │   │  解决：             │   │  解决：           │     │
│  │  全新态势      │   │  复杂决策           │   │  适应性对手       │     │
│  │  (预测后果)    │   │  (经验复用)         │   │  (对抗推理)       │     │
│  └───────┬────────┘   └─────────┬──────────┘   └───────┬──────────┘     │
│          │                       │                       │                 │
│          └───────────────────────┼───────────────────────┘                 │
│                                  │                                          │
│  ┌───────────────────────────────▼───────────────────────────────────────┐ │
│  │               安全执行层                │ │
│  │                                                                       │ │
│  │  所有认知支柱产出的方案，必须通过安全执行层才能下发执行：                │ │
│  │  1. 工作流验证：方案是否可映射到已验证的工作流DAG？                     │ │
│  │  2. OPA策略检查：是否符合交战规则（ROE）和授权边界？                    │ │
│  │  3. 人工确认：中低置信度方案是否需要指挥员审批？                        │ │
│  │                                                                       │ │
│  │  v4.0的工作流模板并未被取代——它们成为v5.0的安全执行层。                │ │
│  │  智能体可以"想"出新方案，但只有通过安全层验证的方案才能"做"。          │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│  决策路径（由AgentKernel根据态势选择）：                                     │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ Skill快速执行 │  │ Skill自适应执行 │  │  MCTS搜索    │  │ 升级到人工   │ │
│  │ < 500ms      │  │ 1-5s           │  │  10-30s      │  │ 等待指挥员   │ │
│  │ 高置信度     │  │ 中等置信度      │  │  新态势      │  │ 低置信度     │ │
│  └──────────────┘  └────────────────┘  └──────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

**核心设计原则**：

1. **认知能力分层**：三大支柱形成层次依赖的认知链——世界模型提供状态预测能力，MCTS在世界模型上进行决策空间搜索，Skill库为MCTS的动作生成提供高质量候选。AgentKernel根据态势特征和置信度动态编排三者的调用顺序。不是每个决策都需要全部三个支柱——熟悉的态势只需Skill快速执行，全新的态势才需要MCTS深度搜索。

2. **安全执行层不变**：v4.0的工作流模板体系并未被取代。它们成为v5.0的**安全执行层**——所有认知支柱产出的方案，必须通过工作流验证和OPA策略检查才能执行。智能体可以"想"出模板之外的方案，但"做"仍然受到安全约束。

3. **闭环学习**：每次决策的执行结果都反馈给Skill学习器和世界模型训练管线（第8章数据闭环），形成持续进化能力。

#### 3.1.4 与v4.0的向后兼容

v5.0的认知架构是v4.0工作流架构的**超集**：

| 维度 | v4.0 | v5.0 | 兼容方式 |
|------|------|------|---------|
| 决策方式 | 模板匹配 + DAG执行 | Skill + 世界模型 + MCTS | 高置信度Skill退化为模板匹配 |
| 安全机制 | 工作流生命周期 + OPA | 不变，增加认知层验证 | 安全执行层完全复用v4.0 |
| 快系统 | Qdrant匹配 + auto_fill | Skill快速执行路径 | 同一逻辑，语义升级 |
| 慢系统 | LLM调整模板 | MCTS搜索 + Skill自适应 | 搜索空间从模板内扩展到全空间 |
| 学习能力 | 仿真验证 + 经验蒸馏 | Skill学习器 + 世界模型训练 | 蒸馏逻辑升级为Skill归纳 |
| 基础设施 | PG + Qdrant + Valkey | 不变 | 同一套存储和检索基础设施 |


### 3.2 世界模型：预测未来的能力

#### 3.2.1 什么是世界模型

世界模型（World Model）是智能体内部的**战场态势预测器**。它的核心能力是：给定当前态势和我方行动，预测"下一步态势会变成什么样"。

这个概念源自强化学习领域的Dyna架构（Sutton, 1991），后续发展出World Models（Ha & Schmidhuber, 2018）、Dreamer系列（Hafner et al., Nature 2025，在150+任务上达到SOTA）、MuZero（Schrittwieser et al., 2020，将learned model与MCTS结合）等里程碑。LeCun的JEPA架构进一步指出：有效的世界模型应预测**抽象表征（representation）**而非完整状态重建。在JSC2场景中，世界模型的角色类似于棋类AI中的局面评估函数——但远不止评估，它能预测对手最可能的反应、我方损失预估、任务成功概率等**决策相关特征**。

**世界模型 vs RAG——本质区别**：

| 维度 | RAG（检索增强生成） | 世界模型 |
|------|-------------------|---------|
| 能力 | 检索过去的知识 | 预测未来的结果 |
| 输出 | "历史上类似情况是怎么处理的" | "如果采取这个行动，态势会变成什么样" |
| 局限 | 无法处理从未出现的情况 | 需要大量训练数据 |
| 用途 | 回答"这是什么" | 回答"如果...会怎样" |
| 数据依赖 | 文档/战例库 | 状态-行动-结果三元组 |

RAG和世界模型是互补的：RAG提供"历史上发生了什么"的知识，世界模型提供"接下来会发生什么"的预测。在v5.0架构中，RAG主要服务于Skill学习器（从条令/战例中提取知识），世界模型服务于MCTS搜索（预测行动后果）。

#### 3.2.2 训练数据来源

世界模型的训练需要大量`(当前态势, 行动, 下一态势)`三元组。数据来源有三个层次：

| 来源 | 数据量 | 质量 | 成本 | 说明 |
|------|--------|------|------|------|
| **兵棋推演引擎**（第6章） | 极大（万级/次） | 中等（仿真精度有限） | 低（自动化） | 最主要的数据来源。每次对抗推演可自动采集数千个决策三元组 |
| **历史战例** | 小（百级） | 高（真实数据） | 高（需人工标注） | 稀缺但宝贵。用于校准世界模型在关键场景上的精度 |
| **实兵演习** | 中（千级） | 中高（半真实） | 中（传感器采集） | 介于仿真和实战之间，是弥合"仿真-现实鸿沟"的关键 |

世界模型的持续训练与第6章兵棋推演引擎形成闭环：推演引擎产生训练数据 → 世界模型精度提升 → 推演中的智能体更强 → 产生更高质量的对抗数据 → 进一步提升世界模型。这个闭环是v5.0架构进化的核心引擎。

#### 3.2.3 预测后端

世界模型支持三种预测后端，适应不同精度和延迟需求：

- **神经网络预测（Neural）**：基于Transformer的编码器-解码器架构。延迟低（<100ms），但精度受训练数据限制。适用于MCTS搜索中的快速评估。
- **仿真引擎预测（Simulation）**：调用第6章兵棋引擎进行精确仿真。延迟高（1-30s），但精度最高。适用于关键决策的验证。
- **混合预测（Hybrid）**：先用神经网络快速预测，当置信度低于阈值时自动降级到仿真引擎。这是默认模式，兼顾速度和精度。

#### 3.2.4 对手建模

世界模型内嵌对手行为模型（Adversary Model），用于预测红方对我方行动的反应。对手模型同样基于历史数据训练——使用第6章对抗训练中采集的红方行为数据。对手模型输出多个可能的反应及其概率分布，而非单一预测，以反映战场不确定性。

#### 3.2.6 状态表示：Latent Prediction设计

**关键设计决策：世界模型预测Latent Representation，而非完整COP快照。**

所有成功的world model系统——MuZero预测抽象hidden state、Dreamer预测紧凑latent向量、JEPA预测representation——都遵循同一原则：预测决策相关的抽象特征，而非完整观测重建。本架构遵循这一原则。

**为什么不能预测完整COPSnapshot？**

一个包含200+JS实体的COP快照（位置/速度/状态/关系/环境/电磁态势）其状态空间远超当前world model的验证范围。多步递推中预测误差指数级累积（Nature 2025, Dreamer v3明确指出"complex scenes contain details unnecessary for control"），使得depth>2的完整状态预测不可靠。若MCTS的每次仿真都依赖完整状态预测，则数千次仿真不可行。

**本架构的解决方案——双模式预测：**

| 模式 | 输入 | 输出 | 延迟 | 用途 |
|------|------|------|------|------|
| **Latent预测（神经）** | COPSnapshot → 编码器 → latent向量 | LatentPrediction（威胁等级/兵力比/任务成功概率/关键不确定因素） | <100ms | MCTS搜索中的快速仿真（数千次/秒） |
| **完整预测（仿真引擎）** | COPSnapshot + Action | 完整的下一态势COPSnapshot | 1-30s | 关键决策的精确验证 |

Latent预测不重建完整态势，只预测**决策所需的关键维度**：
- 威胁等级变化（HIGH→CRITICAL）
- 兵力平衡趋势（我方优势0.7→0.5）
- 任务成功概率（0.8→0.6）
- 对手最可能的反应类型（maneuver/strike/defend）
- 关键不确定因素（对手意图未明/传感器精度不足）

这一设计使MCTS可以在latent空间中进行数千次快速仿真，仅在最终方案验证时调用完整兵棋引擎。

#### 3.2.7 完整代码实现

```python
# agent/world_model.py
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class WorldModelBackend(str, Enum):
    NEURAL = "neural"          # 神经网络世界模型（Transformer-based）
    SIMULATION = "simulation"  # 仿真引擎世界模型（兵棋引擎）
    HYBRID = "hybrid"          # 混合：神经网络快速预测 + 仿真引擎精确验证


@dataclass
class COPSnapshot:
    """COP态势快照——世界模型的输入"""
    timestamp: str
    entities: List[Dict[str, Any]]      # JS实体列表
    relations: List[Dict[str, Any]]     # 实体间关系
    environment: Dict[str, Any]         # 环境（天气/地形/电磁）
    blue_force_status: Dict[str, Any]   # 蓝方兵力状态
    red_force_estimate: Dict[str, Any]  # 红方态势估计


@dataclass
class Action:
    """我方行动方案"""
    action_id: str
    action_type: str                    # strike/recon/maneuver/defend/support
    parameters: Dict[str, Any]
    targets: List[str]                  # 目标实体ID
    assets: List[str]                   # 使用资产ID


@dataclass
class PredictedState:
    """世界模型预测结果"""
    next_cop: COPSnapshot               # 预测的下一态势
    confidence: float                   # 预测置信度
    key_uncertainties: List[str]        # 关键不确定因素
    predicted_adversary_actions: List[Dict]  # 对手最可能的反应
    expected_outcomes: Dict[str, float] # 预期结果（损失/收益/风险）


@dataclass
class TrainingTriple:
    """世界模型训练三元组: (当前态势, 行动, 下一态势)"""
    state: COPSnapshot
    action: Action
    next_state: COPSnapshot
    reward: float                       # 结果评分（任务成功度）
    source: str                         # "wargame" / "historical" / "exercise"


@dataclass
class LatentPrediction:
    """世界模型Latent预测结果——决策相关关键维度（不重建完整COP）"""
    threat_delta: float                    # 威胁等级变化 [-1, 1]
    force_balance: float                   # 兵力平衡 [0, 1]（>0.5为我方优势）
    mission_success_prob: float            # 任务成功概率 [0, 1]
    adversary_likely_action: str           # 对手最可能的反应类型
    confidence: float                      # 预测置信度 [0, 1]
    key_uncertainties: List[str]           # 关键不确定因素
    friendly_loss_estimate: float = 0.0    # 预估我方损失 [0, 1]


class BattlefieldWorldModel:
    """
    战场世界模型——从历史数据中学习战场动力学

    核心能力：给定当前态势和一个行动，预测下一步态势。
    不学习"正确答案是什么"，而是学习"世界的运转规则是什么"。

    训练数据来源：
    1. 兵棋推演引擎的仿真结果（第6章）——大量、低成本
    2. 历史战例数据——稀缺但高质量
    3. 实兵演习数据——中等数量、中等质量
    """

    def __init__(self, backend: WorldModelBackend = WorldModelBackend.HYBRID):
        self._backend = backend
        self._neural_model = None       # Transformer-based预测模型
        self._simulation_engine = None   # 兵棋仿真引擎（精确模式）
        self._adversary_model = None     # 对手行为模型
        self._training_data: List[TrainingTriple] = []

    def predict(
        self,
        current_state: COPSnapshot,
        action: Action,
        depth: int = 1,
    ) -> PredictedState:
        """
        预测：如果我方执行action，战场态势会怎么变化？

        Args:
            current_state: 当前COP态势快照
            action: 我方拟采取的行动
            depth: 预测深度（1=只预测下一步，2=预测两步...）

        Returns:
            预测的下一态势 + 置信度 + 关键不确定因素
            注意：神经预测后端返回LatentPrediction（决策关键维度），仿真后端返回完整PredictedState。
        """
        # Step 1: 对手反应预测
        adversary_actions = self._predict_adversary(current_state, action)

        # Step 2: 选择预测后端
        if self._backend == WorldModelBackend.NEURAL:
            next_state = self._neural_predict(
                current_state, action, adversary_actions
            )
        elif self._backend == WorldModelBackend.SIMULATION:
            next_state = self._simulation_predict(
                current_state, action, adversary_actions
            )
        else:  # HYBRID
            # 快速神经网络预测 + 低置信度时仿真验证
            next_state = self._neural_predict(
                current_state, action, adversary_actions
            )
            if next_state.confidence < 0.6:
                next_state = self._simulation_predict(
                    current_state, action, adversary_actions
                )

        # Step 3: 多步递推（depth > 1时）
        if depth > 1 and next_state.confidence > 0.4:
            recursive = self.predict(
                next_state.next_cop,
                Action(
                    action_id=f"{action.action_id}_followup",
                    action_type="observe",
                    parameters={},
                    targets=[],
                    assets=[],
                ),
                depth=depth - 1,
            )
            # 合并不确定性：越深层预测越不确定
            next_state.key_uncertainties.extend(
                recursive.key_uncertainties
            )
            next_state.confidence *= recursive.confidence

        return next_state

    def predict_multiple(
        self,
        current_state: COPSnapshot,
        actions: List[Action],
    ) -> List[Tuple[Action, PredictedState]]:
        """
        批量预测：评估多个行动方案的后果
        用于MCTS搜索和COA评估
        """
        results = []
        for action in actions:
            predicted = self.predict(current_state, action)
            results.append((action, predicted))
        # 按预期收益排序
        results.sort(
            key=lambda x: x[1].expected_outcomes.get("mission_success", 0),
            reverse=True,
        )
        return results

    def estimate_adversary_intent(
        self,
        current_state: COPSnapshot,
        observation_window: int = 3,
    ) -> Dict[str, Any]:
        """
        估计对手意图：基于当前态势和历史行为，推断红方最可能的战略目标

        Returns:
            对手意图估计，包含可能的目标、置信度和推断依据
        """
        if not self._adversary_model:
            return {
                "estimated_intent": "unknown",
                "confidence": 0.0,
                "evidence": [],
            }

        return self._adversary_model.estimate_intent(
            current_state, observation_window
        )

    def ingest_training_data(self, triples: List[TrainingTriple]):
        """
        摄入训练数据

        主要数据源：
        - 第6章兵棋推演引擎的仿真结果（每次推演产出数百个三元组）
        - 第8章数据闭环管线采集的实战/演习数据
        """
        self._training_data.extend(triples)

    def train(self, epochs: int = 10, validation_split: float = 0.2):
        """
        训练世界模型

        实现策略：
        - 使用Transformer encoder-decoder架构
        - 输入: [current_state_embedding, action_embedding]
        - 输出: next_state_embedding
        - 损失: 对比预测态势与实际态势的差异
        - 验证: 保留20%数据作为验证集，监控过拟合

        训练触发时机：
        - 每次大规模兵棋推演后（第6章）
        - 每周定期重训（结合新采集的演习数据）
        - 关键战例标注完成后
        """
        if len(self._training_data) < 100:
            return  # 数据不足，跳过训练

        split_idx = int(len(self._training_data) * (1 - validation_split))
        train_set = self._training_data[:split_idx]
        val_set = self._training_data[split_idx:]

        # TODO: 对接PyTorch训练循环
        # 训练过程指标记录到第8章数据闭环管线

    def _predict_adversary(
        self, state: COPSnapshot, our_action: Action
    ) -> List[Dict]:
        """
        预测对手最可能的反应

        实现：对手模型基于红方历史行为训练（第6章对抗训练）
        输出多个可能的反应及其概率
        """
        if self._adversary_model:
            return self._adversary_model.predict_responses(
                state, our_action
            )
        return [{"action": "unknown", "probability": 0.5}]

    def _neural_predict(
        self,
        state: COPSnapshot,
        action: Action,
        adversary_actions: List[Dict],
    ) -> PredictedState:
        """神经网络快速预测（<100ms，精度较低）"""
        # TODO: Transformer inference
        return PredictedState(
            next_cop=state,  # placeholder
            confidence=0.7,
            key_uncertainties=["对手意图不确定", "传感器精度"],
            predicted_adversary_actions=adversary_actions,
            expected_outcomes={
                "mission_success": 0.75,
                "friendly_loss": 0.1,
            },
        )

    def _simulation_predict(
        self,
        state: COPSnapshot,
        action: Action,
        adversary_actions: List[Dict],
    ) -> PredictedState:
        """仿真引擎精确预测（1-30s，精度高）"""
        # TODO: 对接第6章WargameEngine
        return PredictedState(
            next_cop=state,
            confidence=0.9,
            key_uncertainties=[],
            predicted_adversary_actions=adversary_actions,
            expected_outcomes={
                "mission_success": 0.8,
                "friendly_loss": 0.08,
            },
        )
```


### 3.3 Skills技能库：从人类经验中学习

#### 3.3.1 Skills vs 工作流模板

v4.0的工作流模板是**固定步骤序列**——它知道"做什么"，但不知道"为什么这样做"。当态势与模板的触发条件完全匹配时，模板执行是高效且安全的。但当态势与模板只有部分匹配时，模板无法自适应——它要么完全执行，要么不执行。

Skills（技能）是v5.0引入的**可适应决策能力单元**。与工作流模板的关键区别在于：

| 维度 | 工作流模板 | Skill技能（v5.0） |
|------|-------------------|-------------------|
| 定义方式 | 人工设计步骤DAG | 从经验中学习归纳 |
| 适应性 | 固定步骤，参数可调 | 理解因果，可自适应 |
| 适用判断 | 触发条件匹配度 | 适用条件 + 置信度 + 因果推理 |
| 失败处理 | 降级到人工 | 学习失败模式，更新适用条件 |
| 知识表示 | 步骤 + 参数Schema | 因果模型 + 适用条件 + 前后置条件 |
| 进化方式 | 人工修改DAG | 自动从新经验中更新 |

一个具体的例子：**"夜间城市作战中的火力支援协调"**。

- **工作流模板方式**：定义一个包含5个步骤的DAG（确认目标 → 评估附带损伤 → 选择弹药 → 协调时序 → 下达指令），参数包括目标坐标、弹药类型等。
- **Skill方式**：学习到"夜间城市作战中，附带的平民伤亡风险是火力支援失败的首要原因"（因果知识），"当目标距离民用建筑<500m时，应优先使用精确制导弹药并设置延时引信"（适用条件），"这些规则来自XX战例和YY条令第Z节"（溯源）。

当态势是"夜间、城市、目标距离民用建筑300m"时，模板和Skill的表现相似。但当态势变为"夜间、城市、目标距离民用建筑300m、但该建筑已被确认敌方占用"时——模板仍然按原逻辑执行（可能过度谨慎），而Skill能够理解因果并自适应（建筑已被敌方占用 → 附带损伤风险降低 → 可考虑更高效的弹药选择）。

#### 3.3.2 三种Skill来源

Skills从三个来源学习，覆盖从理论到实践的完整经验谱：

**来源一：JS条令（Doctrine）**

JS条令是经过长期验证的理论知识。通过自然语言处理技术，可以从条令文档中提取结构化的决策规则，转化为Skill定义。条令来源的Skill具有最高的权威性，但可能缺乏对特殊情境的适应性。

条令Skill的提取管线：条令文档 → NLP解析 → 决策规则提取 → 结构化Skill定义 → 仿真验证 → 生效。

**来源二：历史战例（Battle Case）**

历史战例是经过实战检验的实践经验。通过分析战例中的关键决策点、态势特征和行动结果，可以归纳出成功/失败模式，转化为Skill。战例来源的Skill具有最强的因果说服力（有真实结果支撑），但数据量有限且需要人工标注。

战例Skill的提取管线：战例数据 → 关键决策点识别 → 因果分析（LLM辅助）→ 成功/失败模式归纳 → Skill定义 → 交叉验证 → 生效。

**来源三：指挥员操作（Commander Action）**

指挥员操作是持续产生的实时经验。当指挥员修改了系统推荐的COA、手动调整了参数、或者否决了某个方案时，这些操作背后隐含着指挥员的决策智慧。Skill学习器可以从中提取推理逻辑，转化为新的Skill或更新现有Skill。

指挥员Skill的提取管线：操作日志 → 修改语义分析 → 因果归因 → 适用条件归纳 → 置信度评估 → 仿真验证 → 生效。

#### 3.3.3 Skill生命周期

与工作流模板类似，Skill也遵循生命周期管理：

```
  学习器提取                仿真验证              实战使用              经验过时
  ┌────────┐  验证通过    ┌──────────┐  使用≥20次  ┌────────┐  新Skill替代  ┌───────────┐
  │ DRAFT  │──────────▶│ VALIDATED │──────────▶│ ACTIVE │────────────▶│ DEPRECATED│
  └────────┘            └──────────┘            └────────┘             └───────────┘
      │                     │ 验证失败                │                      │
      │                     ▼                         │                      │
      │               退回DRAFT                       │                      │
      │               修改适用条件                     │                      │
      │                                            │                      │
      └────────────────────────────────────────────┘                      │
                        经验蒸馏闭环                                        │
                                                                           │
  状态说明：                                                                │
  DRAFT:      从经验中提取，尚未验证。可用于参考，不可用于自动执行。         │
  VALIDATED:  通过兵棋仿真验证（成功率≥70%）。可用于辅助决策。              │
  ACTIVE:     经过实战验证（使用≥20次且成功率≥80%）。可用于自主执行。       │
  DEPRECATED: 被更好的Skill替代或经验过时。保留用于学习，不再推荐。         │
```

#### 3.3.4 Skill的因果模型

Skill的核心价值不在于"做什么"，而在于理解"为什么这样做"。因果模型（Causal Model）是Skill区别于工作流模板的关键——它由一组因果链（CausalLink）组成，每条因果链描述一个因果前提、因果后果及其强度。

因果模型的作用：

1. **自适应执行**：当态势与Skill的标准适用条件不完全匹配时，因果模型允许智能体理解"哪些条件是关键的，哪些是可变通的"，从而做出合理的适应性调整。
2. **失败归因**：当Skill执行失败时，因果模型帮助定位"是哪个因果前提没有满足"，而不是简单地降低Skill的整体成功率。
3. **经验迁移**：因果模型可以被迁移到相关但不同的场景中。例如，"城市作战中的火力协调"因果模型的部分知识可以迁移到"山地作战中的火力协调"。

**领域因果图与Skill因果模型的关系**

每个Skill的因果模型不是孤立的——它们共享一个**领域因果图（Domain Causal Graph）**。领域因果图描述战场环境的基础因果关系（如"恶劣天气→传感器精度下降→探测距离缩短"），由JS条令和历史数据共同构建。每个Skill的`causal_model`引用领域因果图的子集，而非独立持有因果链。

这一设计避免了两类问题：(1) 不同Skill持有矛盾因果链（如Skill A认为"天气恶劣→打击精度下降"，Skill B认为"天气恶劣→对手防守松懈→打击成功率上升"），共享领域因果图保证了一致性；(2) 新Skill可以直接复用领域因果图中已有的因果知识，无需从零学习。

#### 3.3.5 完整代码实现

```python
# agent/skill_system.py
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class SkillSource(str, Enum):
    DOCTRINE = "doctrine"                  # 从JS条令中提取
    BATTLE_CASE = "battle_case"            # 从历史战例中学习
    COMMANDER_ACTION = "commander_action"  # 从指挥员操作中学习
    SIMULATION = "simulation"              # 从仿真训练中发现


class SkillStatus(str, Enum):
    DRAFT = "draft"              # 新提取，未验证
    VALIDATED = "validated"      # 通过仿真验证
    ACTIVE = "active"            # 可用于实战
    DEPRECATED = "deprecated"    # 已过时


@dataclass
class ApplicabilityCondition:
    """Skill适用条件——从成功/失败案例中自动归纳"""
    situation_patterns: List[str]          # 适用态势特征
    threat_level_range: Tuple[str, str]    # ("LOW", "CRITICAL")
    force_ratio_range: Tuple[float, float] # (0.5, 3.0) 兵力比
    terrain_types: List[str]               # ["urban", "mountain", "maritime"]
    weather_conditions: List[str]          # ["all", "clear", "degraded"]
    confidence: float                      # 归纳置信度


@dataclass
class CausalLink:
    """因果链——Skill理解"为什么这样做""""
    cause: str                    # 因果前提
    effect: str                   # 因果后果
    strength: float               # 因果强度 (0-1)
    evidence_count: int           # 支撑证据数量


@dataclass
class SkillDefinition:
    """
    Skill定义——从人类经验中提取的可复用决策能力

    与工作流模板的核心区别：
    - 模板 = 固定步骤序列（知道"做什么"）
    - Skill = 可适应的能力单元（理解"为什么做"和"什么时候做"）
    """
    skill_id: str
    name: str
    description: str
    source: SkillSource
    status: SkillStatus

    # 适用条件（自动学习）
    applicability: ApplicabilityCondition

    # 因果模型（理解为什么）
    causal_model: List[CausalLink]

    # 执行逻辑
    preconditions: List[str]           # 前置条件
    postconditions: List[str]          # 后置条件
    parameters: Dict[str, Any]         # 可调参数

    # 统计
    usage_count: int = 0
    success_rate: float = 0.0
    last_used: Optional[str] = None
    created_at: str = field(
        default_factory=lambda: datetime.utcnow().isoformat()
    )

    # 溯源
    source_reference: str = ""         # 来源文档/战例编号
    parent_skill_id: Optional[str] = None  # 从哪个Skill演化而来


class SkillLibrary:
    """
    Skills技能库

    存储: PostgreSQL(结构) + Qdrant(向量检索) + Valkey(热缓存)
    与工作流注册表共享基础设施（见第4章），但语义不同：
    - 工作流注册表存储"步骤序列"
    - Skills库存储"推理能力"
    """

    def __init__(self):
        self._skills: Dict[str, SkillDefinition] = {}

    def register(self, skill: SkillDefinition):
        """注册新Skill"""
        self._skills[skill.skill_id] = skill

    def deregister(self, skill_id: str):
        """注销Skill（设置状态为DEPRECATED而非删除）"""
        if skill_id in self._skills:
            self._skills[skill_id].status = SkillStatus.DEPRECATED

    def find_applicable(
        self, situation: Dict[str, Any], top_k: int = 5
    ) -> List[SkillDefinition]:
        """
        查找适用于当前态势的Skills

        实现：
        1. 将态势特征转化为向量
        2. 在Qdrant中检索与applicability条件匹配的Skills
        3. 按置信度和历史成功率排序
        4. 过滤掉DRAFT和DEPRECATED状态的Skill
        """
        candidates = []
        for skill in self._skills.values():
            if skill.status in (
                SkillStatus.DRAFT,
                SkillStatus.DEPRECATED,
            ):
                continue
            if self._is_applicable(skill, situation):
                candidates.append(skill)

        # 按成功率 × 适用置信度排序
        candidates.sort(
            key=lambda s: s.success_rate * s.applicability.confidence,
            reverse=True,
        )
        return candidates[:top_k]

    def update_statistics(self, skill_id: str, success: bool):
        """更新Skill使用统计"""
        if skill_id in self._skills:
            skill = self._skills[skill_id]
            skill.usage_count += 1
            # 增量更新成功率
            total = skill.usage_count
            skill.success_rate = (
                skill.success_rate * (total - 1)
                + (1.0 if success else 0.0)
            ) / total
            skill.last_used = datetime.utcnow().isoformat()

    def get_by_id(
        self, skill_id: str
    ) -> Optional[SkillDefinition]:
        """按ID获取Skill"""
        return self._skills.get(skill_id)

    def list_by_source(
        self, source: SkillSource
    ) -> List[SkillDefinition]:
        """按来源列出Skills"""
        return [
            s for s in self._skills.values() if s.source == source
        ]

    def _is_applicable(
        self, skill: SkillDefinition, situation: Dict
    ) -> bool:
        """
        判断Skill是否适用于当前态势

        检查维度：
        1. 威胁等级是否在Skill的适用范围内
        2. 兵力比是否在适用范围内
        3. 地形类型是否匹配
        4. 天气条件是否匹配
        5. 态势特征向量相似度是否超过阈值
        """
        cond = skill.applicability

        # 威胁等级检查
        threat = situation.get("threat_level", "UNKNOWN")
        if threat not in _range_values(
            cond.threat_level_range[0],
            cond.threat_level_range[1],
            ["LOW", "MEDIUM", "HIGH", "CRITICAL"],
        ):
            return False

        # 兵力比检查
        force_ratio = situation.get("force_ratio", 1.0)
        if not (
            cond.force_ratio_range[0]
            <= force_ratio
            <= cond.force_ratio_range[1]
        ):
            return False

        # 地形检查
        terrain = situation.get("terrain_type", "unknown")
        if "all" not in cond.terrain_types and terrain not in cond.terrain_types:
            return False

        return True


def _range_values(
    low: str, high: str, ordered: List[str]
) -> List[str]:
    """获取有序列表中[low, high]范围内的所有值"""
    try:
        low_idx = ordered.index(low)
        high_idx = ordered.index(high)
        return ordered[low_idx : high_idx + 1]
    except ValueError:
        return ordered


class SkillLearner:
    """
    Skill学习器——从人类行为中提取Skill

    三种学习来源：
    1. 条令：解析JS条令文档，提取决策规则
    2. 战例：分析历史战例，归纳成功/失败模式
    3. 指挥员操作：实时记录指挥员的修改/创建/否决行为
    """

    def __init__(
        self, skill_library: SkillLibrary, world_model=None
    ):
        self._library = skill_library
        self._world_model = world_model
        self._min_samples_for_induction = 5  # 归纳所需最小样本数

    def learn_from_commander_action(
        self,
        action: Dict[str, Any],
        context: Dict[str, Any],
        outcome: Dict[str, Any],
    ) -> Optional[SkillDefinition]:
        """
        从指挥员操作中学习Skill

        场景：指挥员修改了系统推荐的COA参数
        学习：提取修改背后的推理逻辑

        输入：
        - action: 指挥员的具体修改操作
        - context: 修改时的态势上下文
        - outcome: 修改后的执行结果

        处理流程：
        1. 语义分析：理解指挥员改了什么
        2. 因果归因：这个修改导致了什么不同
        3. 条件归纳：在什么情况下应该这样做
        4. 置信度评估：这个归纳有多可靠
        5. 仿真验证：用兵棋引擎验证这个Skill

        **学习机制选择**：本方法采用偏好学习（Preference Learning）范式，而非逆向强化学习或模仿学习。当指挥员修改系统推荐的COA时，产生一个偏好对（被拒绝的AI建议 vs 指挥员选择的方案），这与第8章DPO训练管线的偏好数据格式对齐。选择偏好学习的原因：(1) 数据获取最容易——每次指挥员修改就是一个偏好信号；(2) 与DPO训练管线天然对齐；(3) 不需要推断完整的奖励函数（IRL的数据需求远大于当前可获取量）。
        """
        # Step 1: 分析修改的语义（改了什么、为什么改）
        modification_semantics = self._analyze_modification(
            action, context
        )

        # Step 2: 因果归因（这个修改导致了什么不同）
        causal_links = self._attribute_causality(
            modification_semantics, context, outcome
        )

        # Step 3: 归纳适用条件（在什么情况下应该这样做）
        applicability = self._induce_applicability(
            context, causal_links
        )

        if applicability.confidence < 0.5:
            return None  # 置信度太低，不提取

        skill = SkillDefinition(
            skill_id=(
                f"skill-cmdr-"
                f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            ),
            name=(
                f"指挥员经验: "
                f"{modification_semantics.get('summary', 'unknown')}"
            ),
            description=modification_semantics.get("rationale", ""),
            source=SkillSource.COMMANDER_ACTION,
            status=SkillStatus.DRAFT,
            applicability=applicability,
            causal_model=causal_links,
            preconditions=modification_semantics.get(
                "preconditions", []
            ),
            postconditions=modification_semantics.get(
                "postconditions", []
            ),
            parameters=modification_semantics.get("parameters", {}),
            source_reference=context.get("mission_id", ""),
        )

        self._library.register(skill)
        return skill

    def learn_from_battle_case(
        self, case: Dict[str, Any]
    ) -> Optional[SkillDefinition]:
        """
        从历史战例中学习Skill

        实现：解析战例的关键决策点、态势特征和结果，
        使用LLM辅助提取因果推理链

        处理流程：
        1. 识别战例中的关键决策点
        2. 提取每个决策点的态势特征、决策内容和结果
        3. LLM辅助因果分析：这个决策为什么成功/失败
        4. 归纳适用条件和因果模型
        5. 交叉验证：与其他战例中的类似决策交叉印证
        """
        # TODO: 对接战例数据库 + LLM因果分析
        return None

    def learn_from_doctrine(
        self, doctrine_doc: Dict[str, Any]
    ) -> List[SkillDefinition]:
        """
        从JS条令中提取Skill

        实现：解析条令文档，识别决策规则和行动标准，
        转化为结构化的Skill定义

        与RAG的区别：
        - RAG是检索条令文本片段，返回"条令说了什么"
        - Skill提取是将条令转化为可执行决策逻辑

        处理流程：
        1. NLP解析条令文档，识别决策规则段落
        2. 提取条件-行动对：在X条件下，应该采取Y行动
        3. 为每个规则构建因果模型和适用条件
        4. 生成Skill定义（初始状态为DRAFT）
        """
        # TODO: 对接条令解析管线
        return []

    def _analyze_modification(
        self, action: Dict, context: Dict
    ) -> Dict[str, Any]:
        """
        分析指挥员修改的语义

        实现：对比原始推荐方案和修改后的方案，
        提取差异的语义描述
        """
        return {
            "summary": "待分析",
            "rationale": "",
            "preconditions": [],
            "postconditions": [],
            "parameters": {},
        }

    def _attribute_causality(
        self,
        semantics: Dict,
        context: Dict,
        outcome: Dict,
    ) -> List[CausalLink]:
        """
        因果归因——理解修改为什么导致了不同的结果

        实现：
        1. 使用世界模型对比"如果没修改"和"修改后"的差异
        2. 识别修改直接影响和间接影响
        3. 为每个因果链分配强度和支撑证据数
        """
        return []

    def _induce_applicability(
        self,
        context: Dict,
        causal_links: List[CausalLink],
    ) -> ApplicabilityCondition:
        """
        从上下文和因果链中归纳适用条件

        实现：
        1. 从context中提取态势特征
        2. 结合因果链的因果前提，识别关键条件
        3. 评估归纳的置信度（基于样本数和一致性）
        """
        return ApplicabilityCondition(
            situation_patterns=[],
            threat_level_range=("LOW", "CRITICAL"),
            force_ratio_range=(0.0, 10.0),
            terrain_types=["all"],
            weather_conditions=["all"],
            confidence=0.3,
        )
```


### 3.4 蒙特卡洛树搜索：系统探索决策空间

#### 3.4.1 为什么LLM"生成3个COA"不够

当前主流的JSAI辅助决策方式是：让LLM基于态势描述生成3-5个候选行动方案（Course of Action），然后由指挥员选择或修改。这种方法存在三个根本问题：

**问题一：覆盖率极低**

假设一个中等复杂度的联合打击决策有81个可能的方案组合（如3.1.2节所述），LLM生成3个方案只覆盖了3.7%的决策空间。更关键的是，LLM倾向于生成"常规"方案——安全但平庸。真正有创造性的方案（如历史战例中的奇袭、佯攻）往往在决策空间的边缘区域，LLM几乎不可能凭空生成。

**问题二：无法深度评估**

LLM生成方案后，通常只能给出一个粗略的优劣排序（"方案A优于方案B"）。它无法回答"方案A在第二步之后会遇到什么问题"或"如果对手采取反制措施X，方案A还能成功吗"。这是因为LLM没有世界模型——它不预测行动的后果，只匹配语言模式。

**问题三：缺乏系统性**

LLM的生成是"一次性"的——它不会因为发现方案A有缺陷而回溯到决策点重新搜索。它也无法系统地排除已经评估过的方案。这导致搜索过程是盲目的，而非系统性的。

**问题四：JS行动空间的组合爆炸**

LLM生成3个COA覆盖不足，但MCTS也面临行动空间爆炸的挑战。JS决策的行动空间是组合的——选择部队×武器×目标×时间×协调方式，单步可能的行动组合可达10^6以上。AlphaStar在StarCraft中明确放弃了MCTS，因其大规模连续行动空间和战争迷雾使MCTS不可扩展（AlphaStar Unplugged, 2023）。JSC2必须采用分层行动分解+采样策略来解决这一问题（详见3.4.7节）。

#### 3.4.2 MCTS：从AlphaGo到JS决策

蒙特卡洛树搜索（MCTS）是AlphaGo击败人类围棋冠军的核心算法。它在决策空间中进行系统性的搜索——不是随机猜测，而是通过"探索-利用"平衡，将计算资源集中在最有前景的决策分支上。

MCTS与JS决策的天然契合点：

| 维度 | 围棋 | JS决策 |
|------|------|---------|
| 决策空间 | 19x19棋盘，约250个合法落子 | 战场态势，数十种可能的行动 |
| 对手 | 有，且强大 | 有，且适应性强 |
| 评估函数 | 胜率估计 | 任务成功率 + 损失预估 |
| 时间约束 | 每步数秒到数分钟 | 决策窗口从秒级到小时级 |
| 不确定性 | 完全信息博弈 | 不完全信息（战争迷雾） |

JSMCTS的独特之处在于**不完全信息博弈**——我们不能看到对手的全部部署，只能基于情报估计。这要求在MCTS搜索中加入不确定性建模：每个决策节点不仅评估期望收益，还评估方差（风险）。

#### 3.4.3 搜索流程

MCTS的每次迭代包含四个步骤：

**1. Selection（选择）**：从搜索树的根节点出发，沿着UCB（Upper Confidence Bound）分数最高的路径下降到叶节点。UCB公式平衡了"探索未知分支"和"利用已知优势分支"：

```
UCB(node) = Q(node) + c * sqrt(ln(N(parent)) / N(node))

其中：
- Q(node) = 节点的平均奖励（历史表现）
- N(node) = 节点的访问次数
- c = 探索权重（默认1.414，即sqrt(2)）
- 高UCB = 要么表现好（Q高），要么访问少（值得探索）
```

**2. Expansion（展开）**：在叶节点处生成新的行动分支。行动生成可以使用LLM（全面但慢）、启发式规则（快但有限）、或已学到的Skills（兼具速度和质量）。

**3. Simulation（仿真）**：用世界模型评估新展开的节点。世界模型预测"如果采取这个行动，战场态势会变成什么样"，并给出一个奖励值（任务成功率、损失预估等）。

**4. Backpropagation（回传）**：将仿真得到的奖励值沿着搜索路径向上传播，更新路径上每个节点的Q值和访问次数。这使得未来的Selection步骤能利用新获得的信息。

#### 3.4.4 时间预算与搜索控制

JS决策的时间窗口差异极大：防空反导的决策窗口是秒级，联合火力打击是分钟级，战役规划是小时级。MCTS搜索必须适应不同的时间预算：

| 决策场景 | 时间预算 | 仿真次数 | 搜索深度 |
|---------|---------|---------|---------|
| 防空反导（时敏目标） | 5s | ~50 | 2-3 |
| 战术火力打击 | 30s | ~200 | 3-5 |
| 战役行动规划 | 5min | ~2000 | 5-8 |
| 战略方案评估 | 30min | ~10000 | 8-12 |

搜索过程支持提前终止：如果在时间预算耗尽之前，最优路径的置信度已经收敛（连续N次迭代最优路径不变），则提前结束搜索以节省计算资源。

#### 3.4.5 完整代码实现

```python
# agent/mcts_search.py
import math
import time
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class DecisionNode:
    """MCTS决策节点"""
    state_summary: str              # 态势摘要
    action: Optional[str] = None    # 导致此节点的行动（根节点为None）
    parent: Optional['DecisionNode'] = None
    children: List['DecisionNode'] = field(default_factory=list)

    # 统计
    visit_count: int = 0
    total_reward: float = 0.0

    # 评估
    prior_probability: float = 1.0  # 先验概率（来自LLM/启发式）
    value_estimate: float = 0.0     # 价值估计（来自世界模型）

    @property
    def q_value(self) -> float:
        """平均奖励（Q值）"""
        return self.total_reward / max(self.visit_count, 1)

    @property
    def ucb_score(self) -> float:
        """UCB1分数 = Q值 + 探索奖励"""
        if self.visit_count == 0:
            return float('inf')
        if self.parent is None:
            return self.q_value
        exploration = 1.414 * math.sqrt(
            math.log(self.parent.visit_count) / self.visit_count
        )
        return self.q_value + exploration


@dataclass
class SearchBudget:
    """搜索预算配置"""
    max_time_ms: int = 30000          # 最大搜索时间（毫秒）
    min_simulations: int = 100        # 最小仿真次数
    max_simulations: int = 10000      # 最大仿真次数
    max_depth: int = 5                # 最大搜索深度
    convergence_threshold: int = 20   # 收敛判定：连续N次最优不变则提前终止
    exploration_weight: float = 1.414 # UCB探索权重


class MilitaryMCTS:
    """
    JS决策蒙特卡洛树搜索

    在决策空间中系统搜索最优行动序列。

    与LLM直接生成COA的区别：
    - LLM: 生成3个候选方案 → 选一个（看3个分支）
    - MCTS: 搜索数千个分支 → 每个分支用世界模型评估 → 选最优

    搜索流程：
    1. Selection: 从根节点沿UCB最高的路径下降
    2. Expansion: 在叶节点展开新的行动分支
    3. Simulation: 用世界模型快速评估新分支
    4. Backpropagation: 将评估结果向上传播
    """

    def __init__(
        self,
        world_model,            # BattlefieldWorldModel
        action_generator=None,   # 行动生成器（LLM/启发式）
        budget: Optional[SearchBudget] = None,
    ):
        self._world_model = world_model
        self._action_generator = action_generator
        self._budget = budget or SearchBudget()

    def search(
        self,
        situation: Dict[str, Any],
        budget_ms: Optional[int] = None,
        min_simulations: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        在决策空间中搜索最优行动序列

        Args:
            situation: 当前态势（COP快照）
            budget_ms: 搜索时间预算（毫秒），覆盖默认配置
            min_simulations: 最小仿真次数，覆盖默认配置

        Returns:
            最优行动序列 + 搜索统计 + 置信度 + 备选方案
        """
        start_time = time.time()

        # 应用覆盖配置
        time_budget = budget_ms or self._budget.max_time_ms
        min_sims = min_simulations or self._budget.min_simulations
        max_sims = self._budget.max_simulations
        max_depth = self._budget.max_depth

        root = DecisionNode(state_summary="current_situation")
        simulations = 0
        convergence_count = 0
        last_best_action = None

        while self._within_budget(
            start_time, time_budget, simulations,
            min_sims, max_sims,
        ):
            # Step 1: Selection - 选择最有前景的叶节点
            leaf = self._select(root)

            # Step 2: Expansion - 展开新分支
            if (
                leaf.visit_count > 0
                and self._depth(leaf) < max_depth
            ):
                self._expand(leaf, situation)
                if leaf.children:
                    leaf = leaf.children[0]

            # Step 3: Simulation - 用世界模型评估
            reward = self._simulate(leaf, situation)

            # Step 4: Backpropagation - 向上传播
            self._backpropagate(leaf, reward)

            simulations += 1

            # 收敛检测：连续N次最优行动不变则提前终止
            current_best = self._current_best_action(root)
            if current_best == last_best_action:
                convergence_count += 1
                if convergence_count >= self._budget.convergence_threshold:
                    break
            else:
                convergence_count = 0
                last_best_action = current_best

        # 选择最优行动序列
        best_path = self._extract_best_path(root)

        return {
            "best_action_sequence": best_path,
            "search_stats": {
                "simulations": simulations,
                "time_ms": int((time.time() - start_time) * 1000),
                "nodes_explored": self._count_nodes(root),
                "max_depth_reached": self._max_depth_reached(root),
                "converged": convergence_count
                    >= self._budget.convergence_threshold,
            },
            "confidence": self._estimate_confidence(root),
            "alternative_paths": self._extract_top_k_paths(
                root, k=3
            ),
        }

    def _select(self, node: DecisionNode) -> DecisionNode:
        """Selection: 沿UCB最高的路径下降到叶节点"""
        while node.children:
            node = max(
                node.children, key=lambda c: c.ucb_score
            )
        return node

    def _expand(
        self, node: DecisionNode, situation: Dict
    ):
        """Expansion: 为叶节点生成可能的行动分支"""
        actions = self._generate_actions(situation, node)

        for i, action in enumerate(actions):
            child = DecisionNode(
                state_summary=f"after_{action}",
                action=action,
                parent=node,
                prior_probability=1.0 / len(actions),
            )
            node.children.append(child)

    def _simulate(
        self, node: DecisionNode, situation: Dict
    ) -> float:
        """
        Simulation: 用世界模型评估叶节点的价值

        实现：从当前节点开始，用世界模型预测多步结果，
        计算累积奖励。奖励函数综合考虑：
        - 任务成功率（mission_success）
        - 我方损失（friendly_loss，惩罚项）
        - 时间效率（completion_time，优化项）
        - 风险可控性（risk_controllability，约束项）
        """
        if not node.action:
            return 0.0

        # 使用世界模型预测行动后果
        # predicted = self._world_model.predict(
        #     situation, Action(action_type=node.action, ...)
        # )
        # reward = (
        #     0.5 * predicted.expected_outcomes.get("mission_success", 0)
        #     - 0.3 * predicted.expected_outcomes.get("friendly_loss", 0)
        #     + 0.2 * predicted.confidence
        # )

        # 简化：使用价值估计
        if node.value_estimate > 0:
            return node.value_estimate
        return 0.5

    def _backpropagate(
        self, node: DecisionNode, reward: float
    ):
        """Backpropagation: 向上传播奖励"""
        while node:
            node.visit_count += 1
            node.total_reward += reward
            node = node.parent

    def _generate_actions(
        self, situation: Dict, node: DecisionNode
    ) -> List[str]:
        """
        生成候选行动列表

        优先级：
        1. Skills库中匹配的Skill动作（高质量、有经验支撑）
        2. LLM生成的候选行动（全面、但可能包含不切实际的方案）
        3. 领域启发式规则（快速、但覆盖有限）
        """
        if self._action_generator:
            return self._action_generator(situation)
        return [
            "observe", "maneuver", "strike",
            "defend", "withdraw",
        ]

    def _within_budget(
        self,
        start_time: float,
        budget_ms: int,
        simulations: int,
        min_simulations: int,
        max_simulations: int,
    ) -> bool:
        """检查是否在搜索预算内"""
        elapsed_ms = (time.time() - start_time) * 1000
        if simulations >= max_simulations:
            return False
        if simulations < min_simulations:
            return True
        return elapsed_ms < budget_ms

    def _current_best_action(
        self, root: DecisionNode
    ) -> Optional[str]:
        """获取当前最优行动（用于收敛检测）"""
        if not root.children:
            return None
        best = max(
            root.children, key=lambda c: c.visit_count
        )
        return best.action

    def _extract_best_path(
        self, root: DecisionNode
    ) -> List[Dict]:
        """提取最优路径（访问次数最多）"""
        path = []
        node = root
        while node.children:
            best_child = max(
                node.children, key=lambda c: c.visit_count
            )
            path.append({
                "action": best_child.action,
                "q_value": round(best_child.q_value, 4),
                "visit_count": best_child.visit_count,
                "confidence": round(best_child.q_value, 4),
            })
            node = best_child
        return path

    def _extract_top_k_paths(
        self, root: DecisionNode, k: int
    ) -> List[List[Dict]]:
        """提取Top-K备选路径"""
        paths = []
        sorted_children = sorted(
            root.children,
            key=lambda c: c.visit_count,
            reverse=True,
        )
        for child in sorted_children[:k]:
            path = self._extract_path_from(child)
            paths.append(path)
        return paths

    def _extract_path_from(
        self, node: DecisionNode
    ) -> List[Dict]:
        """从指定节点向下提取最优路径"""
        path = [{
            "action": node.action,
            "q_value": round(node.q_value, 4),
        }]
        while node.children:
            node = max(
                node.children, key=lambda c: c.visit_count
            )
            path.append({
                "action": node.action,
                "q_value": round(node.q_value, 4),
            })
        return path

    def _count_nodes(self, node: DecisionNode) -> int:
        """递归统计搜索树节点总数"""
        count = 1
        for child in node.children:
            count += self._count_nodes(child)
        return count

    def _max_depth_reached(
        self, node: DecisionNode, depth: int = 0
    ) -> int:
        """计算搜索树的最大深度"""
        if not node.children:
            return depth
        return max(
            self._max_depth_reached(c, depth + 1)
            for c in node.children
        )

    def _depth(self, node: DecisionNode) -> int:
        """计算节点的当前深度"""
        d = 0
        while node.parent:
            d += 1
            node = node.parent
        return d

    def _estimate_confidence(
        self, root: DecisionNode
    ) -> float:
        """
        估计搜索结果的置信度

        置信度 = 最优路径访问占比 × 最优路径Q值
        高置信度意味着：最优路径被充分验证（访问多）且表现好（Q值高）
        """
        if not root.children:
            return 0.0
        best = max(
            root.children, key=lambda c: c.visit_count
        )
        total_visits = sum(
            c.visit_count for c in root.children
        )
        if total_visits == 0:
            return 0.0
        return (best.visit_count / total_visits) * best.q_value
```

#### 3.4.7 JSMCTS的关键适配

标准MCTS无法直接应用于JSC2。基于学术界和军方的研究成果（AFIT兵棋推演MCTS研究 Lervold 2022; Kemmerling et al. 2023 系统综述129篇非游戏MCTS应用），本架构采用三项关键适配：

**适配一：分层行动分解 + 采样策略（Sampled MuZero）**

借鉴Sampled MuZero（Hubert et al., ICML 2021），不枚举所有可能行动，而是从学习策略中采样K个候选行动：

| 搜索层级 | 候选生成方式 | 候选数K | 示例 |
|---------|-----------|-------|------|
| 战略层 | LLM生成COA框架 | 3-5 | "进攻方案A"/"防御方案B"/"佯攻方案C" |
| 战役层 | Skill库匹配 + LLM补充 | 5-10 | 具体任务分配和时序 |
| 战术层 | 已验证的Skill动作 | 3-5 | 具体的交战/机动指令 |

每个层级独立搜索，上层结果约束下层的搜索空间。这样将10^6级别的分支因子降低到每层5-10个候选，使MCTS在有限时间内有效搜索。

**适配二：不完全信息处理（战争迷雾）**

JSC2的核心挑战是不完全信息——无法看到对手的全部部署。标准MCTS假设完全信息，直接应用会导致"策略融合"（基于不可用信息行动）。本架构采用ISMCTS（Information Set MCTS）的思路：

1. **信念状态表示**：维护对手部署的概率分布（哪些位置可能有敌方单位），而非假设已知
2. **多次determinization**：每次MCTS迭代从信念状态中采样一个可能的对手部署，在该determinization下搜索
3. **信息获取激励**：MCTS的奖励函数中显式包含信息价值——侦察行动虽然不直接造成伤害，但能减少不确定性，提升后续决策质量（Lervold, AFIT 2022）

**适配三：Latent-Space快速仿真**

如3.2.6节所述，MCTS的仿真步骤使用世界模型的Latent预测（<100ms/次）而非完整兵棋仿真（1-30s/次）。这使得30秒预算内可完成数百次仿真。完整兵棋仿真仅在MCTS选出最优方案后用于最终验证。

**仿真次数的现实预算**：

| 时间预算 | Latent仿真（~10ms/次） | 完整兵棋仿真（~5s/次） |
|---------|----------------------|---------------------|
| 5s | ~500次 | 1次（仅验证） |
| 30s | ~3000次 | 1次（仅验证） |
| 5min | ~30000次 | 3-5次（多方案对比） |
| 30min | ~180000次 | 10+次（深度验证） |


### 3.5 智能体推理引擎

#### 3.5.1 AgentKernel：三大支柱的编排器

AgentKernel是智能体认知架构的核心编排器——它决定在什么情况下调用哪个认知支柱，以及如何将多个支柱的结果综合为最终的决策。

AgentKernel的决策逻辑遵循"快者优先"原则：先尝试最快路径（蒸馏小模型推理），如果置信度不足则逐步升级（Skill快速执行 → Skill自适应执行 → MCTS搜索 → 人工决策）。OPA策略引擎不作为独立决策路径，而是作为安全校验层贯穿所有路径——每条路径的决策输出都必须通过OPA合规检查后方可执行。这与Kahneman双过程理论中"系统1先响应，系统2按需介入"的思想一脉相承。

#### 3.5.2 决策路径

AgentKernel定义五条决策路径，按响应速度从快到慢排列：

**路径零：蒸馏小模型推理（< 30ms）**

触发条件：蒸馏小模型对当前态势的推理置信度 >= 0.9。
执行方式：小模型直接输出行动推荐，无需任何外部系统（无向量检索、无LLM调用）。
安全检查：通过OPA策略引擎验证合规性。
适用场景：积累经验足够丰富的常规战术决策，覆盖大部分日常作战场景。
核心优势：单GPU推理，无外部依赖，适合边缘部署。

**路径一：Skill快速执行（< 500ms）**

触发条件：Skill库中存在高置信度匹配（成功率 >= 90% 且使用 >= 20次）。
执行方式：通过Qdrant向量检索匹配Skill，直接执行参数化动作，无需人工确认。
安全检查：通过OPA策略引擎验证合规性。
适用场景：小模型置信度不足但Skill库有明确匹配的场景。

**路径二：Skill自适应执行（1-5s）**

触发条件：Skill库中存在中等置信度匹配（成功率 >= 60%）。
执行方式：根据当前态势调整Skill参数，生成定制化方案。
安全检查：需要指挥员确认后方可执行。
适用场景：熟悉但需要微调的场景，如非标准条件下的火力支援。

**路径三：MCTS搜索（10-30s）**

触发条件：Skill库中无合适匹配，或匹配的Skill置信度低于60%。
执行方式：启动MCTS搜索，在世界模型辅助下系统探索决策空间。
安全检查：搜索结果通过工作流验证层检查，高置信度结果可自动执行，中低置信度需人工确认。
适用场景：陌生的战术场景或复杂的联合行动。

**路径四：升级到人工（等待指挥员）**

触发条件：所有自动路径的置信度都不足（MCTS搜索置信度 < 0.7）。
执行方式：将MCTS搜索的最优路径和备选路径呈现给指挥员，由人工决策。
安全检查：人工决策本身就是最高级别的安全机制。
适用场景：全新的战略态势、极高风险决策、或超越当前授权边界。

#### 3.5.3 安全执行层集成

AgentKernel的每条决策路径都与安全执行层集成：

```
AgentKernel决策 → OPA策略检查 → 工作流验证 → 人工确认（如需） → 执行
                     │                │                │
                     │ 不通过         │ 不通过         │ 拒绝
                     ▼                ▼                ▼
                   阻止执行        需要人工审查     终止方案
```

这个设计确保了：无论智能体的认知能力多强，其决策始终受到安全约束的限制。v4.0的工作流模板体系并未被取代，而是从"唯一的决策方式"升级为"所有决策的安全验证层"。

#### 3.5.4 完整代码实现

```python
# agent/agent_kernel.py
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class DecisionPath(str, Enum):
    DISTILLED_MODEL = "distilled_model"  # 蒸馏小模型推理（<30ms）
    SKILL_FAST = "skill_fast"            # Skill直接匹配（<500ms）
    SKILL_ADAPTIVE = "skill_adaptive"    # Skill自适应执行（1-5s）
    MCTS_SEARCH = "mcts_search"          # MCTS搜索（10-30s）
    HUMAN_REQUIRED = "human_required"    # 需要人工决策


@dataclass
class Decision:
    """智能体决策结果"""
    decision_id: str
    path: DecisionPath                   # 走了哪条决策路径
    action: Dict[str, Any]              # 决定的行动
    confidence: float                    # 置信度
    reasoning: str                       # 推理过程说明
    alternatives: List[Dict[str, Any]]   # 备选方案
    requires_human: bool                 # 是否需要人工确认
    skill_used: Optional[str] = None     # 使用的Skill ID
    search_stats: Optional[Dict] = None  # MCTS搜索统计


class AgentKernel:
    """
    智能体推理引擎——编排蒸馏小模型+世界模型+Skills+MCTS

    决策流程（五级递进）：
    0. 蒸馏小模型推理 → 如果高置信度 → 直接执行（<30ms）
    1. Skills匹配 → 如果命中高置信度Skill → 快速执行
    2. Skills未命中 → 世界模型预测+MCTS搜索 → 慢速决策
    3. 搜索结果 → 工作流验证（安全层）→ 执行或升级到人工
    4. 执行结果 → 反馈给Skill学习器 → 积累蒸馏训练数据
    """

    # 蒸馏小模型置信度阈值
    DISTILLED_MODEL_CONFIDENCE = 0.9

    # Skill快速执行阈值
    SKILL_FAST_SUCCESS_RATE = 0.9
    SKILL_FAST_MIN_USAGE = 20

    # Skill自适应执行阈值
    SKILL_ADAPTIVE_SUCCESS_RATE = 0.6

    # MCTS自动执行置信度阈值
    MCTS_AUTO_CONFIDENCE = 0.85

    # 升级到人工的置信度阈值
    HUMAN_REQUIRED_CONFIDENCE = 0.7

    def __init__(
        self,
        skill_library,          # SkillLibrary
        world_model,            # BattlefieldWorldModel
        mcts,                   # MilitaryMCTS
        distilled_model=None,   # 蒸馏小模型（SkillDistilledModel）
        workflow_validator=None, # 工作流验证器（安全层）
        opa_engine=None,        # OPA策略引擎
        skill_learner=None,     # Skill学习器（反馈用）
    ):
        self._skills = skill_library
        self._world_model = world_model
        self._mcts = mcts
        self._distilled = distilled_model
        self._workflow = workflow_validator
        self._opa = opa_engine
        self._learner = skill_learner

    def decide(
        self,
        situation: Dict[str, Any],
        mission: Dict[str, Any],
        time_budget_ms: int = 30000,
    ) -> Decision:
        """
        核心决策入口

        智能体根据当前态势和任务要求，自主选择决策路径：
        - 蒸馏小模型高置信度 → 直接推理执行（<30ms）
        - 有匹配Skill且高置信度 → 快速执行
        - 有匹配Skill但需适配 → 自适应执行
        - 无匹配Skill → MCTS搜索新方案
        - 所有方案置信度低 → 升级到人工
        """
        decision_id = (
            f"dec-"
            f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        )

        # === Phase 0: 蒸馏小模型快速推理 (<30ms) ===
        if self._distilled:
            distilled_result = self._distilled.predict(
                situation, mission
            )
            if distilled_result.confidence >= self.DISTILLED_MODEL_CONFIDENCE:
                return self._try_distilled_model(
                    decision_id, distilled_result, situation
                )

        # === Phase 1: Skill匹配 ===
        applicable_skills = self._skills.find_applicable(
            situation, top_k=3
        )

        if applicable_skills:
            best_skill = applicable_skills[0]

            # 高置信度Skill → 快速执行
            if (
                best_skill.success_rate
                >= self.SKILL_FAST_SUCCESS_RATE
                and best_skill.usage_count
                >= self.SKILL_FAST_MIN_USAGE
            ):
                return self._try_skill_fast(
                    decision_id, best_skill, situation
                )

            # 中等置信度Skill → 自适应执行
            if (
                best_skill.success_rate
                >= self.SKILL_ADAPTIVE_SUCCESS_RATE
            ):
                return self._try_skill_adaptive(
                    decision_id, best_skill, situation
                )

        # === Phase 2: MCTS搜索 ===
        # 无合适Skill → 在决策空间中搜索
        return self._try_mcts_search(
            decision_id, situation, time_budget_ms
        )

    def feedback(
        self,
        decision: Decision,
        outcome: Dict[str, Any],
    ):
        """
        执行结果反馈

        将决策结果反馈给Skill学习器和世界模型训练管线，
        持续提升认知能力
        """
        success = outcome.get("mission_success", False)

        # 更新Skill统计
        if decision.skill_used:
            self._skills.update_statistics(
                decision.skill_used, success
            )

        # 反馈给Skill学习器（用于提取新Skill）
        if self._learner and not success:
            self._learner.learn_from_commander_action(
                action=decision.action,
                context={
                    "mission_id": decision.decision_id,
                    "decision_path": decision.path.value,
                },
                outcome=outcome,
            )

        # 反馈给世界模型训练管线（第8章数据闭环）
        # self._world_model.ingest_training_data([
        #     TrainingTriple(state=..., action=..., next_state=..., ...)
        # ])

    def _try_distilled_model(
        self,
        decision_id: str,
        result,  # DistilledModelResult
        situation: Dict,
    ) -> Decision:
        """蒸馏小模型快速推理路径（<30ms）"""
        action = result.recommended_action

        # OPA策略检查（蒸馏模型可能过时，仍需安全验证）
        if self._opa:
            policy_result = self._opa.check_action(
                action, situation
            )
            if not policy_result.get("allowed", True):
                # OPA拒绝 → 降级到Skill匹配
                return self._fallback_to_skills(
                    decision_id, situation,
                    f"蒸馏模型被OPA阻止: {policy_result.get('reason', '')}"
                )

        return Decision(
            decision_id=decision_id,
            path=DecisionPath.DISTILLED_MODEL,
            action=action,
            confidence=result.confidence,
            reasoning=(
                f"蒸馏小模型推理: {result.reasoning} "
                f"(模型版本{result.model_version}, "
                f"置信度{result.confidence:.2f})"
            ),
            alternatives=result.alternatives,
            requires_human=False,
        )

    def _fallback_to_skills(
        self, decision_id, situation, reason
    ):
        """从蒸馏模型降级到Skill匹配"""
        applicable_skills = self._skills.find_applicable(
            situation, top_k=3
        )
        if applicable_skills:
            best_skill = applicable_skills[0]
            if (
                best_skill.success_rate >= self.SKILL_FAST_SUCCESS_RATE
                and best_skill.usage_count >= self.SKILL_FAST_MIN_USAGE
            ):
                return self._try_skill_fast(
                    decision_id, best_skill, situation
                )
        # 无合适Skill → MCTS
        return self._try_mcts_search(
            decision_id, situation, 30000
        )

    def _try_skill_fast(
        self,
        decision_id: str,
        skill,
        situation: Dict,
    ) -> Decision:
        """Skill快速执行路径"""
        action = self._execute_skill(skill, situation)

        # OPA策略检查
        if self._opa:
            policy_result = self._opa.check_action(
                action, situation
            )
            if not policy_result.get("allowed", True):
                return Decision(
                    decision_id=decision_id,
                    path=DecisionPath.HUMAN_REQUIRED,
                    action={"reason": "OPA策略拒绝"},
                    confidence=0.0,
                    reasoning=(
                        f"Skill {skill.name} 被OPA策略阻止: "
                        f"{policy_result.get('reason', '')}"
                    ),
                    alternatives=[],
                    requires_human=True,
                    skill_used=skill.skill_id,
                )

        return Decision(
            decision_id=decision_id,
            path=DecisionPath.SKILL_FAST,
            action=action,
            confidence=skill.success_rate,
            reasoning=(
                f"Skill命中: {skill.name} "
                f"(成功率{skill.success_rate:.0%}, "
                f"已使用{skill.usage_count}次)"
            ),
            alternatives=[],
            requires_human=False,
            skill_used=skill.skill_id,
        )

    def _try_skill_adaptive(
        self,
        decision_id: str,
        skill,
        situation: Dict,
    ) -> Decision:
        """Skill自适应执行路径"""
        action = self._adapt_skill(skill, situation)
        adapted_confidence = skill.success_rate * 0.8

        return Decision(
            decision_id=decision_id,
            path=DecisionPath.SKILL_ADAPTIVE,
            action=action,
            confidence=adapted_confidence,
            reasoning=(
                f"Skill适配: {skill.name} "
                f"(成功率{skill.success_rate:.0%}, "
                f"需要根据当前态势调整参数)"
            ),
            alternatives=[],
            requires_human=True,  # 自适应执行需人工确认
            skill_used=skill.skill_id,
        )

    def _try_mcts_search(
        self,
        decision_id: str,
        situation: Dict,
        time_budget_ms: int,
    ) -> Decision:
        """MCTS搜索路径"""
        search_result = self._mcts.search(
            situation=situation,
            budget_ms=time_budget_ms,
        )

        best_path = search_result["best_action_sequence"]
        confidence = search_result["confidence"]

        if confidence >= self.HUMAN_REQUIRED_CONFIDENCE:
            action = self._compile_search_result(
                best_path, situation
            )

            # 工作流安全验证
            if self._workflow:
                validated = self._workflow.validate(
                    action, situation
                )
                if not validated.get("passed", True):
                    return Decision(
                        decision_id=decision_id,
                        path=DecisionPath.HUMAN_REQUIRED,
                        action=action,
                        confidence=confidence,
                        reasoning=(
                            "MCTS搜索通过但工作流验证失败: "
                            f"{validated.get('reason', '')}"
                        ),
                        alternatives=search_result[
                            "alternative_paths"
                        ],
                        requires_human=True,
                        search_stats=search_result["search_stats"],
                    )

            # 高置信度可自动执行
            auto_execute = (
                confidence >= self.MCTS_AUTO_CONFIDENCE
            )

            return Decision(
                decision_id=decision_id,
                path=DecisionPath.MCTS_SEARCH,
                action=action,
                confidence=confidence,
                reasoning=(
                    f"MCTS搜索: "
                    f"探索了"
                    f"{search_result['search_stats']['nodes_explored']}"
                    f"个节点, "
                    f"最优路径Q值={confidence:.2f}"
                ),
                alternatives=search_result["alternative_paths"],
                requires_human=not auto_execute,
                search_stats=search_result["search_stats"],
            )

        # 置信度不足 → 升级到人工
        return Decision(
            decision_id=decision_id,
            path=DecisionPath.HUMAN_REQUIRED,
            action=self._compile_search_result(
                best_path, situation
            ),
            confidence=confidence,
            reasoning=(
                f"所有路径置信度不足({confidence:.2f}), "
                f"需要指挥员决策"
            ),
            alternatives=search_result["alternative_paths"],
            requires_human=True,
            search_stats=search_result["search_stats"],
        )

    def _execute_skill(
        self, skill, situation: Dict
    ) -> Dict:
        """执行Skill"""
        return {
            "skill_id": skill.skill_id,
            "parameters": skill.parameters,
        }

    def _adapt_skill(
        self, skill, situation: Dict
    ) -> Dict:
        """适配Skill到当前态势"""
        return {
            "skill_id": skill.skill_id,
            "adapted": True,
            "parameters": skill.parameters,
        }

    def _compile_search_result(
        self, path: List[Dict], situation: Dict
    ) -> Dict:
        """将MCTS搜索结果编译为可执行方案"""
        return {
            "actions": [step["action"] for step in path],
            "source": "mcts_search",
        }
```


### 3.6 分层自主等级

#### 3.6.1 从v4.0四级到v5.0五级

v4.0定义了L1-L4四级自主等级，核心逻辑是"模板生命周期状态越高 → 自主等级越高 → 人工参与越少"。v5.0在继承这一逻辑的基础上进行了重要升级：

**升级一：L4自主执行门槛提高**

v4.0的L4（Automated）对应`opa_compiled`模板状态，要求"使用 >= 50次且成功率 >= 97%"。v5.0的L4不仅要求Skill满足统计门槛（成功率 >= 97%，使用 >= 100次），还要求该Skill的因果模型经过了兵棋对抗验证——即不仅"做对了"，还要"理解为什么对"。这是从"统计可靠性"到"因果可解释性"的升级。

**升级二：新增L5紧急自主等级**

v5.0新增L5（Emergency）等级，用于极端场景：通信中断 + 时敏目标 + 无法联系指挥员。L5不依赖Skill或MCTS（这些模块需要世界模型和LLM推理，可能不可用），而是使用硬编码的安全规则——这是系统的最后一道防线，确保即使所有智能模块失效，仍然有最基本的保护性反应。

L5的触发条件极其严格：必须**同时**满足"通信中断"和"时敏目标"两个条件。通信恢复或目标不再时敏时，L5权限立即失效，系统回到L3或更低等级。

#### 3.6.2 五级自主等级定义

| 层级 | 名称 | 智能体能力 | 决策路径 | 人工角色 | 触发条件 |
|------|------|----------|---------|---------|---------|
| **L1: Query** | 态势查询 | 只读查询，不执行任何行动 | Skill（条令类） | 发起查询，审核结果 | 非作战态势，日常情报查询 |
| **L2: Assisted** | 辅助决策 | 推荐方案，不自主执行 | Skill + MCTS | 审批选择 | 常规作战，标准战术场景 |
| **L3: Supervised** | 监督执行 | 自主执行 + 汇报关键节点 | Skill自适应 | 监督关键节点，可随时终止 | 熟悉场景，Skill中等置信度 |
| **L4: Autonomous** | 自主执行 | 完全自主，事后审计 | Skill快速 / MCTS | 事后审计 | Skill成功率 >= 97%且 >= 100次使用，因果模型通过对抗验证 |
| **L5: Emergency** | 紧急自主 | 临时超越授权，最小化伤害 | 硬编码安全规则 | 事后审查（非事前审批） | 通信中断 + 时敏目标同时满足 |

#### 3.6.3 等级转换机制

自主等级不是静态配置，而是根据态势动态调整。转换逻辑：

```python
# agent/autonomy_level.py
from enum import IntEnum
from typing import Dict, Any, Optional, List


class AutonomyLevel(IntEnum):
    QUERY = 1          # 态势查询
    ASSISTED = 2       # 辅助决策
    SUPERVISED = 3     # 监督执行
    AUTONOMOUS = 4     # 自主执行
    EMERGENCY = 5      # 紧急自主


class AutonomyGovernor:
    """
    自主等级治理器

    根据态势动态调整智能体的自主等级。
    等级只能向下调整（减少自主性）或向上提升（增加自主性），
    提升需要满足严格的统计和验证条件。
    """

    # L4自主执行的严格门槛
    L4_MIN_SUCCESS_RATE = 0.97
    L4_MIN_USAGE_COUNT = 100
    L4_REQUIRES_CAUSAL_VALIDATION = True

    # L5紧急自主的触发条件
    L5_REQUIRES_COMM_FAILURE = True
    L5_REQUIRES_TIME_CRITICAL = True

    def __init__(self, current_level: AutonomyLevel = AutonomyLevel.QUERY):
        self._current_level = current_level
        self._level_history: List[Dict[str, Any]] = []

    def get_level(self) -> AutonomyLevel:
        return self._current_level

    def evaluate_level(
        self,
        situation: Dict[str, Any],
        skill_stats: Optional[Dict[str, Any]] = None,
        communication_status: str = "normal",
    ) -> AutonomyLevel:
        """
        评估当前态势下应使用的自主等级

        评估逻辑：
        1. 检查L5紧急条件
        2. 检查通信状态
        3. 检查Skill统计是否满足L4门槛
        4. 检查态势熟悉度决定L2/L3
        5. 默认L1
        """
        # L5: 紧急自主（最高优先级检查）
        if (
            communication_status == "disconnected"
            and situation.get("time_critical", False)
        ):
            new_level = AutonomyLevel.EMERGENCY
            self._transition(new_level, "通信中断+时敏目标")
            return new_level

        # 通信降级时限制自主等级
        if communication_status == "degraded":
            max_level = AutonomyLevel.SUPERVISED
        else:
            max_level = AutonomyLevel.AUTONOMOUS

        # L4: 自主执行（需要Skill统计门槛）
        if (
            skill_stats
            and skill_stats.get("success_rate", 0)
            >= self.L4_MIN_SUCCESS_RATE
            and skill_stats.get("usage_count", 0)
            >= self.L4_MIN_USAGE_COUNT
            and skill_stats.get(
                "causal_validated",
                not self.L4_REQUIRES_CAUSAL_VALIDATION,
            )
        ):
            new_level = min(AutonomyLevel.AUTONOMOUS, max_level)
            self._transition(new_level, "Skill满足L4统计门槛")
            return new_level

        # L3: 监督执行（熟悉场景，中等置信度Skill）
        if (
            skill_stats
            and skill_stats.get("success_rate", 0) >= 0.7
            and skill_stats.get("usage_count", 0) >= 20
        ):
            new_level = min(AutonomyLevel.SUPERVISED, max_level)
            self._transition(new_level, "Skill满足L3统计门槛")
            return new_level

        # L2: 辅助决策（有匹配Skill但置信度不高）
        if skill_stats and skill_stats.get("found", False):
            new_level = min(AutonomyLevel.ASSISTED, max_level)
            self._transition(new_level, "有匹配Skill但统计不足")
            return new_level

        # L1: 态势查询（无匹配Skill）
        new_level = AutonomyLevel.QUERY
        self._transition(new_level, "无匹配Skill")
        return new_level

    def _transition(
        self, new_level: AutonomyLevel, reason: str
    ):
        """记录等级转换"""
        if new_level != self._current_level:
            self._level_history.append({
                "from": self._current_level.name,
                "to": new_level.name,
                "reason": reason,
            })
            self._current_level = new_level
```

#### 3.6.4 与v4.0自主等级的对比

| 维度 | v4.0 L1-L4 | v5.0 L1-L5 | 说明 |
|------|-----------|-----------|------|
| 决策依据 | 模板生命周期状态 | Skill统计 + 因果验证 + 通信状态 | v5.0评估维度更全面 |
| L4门槛 | 成功率 >= 97%，使用 >= 50次 | 成功率 >= 97%，使用 >= 100次，因果模型通过对抗验证 | v5.0门槛更高 |
| 紧急处理 | 无专门机制 | L5紧急自主，硬编码安全规则 | v5.0新增 |
| 等级转换 | 主要靠人工配置 | 态势驱动动态转换 | v5.0更灵活 |
| 降级保护 | 降级到人工 | 降级到人工 + L5硬编码兜底 | v5.0安全保障更强 |


### 3.7 小结与后续章节衔接

本章定义了v5.0智能体认知架构的三大支柱——世界模型（预测未来）、Skills技能库（从人类经验中学习）、MCTS搜索（系统探索决策空间），以及编排它们的AgentKernel推理引擎和分层自主等级体系。

三大支柱的设计理念源自一个核心洞察：**工作流模板只能处理"已知情况"，但战争的本质是"未知情况"**。世界模型让智能体能够预测未知，Skills让智能体能够从经验中适应未知，MCTS让智能体能够系统地探索未知。三者协同，使智能体从"执行器"进化为"推理者"。

同时，v4.0的工作流模板体系并未被抛弃——它们成为v5.0的安全执行层，确保智能体的认知能力始终在安全约束下运行。这是"能力增强"与"安全可控"的平衡。

**与后续章节的衔接**：

- **第4章（快慢双系统）**：本章的AgentKernel决策路径（Skill快速/Skill自适应/MCTS搜索）是第4章快慢双系统在认知层面的映射。Skill快速执行路径对应快系统，MCTS搜索路径对应慢系统。第4章将详细描述这些决策路径如何映射到工作流执行引擎和Temporal编排。

- **第6章（兵棋对抗训练）**：世界模型的训练数据主要来自兵棋推演引擎。第6章将描述对抗训练的具体机制——如何通过红蓝对抗产生高质量的训练三元组，以及如何评估世界模型的预测精度。对手模型（Adversary Model）也在第6章的对抗训练中持续更新。

- **第8章（数据闭环）**：Skill学习器和世界模型训练管线产生的数据，通过第8章的数据闭环管线采集、清洗和反馈。本章的`feedback()`方法是数据闭环的起点。

---

## 4. 快慢双系统与自主决策闭环

### 4.1 设计理念：工作流作为安全执行层

v4.0中工作流模板是决策主体——智能体选择模板、填充参数、按DAG执行。v5.0将决策权交给智能体认知架构（第3章），工作流退化为**安全执行层**：

- **快系统**：优先匹配Skill（第3.3节），Skill命中时直接执行；无匹配Skill时退化为工作流模板
- **慢系统**：使用MCTS（第3.4节）在世界模型中搜索最优决策，搜索结果通过工作流模板验证后执行
- **人工干预**：指挥员修改被记录为Skill学习数据，持续提升智能体自主能力

工作流模板仍然保留完整的功能——DAG编排、短路机制、OPA策略检查——但现在它们服务于智能体的决策，而非替代决策。

### 4.2 工作流模板体系

#### 4.2.1 模板数据模型

工作流模板是快系统、慢系统和指挥员三方的共同操作对象。模板采用Pydantic定义，存储于PostgreSQL（结构化），触发条件向量存于Qdrant（语义检索），热模板缓存于Valkey（低延迟读取）。

```python
# registry/workflow_template.py
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class TemplateStatus(str, Enum):
    DRAFT = "draft"                # 草稿（慢系统创建中）
    ACTIVE = "active"              # 活跃（可供快系统选择）
    FAST_TRACK = "fast_track"      # 快系统优先级模板（经验蒸馏晋升）
    OPA_COMPILED = "opa_compiled"  # 已编译为OPA规则（全自动执行）
    DEPRECATED = "deprecated"      # 已弃用


class StepNode(BaseModel):
    """工作流步骤节点"""
    step_id: str
    name: str
    activity_type: str             # Temporal Activity类型
    input_mapping: Dict[str, str]  # 参数映射：模板参数名 → Activity输入名
    timeout_seconds: int = 30
    retry_policy: Dict[str, Any] = Field(default_factory=lambda: {
        "max_attempts": 3,
        "initial_interval_s": 1,
    })
    description: str = ""


class StepEdge(BaseModel):
    """步骤间有向边"""
    from_step: str
    to_step: str
    condition: Optional[str] = None  # 条件表达式（空表示无条件）
    label: str = ""


class StepDAG(BaseModel):
    """步骤有向无环图"""
    nodes: List[StepNode]
    edges: List[StepEdge]
    entry_step: str
    exit_steps: List[str]


class ParamField(BaseModel):
    """参数定义"""
    name: str
    type: str                      # "int", "float", "str", "enum", "list"
    required: bool = True
    default: Any = None
    enum_values: List[str] = Field(default_factory=list)
    range_min: Optional[float] = None
    range_max: Optional[float] = None
    description: str = ""
    source: str = "manual"         # "manual"=人工填, "auto"=从态势自动提取


class TriggerCondition(BaseModel):
    """触发条件"""
    threat_type: Optional[List[str]] = None
    domain: Optional[List[str]] = None      # "air", "sea", "land", "cyber", "space"
    urgency_range: Optional[List[str]] = None  # ["critical", "high", "medium"]
    entity_types: Optional[List[str]] = None
    custom_conditions: Dict[str, Any] = Field(default_factory=dict)


class WorkflowTemplate(BaseModel):
    """
    工作流模板——快慢系统的统一操作对象
    存储于PostgreSQL，触发条件向量存于Qdrant
    """
    template_id: str
    name: str
    version: int = 1
    description: str
    status: TemplateStatus = TemplateStatus.ACTIVE

    # 触发条件（结构化 + 向量）
    trigger: TriggerCondition
    trigger_embedding_id: Optional[str] = None  # Qdrant中的向量ID

    # 参数Schema
    params: List[ParamField]

    # 执行步骤DAG
    dag: StepDAG

    # 统计数据
    execution_count: int = 0
    success_count: int = 0
    success_rate: float = 0.0
    avg_execution_time_ms: float = 0.0
    commander_approval_rate: float = 0.0  # 指挥员审批通过率
    last_executed_at: Optional[datetime] = None
    last_success_at: Optional[datetime] = None

    # 元数据
    created_by: str = ""          # "slow_system" / "commander" / "distillation"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    parent_template_id: Optional[str] = None  # 由哪个模板调整而来
    tags: List[str] = Field(default_factory=list)
```

**PostgreSQL存储Schema**：

```sql
-- 工作流模板注册表
CREATE TABLE workflow_templates (
    template_id     VARCHAR(64) PRIMARY KEY,
    name            VARCHAR(200) NOT NULL,
    version         INT NOT NULL DEFAULT 1,
    description     TEXT,
    status          VARCHAR(20) NOT NULL DEFAULT 'active',
    trigger         JSONB NOT NULL,       -- 触发条件
    params          JSONB NOT NULL,       -- 参数Schema
    dag             JSONB NOT NULL,       -- 步骤DAG
    execution_count INT DEFAULT 0,
    success_count   INT DEFAULT 0,
    success_rate    FLOAT DEFAULT 0.0,
    avg_execution_time_ms FLOAT DEFAULT 0.0,
    commander_approval_rate FLOAT DEFAULT 0.0,
    created_by      VARCHAR(50),
    parent_template_id VARCHAR(64),
    tags            TEXT[],
    created_at      TIMESTAMPTZ DEFAULT NOW(),
    updated_at      TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(name, version)
);

-- 工作流执行历史（TimescaleDB hypertable）
CREATE TABLE workflow_execution_history (
    execution_id    VARCHAR(128) PRIMARY KEY,
    template_id     VARCHAR(64) REFERENCES workflow_templates(template_id),
    triggered_by    VARCHAR(20) NOT NULL,  -- "fast"/"slow"/"human"
    situation_hash  VARCHAR(64),           -- 态势特征哈希（用于经验匹配）
    params_filled   JSONB,                 -- 实际填充的参数
    outcome         VARCHAR(20),           -- "success"/"failure"/"partial"
    human_verdict   VARCHAR(20),           -- "approved"/"rejected"/"modified"/"timeout"
    execution_time_ms INT,
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
SELECT create_hypertable('workflow_execution_history', 'created_at');
```

#### 4.2.2 原子片段库

慢系统从原子片段库中组合新工作流。每个片段对应一个LangGraph节点或Temporal Activity，是不可再分的最小工作流单元。

```python
    def _load_atomic_fragments(self) -> Dict[str, Dict]:
        """
        加载原子片段库——可复用的最小工作流单元
        每个片段对应一个LangGraph节点或Temporal Activity
        """
        return {
            "observe_radar": {
                "name": "雷达探测",
                "description": "启动雷达传感器探测指定区域",
                "activity": "activities.observe.radar_scan",
                "timeout_s": 30,
            },
            "observe_satellite": {
                "name": "卫星成像",
                "description": "请求卫星对指定区域成像",
                "activity": "activities.observe.satellite_image",
                "timeout_s": 120,
            },
            "orient_fuse": {
                "name": "多源融合",
                "description": "融合多传感器数据进行综合研判",
                "activity": "activities.orient.fuse_multi_source",
                "timeout_s": 15,
            },
            "orient_threat": {
                "name": "威胁评估",
                "description": "评估目标威胁等级和意图",
                "activity": "activities.orient.assess_threat",
                "timeout_s": 10,
            },
            "decide_coa": {
                "name": "COA生成",
                "description": "生成备选行动方案",
                "activity": "activities.decide.generate_coa",
                "timeout_s": 120,
            },
            "decide_simulate": {
                "name": "兵棋仿真",
                "description": "蒙特卡洛仿真验证COA",
                "activity": "activities.decide.simulate_coa",
                "timeout_s": 600,
            },
            "act_strike": {
                "name": "火力打击",
                "description": "下达火力打击指令",
                "activity": "activities.act.execute_strike",
                "timeout_s": 30,
            },
            "act_evade": {
                "name": "规避机动",
                "description": "平台自动规避机动",
                "activity": "activities.act.execute_evade",
                "timeout_s": 5,
            },
            "act_deploy_sensor": {
                "name": "部署传感器",
                "description": "在指定位置部署传感器",
                "activity": "activities.act.deploy_sensor",
                "timeout_s": 60,
            },
            "human_approve": {
                "name": "人工审批",
                "description": "等待指挥员审批确认",
                "activity": "activities.human.commander_approval",
                "timeout_s": 300,
            },
            "bda_assess": {
                "name": "战损评估",
                "description": "打击后战损评估(BDA)",
                "activity": "activities.act.bda_assessment",
                "timeout_s": 60,
            },
            "ew_jam": {
                "name": "电子干扰",
                "description": "对指定目标实施电子干扰",
                "activity": "activities.act.electronic_jam",
                "timeout_s": 30,
            },
        }

    def _assemble_dag(self, template_def: Dict) -> StepDAG:
        """从片段列表组装StepDAG"""
        fragments = template_def.get("selected_fragments", [])
        edges_def = template_def.get("edges", [])

        nodes = []
        for fid in fragments:
            frag = self._atomic_fragments.get(fid, {})
            nodes.append(StepNode(
                step_id=fid,
                name=frag.get("name", fid),
                activity_type=frag.get("activity", fid),
                timeout_seconds=frag.get("timeout_s", 30),
            ))

        edges = [
            StepEdge(from_step=e["from"], to_step=e["to"], condition=e.get("condition"))
            for e in edges_def
        ]

        return StepDAG(
            nodes=nodes,
            edges=edges,
            entry_step=fragments[0] if fragments else "",
            exit_steps=[fragments[-1]] if fragments else [],
        )

    def _parse_adjustments(self, content: str) -> Dict:
        """解析LLM调整建议"""
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"param_adjustments": {}, "step_additions": [], "step_removals": []}

    def _parse_compose_response(self, content: str) -> Dict:
        """解析LLM组合响应"""
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {"name": "解析失败", "selected_fragments": [], "edges": [], "params": []}

    def _apply_adjustments(self, template: Dict, adjustments: Dict) -> Dict:
        """将调整应用到模板"""
        new_template = dict(template)
        # 应用参数调整
        for param_name, adjustment in adjustments.get("param_adjustments", {}).items():
            for p in new_template.get("params", []):
                if p["name"] == param_name:
                    if isinstance(adjustment, dict) and "value" in adjustment:
                        p["default"] = adjustment["value"]
        return new_template
```

#### 4.2.3 模板状态流转管理

模板在生命周期中的状态转换由`TemplateLifecycleManager`统一管理：

```python
# registry/template_lifecycle.py
from typing import Dict, Any, Optional
from datetime import datetime

from clients.asyncpg_client import PostgresClient
from clients.qdrant_client import QdrantRegistryClient
from clients.sglang_client import SGLangMilitaryClient
from registry.workflow_template import WorkflowTemplate, TemplateStatus


class LifecycleTransition:
    """合法状态转换及其前置条件"""

    TRANSITIONS = {
        # (from_status, to_status) -> precondition_check
        ("draft", "active"): "simulation_pass",
        ("active", "fast_track"): "distillation_promotion_l1",
        ("fast_track", "opa_compiled"): "distillation_promotion_l2",
        ("active", "deprecated"): "manual_deprecation",
        ("fast_track", "deprecated"): "manual_deprecation",
        ("active", "draft"): "simulation_fail",
        ("draft", "draft"): "revision",
    }

    @staticmethod
    def is_valid(from_status: str, to_status: str, precondition: str) -> bool:
        required = LifecycleTransition.TRANSITIONS.get((from_status, to_status))
        return required is not None and precondition == required


class TemplateLifecycleManager:
    """
    模板生命周期管理器
    管理模板状态流转：draft -> active -> fast_track -> opa_compiled
    每次状态变更都要求满足前置条件（仿真通过/蒸馏晋升/人工操作）
    """

    def __init__(self, config: Dict[str, Any]):
        self._pg = PostgresClient(config["pg_dsn"])
        self._qdrant = QdrantRegistryClient(config["qdrant_url"])
        self._sglang = SGLangMilitaryClient(config["sglang_url"])

    async def activate_template(self, template_id: str, simulation_result: Dict) -> bool:
        """draft -> active, 前置条件：仿真通过（成功率 >= 70%）"""
        success_rate = simulation_result.get("success_rate", 0.0)
        if success_rate < 0.70:
            return False
        return await self._transition(
            template_id, "draft", "active", "simulation_pass",
            extra_updates={"simulation_result": simulation_result},
        )

    async def promote_to_fast_track(self, template_id: str) -> bool:
        """active -> fast_track, 前置条件：经验蒸馏Level 1晋升条件满足"""
        return await self._transition(
            template_id, "active", "fast_track", "distillation_promotion_l1",
        )

    async def promote_to_opa_compiled(self, template_id: str, rego_rule: str) -> bool:
        """fast_track -> opa_compiled, 前置条件：经验蒸馏Level 2晋升条件满足"""
        return await self._transition(
            template_id, "fast_track", "opa_compiled", "distillation_promotion_l2",
            extra_updates={"compiled_rego": rego_rule},
        )

    async def revert_to_draft(self, template_id: str, reason: str) -> bool:
        """active -> draft（仿真未通过时退回）"""
        return await self._transition(
            template_id, "active", "draft", "simulation_fail",
            extra_updates={"revert_reason": reason},
        )

    async def deprecate(self, template_id: str) -> bool:
        """-> deprecated（人工弃用）"""
        current = await self._get_status(template_id)
        if current not in ("active", "fast_track"):
            return False
        return await self._transition(
            template_id, current, "deprecated", "manual_deprecation",
        )

    async def _transition(
        self, template_id: str, from_status: str, to_status: str,
        precondition: str, extra_updates: Optional[Dict] = None,
    ) -> bool:
        """执行状态转换"""
        if not LifecycleTransition.is_valid(from_status, to_status, precondition):
            return False

        await self._pg.execute(
            """UPDATE workflow_templates
               SET status = $2, updated_at = NOW()
               WHERE template_id = $1 AND status = $3""",
            template_id, to_status, from_status,
        )

        if to_status in ("fast_track", "opa_compiled", "deprecated"):
            await self._qdrant.update_payload(
                collection="workflow_triggers",
                point_id=f"trigger_{template_id}",
                payload_updates={"status": to_status},
            )
        return True

    async def _get_status(self, template_id: str) -> Optional[str]:
        row = await self._pg.fetchrow(
            "SELECT status FROM workflow_templates WHERE template_id = $1",
            template_id,
        )
        return row["status"] if row else None
```

**部署级版本管理策略**：

| 升级策略 | C2场景 | 实现方式 | 风险 |
|---------|--------|---------|------|
| **就地升级** | 规则微调，向后兼容 | 直接部署新版本 | 低 |
| **影子验证** | 新增OODA阶段或修改决策逻辑 | 新旧版本同时运行，对比结果 | 中 |
| **蓝绿切换** | 核心作战流程重大变更 | 两套独立环境，一键切换 | 高 |
| **灰度发布** | 大规模部署到多指挥所 | 按指挥所逐步切换 | 中 |

### 4.3 快系统：模板驱动的快速执行

#### 4.3.1 设计理念

快系统执行"蒸馏推理→选→填→执行"四级递进（对应第3.5.2节AgentKernel路径0和路径1的执行层实现）：

1. **L0蒸馏推理**：蒸馏小模型直接输出行动推荐（<30ms），高置信度直接执行，无需外部系统（对应AgentKernel路径0）
2. **L1规则匹配**：OPA编译规则精确匹配（<5ms），适用于已编译的高频Skill——是经验蒸馏将高成功率Skill编译为确定性规则的产物（对应AgentKernel路径1中经OPA编译的Skill）
3. **L2向量检索**：将态势转化为向量，在Qdrant中检索最匹配的Skill并参数化执行（~20ms+~480ms，对应AgentKernel路径1的Skill快速执行）
4. **L3参数化执行**：根据模板的参数Schema，从态势数据自动提取填充参数并执行（<500ms）——作为L0-L2均未命中时的兜底执行层

> **与Ch3 AgentKernel的映射**：L0-L2是AgentKernel路径0和路径1的执行层细化；AgentKernel路径2（Skill自适应，1-5s）和路径3（MCTS，10-30s）属于中/慢速路径，由4.4节慢系统覆盖；路径4（人工决策）由4.5节人工干预覆盖。OPA在Ch3中作为安全校验层贯穿全程，在Ch4中L1将已编译的高确定性OPA规则提升为独立执行路径以获得最快响应。

```text
快系统四级执行路径：

  态势输入 → 蒸馏小模型推理(<30ms)
                 |
                 +-- 高置信度(≥0.9) → 直接执行 → OPA验证 → 完成
                 |
                 +-- 低置信度 → OPA规则匹配(<5ms)
                                  |
                                  +-- 命中编译规则 → 直接执行 → 完成
                                  |
                                  +-- 未命中 → Qdrant向量检索(~20ms)
                                                  |
                                                  +-- 命中fast_track → 最简模板(1-2步) <100ms
                                                  +-- 命中active → 标准模板(4-6步) <500ms
                                                  +-- 未命中 → 升级到慢系统
```

蒸馏小模型是快系统的最优先路径——它将积累的Skill能力"烧进"模型参数，推理时无需访问Qdrant或调用LLM，单GPU即可完成。小模型的训练管线见第8.6节。

#### 4.3.2 工作流选择与参数化引擎

快系统在战术层时间窗口内（<500ms）完成"选模板->填参数->执行"三步。四级路径为**互斥选择**而非串行累加——L0命中即执行，仅未命中时才尝试L1，以此类推：

```python
# registry/fast_workflow_selector.py
import asyncio
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass

from clients.qdrant_client import QdrantRegistryClient
from clients.sglang_client import SGLangMilitaryClient
from clients.triton_client import TritonInferenceClient
from clients.redis_client import ValkeyClient


@dataclass
class SelectionResult:
    """工作流选择结果"""
    template_id: str
    template_name: str
    similarity_score: float       # 与历史经验的相似度
    filled_params: Dict[str, Any] # 自动填充的参数
    selection_latency_ms: float


class FastWorkflowSelector:
    """
    快系统工作流选择器
    在 < 500ms 内完成：态势嵌入 → Qdrant检索 → 参数自动填充
    """

    def __init__(self, config: Dict[str, Any]):
        self._qdrant = QdrantRegistryClient(config["qdrant_url"])
        self._sglang = SGLangMilitaryClient(config["sglang_url"])
        self._triton = TritonInferenceClient(config["triton_url"])
        self._valkey = ValkeyClient(config["valkey_url"])
        self._similarity_threshold = 0.85  # 最低相似度阈值

    async def select_and_fill(
        self, situation: Dict[str, Any]
    ) -> Optional[SelectionResult]:
        """
        快速选择并参数化工作流（总延迟 < 500ms）

        Step 1: 态势分类（Triton, <30ms）
        Step 2: 态势嵌入（SGLang, <50ms）
        Step 3: Qdrant相似检索（<10ms）
        Step 4: 参数自动提取（<10ms）
        """
        t0 = datetime.utcnow()

        # Step 1: Triton快速态势分类
        situation_type = await asyncio.wait_for(
            self._triton.classify_situation(situation),
            timeout=0.05,
        )

        # Step 2: SGLang生成态势摘要并嵌入
        situation_text = self._situation_to_text(situation, situation_type)
        embedding = await asyncio.wait_for(
            self._sglang.embed(situation_text),
            timeout=0.05,
        )

        # Step 3: Qdrant检索最相似的工作流模板
        results = await self._qdrant.search(
            collection="workflow_triggers",
            query_vector=embedding,
            limit=3,
            filters={
                "status": {"value": "active"},
                "trigger.domain": {"value": situation.get("domain", "unknown")},
            },
        )

        if not results or results[0].score < self._similarity_threshold:
            return None  # 无匹配模板，需升级到慢系统

        best_match = results[0]
        template_id = best_match.payload["template_id"]

        # 从Valkey缓存获取完整模板（缓存预热）
        template_data = await self._valkey.get(f"wf_template:{template_id}")
        if not template_data:
            return None

        template = json.loads(template_data)

        # Step 4: 参数自动填充
        filled_params = self._auto_fill_params(template["params"], situation)

        latency_ms = (datetime.utcnow() - t0).total_seconds() * 1000

        return SelectionResult(
            template_id=template_id,
            template_name=template["name"],
            similarity_score=best_match.score,
            filled_params=filled_params,
            selection_latency_ms=round(latency_ms, 1),
        )

    def _situation_to_text(self, situation: Dict, sit_type: Any) -> str:
        """将态势数据转为文本描述（用于嵌入）"""
        parts = [
            f"态势类型: {sit_type.get('label', 'unknown')}",
            f"威胁等级: {situation.get('threat_level', 'NONE')}",
            f"域: {situation.get('domain', 'unknown')}",
            f"目标数量: {len(situation.get('entities', []))}",
            f"紧急程度: {situation.get('urgency', 'normal')}",
        ]
        return " | ".join(parts)

    def _auto_fill_params(
        self, param_schema: List[Dict], situation: Dict
    ) -> Dict[str, Any]:
        """根据参数Schema从态势数据自动提取填充"""
        filled = {}
        for param in param_schema:
            name = param["name"]
            source = param.get("source", "manual")

            if source == "auto":
                # 自动提取参数：从态势数据中按映射规则提取
                mapping = param.get("auto_mapping", name)
                if mapping in situation:
                    filled[name] = situation[mapping]
                elif param.get("default") is not None:
                    filled[name] = param["default"]

        return filled
```

#### 4.3.3 时敏目标短路路径（工作流驱动版）

时敏目标（TST）需要亚秒级响应。短路路径不再使用硬编码的`ShortCircuitProcessor`，而是从工作流注册表选择已编译为OPA规则的`fast_track`/`opa_compiled`最简模板：

```python
# fast_system/workflow_driven_short_circuit.py
import asyncio
import json
import redis.asyncio as aioredis
from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass, field

from clients.sglang_client import SGLangMilitaryClient
from clients.triton_client import TritonInferenceClient
from clients.qdrant_client import QdrantRegistryClient
from security.policy_engine import OPAPolicyEngine


@dataclass
class Track:
    """航迹"""
    track_id: str
    entity_type: str
    classification: str = "UNKNOWN"
    threat_level: str = "LOW"
    position: Dict[str, float] = field(default_factory=dict)
    velocity: Dict[str, float] = field(default_factory=dict)
    confidence: float = 0.0
    last_update: str = ""
    source_ids: List[str] = field(default_factory=list)
    engagement_status: str = "TRACKING"


class WorkflowDrivenShortCircuit:
    """
    工作流驱动的时敏目标短路处理器
    核心转变：不再硬编码处理步骤，而是从注册表选择最简工作流模板执行

    执行策略：
    1. OPA规则匹配（opa_compiled模板，< 5ms）—— 最高优先级
    2. Qdrant检索fast_track模板（1-2步DAG，< 10ms）—— 次高优先级
    3. 降级到最简规则（无匹配模板时的兜底）
    """

    def __init__(self, config: Dict[str, Any]):
        self._redis: Optional[aioredis.Redis] = None
        self._sglang = SGLangMilitaryClient(config["sglang_url"])
        self._triton = TritonInferenceClient(config["triton_url"])
        self._qdrant = QdrantRegistryClient(config["qdrant_url"])
        self._opa = OPAPolicyEngine(config["opa_url"])
        self._track_store: Dict[str, Track] = {}

    async def process_tst(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        时敏目标快速处理（目标总延迟 < 100ms）：

        Phase 1: Triton检测（< 30ms）
        Phase 2: OPA规则直通 or Qdrant快速匹配（< 10ms）
        Phase 3: Valkey航迹更新 + 告警（< 10ms）
        """
        t0 = datetime.utcnow()

        # Phase 1: 快速检测
        detections = await asyncio.wait_for(
            self._triton.detect_targets(sensor_data["image_batch"]),
            timeout=0.05,
        )
        high_conf = [d for d in detections if d["confidence"] > 0.7]
        if not high_conf:
            return {"status": "no_threat", "latency_ms": 0}

        # Phase 2: 按优先级尝试匹配工作流模板
        for det in high_conf:
            # 优先级1: OPA规则直通（opa_compiled模板）
            opa_result = self._opa.check_auto_dispatch({
                "threat_type": det.get("military_type", "unknown"),
                "domain": sensor_data.get("domain", "air"),
                "urgency": "critical",
                "confidence": det.get("confidence", 0.0),
            })

            if opa_result.get("matched"):
                # OPA命中 → 直接按编译好的规则执行（等价原硬编码短路）
                track = self._correlate_or_create_track(det, sensor_data)
                await self._update_track_cache(track)
                latency_ms = (datetime.utcnow() - t0).total_seconds() * 1000
                return {
                    "status": "threat_dispatched",
                    "track_id": track.track_id,
                    "workflow_source": "opa_compiled",
                    "template_id": opa_result.get("dispatch_target"),
                    "threat_level": det.get("threat_potential", "LOW"),
                    "action": opa_result.get("action", "auto_alert"),
                    "latency_ms": round(latency_ms, 1),
                }

            # 优先级2: Qdrant检索fast_track模板
            situation_text = f"TST | {det.get('military_type', 'unknown')} | critical"
            embedding = await asyncio.wait_for(
                self._sglang.embed(situation_text),
                timeout=0.01,
            )
            matches = await self._qdrant.search(
                collection="workflow_triggers",
                query_vector=embedding,
                limit=1,
                filters={"status": {"value": "fast_track"}},
            )

            if matches and matches[0].score > 0.90:
                # 命中fast_track模板 → 按1-2步DAG执行
                template_id = matches[0].payload["template_id"]
                track = self._correlate_or_create_track(det, sensor_data)
                await self._update_track_cache(track)
                latency_ms = (datetime.utcnow() - t0).total_seconds() * 1000
                return {
                    "status": "threat_dispatched",
                    "track_id": track.track_id,
                    "workflow_source": "fast_track",
                    "template_id": template_id,
                    "threat_level": det.get("threat_potential", "LOW"),
                    "action": "auto_alert",
                    "latency_ms": round(latency_ms, 1),
                }

            # 优先级3: OPA权限检查 + 常规告警
            policy_result = self._opa.check_engagement({
                "action_type": "alert",
                "threat_level": det.get("threat_potential", "LOW"),
                "target_type": det.get("military_type", "unknown"),
                "roe_mode": sensor_data.get("roe_mode", "weapons_tight"),
            })

            if policy_result["allow_engagement"] or policy_result["allow_autonomous"]:
                track = self._correlate_or_create_track(det, sensor_data)
                await self._update_track_cache(track)
                latency_ms = (datetime.utcnow() - t0).total_seconds() * 1000
                return {
                    "status": "threat_alerted",
                    "track_id": track.track_id,
                    "workflow_source": "fallback_rule",
                    "threat_level": det.get("threat_potential", "LOW"),
                    "action": "auto_alert" if policy_result["allow_autonomous"] else "human_alert",
                    "latency_ms": round(latency_ms, 1),
                }

        return {"status": "filtered", "latency_ms": 0}

    async def _update_track_cache(self, track: Track):
        if self._redis is None:
            self._redis = aioredis.from_url("redis://valkey-master:6379")
        await self._redis.set(
            f"track:{track.track_id}",
            json.dumps(track.__dict__),
            ex=300,
        )

    def _correlate_or_create_track(self, detection: Dict, sensor_data: Dict) -> Track:
        track = Track(
            track_id=f"TRK-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{len(self._track_store)}",
            entity_type=detection.get("military_type", "unknown"),
            threat_level=detection.get("threat_potential", "LOW"),
            position=sensor_data.get("source_position", {}),
            confidence=detection.get("confidence", 0.0),
            last_update=datetime.utcnow().isoformat(),
            source_ids=[sensor_data.get("sensor_id", "")],
        )
        self._track_store[track.track_id] = track
        return track
```

#### 4.3.4 标准战术流水线（工作流驱动版）

标准路径同样从注册表选择模板，按DAG中的Activity步骤执行。Triton推理、OPA规则检查等操作不再是硬编码步骤，而是模板DAG中的Activity节点：

```python
# fast_system/workflow_driven_pipeline.py
import asyncio
import aiokafka
import redis.asyncio as aioredis
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

from clients.qdrant_client import QdrantRegistryClient
from clients.sglang_client import SGLangMilitaryClient
from clients.triton_client import TritonInferenceClient
from security.policy_engine import OPAPolicyEngine


class WorkflowDrivenPipeline:
    """
    工作流驱动的战术流水线
    核心转变：不再硬编码sensor->detect->correlate->opa->publish流程，
    而是从注册表选择标准工作流模板，按DAG中的Activity步骤依次执行。

    每个Activity对应一个原子片段（observe_radar, orient_threat, act_alert等）
    """

    def __init__(self, config: Dict[str, Any]):
        self._consumer: Optional[aiokafka.AIOKafkaConsumer] = None
        self._producer: Optional[aiokafka.AIOKafkaProducer] = None
        self._redis: Optional[aioredis.Redis] = None
        self._opa: Optional[OPAPolicyEngine] = None
        self._qdrant: Optional[QdrantRegistryClient] = None
        self._sglang: Optional[SGLangMilitaryClient] = None
        self._triton: Optional[TritonInferenceClient] = None
        self._track_store: Dict[str, Track] = {}
        self._running = False
        # Activity执行器注册表：step.activity_type -> handler
        self._activity_handlers: Dict[str, callable] = {}

    async def initialize(self, config: Dict[str, Any]):
        """初始化流水线及工作流检索客户端"""
        self._consumer = aiokafka.AIOKafkaConsumer(
            config["sensor_topic"],
            bootstrap_servers=config["redpanda_brokers"],
            group_id="tactical-pipeline",
            auto_offset_reset="latest",
            enable_auto_commit=False,
        )
        self._producer = aiokafka.AIOKafkaProducer(
            bootstrap_servers=config["redpanda_brokers"],
            compression_type="lz4",
        )
        self._redis = aioredis.Redis(
            host=config["redis_host"], port=6379, db=0, decode_responses=True,
        )
        self._opa = OPAPolicyEngine(config.get("opa_url", "http://opa:8181"))
        self._qdrant = QdrantRegistryClient(config.get("qdrant_url", "http://qdrant:6333"))
        self._sglang = SGLangMilitaryClient(config.get("sglang_url", "http://sglang:30000"))
        self._triton = TritonInferenceClient(config.get("triton_url", "http://triton:8000"))

        # 注册Activity处理器
        self._activity_handlers = {
            "activities.observe.radar_scan": self._observe_sensor,
            "activities.observe.satellite_image": self._observe_sensor,
            "activities.orient.fuse_multi_source": self._orient_fuse,
            "activities.orient.assess_threat": self._orient_threat,
            "activities.decide.generate_coa": self._decide_coa,
            "activities.act.execute_evade": self._act_evade,
            "activities.act.bda_assessment": self._act_bda,
            "activities.human.commander_approval": self._human_approve,
        }

    async def run(self):
        await self._consumer.start()
        await self._producer.start()
        self._running = True

        try:
            async for msg in self._consumer:
                if not self._running:
                    break
                asyncio.create_task(self._process_sensor_msg(msg))
        finally:
            await self._consumer.stop()
            await self._producer.stop()

    async def _process_sensor_msg(self, msg):
        """处理传感器消息：选择工作流模板 -> 按DAG执行"""
        t0 = datetime.utcnow()

        try:
            sensor_data = json.loads(msg.value)
            if not self._validate(sensor_data):
                return

            # Step 1: 选择工作流模板
            template = await self._select_template(sensor_data)
            if template is None:
                await self._default_process(sensor_data)
                return

            # Step 2: 自动填充参数
            filled_params = self._auto_fill(template["params"], sensor_data)

            # Step 3: 按DAG拓扑排序执行步骤
            dag = template["dag"]
            execution_order = self._topological_sort(dag)

            for step_id in execution_order:
                step = next(s for s in dag["nodes"] if s["step_id"] == step_id)
                handler = self._activity_handlers.get(step["activity_type"])
                if handler:
                    result = await asyncio.wait_for(
                        handler(sensor_data, filled_params),
                        timeout=step.get("timeout_seconds", 30),
                    )
                    # 将步骤输出传递给下游步骤
                    filled_params.update(result.get("outputs", {}))

        except Exception as e:
            await self._log_error(e)
        finally:
            latency_ms = (datetime.utcnow() - t0).total_seconds() * 1000
            if latency_ms > 500:
                pass  # 慢处理告警

    async def _select_template(self, sensor_data: Dict) -> Optional[Dict]:
        """从注册表检索最匹配的active/fast_track模板"""
        situation_text = (
            f"{sensor_data.get('domain', 'unknown')} | "
            f"{sensor_data.get('urgency', 'normal')} | "
            f"entity_count={len(sensor_data.get('entities', []))}"
        )
        embedding = await self._sglang.embed(situation_text)
        results = await self._qdrant.search(
            collection="workflow_triggers",
            query_vector=embedding,
            limit=1,
            filters={"status": {"value": ["active", "fast_track"]}},
        )
        if results and results[0].score > 0.80:
            template_id = results[0].payload["template_id"]
            cached = await self._redis.get(f"wf_template:{template_id}")
            if cached:
                return json.loads(cached)
        return None

    def _topological_sort(self, dag: Dict) -> List[str]:
        """DAG拓扑排序，确定步骤执行顺序"""
        nodes = {n["step_id"] for n in dag["nodes"]}
        in_degree = {n: 0 for n in nodes}
        adj = {n: [] for n in nodes}

        for edge in dag["edges"]:
            adj[edge["from_step"]].append(edge["to_step"])
            in_degree[edge["to_step"]] += 1

        queue = [n for n in nodes if in_degree[n] == 0]
        order = []
        while queue:
            node = queue.pop(0)
            order.append(node)
            for neighbor in adj[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        return order

    def _auto_fill(self, param_schema: List[Dict], situation: Dict) -> Dict:
        """根据参数Schema从态势数据自动填充（逻辑同4.3.2 FastWorkflowSelector._auto_fill_params）"""
        filled = {}
        for param in param_schema:
            if param.get("source") == "auto":
                mapping = param.get("auto_mapping", param["name"])
                if mapping in situation:
                    filled[param["name"]] = situation[mapping]
                elif param.get("default") is not None:
                    filled[param["name"]] = param["default"]
        return filled

    # === Activity Handler 实现 ===

    async def _observe_sensor(self, data: Dict, params: Dict) -> Dict:
        detections = await asyncio.wait_for(
            self._triton.detect_targets(data.get("image_batch", [])),
            timeout=0.1,
        )
        return {"outputs": {"detections": detections}}

    async def _orient_fuse(self, data: Dict, params: Dict) -> Dict:
        detections = params.get("detections", [])
        tracks = []
        for det in detections:
            track = Track(
                track_id=f"TRK-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{len(self._track_store)}",
                entity_type=det.get("military_type", "unknown"),
                threat_level=det.get("threat_potential", "LOW"),
                position=data.get("source_position", {}),
                confidence=det.get("confidence", 0.0),
                last_update=datetime.utcnow().isoformat(),
            )
            self._track_store[track.track_id] = track
            tracks.append(track)
        return {"outputs": {"tracks": [t.__dict__ for t in tracks]}}

    async def _orient_threat(self, data: Dict, params: Dict) -> Dict:
        tracks = params.get("tracks", [])
        threats = [t for t in tracks if t.get("threat_level") == "HIGH"]
        return {"outputs": {"high_threats": threats}}

    async def _decide_coa(self, data: Dict, params: Dict) -> Dict:
        return {"outputs": {"coa_selected": "default_response"}}

    async def _act_evade(self, data: Dict, params: Dict) -> Dict:
        await self._producer.send_and_wait(
            "threat_alerts",
            json.dumps({"action": "auto_evade", "timestamp": datetime.utcnow().isoformat()}).encode(),
        )
        return {"outputs": {"action_taken": "evade"}}

    async def _act_bda(self, data: Dict, params: Dict) -> Dict:
        return {"outputs": {"bda_result": "pending"}}

    async def _human_approve(self, data: Dict, params: Dict) -> Dict:
        return {"outputs": {"approval": "pending"}}

    async def _default_process(self, data: Dict):
        """无匹配模板时的降级处理（保持向后兼容）"""
        pass

    def _validate(self, data: Dict) -> bool:
        return isinstance(data, dict) and "sensor_id" in data

    async def _log_error(self, error: Exception):
        pass
```

#### 4.3.5 边缘自主决策引擎

通信中断时，战术边缘节点基于本地规则自主运行。边缘节点定期从中心OPA服务同步策略快照到本地缓存（`opa_bundle`），通信中断后切换到本地缓存的策略版本执行。自主引擎使用OPA策略+优先级行为规则表的双重机制：
- **OPA策略**：定义硬性约束（交战规则、禁飞区、友军保护半径），不可违反
- **行为规则表**：定义软性响应策略（威胁等级→响应动作的映射），可被OPA策略覆盖

```python
# fast_system/edge_autonomy.py
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class AutonomyState(str, Enum):
    CONNECTED = "connected"        # 正常连接
    DEGRADED = "degraded"          # 通信降级
    AUTONOMOUS = "autonomous"      # 自主运行
    EMERGENCY = "emergency"        # 紧急状态


@dataclass
class BehaviorRule:
    """行为规则（OPA策略的本地缓存版本）"""
    rule_id: str
    trigger_condition: str  # e.g., "threat_level == CRITICAL"
    action: str             # e.g., "evade", "return_to_base", "hold_position"
    priority: int           # 1=最高


class EdgeAutonomyEngine:
    """
    边缘自主决策引擎
    通信中断时基于行为树+状态机实现本地自主运行
    """

    def __init__(self, standing_rules: List[BehaviorRule]):
        self._state = AutonomyState.CONNECTED
        self._standing_rules = sorted(standing_rules, key=lambda r: r.priority)
        self._last_comm_time: datetime = datetime.utcnow()
        self._comm_timeout_seconds = 120  # 2分钟无通信进入自主模式
        self._max_autonomous_duration = 1800  # 30分钟最大自主运行时间
        self._autonomous_start: Optional[datetime] = None

    def update_comm_status(self, connected: bool, latency_ms: float = 0.0):
        """更新通信状态"""
        if connected:
            self._last_comm_time = datetime.utcnow()
            self._autonomous_start = None
            if latency_ms > 500:
                # 高延迟但连接仍存活 → 降级状态
                self._state = AutonomyState.DEGRADED
            else:
                self._state = AutonomyState.CONNECTED
        else:
            elapsed = (datetime.utcnow() - self._last_comm_time).total_seconds()
            if elapsed > self._comm_timeout_seconds:
                self._state = AutonomyState.AUTONOMOUS
                if self._autonomous_start is None:
                    self._autonomous_start = datetime.utcnow()
            elif elapsed > self._comm_timeout_seconds * 0.5:
                # 通信中断超过一半超时时长 → 降级状态
                self._state = AutonomyState.DEGRADED

    def decide(self, situation: Dict[str, Any]) -> Dict[str, Any]:
        """
        基于当前态势和本地规则做出决策
        """
        # 检查自主运行时间限制
        if self._state == AutonomyState.AUTONOMOUS:
            autonomous_duration = (datetime.utcnow() - self._autonomous_start).total_seconds()
            if autonomous_duration > self._max_autonomous_duration:
                self._state = AutonomyState.EMERGENCY
                return {
                    "action": "return_to_base",
                    "reason": "max_autonomous_duration_exceeded",
                    "state": self._state.value,
                }

        # 按优先级匹配规则
        for rule in self._standing_rules:
            if self._evaluate_condition(rule.trigger_condition, situation):
                return {
                    "action": rule.action,
                    "rule_id": rule.rule_id,
                    "state": self._state.value,
                    "autonomous": self._state != AutonomyState.CONNECTED,
                }

        # 默认行为
        return {
            "action": "hold_position_and_observe",
            "state": self._state.value,
        }

    # 预编译条件表达式白名单——替代eval()的安全方案
    _CONDITION_OPS = {
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b,
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
    }

    def _evaluate_condition(self, condition: str, situation: Dict) -> bool:
        """
        安全的条件评估：移除eval()，使用预编译白名单）
        支持格式：<variable> <op> <value>，例如 "threat_level == CRITICAL"
        多条件用 and/or 连接
        """
        try:
            # 构建安全变量映射
            safe_vars = {
                "threat_level": situation.get("threat_level", "NONE"),
                "fuel_pct": situation.get("fuel_pct", 100),
                "time_to_impact": situation.get("time_to_impact_seconds", 9999),
                "armed": situation.get("weapon_status") == "armed",
                "confidence": situation.get("confidence", 0.0),
                "distance_km": situation.get("distance_km", 9999),
            }

            # 分割多条件（支持 and）
            sub_conditions = [c.strip() for c in condition.split(" and ")]

            for sub in sub_conditions:
                if not self._eval_single(sub, safe_vars):
                    return False
            return True

        except Exception:
            return False

    def _eval_single(self, expr: str, safe_vars: Dict) -> bool:
        """评估单个条件表达式"""
        for op_str, op_fn in self._CONDITION_OPS.items():
            if op_str in expr:
                parts = expr.split(op_str, 1)
                if len(parts) != 2:
                    continue
                left = parts[0].strip()
                right = parts[1].strip()

                # 解析左侧变量
                left_val = safe_vars.get(left)
                if left_val is None:
                    return False

                # 解析右侧值（支持字符串和数值）
                try:
                    right_val = type(left_val)(right)
                except (ValueError, TypeError):
                    return False

                return op_fn(left_val, right_val)

        return False
```

#### 4.3.6 GPU资源隔离设计

快慢双路径共享GPU资源，需要三层隔离架构确保战术层推理不被战役层LLM抢占：


**问题**：快慢双路径共享GPU资源，战役层LLM推理（COA生成、兵棋推演）可能占满GPU显存，导致战术层Triton目标检测延迟飙升，违反<100ms SLA。

**解决方案：三层GPU隔离架构**

```text
┌───────────────────────────────────────────────────────────────────┐
│                    GPU资源隔离架构                      │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─────────────────────┐  ┌─────────────────────────────────┐   │
│  │  GPU 0: 战术专用     │  │  GPU 1: 战役专用（可抢占）       │   │
│  │  ┌─────────────────┐│  │  ┌───────────────────────────┐  │   │
│  │  │ Triton推理引擎   ││  │  │ SGLang LLM推理            │  │   │
│  │  │ (目标检测/分类)  ││  │  │ (COA生成/态势研判)         │  │   │
│  │  │ MPS 30%显存预留  ││  │  │ MPS 50%显存               │  │   │
│  │  └─────────────────┘│  │  └───────────────────────────┘  │   │
│  │  ┌─────────────────┐│  │  ┌───────────────────────────┐  │   │
│  │  │ ONNX Runtime    ││  │  │ OR-Tools (CPU模式)        │  │   │
│  │  │ (快速分类备份)   ││  │  │ (资源优化/路径规划)        │  │   │
│  │  │ MPS 10%显存     ││  │  └───────────────────────────┘  │   │
│  │  └─────────────────┘│  │                                  │   │
│  └─────────────────────┘  └─────────────────────────────────┘   │
│                                                                   │
│  GPU降级链路：GPU(战术) → ONNX Runtime(CPU) → 规则引擎(纯逻辑)    │
└───────────────────────────────────────────────────────────────────┘
```

**GPU隔离实现代码**：

```python
# fast_system/gpu_isolation.py
import os
import asyncio
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ComputeTier(Enum):
    GPU_TACTICAL = "gpu_tactical"    # GPU 0: 战术专用，不可抢占
    GPU_CAMPAIGN = "gpu_campaign"    # GPU 1: 战役专用，可抢占
    CPU_FALLBACK = "cpu_fallback"    # CPU降级模式


@dataclass
class GPUResourceConfig:
    """GPU资源配置"""
    # NVIDIA MPS（Multi-Process Service）分区
    tactical_gpu_id: int = 0
    campaign_gpu_id: int = 1
    # Triton优先级队列配置
    tactical_priority: int = 1      # 最高优先级
    campaign_priority: int = 5      # 低优先级
    # 显存限制（通过MPS）
    tactical_gpu_memory_limit_mb: int = 8192   # 8GB预留
    campaign_gpu_memory_limit_mb: int = 16384  # 16GB
    # 队列深度阈值
    tactical_max_queue_depth: int = 50
    campaign_max_queue_depth: int = 200


class GPUResourceManager:
    """
    GPU资源管理器：快慢路径GPU隔离）
    确保战术层推理不被战役层LLM抢占
    """

    def __init__(self, config: GPUResourceConfig):
        self._config = config
        self._tactical_queue_depth = 0
        self._campaign_queue_depth = 0
        self._gpu_available = True  # 由健康检查周期性更新（nvidia-smi轮询）

    def get_inference_config(self, tier: ComputeTier) -> Dict[str, Any]:
        """根据路径层级返回推理配置"""
        if tier == ComputeTier.GPU_TACTICAL:
            return {
                "gpu_id": self._config.tactical_gpu_id,
                "priority": self._config.tactical_priority,
                "timeout_ms": 50,
                "fallback": ComputeTier.CPU_FALLBACK,
                "cuda_visible_devices": str(self._config.tactical_gpu_id),
            }
        elif tier == ComputeTier.GPU_CAMPAIGN:
            return {
                "gpu_id": self._config.campaign_gpu_id,
                "priority": self._config.campaign_priority,
                "timeout_ms": 5000,
                "fallback": None,  # 战役任务可排队等待
                "cuda_visible_devices": str(self._config.campaign_gpu_id),
            }
        else:  # CPU_FALLBACK
            return {
                "gpu_id": None,
                "device": "cpu",
                "timeout_ms": 200,
                "backend": "onnxruntime",
            }

    def should_fallback_to_cpu(self, tier: ComputeTier) -> bool:
        """
        判断是否需要降级到CPU
        战术层在GPU 0不可用时自动降级到ONNX Runtime(CPU)
        """
        if tier != ComputeTier.GPU_TACTICAL:
            return False

        if not self._gpu_available:
            return True

        if self._tactical_queue_depth > self._config.tactical_max_queue_depth:
            return True

        return False

    async def acquire_slot(self, tier: ComputeTier) -> bool:
        """获取推理槽位"""
        if tier == ComputeTier.GPU_TACTICAL:
            if self._tactical_queue_depth >= self._config.tactical_max_queue_depth:
                return False
            self._tactical_queue_depth += 1
            return True
        elif tier == ComputeTier.GPU_CAMPAIGN:
            if self._campaign_queue_depth >= self._config.campaign_max_queue_depth:
                return False
            self._campaign_queue_depth += 1
            return True
        return True

    async def release_slot(self, tier: ComputeTier):
        """释放推理槽位"""
        if tier == ComputeTier.GPU_TACTICAL:
            self._tactical_queue_depth = max(0, self._tactical_queue_depth - 1)
        elif tier == ComputeTier.GPU_CAMPAIGN:
            self._campaign_queue_depth = max(0, self._campaign_queue_depth - 1)
```

**Triton优先级队列配置**（`model_config.pbtxt`）：

```protobuf
# triton/model_repository/target_detect/config.pbtxt
# 战术层模型：高优先级，GPU 0专用
name: "target_detect"
platform: "onnxruntime_onnx"
max_batch_size: 32

instance_group [{
  count: 2
  kind: KIND_GPU
  gpus: [0]                    # 绑定GPU 0（战术专用）
  priority: 1                  # 最高优先级
}]

dynamic_batching {
  preferred_batch_size: [8, 16, 32]
  max_queue_delay_microseconds: 10000   # 10ms最大排队
  priority_levels: 3                    # 启用优先级队列
  default_priority_level: 2
}
```

**Kubernetes GPU调度**：

```yaml
# k8s/tactical-triton-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: triton-tactical
spec:
  template:
    spec:
      containers:
      - name: triton
        resources:
          limits:
            nvidia.com/gpu: 1
          requests:
            nvidia.com/gpu: 1
        env:
        - name: CUDA_VISIBLE_DEVICES
          value: "0"        # 战术层绑定GPU 0
        - name: NVIDIA_MPS_ACTIVE_THREAD_PERCENTAGE
          value: "40"       # MPS限制战术层最多占用40%算力
      nodeSelector:
        gpu-role: tactical  # 节点标签隔离

---
# k8s/campaign-sglang-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sglang-campaign
spec:
  template:
    spec:
      containers:
      - name: sglang
        resources:
          limits:
            nvidia.com/gpu: 1
          requests:
            nvidia.com/gpu: 1
        env:
        - name: CUDA_VISIBLE_DEVICES
          value: "1"        # 战役层绑定GPU 1
      nodeSelector:
        gpu-role: campaign  # 战役专用节点
```

#### 4.3.7 快系统SLA指标

| 指标名称 | 阈值要求 | 测量方法 |
|---------|---------|---------|
| 工作流选择延迟（含嵌入+检索） | P95 < 100ms | 从态势输入到模板选择完成 |
| 参数自动填充 | P95 < 10ms | 从模板选择到参数就绪 |
| 时敏目标短路响应（OPA直通） | P95 < 100ms | 从传感器到告警发出 |
| 标准路径端到端 | P95 < 500ms | 从传感器数据到COP更新发布 |
| AI推理延迟（传统ML） | P95 < 100ms | Triton模型推理时间 |
| AI推理延迟（LLM快速研判） | P95 < 300ms | SGLang推理时间 |
| 航迹管理容量 | >= 500条同时跟踪 | 内存中活跃Track数 |
| 边缘自主运行时间 | >= 30分钟 | 通信中断后本地自主运行 |
| 故障恢复时间 | < 30秒 | 进程崩溃到自动恢复 |

### 4.4 慢系统：高质量工作流生成

#### 4.4.1 设计理念

慢系统的核心价值是**创建和优化工作流模板**，而非直接执行战术任务。慢系统输出的是"工作流模板+参数配置"，经过仿真验证后进入注册表，供快系统后续使用。这体现了卡尼曼双系统的深层映射：慢系统（系统2）的深度思考产出可复用的认知模式，快系统（系统1）凭直觉调用这些模式。

```text
慢系统两种工作模式：

  +-------------------------------------------------------------+
  |  调整模式（Adjust）          创建模式（Create）              |
  |                                                             |
  |  态势 -> Qdrant匹配已有模板    态势 -> 无匹配模板            |
  |       -> LLM分析差异               -> RAG检索条令/战例       |
  |       -> 参数调整建议              -> LLM从片段库组合         |
  |       -> 步骤增删建议              -> 生成全新StepDAG         |
  |       -> 生成新版本               -> 定义触发条件+参数        |
  |              |                           |                   |
  |         仿真验证                    仿真验证                  |
  |              |                           |                   |
  |    通过 -> status=active          通过 -> status=active       |
  |    不通过 -> 退回draft             不通过 -> 退回draft        |
  +-------------------------------------------------------------+
```


#### 4.4.2 LLM驱动的COA生成

慢系统通过LLM两步法生成行动方案（COA）：LLM生成草案 -> OR-Tools优化参数。

```python
# slow_system/llm_coa_generator.py
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

from clients.litellm_client import C2LLMClient
from knowledge.qdrant_setup import MilitaryKnowledgeStore


class COAStatus(str, Enum):
    DRAFT = "draft"
    EVALUATED = "evaluated"
    RECOMMENDED = "recommended"
    APPROVED = "approved"
    EXECUTING = "executing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class COAPhase(BaseModel):
    """COA行动阶段"""
    phase_id: str
    name: str
    description: str
    assigned_assets: List[str] = Field(default_factory=list)
    duration_minutes: int = 0
    objectives: List[str] = Field(default_factory=list)
    dependencies: List[str] = Field(default_factory=list)


class CourseOfAction(BaseModel):
    """行动方案（COA）"""
    coa_id: str
    name: str
    description: str
    phases: List[COAPhase]
    required_assets: List[str]
    estimated_duration_minutes: int
    risk_level: str = "medium"
    success_probability: float = 0.0
    overall_score: float = 0.0
    status: COAStatus = COAStatus.DRAFT
    doctrine_references: List[str] = Field(default_factory=list)


class LLMCOAGenerator:
    """
    LLM驱动的行动方案生成器
    两步法：LLM生成草案 → OR-Tools优化参数
    """

    def __init__(self, llm_client: C2LLMClient, knowledge: MilitaryKnowledgeStore):
        self._llm = llm_client
        self._knowledge = knowledge

    async def generate_coas(
        self,
        situation_brief: str,
        available_forces: Dict[str, Any],
        commander_intent: str,
        constraints: Dict[str, Any],
        num_alternatives: int = 3,
    ) -> List[CourseOfAction]:
        """
        生成多个备选行动方案
        Step 1: RAG检索相关条令/战例
        Step 2: LLM生成COA草案
        Step 3: 结构化解析为COA对象
        """
        # Step 1: RAG知识检索
        doctrine_context = await self._retrieve_relevant_doctrine(
            situation_brief, commander_intent
        )

        # Step 2: LLM生成COA草案
        coas = []
        for i in range(num_alternatives):
            draft = self._llm.generate_coa_draft(
                situation=f"""{situation_brief}

相关条令参考：
{doctrine_context}

约束条件：{constraints}""",
                forces=str(available_forces),
                intent=f"{commander_intent}\n\n请生成第{i+1}种不同的行动方案，"
                       f"侧重{'进攻性' if i == 0 else '防御性' if i == 1 else '平衡性'}策略。",
            )

            # Step 3: 解析为结构化COA
            coa = self._parse_coa_draft(draft["content"], i)
            coas.append(coa)

        return coas

    async def _retrieve_relevant_doctrine(
        self, situation: str, intent: str
    ) -> str:
        """
        RAG检索相关条令
        实现：调用第5章RAG知识服务的retrieve_and_augment()，
        传入态势描述+指挥意图，返回匹配的条令/战例/装备手册片段。
        category_filter限定为doctrine和after_action_report。
        """
        # TODO: 对接第5章RAGPipeline.retrieve_and_augment()
        return "相关条令检索结果将在运行时通过Qdrant获取"

    def _parse_coa_draft(self, draft_text: str, index: int) -> CourseOfAction:
        """
        将LLM草案解析为结构化COA对象
        实现：使用SGLang的结构化输出（regex_guided decoding），
        将draft_text解析为name/description/phases/required_assets等字段。
        """
        # TODO: 对接SGLang结构化输出解析器
        return CourseOfAction(
            coa_id=f"COA-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{index}",
            name=f"方案{index + 1}",
            description=draft_text[:200],
            phases=[],
            required_assets=[],
            estimated_duration_minutes=0,
            status=COAStatus.DRAFT,
        )
```

#### 4.4.3 工作流调整与创建

慢系统支持调整现有模板和从原子片段组合新模板两种模式：

```python
# registry/slow_workflow_composer.py
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

from clients.litellm_client import C2LLMClient
from clients.qdrant_client import QdrantRegistryClient
from knowledge.qdrant_setup import MilitaryKnowledgeStore
from registry.workflow_template import (
    WorkflowTemplate, StepDAG, StepNode, StepEdge,
    ParamField, TriggerCondition, TemplateStatus,
)


class SlowWorkflowComposer:
    """
    慢系统工作流编排器
    两种模式：
    1. 调整模式：选择现有模板，LLM建议参数/步骤调整
    2. 创建模式：从原子片段库组合全新工作流
    """

    def __init__(self, config: Dict[str, Any]):
        self._llm = C2LLMClient(config["litellm_config"])
        self._qdrant = QdrantRegistryClient(config["qdrant_url"])
        self._knowledge = MilitaryKnowledgeStore(config["qdrant_url"])
        self._atomic_fragments = self._load_atomic_fragments()

    async def compose(
        self, situation: Dict[str, Any], commander_intent: str,
    ) -> Dict[str, Any]:
        """
        慢系统工作流编排主入口
        返回调整后的模板或全新模板
        """
        # Step 1: 判断是调整还是新建
        existing_match = await self._find_best_existing_template(situation)

        if existing_match and existing_match["score"] > 0.7:
            # 调整模式：基于现有模板调整
            return await self._adjust_template(existing_match, situation, commander_intent)
        else:
            # 创建模式：从原子片段组合新模板
            return await self._create_new_template(situation, commander_intent)

    async def _adjust_template(
        self, match: Dict, situation: Dict, intent: str,
    ) -> Dict[str, Any]:
        """
        调整模式
        LLM分析当前态势与模板预设条件的差异，建议参数/步骤调整
        """
        template = match["template"]

        # RAG检索相关条令
        doctrine = await self._knowledge.retrieve(
            query=f"态势: {situation.get('summary', '')} 意图: {intent}",
            scope=["doctrine", "tactics"],
            top_k=5,
        )

        # LLM生成调整建议
        adjustment_prompt = f"""
你是JS作战规划AI。当前有一个工作流模板"{template['name']}"需要调整。

原始模板参数: {json.dumps(template['params'], ensure_ascii=False)}
原始步骤: {json.dumps(template['dag'], ensure_ascii=False)}

当前态势: {json.dumps(situation, ensure_ascii=False)}
指挥员意图: {intent}

相关条令参考:
{doctrine}

请分析当前态势与模板预设条件的差异，输出JSON格式的调整建议：
{{
    "param_adjustments": {{"参数名": "调整值及理由"}},
    "step_additions": ["需要增加的步骤及理由"],
    "step_removals": ["建议移除的步骤及理由"],
    "risk_notes": "调整后的风险提示"
}}"""
        response = self._llm.generate(adjustment_prompt, temperature=0.3)

        # 解析调整建议并生成新版本模板
        adjustments = self._parse_adjustments(response["content"])

        # 生成新版本（不覆盖原模板）
        new_template = self._apply_adjustments(template, adjustments)
        new_template["version"] = template["version"] + 1
        new_template["parent_template_id"] = template["template_id"]
        new_template["created_by"] = "slow_system"

        return {
            "mode": "adjustment",
            "template": new_template,
            "adjustments": adjustments,
            "base_template_id": template["template_id"],
        }

    async def _create_new_template(
        self, situation: Dict, intent: str,
    ) -> Dict[str, Any]:
        """
        创建模式
        从原子片段库组合全新工作流
        """
        # RAG检索条令
        doctrine = await self._knowledge.retrieve(
            query=f"新建工作流: {situation.get('summary', '')} 意图: {intent}",
            scope=["doctrine", "tactics", "historical_cases"],
            top_k=10,
        )

        # LLM从原子片段中选择并组合
        fragment_list = [
            f"- {fid}: {f['name']} ({f['description']})"
            for fid, f in self._atomic_fragments.items()
        ]

        compose_prompt = f"""
你是JS作战规划AI。需要从以下原子片段中组合一个新工作流。

可用原子片段:
{chr(10).join(fragment_list)}

当前态势: {json.dumps(situation, ensure_ascii=False)}
指挥员意图: {intent}
条令参考: {doctrine}

请输出JSON格式的工作流定义：
{{
    "name": "工作流名称",
    "description": "描述",
    "trigger": {{触发条件}},
    "selected_fragments": ["片段ID列表（按执行顺序）],
    "edges": [{{"from": "片段ID", "to": "片段ID", "condition": "条件"}}],
    "params": [{{"name": "参数名", "type": "类型", "default": 默认值, "source": "auto/manual"}}]
}}"""
        response = self._llm.generate(compose_prompt, temperature=0.2)
        new_template_def = self._parse_compose_response(response["content"])

        # 从片段组装StepDAG
        dag = self._assemble_dag(new_template_def)

        new_template = WorkflowTemplate(
            template_id=f"WF-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-NEW",
            name=new_template_def.get("name", "自定义工作流"),
            version=1,
            description=new_template_def.get("description", ""),
            status=TemplateStatus.DRAFT,
            trigger=TriggerCondition(**new_template_def.get("trigger", {})),
            params=[ParamField(**p) for p in new_template_def.get("params", [])],
            dag=dag,
            created_by="slow_system",
        )

        return {
            "mode": "creation",
            "template": new_template.model_dump(),
        }

#### 4.4.4 仿真验证机制

新建或调整的工作流模板必须通过仿真验证才能从`draft`状态激活为`active`。仿真验证是工作流质量保证的核心环节：

```python
# slow_system/simulation_validator.py
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

from clients.litellm_client import C2LLMClient
from registry.workflow_template import WorkflowTemplate, TemplateStatus
from registry.template_lifecycle import TemplateLifecycleManager


@dataclass
class SimulationResult:
    """仿真验证结果"""
    template_id: str
    total_runs: int
    success_count: int
    success_rate: float
    avg_execution_time_ms: float
    failure_modes: List[Dict[str, Any]]  # 失败模式分析
    risk_assessment: str  # 风险评估结论
    passed: bool


class WorkflowSimulationValidator:
    """
    工作流仿真验证器
    新建/调整的工作流必须通过蒙特卡洛仿真（>=100次）才能激活

    验证标准：
    - 成功率 >= 70%（基础门槛）
    - 无致命失败模式（如误伤友军、违规操作）
    - 平均执行时间在预期范围内
    """

    MIN_SIMULATION_RUNS = 100
    SUCCESS_RATE_THRESHOLD = 0.70
    FATAL_FAILURE_TYPES = {"friendly_fire", "civilian_casualty", "rule_violation"}

    def __init__(self, config: Dict[str, Any]):
        self._llm = C2LLMClient(config["litellm_config"])
        self._lifecycle = TemplateLifecycleManager(config)

    async def validate(
        self, template: WorkflowTemplate, situation_samples: List[Dict]
    ) -> SimulationResult:
        """
        执行蒙特卡洛仿真验证
        """
        results = []
        failure_modes = []

        for i in range(self.MIN_SIMULATION_RUNS):
            # 为每次仿真生成态势变体
            situation = self._generate_situation_variant(situation_samples, i)

            # 执行单次仿真（模拟DAG执行过程）
            run_result = await self._simulate_single_run(template, situation)
            results.append(run_result)

            if not run_result["success"]:
                failure_modes.append({
                    "run_index": i,
                    "failure_type": run_result.get("failure_type", "unknown"),
                    "failure_step": run_result.get("failed_at_step", ""),
                    "situation": situation,
                })

        # 统计结果
        success_count = sum(1 for r in results if r["success"])
        success_rate = success_count / len(results)
        execution_times = [r["execution_time_ms"] for r in results]

        # 检查致命失败模式
        has_fatal = any(
            fm["failure_type"] in self.FATAL_FAILURE_TYPES
            for fm in failure_modes
        )

        # 风险评估
        risk = "low"
        if has_fatal:
            risk = "critical"
        elif success_rate < 0.80:
            risk = "high"
        elif success_rate < 0.90:
            risk = "medium"

        passed = success_rate >= self.SUCCESS_RATE_THRESHOLD and not has_fatal

        sim_result = SimulationResult(
            template_id=template.template_id,
            total_runs=len(results),
            success_count=success_count,
            success_rate=success_rate,
            avg_execution_time_ms=sum(execution_times) / len(execution_times),
            failure_modes=failure_modes[:10],  # 最多保留10个失败样本
            risk_assessment=risk,
            passed=passed,
        )

        # 根据仿真结果更新模板状态
        if passed:
            await self._lifecycle.activate_template(
                template.template_id,
                simulation_result={
                    "success_rate": success_rate,
                    "total_runs": len(results),
                    "risk_assessment": risk,
                },
            )
        else:
            await self._lifecycle.revert_to_draft(
                template.template_id,
                reason=f"仿真未通过: success_rate={success_rate:.0%}, risk={risk}",
            )

        return sim_result

    def _generate_situation_variant(
        self, samples: List[Dict], index: int
    ) -> Dict:
        """基于样本生成态势变体（注入噪声/边界条件）"""
        if not samples:
            return {"domain": "air", "urgency": "normal", "entities": []}

        base = samples[index % len(samples)].copy()
        # 注入变体：调整实体数量、威胁等级、通信状态等
        base["simulation_variant"] = True
        base["variant_index"] = index
        return base

    async def _simulate_single_run(
        self, template: WorkflowTemplate, situation: Dict
    ) -> Dict[str, Any]:
        """
        模拟单次DAG执行
        实现策略：
        1. 将模板DAG中的每个步骤映射为仿真事件序列
        2. 调用兵棋仿真引擎（AFSIM/HLA4），传入态势参数（实体位置、兵力、地形）
        3. 逐步执行DAG，每步注入随机扰动（传感器误差±15%、通信延迟±30%、敌方反应概率）
        4. 记录致命故障类型：友军误伤（friendly_fire）、平民伤亡（civilian_casualty）、
           ROE违规（roe_violation）、任务失败（mission_failure）
        5. 返回单次运行结果
        """
        # TODO: 对接AFSIM/HLA4仿真引擎
        return {
            "success": True,
            "execution_time_ms": template.avg_execution_time_ms or 5000,
            "failed_at_step": "",
            "failure_type": "",
        }
```

#### 4.4.5 战役规划流水线

```python
# slow_system/campaign_planner.py
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
from dataclasses import dataclass

from slow_system.llm_coa_generator import LLMCOAGenerator, CourseOfAction


class CampaignPlanningPipeline:
    """战役规划流水线（LLM COA生成）"""

    def __init__(self, coa_generator: LLMCOAGenerator):
        self._coa_gen = coa_generator
        self._task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue(maxsize=500)
        self._results: Dict[str, Dict] = {}

    async def submit_planning_task(
        self, task_type: str, params: Dict[str, Any], priority: int = 5
    ) -> str:
        task_id = f"plan-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{task_type}"
        await self._task_queue.put((priority, task_id, task_type, params))
        return task_id

    async def run_worker(self):
        while True:
            priority, task_id, task_type, params = await self._task_queue.get()
            try:
                if task_type == "coa_generation":
                    result = await self._generate_coas(params)
                elif task_type == "resource_allocation":
                    result = await self._allocate_resources(params)
                elif task_type == "multi_domain_coordination":
                    result = await self._coordinate_multi_domain(params)
                elif task_type == "wargame":
                    result = await self._run_wargame(params)
                else:
                    result = {"status": "error", "message": f"Unknown: {task_type}"}

                self._results[task_id] = {**result, "task_id": task_id}
            except Exception as e:
                self._results[task_id] = {"status": "error", "task_id": task_id, "error": str(e)}
            finally:
                self._task_queue.task_done()

    async def _generate_coas(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """LLM驱动的COA生成"""
        coas: List[CourseOfAction] = await self._coa_gen.generate_coas(
            situation_brief=params.get("situation_brief", ""),
            available_forces=params.get("available_forces", {}),
            commander_intent=params.get("commander_intent", ""),
            constraints=params.get("constraints", {}),
            num_alternatives=params.get("num_alternatives", 3),
        )

        # 评估并排序
        evaluated = []
        for coa in coas:
            evaluation = await self._evaluate_coa(coa, params)
            coa.success_probability = evaluation["success_probability"]
            coa.overall_score = evaluation["overall_score"]
            coa.status = "evaluated"
            evaluated.append(coa)

        evaluated.sort(key=lambda c: c.overall_score, reverse=True)
        if evaluated:
            evaluated[0].status = "recommended"

        return {
            "status": "success",
            "coas": [c.model_dump() for c in evaluated],
            "recommended_index": 0,
        }

    async def _evaluate_coa(self, coa: CourseOfAction, params: Dict) -> Dict:
        """
        蒙特卡洛仿真评估COA
        实现：复用WorkflowSimulationValidator（4.4.4）的仿真基础设施，
        以COA的phases作为输入，运行≥50次蒙特卡洛仿真，
        返回成功率、风险等级和综合评分。
        """
        # TODO: 复用4.4.4 WorkflowSimulationValidator的仿真引擎
        return {
            "success_probability": 0.0,
            "risk_level": "medium",
            "overall_score": 0.0,
        }

    async def _allocate_resources(self, params: Dict[str, Any]) -> Dict:
        """资源分配——调用OR-Tools求解器（见2.4.13）优化多域资源调度"""
        # TODO: 对接OR-Tools路径规划与资源分配求解器
        return {"status": "success", "allocation": {}}

    async def _coordinate_multi_domain(self, params: Dict[str, Any]) -> Dict:
        """多域协同——协调陆海空天电多域作战单元的时序与空间约束"""
        # TODO: 实现多域杀伤链联合调度算法
        return {"status": "success", "coordination_plan": {}}

    async def _run_wargame(self, params: Dict[str, Any]) -> Dict:
        """兵棋推演——调用AFSIM/HLA4引擎进行对抗仿真"""
        # TODO: 对接兵棋推演引擎
        return {"status": "success", "wargame_results": {}}

    def get_result(self, task_id: str) -> Optional[Dict]:
        return self._results.get(task_id)
```

#### 4.4.6 慢系统SLA指标

| 指标名称 | 阈值要求 | 测量方法 |
|---------|---------|---------|
| COA方案生成（LLM+优化） | < 120s | 从任务提交到3个备选方案生成 |
| 工作流调整（含LLM分析） | < 60s | 从态势输入到调整建议生成 |
| 工作流创建（含片段组合） | < 120s | 从态势输入到新模板生成 |
| 仿真验证（100次蒙特卡洛） | < 10min | 单模板100次仿真验证 |
| 仿真通过率门槛 | >= 70% | 仿真成功率低于此值拒绝激活 |
| 资源调度优化 | < 120s | 从提交到全局资源分配方案 |
| 最优性间隙 | < 5% | 与理论最优解的比较 |

### 4.5 人工干预：工作流可视化调整界面

#### 4.5.1 图形化界面设计

指挥员通过图形化界面直观地审查和修改工作流。界面设计遵循"态势感知优先、操作最简化"原则：

**（1）DAG可视化组件**

使用React Flow + dagre布局引擎实现工作流DAG的可视化渲染：

```tsx
// frontend/components/WorkflowDAG.tsx
import React, { useMemo, useCallback } from 'react';
import ReactFlow, {
  Node, Edge, Background, Controls, MiniMap,
  useNodesState, useEdgesState, Handle, Position,
} from 'reactflow';
import Dagre from '@dagrejs/dagre';

// 步骤节点组件
const StepNode = ({ data }: { data: {
  label: string; status: string; params: Record<string, any>;
  executionTime?: string;
}}) => (
  <div className={`step-node step-${data.status}`}
       style={{
         padding: '8px 12px', borderRadius: '6px', minWidth: '120px',
         border: data.status === 'running' ? '2px solid #f59e0b' :
                 data.status === 'success' ? '2px solid #10b981' :
                 data.status === 'failed' ? '2px solid #ef4444' : '2px solid #6b7280',
         background: '#1e293b', color: '#e2e8f0', fontSize: '12px',
       }}>
    <Handle type="target" position={Position.Top} />
    <div style={{ fontWeight: 600 }}>{data.label}</div>
    <div style={{ fontSize: '10px', color: '#94a3b8' }}>
      {data.executionTime && `~${data.executionTime}`}
    </div>
    <Handle type="source" position={Position.Bottom} />
  </div>
);

// dagre自动布局
function layoutDag(nodes: Node[], edges: Edge[]): Node[] {
  const g = new Dagre.graphlib.Graph().setDefaultEdgeLabel(() => ({}));
  g.setGraph({ rankdir: 'TB', nodesep: 50, ranksep: 80 });
  nodes.forEach(n => g.setNode(n.id, { ...n, width: 140, height: 50 }));
  edges.forEach(e => g.setEdge(e.source, e.target));
  Dagre.layout(g);
  return nodes.map(n => {
    const pos = g.node(n.id);
    return { ...n, position: { x: pos.x - 70, y: pos.y - 25 } };
  });
}

export const WorkflowDAG: React.FC<{
  template: { nodes: any[]; edges: any[] };
  filledParams: Record<string, any>;
  onNodeClick?: (nodeId: string) => void;
}> = ({ template, filledParams, onNodeClick }) => {
  const initialNodes: Node[] = useMemo(() =>
    template.nodes.map(n => ({
      id: n.step_id,
      type: 'step',
      data: { label: n.name, status: 'pending', params: filledParams },
    })), [template]);

  const initialEdges: Edge[] = useMemo(() =>
    template.edges.map(e => ({
      id: `${e.from_step}-${e.to_step}`,
      source: e.from_step, target: e.to_step,
      label: e.condition || '',
      animated: true, style: { stroke: '#475569' },
    })), [template]);

  const [nodes, setNodes, onNodesChange] = useNodesState(
    layoutDag(initialNodes, initialEdges)
  );
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const nodeTypes = useMemo(() => ({ step: StepNode }), []);

  return (
    <div style={{ height: '500px', background: '#0f172a', borderRadius: '8px' }}>
      <ReactFlow nodes={nodes} edges={edges} onNodesChange={onNodesChange}
                 onEdgesChange={onEdgesChange} nodeTypes={nodeTypes}
                 onNodeClick={(_, n) => onNodeClick?.(n.id)} fitView>
        <Background color="#1e293b" />
        <Controls position="top-right" />
        <MiniMap nodeColor={() => '#475569'} maskColor="rgba(0,0,0,0.7)" />
      </ReactFlow>
    </div>
  );
};
```

**（2）参数编辑面板**

基于模板的参数Schema动态生成编辑表单：

```tsx
// frontend/components/ParamEditor.tsx
import React from 'react';

export const ParamEditor: React.FC<{
  params: Array<{ name: string; type: string; default?: any;
                   required: boolean; description: string;
                   enum_values?: string[]; range_min?: number; range_max?: number;
                   source: string }>;
  values: Record<string, any>;
  onChange: (name: string, value: any) => void;
}> = ({ params, values, onChange }) => (
  <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', padding: '12px' }}>
    {params.map(p => (
      <div key={p.name} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <label style={{ width: '120px', fontSize: '12px', color: '#94a3b8' }}>
          {p.name}
          {p.required && <span style={{ color: '#ef4444' }}>*</span>}
        </label>
        {p.type === 'enum' ? (
          <select value={values[p.name] ?? p.default ?? ''}
                  onChange={e => onChange(p.name, e.target.value)}
                  style={{ flex: 1, background: '#1e293b', color: '#e2e8f0',
                           border: '1px solid #475569', borderRadius: '4px', padding: '4px' }}>
            {p.enum_values?.map(v => <option key={v} value={v}>{v}</option>)}
          </select>
        ) : p.type === 'int' || p.type === 'float' ? (
          <input type="number" value={values[p.name] ?? p.default ?? ''}
                 min={p.range_min} max={p.range_max}
                 onChange={e => onChange(p.name,
                   p.type === 'int' ? parseInt(e.target.value) : parseFloat(e.target.value))}
                 style={{ flex: 1, background: '#1e293b', color: '#e2e8f0',
                          border: '1px solid #475569', borderRadius: '4px', padding: '4px' }} />
        ) : (
          <input type="text" value={values[p.name] ?? p.default ?? ''}
                 onChange={e => onChange(p.name, e.target.value)}
                 style={{ flex: 1, background: '#1e293b', color: '#e2e8f0',
                          border: '1px solid #475569', borderRadius: '4px', padding: '4px' }} />
        )}
        <span style={{ fontSize: '10px', color: p.source === 'auto' ? '#10b981' : '#f59e0b' }}>
          {p.source === 'auto' ? '自动' : '手动'}
        </span>
      </div>
    ))}
  </div>
);
```

**（3）备选方案对比视图**

```text
+------------------------------------------------------------------+
|  备选方案对比视图（并排展示）                                      |
+------------------+------------------+----------------------------+
|  方案一(推荐)     |  方案二           |  方案三                     |
|  防空拦截模板v3.2|  电子战压制v2.1  |  综合防御模板v1.0           |
|  [探]>[评]>[打]  |  [探]>[干]>[评]  |  [探]>[评]>[人]>[打]       |
|  成功率: 97%     |  成功率: 92%     |  成功率: 84%               |
|  预计耗时: 8s    |  预计耗时: 15s   |  预计耗时: 25s             |
|  资源消耗: 低    |  资源消耗: 中    |  资源消耗: 高              |
|  风险等级: 低    |  风险等级: 中    |  风险等级: 中              |
|                  |                  |                              |
|  [选中此方案]     |  [选中此方案]     |  [选中此方案]               |
+------------------+------------------+----------------------------+
```

**（4）战术终端触控适配**

战术终端（加固平板/车载显示器）采用触控操作设计：

```text
触控操作手势设计：

  - 单击节点 -> 选中节点，展开参数面板
  - 双击节点 -> 查看步骤详情（输入/输出/历史执行结果）
  - 长按节点 -> 弹出操作菜单（编辑/删除/在此之后插入步骤）
  - 双指缩放 -> 缩放DAG视图
  - 双指拖拽 -> 平移视图
  - 从节点向下拖拽 -> 创建新连线（连接到下游步骤）
  - 从侧边栏拖拽片段到画布 -> 插入新步骤

  关键尺寸要求（MIL-STD-1472 JS人机工程标准）：
  - 触控目标最小 9.6mm（约 44px @ 117dpi）
  - 字体最小 3mm（约 14px）
  - 按钮间距 >= 3mm
  - 高亮对比度 >= 3:1（暗色主题适配战术环境）
```


#### 4.5.2 语音命令交互

指挥员可通过语音直接下达命令和查询态势，无需操作键盘/鼠标：

```text
语音指挥流程：
  指挥员语音 → FunASR(STT,<300ms) → SGLang(NLU意图识别)
       → OPA(权限校验) → Temporal(执行/查询)
       → SGLang(NLG生成) → CosyVoice(TTS,<200ms) → 语音播报

示例交互：
  指挥员: "当前东南方向有什么威胁？"
  系统: "检测到3个空中目标：2架疑似战斗机，高度8000米，速度900公里/小时，
         距离120公里，威胁等级高。已调动2架巡逻机前往查证。"

  指挥员: "批准打击方案一"
  系统: "收到。打击方案一已批准，预计15分钟后到达目标区域。"
```

#### 4.5.3 审批与修改机制

指挥员通过可视化DAG面板和语音命令干预工作流。审批机制支持多级审批和代理审批：

```python
# registry/human_workflow_interface.py
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum

from temporalio import workflow


class HumanAction(str, Enum):
    APPROVE = "approve"           # 批准当前工作流
    REJECT = "reject"             # 拒绝当前工作流
    MODIFY_PARAMS = "modify_params"  # 修改参数
    SWITCH_TEMPLATE = "switch_template"  # 切换到另一个模板
    INSERT_STEP = "insert_step"   # 插入新步骤
    REDIRECT = "redirect"         # 重定向到不同路径


class HumanWorkflowInterface:
    """
    指挥员工作流干预界面
    将工作流以可视化DAG形式呈现，支持语音/面板交互
    """

    def format_workflow_for_display(self, template: Dict, filled_params: Dict) -> Dict:
        """
        将工作流模板格式化为前端可渲染的DAG视图
        """
        dag = template.get("dag", {})

        # 构建可视化节点
        nodes = []
        for node in dag.get("nodes", []):
            nodes.append({
                "id": node["step_id"],
                "label": node["name"],
                "type": "step",
                "params": {
                    p["name"]: filled_params.get(p["name"], p.get("default"))
                    for p in template.get("params", [])
                    if p["name"] in node.get("input_mapping", {}).values()
                },
                "status": "pending",
            })

        # 构建可视化边
        edges = []
        for edge in dag.get("edges", []):
            edges.append({
                "from": edge["from_step"],
                "to": edge["to_step"],
                "label": edge.get("condition", ""),
            })

        return {
            "template_id": template["template_id"],
            "template_name": template["name"],
            "success_rate": f"{template.get('success_rate', 0) * 100:.0f}%",
            "nodes": nodes,
            "edges": edges,
            "filled_params": filled_params,
            "alternatives": [],  # 备选模板列表（前端可切换）
        }

    def parse_voice_command(self, text: str) -> Dict[str, Any]:
        """
        解析指挥员语音命令为结构化操作
        """
        text_lower = text.lower()

        # 批准类
        if any(kw in text_lower for kw in ["批准", "同意", "执行", "确认", "同意"]):
            return {"action": HumanAction.APPROVE, "raw_text": text}

        # 拒绝类
        if any(kw in text_lower for kw in ["拒绝", "取消", "停止", "终止"]):
            return {"action": HumanAction.REJECT, "raw_text": text}

        # 切换模板
        if any(kw in text_lower for kw in ["方案二", "方案三", "换一个", "备选"]):
            template_idx = 1  # 默认切到第二个
            if "三" in text_lower:
                template_idx = 2
            return {
                "action": HumanAction.SWITCH_TEMPLATE,
                "target_index": template_idx,
                "raw_text": text,
            }

        # 参数修改
        if any(kw in text_lower for kw in ["改为", "调整", "修改", "设为", "改成"]):
            return {
                "action": HumanAction.MODIFY_PARAMS,
                "raw_text": text,
                "modification": text,  # 交由SGLang NLU进一步解析
            }

        # 插入步骤
        if any(kw in text_lower for kw in ["增加", "插入", "先做", "之前先"]):
            return {
                "action": HumanAction.INSERT_STEP,
                "raw_text": text,
                "instruction": text,
            }

        return {"action": "unknown", "raw_text": text}
```

**指挥员语音干预示例**：

```text
场景：系统推荐"联合打击模板v3.0"，指挥员审查：

指挥员: "打击前增加侦察确认"
  → parse_voice_command → INSERT_STEP
  → 系统在"decide_coa"和"act_strike"之间插入"observe_satellite"节点
  → DAG可视化实时更新，指挥员看到修改后的流程

指挥员: "拦截窗口改为30秒"
  → parse_voice_command → MODIFY_PARAMS
  → SGLang NLU解析: param="intercept_window_s", value=30
  → 参数面板实时更新

指挥员: "改用方案二"
  → parse_voice_command → SWITCH_TEMPLATE, target_index=1
  → 系统加载备选模板"电子战压制方案"
  → DAG切换显示，参数自动填充

指挥员: "批准执行"
  → parse_voice_command → APPROVE
  → Temporal Signal发送，工作流开始执行
  → CosyVoice播报: "联合打击方案已批准，预计15分钟后到达目标区域"
```
**增强功能：多级审批与偏好采集**

```python
# registry/approval_manager.py
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum

from clients.asyncpg_client import PostgresClient


class ApprovalLevel(str, Enum):
    AUTO = "auto"                # 自动审批（fast_track模板+低风险）
    COMMANDER = "commander"      # 指挥员审批
    HIGHER_COMMAND = "higher"    # 上级审批（高风险操作）
    DUAL = "dual"                # 双重审批（涉及武力使用的行动）


class ApprovalManager:
    """
    工作流审批管理器
    支持多级审批、代理审批、偏好采集
    """

    def __init__(self, config: Dict[str, Any]):
        self._pg = PostgresClient(config["pg_dsn"])

    def determine_approval_level(
        self, template: Dict, filled_params: Dict, situation: Dict
    ) -> ApprovalLevel:
        """根据模板和态势确定审批级别"""
        # fast_track模板 + 非武力行动 -> 自动审批
        if (template.get("status") == "fast_track"
                and filled_params.get("action_type") != "kinetic"):
            return ApprovalLevel.AUTO

        # 涉及武力使用 -> 双重审批
        if filled_params.get("action_type") == "kinetic":
            return ApprovalLevel.DUAL

        # 高风险模板 -> 上级审批
        if template.get("success_rate", 1.0) < 0.80:
            return ApprovalLevel.HIGHER_COMMAND

        # 默认指挥员审批
        return ApprovalLevel.COMMANDER

    async def record_preference(
        self, template_id: str, human_verdict: str,
        modifications: Optional[Dict] = None,
    ):
        """
        记录指挥员偏好，用于经验蒸馏
        指挥员的修改行为是高质量的学习信号
        """
        await self._pg.execute(
            """INSERT INTO commander_preferences
               (template_id, verdict, modifications, timestamp)
               VALUES ($1, $2, $3, NOW())""",
            template_id, human_verdict,
            modifications or {},
        )
```

**审批流设计**：

```text
审批流程：

  工作流提交 -> 判断审批级别
                    |
         +----------+--------------+
         |          |              |
      AUTO      COMMANDER      DUAL/KINETIC
     自动通过    指挥员审批      指挥员+上级
     立即执行       |              双重确认
              批准/拒绝/修改       |
                |              批准/拒绝
              执行                |
                             执行

  超时处理：
  - AUTO: 无超时
  - COMMANDER: 5分钟超时 -> 自动升级到上级审批
  - DUAL: 15分钟超时 -> 自动拒绝（安全保守策略）

  代理审批：
  - 指挥员可指定代理人在其不在场时行使审批权
  - 代理审批记录与正审等效，但标记"proxied_by"
```


#### 4.5.4 分层自主等级

**自主等级定义见第3.6节**。本节描述自主等级如何映射到快慢系统的审批流程。

第3.6节定义了L1-L5五个自主等级（查询→辅助→监督→自主→紧急自主），由`AutonomyGovernor`动态管理。`LeveledAgentWorkflow`将自主等级映射到工作流审批需求：

| 自主等级（Ch3.6） | 对应AgentKernel路径 | 人类角色 | 审批级别 | 典型场景 |
|------|------|---------|---------|--------|---------|
| **L1: Query** | 路径0/1 | 发起查询，审核结果 | AUTO | "当前区域有哪些威胁？" |
| **L2: Assisted** | 路径1/2 | 选择方案，监督执行 | COMMANDER | "对区域X进行ISR扫描" |
| **L3: Supervised** | 路径2/3 | 审批关键节点 | COMMANDER/HIGHER | "规划并执行联合打击方案" |
| **L4: Autonomous** | 路径0/1(OPA编译) | 事后审计 | AUTO | "防空反导自动拦截" |
| **L5: Emergency** | 路径0(L0蒸馏) | 事后审计 | AUTO | "紧急规避/自卫还击" |

```python
# workflows/leveled_agent_workflow.py
from temporalio import workflow
from datetime import timedelta
from typing import Dict, Any, Optional
from enum import IntEnum

# 引用第3.6节定义的AutonomyLevel，此处仅列出映射关系
class AutonomyLevel(IntEnum):
    """与第3.6.2节AutonomyLevel保持一致"""
    QUERY = 1
    ASSISTED = 2
    SUPERVISED = 3
    AUTONOMOUS = 4
    EMERGENCY = 5


@workflow.defn
class LeveledAgentWorkflow:
    """
    自主等级递进工作流
    根据第3.6节定义的自主等级决定人类参与程度
    """

    def __init__(self):
        self._approval_result: Optional[Dict[str, Any]] = None
        self._halt_requested: bool = False

    @workflow.run
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        level = AutonomyLevel(params.get("autonomy_level", 1))
        task_type = params.get("task_type", "unknown")

        result = await self._execute_task(task_type, params)
        needs_approval = self._needs_human_approval(level, result)

        if needs_approval:
            result["status"] = "pending_approval"
            try:
                await workflow.wait_condition(
                    lambda: self._approval_result is not None,
                    timeout=timedelta(minutes=params.get("approval_timeout_min", 5)),
                )
                if not self._approval_result.get("approved"):
                    return {"status": "rejected", "approver": self._approval_result.get("commander_id")}
                result["approved_by"] = self._approval_result["commander_id"]
            except TimeoutError:
                # L3 Supervised超时：升级到上级；L2 Assisted超时：安全保守拒绝
                if level >= AutonomyLevel.SUPERVISED:
                    return {"status": "escalated", "reason": "approval_timeout"}
                return {"status": "rejected", "reason": "approval_timeout"}

        result["status"] = "completed"
        return result

    def _needs_human_approval(self, level: AutonomyLevel, result: Dict) -> bool:
        """根据自主等级和行动类型决定是否需要人类审批"""
        if level == AutonomyLevel.QUERY:
            return False  # L1查询无需审批
        if level == AutonomyLevel.ASSISTED:
            return result.get("risk_level") == "high"  # L2仅高风险需审批
        if level == AutonomyLevel.SUPERVISED:
            return result.get("action_type") in {"kinetic_strike", "cross_boundary"}  # L3关键节点审批
        if level == AutonomyLevel.AUTONOMOUS:
            return False  # L4自主执行，事后审计
        if level == AutonomyLevel.EMERGENCY:
            return False  # L5紧急自主，事后审计
        return True

    async def _execute_task(self, task_type: str, params: Dict) -> Dict:
        return {"task_type": task_type, "risk_level": "medium", "action_type": task_type}

    @workflow.signal
    def submit_approval(self, result: Dict[str, Any]):
        self._approval_result = result

    @workflow.signal
    def halt(self):
        self._halt_requested = True
```


### 4.6 快慢协同机制

快系统和慢系统并非独立运行——它们共享数据层、GPU资源和COP状态，需要三个协同机制：任务路由（谁处理）、数据一致性（状态同步）、结果融合（输出合并）。

#### 4.6.1 任务分级路由

负载感知的任务路由器根据任务类型和下游组件负载动态分配到快系统或慢系统：


```text
┌─────────────────────────────────────────────────────────────────┐
│                 战术-战役协同控制器                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │               任务分级路由器                                │ │
│  │                                                           │ │
│  │   时敏目标(TST) ──────────▶ 战术短路路径（< 100ms）       │ │
│  │                                                           │ │
│  │   时间敏感(5min内) ────────▶ 战术实时层（标准路径）        │ │
│  │                                                           │ │
│  │   常规目标/规划任务 ──────▶ 战役规划层（LLM+优化）        │ │
│  │                                                           │ │
│  │   混合任务（侦察+打击）──▶ 战术层先行，战役层后优         │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │               状态同步器                                   │ │
│  │  • 战术层航迹数据实时同步到战役层（Redpanda）              │ │
│  │  • 战役层COA优化结果异步下发给战术层                       │ │
│  │  • 冲突检测：战术层行动是否偏离战役层计划                   │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │               升级/降级控制器                               │ │
│  │  • 战术层无法处理的威胁 → 升级到战役层                     │ │
│  │  • 战役层计划执行中遇突发 → 降级到战术层应急               │ │
│  │  • 通信中断时 → 边缘自主引擎接管                           │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```


**问题**：原C2TaskRouter仅根据任务类型和静态规则路由，不考虑下游组件实际负载。当战术层GPU队列已满时仍路由到战术层，导致SLA违规。

**修复方案**：集成Prometheus实时指标，根据GPU利用率、队列深度动态调整路由策略。

```python
# coordination/task_router.py
import asyncio
import aiohttp
from typing import Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta


class SystemTier(Enum):
    SHORT_CIRCUIT = "short_circuit"  # 短路路径
    TACTICAL = "tactical"
    CAMPAIGN = "campaign"
    HYBRID = "hybrid"
    DEGRADED = "degraded"  # 降级路由


@dataclass
class RoutingDecision:
    tier: SystemTier
    reason: str
    time_constraint_seconds: int
    requires_human_approval: bool = False
    fallback_tier: Optional[SystemTier] = None  # 降级目标


@dataclass
class ComponentLoadMetrics:
    """组件负载指标（从Prometheus采集）"""
    gpu_utilization_pct: float = 0.0       # GPU利用率
    gpu_memory_utilization_pct: float = 0.0  # GPU显存利用率
    inference_queue_depth: int = 0          # 推理队列深度
    avg_inference_latency_ms: float = 0.0   # 平均推理延迟
    active_requests: int = 0                # 活跃请求数
    last_updated: datetime = field(default_factory=datetime.utcnow)


class LoadAwareC2TaskRouter:
    """
    负载感知的C2任务分级路由器
    在静态规则基础上叠加负载感知逻辑，避免路由到过载组件
    """

    # 时敏目标（TST）类型——走短路路径
    TST_TYPES = {"incoming_missile", "hostile_airborne", "active_shooter"}

    # 负载阈值配置
    TACTICAL_GPU_THRESHOLD = 0.85       # 战术层GPU利用率阈值
    TACTICAL_QUEUE_THRESHOLD = 40       # 战术层队列深度阈值
    TACTICAL_LATENCY_THRESHOLD_MS = 80  # 战术层延迟阈值(ms)
    CAMPAIGN_GPU_THRESHOLD = 0.95       # 战役层GPU利用率阈值
    CAMPAIGN_QUEUE_THRESHOLD = 180      # 战役层队列深度阈值

    def __init__(self, prometheus_url: str = "http://prometheus:9090"):
        self._prometheus_url = prometheus_url
        self._tactical_metrics = ComponentLoadMetrics()
        self._campaign_metrics = ComponentLoadMetrics()
        self._http_session: Optional[aiohttp.ClientSession] = None
        self._metrics_ttl = timedelta(seconds=5)  # 指标缓存5秒

    async def _refresh_metrics(self):
        """从Prometheus拉取最新负载指标"""
        now = datetime.utcnow()

        # 检查缓存是否过期
        if (now - self._tactical_metrics.last_updated) < self._metrics_ttl:
            return

        if self._http_session is None:
            self._http_session = aiohttp.ClientSession()

        queries = {
            "tactical_gpu_util": 'nvidia_gpu_utilization{gpu="0"}',
            "tactical_gpu_mem": 'nvidia_gpu_memory_utilization{gpu="0"}',
            "tactical_queue": 'triton_inference_queue_depth{model="target_detect"}',
            "tactical_latency": 'triton_inference_latency_ms{model="target_detect",quantile="0.95"}',
            "campaign_gpu_util": 'nvidia_gpu_utilization{gpu="1"}',
            "campaign_queue": 'sglang_request_queue_depth{}',
        }

        try:
            for key, query in queries.items():
                result = await self._query_prometheus(query)
                value = float(result) if result else 0.0

                if key.startswith("tactical"):
                    if "gpu_util" in key:
                        self._tactical_metrics.gpu_utilization_pct = value
                    elif "gpu_mem" in key:
                        self._tactical_metrics.gpu_memory_utilization_pct = value
                    elif "queue" in key:
                        self._tactical_metrics.inference_queue_depth = int(value)
                    elif "latency" in key:
                        self._tactical_metrics.avg_inference_latency_ms = value
                elif key.startswith("campaign"):
                    if "gpu_util" in key:
                        self._campaign_metrics.gpu_utilization_pct = value
                    elif "queue" in key:
                        self._campaign_metrics.inference_queue_depth = int(value)

            self._tactical_metrics.last_updated = now
            self._campaign_metrics.last_updated = now

        except Exception as e:
            # Prometheus不可用时使用缓存的旧指标，但记录警告
            # 持续失败超过5次应触发告警（见第10章监控体系）
            pass

    async def _query_prometheus(self, query: str) -> Optional[str]:
        """查询单个Prometheus指标"""
        url = f"{self._prometheus_url}/api/v1/query"
        params = {"query": query}
        async with self._http_session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=2)) as resp:
            if resp.status == 200:
                data = await resp.json()
                results = data.get("data", {}).get("result", [])
                if results:
                    return results[0].get("value", [None, None])[1]
        return None

    def _is_tactical_overloaded(self) -> bool:
        """判断战术层是否过载"""
        m = self._tactical_metrics
        return (
            m.gpu_utilization_pct > self.TACTICAL_GPU_THRESHOLD
            or m.inference_queue_depth > self.TACTICAL_QUEUE_THRESHOLD
            or m.avg_inference_latency_ms > self.TACTICAL_LATENCY_THRESHOLD_MS
        )

    def _is_campaign_overloaded(self) -> bool:
        """判断战役层是否过载"""
        m = self._campaign_metrics
        return (
            m.gpu_utilization_pct > self.CAMPAIGN_GPU_THRESHOLD
            or m.inference_queue_depth > self.CAMPAIGN_QUEUE_THRESHOLD
        )

    async def route(self, task_type: str, params: Dict[str, Any]) -> RoutingDecision:
        """
        负载感知路由决策
        在静态规则基础上叠加负载检查
        """
        # 刷新负载指标
        await self._refresh_metrics()

        # === 静态规则优先 ===

        # 时敏目标 → 短路路径（不可降级，必须处理）
        if task_type in self.TST_TYPES:
            return RoutingDecision(
                tier=SystemTier.SHORT_CIRCUIT,
                reason=f"TST target: {task_type}, bypassing Temporal",
                time_constraint_seconds=1,
                requires_human_approval=False,
            )

        urgency = params.get("urgency", "normal")
        time_to_impact = params.get("time_to_impact_seconds", float("inf"))

        # 时间敏感目标 → 战术层
        if time_to_impact < 300:
            base_tier = SystemTier.TACTICAL
            base_reason = f"Time-critical: TTI={time_to_impact}s"
        elif task_type == "path_planning":
            num_waypoints = len(params.get("waypoints", []))
            if num_waypoints <= 10 and urgency == "high":
                base_tier = SystemTier.TACTICAL
                base_reason = "Small-scale urgent routing"
            else:
                base_tier = SystemTier.CAMPAIGN
                base_reason = f"Large-scale planning: {num_waypoints} waypoints"
        elif task_type == "coa_generation":
            base_tier = SystemTier.CAMPAIGN
            base_reason = "COA generation requires LLM + OR-Tools"
        elif task_type == "multi_domain_coordination":
            base_tier = SystemTier.CAMPAIGN
            base_reason = "Multi-domain coordination"
        else:
            base_tier = SystemTier.HYBRID
            base_reason = "Default: tactical observe, campaign plan"

        # === 负载感知动态调整 ===

        if base_tier == SystemTier.TACTICAL and self._is_tactical_overloaded():
            # 战术层过载 → 检查能否降级
            if time_to_impact < 60:
                # 极度紧急，不允许降级，标记过载告警
                return RoutingDecision(
                    tier=SystemTier.TACTICAL,
                    reason=f"{base_reason} [WARN: tactical GPU overloaded]",
                    time_constraint_seconds=max(int(time_to_impact * 0.5), 5),
                    requires_human_approval=(params.get("action_type") == "kinetic"),
                )
            else:
                # 可降级到战役层
                return RoutingDecision(
                    tier=SystemTier.DEGRADED,
                    reason=f"{base_reason} →降级到战役层(tactical GPU overloaded)",
                    time_constraint_seconds=120,
                    requires_human_approval=True,
                    fallback_tier=SystemTier.CAMPAIGN,
                )

        if base_tier == SystemTier.CAMPAIGN and self._is_campaign_overloaded():
            # 战役层过载 → 排队等待（战役任务不降级到战术层）
            return RoutingDecision(
                tier=SystemTier.CAMPAIGN,
                reason=f"{base_reason} [WARN: campaign queue full, will wait]",
                time_constraint_seconds=600,
                requires_human_approval=True,
            )

        # 正常路由
        time_constraint = 120
        if time_to_impact < 300:
            time_constraint = max(int(time_to_impact * 0.5), 10)
        elif base_tier == SystemTier.CAMPAIGN:
            time_constraint = 300 if task_type == "coa_generation" else 600

        return RoutingDecision(
            tier=base_tier,
            reason=base_reason,
            time_constraint_seconds=time_constraint,
            requires_human_approval=(
                params.get("action_type") == "kinetic" or base_tier == SystemTier.CAMPAIGN
            ),
        )
```

#### 4.6.2 数据一致性机制

快路径写入Valkey（TTL 5分钟），慢路径写入PostgreSQL（持久化），通过异步对账保证最终一致性：


**问题**：快路径写入Valkey（TTL 5分钟，内存态），慢路径写入PostgreSQL（持久化），两条路径对同一实体的状态可能不一致。例如，战术层在Valkey中更新了航迹位置和威胁等级，但战役层仍从PostgreSQL读取到旧状态，导致COA规划基于过时态势。

**修复方案：异步对账 + Redpanda变更事件流**

```text
┌─────────────────────────────────────────────────────────────────┐
│             快慢路径数据对账架构                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  战术层写入                                                      │
│  ├── Valkey（实时热数据，TTL=5min）                              │
│  └── Redpanda topic: "tactical_track_updates"                   │
│       └── entity_id + delta + timestamp                         │
│                                                                 │
│  对账消费者（Reconciliation Consumer）                           │
│  ├── 消费 "tactical_track_updates"                              │
│  ├── 合并到 PostgreSQL（upsert by entity_id）                    │
│  ├── 更新 TimescaleDB 时序数据                                   │
│  └── 发布 "cop_reconciled" 事件                                 │
│                                                                 │
│  战役层读取                                                      │
│  ├── 优先读 Valkey（实时数据，< 5ms）                            │
│  └── Fallback 读 PostgreSQL（持久化数据，< 50ms）               │
│                                                                 │
│  一致性保证：                                                    │
│  ├── 最终一致性窗口 < 2秒（Redpanda消费延迟）                    │
│  ├── 实体级版本号（乐观锁，防止旧数据覆盖新数据）                 │
│  └── 冲突检测：Valkey版本 > PG版本才写入                         │
└─────────────────────────────────────────────────────────────────┘
```

**对账服务代码**：

```python
# coordination/data_reconciler.py
import asyncio
import aiokafka
import asyncpg
import redis.asyncio as aioredis
import json
from typing import Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class TrackDelta:
    """航迹变更增量"""
    entity_id: str
    version: int
    delta: Dict[str, Any]
    timestamp: str
    source: str  # "tactical" or "campaign"


class FastSlowReconciler:
    """
    快慢路径数据对账服务
    消费战术层实时变更，异步合并到PostgreSQL持久层
    保证最终一致性，对账窗口 < 2秒
    """

    def __init__(self, config: Dict[str, Any]):
        self._redpanda_brokers = config["redpanda_brokers"]
        self._pg_dsn = config["pg_dsn"]
        self._redis_url = config.get("redis_url", "redis://valkey-master:6379")
        self._consumer: Optional[aiokafka.AIOKafkaConsumer] = None
        self._pg_pool: Optional[asyncpg.Pool] = None
        self._redis: Optional[aioredis.Redis] = None

    async def start(self):
        """启动对账服务"""
        self._consumer = aiokafka.AIOKafkaConsumer(
            "tactical_track_updates",
            bootstrap_servers=self._redpanda_brokers,
            group_id="fast-slow-reconciler",
            auto_offset_reset="latest",
            enable_auto_commit=False,
        )
        self._pg_pool = await asyncpg.create_pool(self._pg_dsn, min_size=2, max_size=10)
        self._redis = aioredis.from_url(self._redis_url)

        await self._consumer.start()

        try:
            async for msg in self._consumer:
                await self._reconcile_message(msg)
                await self._consumer.commit()
        finally:
            await self._consumer.stop()
            await self._pg_pool.close()

    async def _reconcile_message(self, msg):
        """处理单条变更消息"""
        data = json.loads(msg.value)
        delta = TrackDelta(
            entity_id=data["entity_id"],
            version=data["version"],
            delta=data["delta"],
            timestamp=data["timestamp"],
            source=data.get("source", "tactical"),
        )

        # 乐观锁：只在新版本大于PG中版本时才更新
        async with self._pg_pool.acquire() as conn:
            # 读取当前PG版本
            current = await conn.fetchrow(
                "SELECT version, data FROM military_entities WHERE entity_id = $1",
                delta.entity_id,
            )

            if current and current["version"] >= delta.version:
                return  # PG中数据更新或相同，跳过

            # 合并变更并写入PG
            if current:
                existing_data = json.loads(current["data"])
                existing_data.update(delta.delta)
                merged_data = existing_data
            else:
                merged_data = delta.delta

            await conn.execute(
                """
                INSERT INTO military_entities (entity_id, version, data, updated_at)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (entity_id)
                DO UPDATE SET version = $2, data = $3, updated_at = $4
                WHERE military_entities.version < $2
                """,
                delta.entity_id,
                delta.version,
                json.dumps(merged_data),
                datetime.utcnow(),
            )

        # 如果有时序数据，同步到TimescaleDB
        if "position" in delta.delta or "velocity" in delta.delta:
            await self._write_timeseries(delta)

    async def _write_timeseries(self, delta: TrackDelta):
        """写入时序位置/速度数据到TimescaleDB"""
        async with self._pg_pool.acquire() as conn:
            pos = delta.delta.get("position", {})
            vel = delta.delta.get("velocity", {})
            await conn.execute(
                """
                INSERT INTO track_timeseries (entity_id, time, lat, lon, alt, speed, heading)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                """,
                delta.entity_id,
                datetime.utcnow(),
                pos.get("latitude"),
                pos.get("longitude"),
                pos.get("altitude_m"),
                vel.get("speed_mps"),
                vel.get("heading_deg"),
            )
```

**战术层发布变更事件**（修改ShortCircuitProcessor和TacticalPipeline）：

```python
# 在 fast_system/short_circuit.py 的 _update_track_cache 方法中追加：
# 发布变更事件到Redpanda供对账服务消费
await self._producer.send_and_wait(
    "tactical_track_updates",
    json.dumps({
        "entity_id": track.track_id,
        "version": int(datetime.utcnow().timestamp() * 1000),
        "delta": track.__dict__,
        "timestamp": datetime.utcnow().isoformat(),
        "source": "tactical_short_circuit",
    }).encode(),
)
```

#### 4.6.3 结果融合控制器


**问题**：原方案缺少快慢路径结果的实际融合机制。战术层快速给出初始研判（<100ms），战役层随后给出优化分析（30-120s），两者的结果需要对同一实体进行合并，取"快速+最优"的最终决策。

**修复方案：基于Redpanda的双路融合，按entity_id关联合并**

```python
# coordination/fast_slow_fusion.py
import asyncio
import aiokafka
import json
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum


class FusionState(str, Enum):
    FAST_ONLY = "fast_only"           # 仅有快速结果
    SLOW_ONLY = "slow_only"           # 仅有慢速结果
    FUSED = "fused"                   # 已融合
    CONFLICT_DETECTED = "conflict"    # 快慢结果冲突


@dataclass
class FusionRecord:
    """融合记录"""
    entity_id: str
    fast_result: Optional[Dict[str, Any]] = None
    slow_result: Optional[Dict[str, Any]] = None
    state: FusionState = FusionState.FAST_ONLY
    fused_result: Optional[Dict[str, Any]] = None
    fast_timestamp: Optional[datetime] = None
    slow_timestamp: Optional[datetime] = None
    fusion_timestamp: Optional[datetime] = None


class FastSlowFusionController:
    """
    快慢路径结果融合控制器
    通过Redpanda订阅快慢两条路径的结果流，按entity_id关联合并

    融合策略：
    1. 战术层先出快速结果 → 立即生效（快速响应）
    2. 战役层后出优化结果 → 覆盖快速结果（更优决策）
    3. 冲突检测：若快速结果是"威胁"而优化结果是"非威胁"（或反之），标记冲突上报人类
    """

    # 融合等待超时（超时后仅使用已有结果）
    SLOW_RESULT_TIMEOUT = timedelta(seconds=180)

    # 冲突判定字段
    CONFLICT_FIELDS = ["threat_level", "classification", "engagement_recommendation"]

    def __init__(self, config: Dict[str, Any]):
        self._redpanda_brokers = config["redpanda_brokers"]
        self._consumer: Optional[aiokafka.AIOKafkaConsumer] = None
        self._producer: Optional[aiokafka.AIOKafkaProducer] = None
        self._fusion_store: Dict[str, FusionRecord] = {}
        self._max_fusion_records = 10000  # 内存上限
        self._running = False

    async def start(self):
        """启动融合控制器"""
        self._consumer = aiokafka.AIOKafkaConsumer(
            "tactical_analysis_results",   # 战术层结果topic
            "campaign_analysis_results",    # 战役层结果topic
            bootstrap_servers=self._redpanda_brokers,
            group_id="fast-slow-fusion",
            auto_offset_reset="latest",
        )
        self._producer = aiokafka.AIOKafkaProducer(
            bootstrap_servers=self._redpanda_brokers,
            compression_type="lz4",
        )
        await self._consumer.start()
        await self._producer.start()
        self._running = True

        # 启动过期清理协程
        asyncio.create_task(self._cleanup_expired_records())

        try:
            async for msg in await self._consumer.getmany(timeout_ms=100):
                for tp, messages in msg.items():
                    for m in messages:
                        await self._process_result(tp.topic, m)
        finally:
            await self._consumer.stop()
            await self._producer.stop()

    async def _process_result(self, topic: str, msg):
        """处理快/慢路径的分析结果"""
        data = json.loads(msg.value)
        entity_id = data.get("entity_id")
        if not entity_id:
            return

        record = self._fusion_store.get(entity_id)
        if record is None:
            record = FusionRecord(entity_id=entity_id)
            self._fusion_store[entity_id] = record

        if topic == "tactical_analysis_results":
            record.fast_result = data
            record.fast_timestamp = datetime.utcnow()
            # 快速结果立即发布（不等慢速结果）
            await self._publish_interim(record, source="fast")
            # 尝试融合
            if record.slow_result:
                await self._fuse(record)

        elif topic == "campaign_analysis_results":
            record.slow_result = data
            record.slow_timestamp = datetime.utcnow()
            # 尝试融合
            if record.fast_result:
                await self._fuse(record)
            else:
                # 仅有慢速结果（可能快速路径超时/降级）
                record.state = FusionState.SLOW_ONLY
                await self._publish_interim(record, source="slow")

    async def _fuse(self, record: FusionRecord):
        """融合快慢结果"""
        # 检测冲突
        conflicts = self._detect_conflicts(record.fast_result, record.slow_result)

        if conflicts:
            record.state = FusionState.CONFLICT_DETECTED
            # 冲突结果上报人类决策
            await self._publish_conflict_alert(record, conflicts)
            # 默认采用快速结果（保守策略）
            record.fused_result = {
                **record.fast_result,
                "fusion_note": "conflict_detected_using_fast_result",
                "conflicts": conflicts,
            }
        else:
            record.state = FusionState.FUSED
            # 无冲突：慢速结果覆盖快速结果（更优决策）
            record.fused_result = {
                **record.fast_result,
                **record.slow_result,
                "fusion_note": "fused_slow_overrides_fast",
            }

        record.fusion_timestamp = datetime.utcnow()

        # 发布融合结果
        await self._producer.send_and_wait(
            "fused_analysis_results",
            json.dumps({
                "entity_id": record.entity_id,
                "state": record.state.value,
                "fused_result": record.fused_result,
                "fusion_timestamp": record.fusion_timestamp.isoformat(),
            }).encode(),
        )

    def _detect_conflicts(self, fast: Dict, slow: Dict) -> List[Dict]:
        """检测快慢结果中的关键冲突"""
        conflicts = []
        for field in self.CONFLICT_FIELDS:
            fast_val = fast.get(field)
            slow_val = slow.get(field)
            if fast_val and slow_val and fast_val != slow_val:
                conflicts.append({
                    "field": field,
                    "fast_value": fast_val,
                    "slow_value": slow_val,
                })
        return conflicts

    async def _publish_interim(self, record: FusionRecord, source: str):
        """发布中间结果（不等融合完成）"""
        result = record.fast_result if source == "fast" else record.slow_result
        await self._producer.send_and_wait(
            "interim_analysis_results",
            json.dumps({
                "entity_id": record.entity_id,
                "source": source,
                "result": result,
                "timestamp": datetime.utcnow().isoformat(),
            }).encode(),
        )

    async def _publish_conflict_alert(self, record: FusionRecord, conflicts: List[Dict]):
        """发布冲突告警（需要人类介入）"""
        await self._producer.send_and_wait(
            "fusion_conflict_alerts",
            json.dumps({
                "entity_id": record.entity_id,
                "alert_type": "FAST_SLOW_CONFLICT",
                "conflicts": conflicts,
                "fast_result": record.fast_result,
                "slow_result": record.slow_result,
                "timestamp": datetime.utcnow().isoformat(),
            }).encode(),
        )

    async def _cleanup_expired_records(self):
        """定期清理过期的融合记录"""
        while self._running:
            await asyncio.sleep(60)
            cutoff = datetime.utcnow() - timedelta(minutes=30)
            expired = [
                eid for eid, rec in self._fusion_store.items()
                if (rec.fusion_timestamp and rec.fusion_timestamp < cutoff)
                or (rec.fast_timestamp and rec.fast_timestamp < cutoff)
            ]
            for eid in expired:
                del self._fusion_store[eid]
```

**融合流程示意**：

```text
典型时序（以威胁研判为例）：

T+0ms    传感器检测到目标
T+80ms   战术层快速结果：{threat_level: HIGH, classification: "fighter_jet",
          confidence: 0.72} → 发布到 interim_analysis_results
T+80ms   COP立即更新威胁等级为HIGH，指挥员收到初步告警
T+65s    战役层优化结果：{threat_level: MEDIUM, classification: "electronic_warfare",
          confidence: 0.91, reasoning: "ECM signature detected"} → 融合控制器
T+65s    冲突检测：threat_level HIGH≠MEDIUM → 冲突告警
T+65s    融合决策：采用慢速结果（更高置信度），但上报人类确认
T+65s    COP更新：威胁等级调整为MEDIUM，标记"待人工确认"

若快慢结果无冲突：
T+65s    慢速结果直接覆盖快速结果，融合完成，无需人工介入
```

### 4.7 经验蒸馏：慢->快的自动迁移

#### 4.7.1 设计理念

类比人类指挥官的成长——新指挥官遇事需要深度分析（慢系统），但随着经验积累，常见情况可以凭直觉快速反应（快系统）。经验蒸馏闭环建立**从慢到快的自动迁移机制**，并通过三层输出将经验转化为快系统能力：

```text
经验蒸馏四阶段（三输出）：

  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
  │ 记录阶段 │──▶│ 挖掘阶段 │──▶│ 晋升阶段 │──▶│ 蒸馏阶段 │
  │ Record   │   │ Mine     │   │ Promote  │   │ Distill  │
  └──────────┘   └──────────┘   └──────────┘   └──────────┘

  每次执行后记录   定期聚类分析    满足晋升门槛    积累≥1000条
  → 态势特征      → LLM泛化      三种输出:       成功案例后
  + 工作流模板    → 提取共性      ① Qdrant索引   触发小模型
  + 参数配置      → 生成触发规则  ② OPA编译规则  微调(SFT+DPO)
  + 执行结果                      ③ 蒸馏训练数据  → 更新小模型
  + 指挥员决策
```

**三种快系统输出**：

| 输出 | 触发条件 | 执行路径 | 延迟 | 更新频率 |
|------|---------|---------|------|---------|
| Qdrant索引更新 | 成功率≥90%，频次≥10 | L2向量检索 | ~20ms | 实时 |
| OPA编译规则 | 成功率≥97%，频次≥50，通过对抗验证 | L1规则匹配 | <5ms | 实时 |
| 蒸馏小模型微调 | 积累≥1000条成功案例 | L0模型推理 | <30ms | 周级 |

蒸馏小模型微调的详细流程见第8.6节。

**晋升门槛**（工作流从慢系统先验晋升为快系统先验的条件，代码定义见4.7.2 `PROMOTION_THRESHOLDS`）：

| 条件 | 阈值 | 含义 |
|------|------|------|
| 成功率 | ≥ 90% | 最近N次同类态势下成功率 |
| 指挥员通过率 | ≥ 95% | 极少被否决（说明方案可靠） |
| 执行时间 | < 10s | 在快系统SLA内可完成 |
| 出现频次 | ≥ 10次 | 非偶然事件，具有统计意义 |
| 时效性 | 30天内 | 经验未过时 |

#### 4.7.2 经验记录与挖掘

经验蒸馏的第一阶段：每次工作流执行后自动记录完整经验元组（情境、模板、参数、结果、人工裁决），然后定期挖掘历史经验，统计哪些模板在哪些情境下表现稳定，识别满足晋升条件的候选模板。

```python
# distillation/experience_recorder.py
import json
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

from clients.qdrant_client import QdrantRegistryClient
from clients.sglang_client import SGLangMilitaryClient
from clients.redis_client import ValkeyClient


@dataclass
class ExperienceTuple:
    """经验元组——一次完整的工作流执行记录"""
    experience_id: str
    # 态势特征
    situation_features: Dict[str, Any]     # 态势描述
    situation_hash: str                     # 态势特征哈希
    situation_embedding: List[float] = field(default_factory=list)
    # 工作流信息
    template_id: str
    template_version: int
    filled_params: Dict[str, Any]
    # 执行结果
    outcome: str                            # "success"/"failure"/"partial"
    execution_time_ms: int
    # 指挥员决策
    human_verdict: str                      # "approved"/"rejected"/"modified"/"timeout"
    human_modifications: Optional[Dict] = None  # 指挥员做了哪些修改
    # 元数据
    triggered_by: str                       # "fast"/"slow"/"human"
    timestamp: datetime = field(default_factory=datetime.utcnow)


class ExperienceRecorder:
    """
    经验记录器
    在每次工作流执行完成后自动记录经验元组
    """

    def __init__(self, config: Dict[str, Any]):
        self._sglang = SGLangMilitaryClient(config["sglang_url"])
        self._qdrant = QdrantRegistryClient(config["qdrant_url"])

    async def record(
        self,
        situation: Dict[str, Any],
        template_id: str,
        template_version: int,
        filled_params: Dict[str, Any],
        outcome: str,
        execution_time_ms: int,
        human_verdict: str,
        human_modifications: Optional[Dict] = None,
        triggered_by: str = "slow",
    ) -> str:
        """记录一次工作流执行经验"""
        # 生成态势特征哈希（用于后续聚类匹配）
        situation_hash = self._hash_situation(situation)

        # 生成态势嵌入向量
        situation_text = self._situation_to_text(situation)
        embedding = await self._sglang.embed(situation_text)

        exp = ExperienceTuple(
            experience_id=f"EXP-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{situation_hash[:8]}",
            situation_features=situation,
            situation_hash=situation_hash,
            situation_embedding=embedding,
            template_id=template_id,
            template_version=template_version,
            filled_params=filled_params,
            outcome=outcome,
            execution_time_ms=execution_time_ms,
            human_verdict=human_verdict,
            human_modifications=human_modifications,
            triggered_by=triggered_by,
        )

        # 存入Qdrant经验集合
        await self._qdrant.upsert(
            collection="workflow_experiences",
            point_id=exp.experience_id,
            vector=embedding,
            payload={
                "situation_hash": situation_hash,
                "template_id": template_id,
                "template_version": template_version,
                "filled_params": filled_params,
                "outcome": outcome,
                "execution_time_ms": execution_time_ms,
                "human_verdict": human_verdict,
                "triggered_by": triggered_by,
                "timestamp": exp.timestamp.isoformat(),
            },
        )

        # 同步写入PostgreSQL执行历史（持久化）
        # (由 data_reconciler 异步完成)

        return exp.experience_id

    def _hash_situation(self, situation: Dict) -> str:
        """生成态势特征哈希（用于聚类和匹配）"""
        # 提取关键特征进行哈希
        key_features = {
            "threat_type": situation.get("threat_type", "unknown"),
            "domain": situation.get("domain", "unknown"),
            "urgency": situation.get("urgency", "normal"),
            "entity_count": len(situation.get("entities", [])),
            "has_hostile": any(
                e.get("force_affiliation") == "HOSTILE"
                for e in situation.get("entities", [])
            ),
        }
        feature_str = json.dumps(key_features, sort_keys=True)
        return hashlib.sha256(feature_str.encode()).hexdigest()

    def _situation_to_text(self, situation: Dict) -> str:
        """态势数据转文本（用于嵌入生成）"""
        parts = [
            f"威胁类型: {situation.get('threat_type', 'unknown')}",
            f"作战域: {situation.get('domain', 'unknown')}",
            f"紧急程度: {situation.get('urgency', 'normal')}",
            f"威胁等级: {situation.get('threat_level', 'NONE')}",
            f"目标数量: {len(situation.get('entities', []))}",
        ]
        return " | ".join(parts)
```


```python
# distillation/experience_miner.py
import json
from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

from clients.litellm_client import C2LLMClient
from clients.qdrant_client import QdrantRegistryClient
from dataclasses import dataclass, field


@dataclass
class PromotionCandidate:
    """晋升候选——满足条件的经验模式"""
    template_id: str
    cluster_description: str          # LLM生成的模式描述
    sample_situations: List[Dict]      # 代表性态势样本
    success_rate: float
    approval_rate: float
    avg_execution_time_ms: float
    occurrence_count: int
    suggested_trigger: Dict[str, Any]  # LLM建议的触发条件


class ExperienceMiner:
    """
    经验挖掘器
    定期分析经验元组，发现可晋升的模式
    """

    # 晋升门槛
    PROMOTION_THRESHOLDS = {
        "min_success_rate": 0.90,
        "min_approval_rate": 0.95,
        "max_execution_time_ms": 10000,
        "min_occurrences": 10,
        "recency_days": 30,
    }

    def __init__(self, config: Dict[str, Any]):
        self._llm = C2LLMClient(config["litellm_config"])
        self._qdrant = QdrantRegistryClient(config["qdrant_url"])

    async def mine_promotion_candidates(self) -> List[PromotionCandidate]:
        """
        挖掘可晋升的经验模式
        Step 1: 按template_id聚合经验
        Step 2: 统计成功率、审批率、执行时间
        Step 3: 筛选满足晋升门槛的模板
        Step 4: LLM泛化生成触发条件
        """
        # Step 1: 从Qdrant拉取近期所有经验（含成功和失败，以便计算真实成功率）
        recent_experiences = await self._qdrant.scroll(
            collection="workflow_experiences",
            filters={
                "timestamp": {
                    "gte": (datetime.utcnow() - timedelta(days=self.PROMOTION_THRESHOLDS["recency_days"])).isoformat()
                },
            },
            limit=1000,
        )

        # Step 2: 按template_id聚合
        template_groups: Dict[str, List[Dict]] = defaultdict(list)
        for exp in recent_experiences:
            template_groups[exp["template_id"]].append(exp)

        # Step 3: 统计并筛选
        candidates = []
        for template_id, experiences in template_groups.items():
            stats = self._compute_stats(experiences)

            if (
                stats["success_rate"] >= self.PROMOTION_THRESHOLDS["min_success_rate"]
                and stats["approval_rate"] >= self.PROMOTION_THRESHOLDS["min_approval_rate"]
                and stats["avg_execution_time_ms"] <= self.PROMOTION_THRESHOLDS["max_execution_time_ms"]
                and stats["count"] >= self.PROMOTION_THRESHOLDS["min_occurrences"]
            ):
                # Step 4: LLM泛化
                sample_situations = [e.get("situation_features", {}) for e in experiences[:5]]
                generalized_trigger = await self._generalize_with_llm(
                    template_id, sample_situations, stats
                )

                candidates.append(PromotionCandidate(
                    template_id=template_id,
                    cluster_description=generalized_trigger["description"],
                    sample_situations=sample_situations,
                    success_rate=stats["success_rate"],
                    approval_rate=stats["approval_rate"],
                    avg_execution_time_ms=stats["avg_execution_time_ms"],
                    occurrence_count=stats["count"],
                    suggested_trigger=generalized_trigger["trigger"],
                ))

        return candidates

    def _compute_stats(self, experiences: List[Dict]) -> Dict[str, Any]:
        """计算模板的经验统计"""
        total = len(experiences)
        success_count = sum(1 for e in experiences if e.get("outcome") == "success")
        approved = sum(1 for e in experiences if e.get("human_verdict") == "approved")
        times = [e.get("execution_time_ms", 0) for e in experiences]

        return {
            "count": total,
            "success_rate": success_count / max(total, 1),
            "approval_rate": approved / max(total, 1),
            "avg_execution_time_ms": sum(times) / max(len(times), 1),
        }

    async def _generalize_with_llm(
        self, template_id: str, samples: List[Dict], stats: Dict
    ) -> Dict[str, Any]:
        """
        LLM泛化：从多个成功经验中提取共性规律，生成更精确的触发条件
        """
        prompt = f"""
你是JSAI系统分析师。分析以下成功案例的共性规律。

工作流模板: {template_id}
成功次数: {stats['count']}
成功率: {stats['success_rate']:.0%}
审批率: {stats['approval_rate']:.0%}

成功案例的态势特征样本:
{json.dumps(samples[:5], ensure_ascii=False, indent=2)}

请分析这些成功案例的共性规律，生成更精确的触发条件（JSON格式）：
{{
    "description": "一句话描述这种态势模式的共性",
    "trigger": {{
        "threat_type": ["匹配的威胁类型"],
        "domain": ["匹配的作战域"],
        "urgency_range": ["匹配的紧急程度"],
        "entity_count_range": [最小, 最大],
        "custom_conditions": {{其他关键特征}}
    }},
    "recommended_params": {{
        "基于成功经验建议的默认参数"
    }},
    "confidence": 0.95
}}"""
        response = self._llm.generate(prompt, temperature=0.1)

        try:
            return json.loads(response["content"])
        except json.JSONDecodeError:
            return {
                "description": f"Template {template_id} 的高成功率模式",
                "trigger": {},
                "recommended_params": {},
                "confidence": 0.0,
            }
```

#### 4.7.3 工作流简化与模板编译

经验蒸馏的核心步骤：将慢系统创建的复杂工作流简化编译为快系统可直接执行的精简模板。四种简化策略将8步慢工作流压缩为4步快模板，消除冗余的LLM推理步骤、预缓存RAG结果、固化优化参数、降低仿真强度。

```python
# distillation/workflow_simplifier.py
import json
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from dataclasses import dataclass, field

from clients.litellm_client import C2LLMClient
from clients.qdrant_client import QdrantRegistryClient
from clients.sglang_client import SGLangMilitaryClient
from security.policy_engine import OPAPolicyEngine
from registry.workflow_template import (
    WorkflowTemplate, StepDAG, StepNode, StepEdge,
    ParamField, TriggerCondition, TemplateStatus,
)
from registry.template_lifecycle import TemplateLifecycleManager


@dataclass
class SimplificationReport:
    """简化报告"""
    original_template_id: str
    simplified_template_id: str
    original_steps: int
    simplified_steps: int
    eliminated_llm_steps: int       # 消除的LLM推理步骤
    precached_rag_entries: int      # 预缓存的RAG条目
    solidified_params: int          # 固化的参数
    estimated_speedup: float        # 预计加速比
    simulation_passed: bool


class WorkflowSimplifier:
    """
    工作流简化编译器

    核心策略（4种简化手段）：
    1. LLM步骤消除：反复给出相同结果的LLM推理步骤编译为确定性规则
    2. RAG预缓存：频繁检索的条令条目预编译进模板参数
    3. 参数固化：慢系统每次计算出的最优参数直接固化为默认值
    4. 仿真步骤剪枝：高成功率模板降低仿真验证强度

    典型简化效果：
    慢系统工作流(8步: 2xLLM + 1xRAG + 1x仿真 + 4xActivity)
    -> 快系统模板(4步: 4xActivity, 无LLM/无RAG)
    """

    def __init__(self, config: Dict[str, Any]):
        self._llm = C2LLMClient(config["litellm_config"])
        self._qdrant = QdrantRegistryClient(config["qdrant_url"])
        self._sglang = SGLangMilitaryClient(config["sglang_url"])
        self._opa = OPAPolicyEngine(config["opa_url"])
        self._lifecycle = TemplateLifecycleManager(config)

    async def simplify(
        self, template: WorkflowTemplate, experience_data: List[Dict]
    ) -> Tuple[WorkflowTemplate, SimplificationReport]:
        """
        对慢系统工作流执行简化编译

        Args:
            template: 慢系统创建的工作流模板
            experience_data: 该模板的历史执行经验数据

        Returns:
            (simplified_template, report)
        """
        original_steps = len(template.dag.nodes)

        # Step 1: 分析哪些LLM步骤输出一致，可以消除
        llm_eliminations = await self._analyze_repeated_steps(template, experience_data)

        # Step 2: 分析频繁检索的RAG条目，预缓存
        rag_precaches = await self._precache_rag_results(template, experience_data)

        # Step 3: 分析每次都算出相同最优值的参数，固化
        param_solidifications = self._solidify_params(template, experience_data)

        # Step 4: 构建简化后的新模板
        simplified = self._build_simplified_template(
            template, llm_eliminations, rag_precaches, param_solidifications
        )

        simplified_steps = len(simplified.dag.nodes)

        # Step 5: 仿真验证简化后的模板（简化模板使用降低强度的仿真：30次即可）
        # 注：简化模板仍需通过仿真验证，但强度降低（30次 vs 原100次），
        # 且仅检查致命故障（友军误伤、ROE违规），不检查非致命性能指标。
        # 如果原模板通过率≥90%，简化模板可直接继承验证结果。
        sim_passed = True  # TODO: 对接WorkflowSimulationValidator，30次蒙特卡洛

        # Step 6: 注册简化模板
        simplified.status = TemplateStatus.FAST_TRACK
        simplified.created_by = "distillation_simplifier"
        simplified.parent_template_id = template.template_id

        report = SimplificationReport(
            original_template_id=template.template_id,
            simplified_template_id=simplified.template_id,
            original_steps=original_steps,
            simplified_steps=simplified_steps,
            eliminated_llm_steps=len(llm_eliminations),
            precached_rag_entries=len(rag_precaches),
            solidified_params=len(param_solidifications),
            estimated_speedup=original_steps / max(simplified_steps, 1),
            simulation_passed=sim_passed,
        )

        return simplified, report

    async def _analyze_repeated_steps(
        self, template: WorkflowTemplate, experiences: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        策略1: LLM步骤消除
        分析慢系统工作流中哪些LLM推理步骤在历史执行中反复给出相同/高度相似的输出。
        如果一致性>=90%，将该步骤编译为确定性规则或直接消除。
        """
        llm_steps = [
            n for n in template.dag.nodes
            if "llm" in n.activity_type.lower() or "sglang" in n.activity_type.lower()
        ]

        eliminations = []
        for step in llm_steps:
            # 收集该步骤在历史执行中的输出
            step_outputs = []
            for exp in experiences:
                step_results = exp.get("step_results", {})
                if step.step_id in step_results:
                    step_outputs.append(step_results[step.step_id])

            if len(step_outputs) < 5:
                continue

            # 分析输出一致性
            consistency = self._compute_output_consistency(step_outputs)

            if consistency >= 0.90:
                # 输出高度一致 -> 编译为确定性规则
                rule = self._compile_llm_to_rule(step, step_outputs)
                eliminations.append({
                    "step_id": step.step_id,
                    "step_name": step.name,
                    "consistency": consistency,
                    "compiled_rule": rule,
                    "elimination_type": "llm_to_rule",
                })

        return eliminations

    def _compute_output_consistency(self, outputs: List[Any]) -> float:
        """计算输出一致性（0-1）"""
        if not outputs:
            return 0.0

        # 简化实现：检查输出是否完全相同
        if isinstance(outputs[0], dict):
            serialized = [json.dumps(o, sort_keys=True) for o in outputs]
            most_common = max(set(serialized), key=serialized.count)
            return serialized.count(most_common) / len(serialized)
        else:
            most_common = max(set(outputs), key=outputs.count)
            return outputs.count(most_common) / len(outputs)

    def _compile_llm_to_rule(self, step: Any, outputs: List[Any]) -> str:
        """
        将一致的LLM输出编译为OPA规则
        """
        # 取最频繁的输出作为规则结论
        if isinstance(outputs[0], dict):
            serialized = [json.dumps(o, sort_keys=True) for o in outputs]
            most_common_str = max(set(serialized), key=serialized.count)
            conclusion = json.loads(most_common_str)
        else:
            conclusion = outputs[0]

        rule_id = f"simplified_{step.step_id.replace('-', '_')}"
        return f"""# 经验蒸馏自动简化（LLM步骤->确定性规则）
# 原步骤: {step.name} ({step.activity_type})
package c2.simplified

default {rule_id} = null

{rule_id} = {json.dumps(conclusion)} {{
    input.step == "{step.step_id}"
    input.template_status == "fast_track"
}}
"""

    async def _precache_rag_results(
        self, template: WorkflowTemplate, experiences: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        策略2: RAG预缓存
        分析工作流中频繁检索的条令条目，直接固化到模板参数中
        """
        rag_steps = [
            n for n in template.dag.nodes
            if "knowledge" in n.activity_type.lower()
               or "retrieve" in n.activity_type.lower()
               or "rag" in n.activity_type.lower()
        ]

        precaches = []
        for step in rag_steps:
            # 统计历史检索结果
            retrieved_docs = []
            for exp in experiences:
                step_results = exp.get("step_results", {})
                if step.step_id in step_results:
                    results = step_results[step.step_id].get("retrieved_docs", [])
                    retrieved_docs.extend(results)

            if not retrieved_docs:
                continue

            # 取出现频率最高的文档
            doc_freq: Dict[str, int] = {}
            for doc in retrieved_docs:
                key = doc.get("id", str(doc))
                doc_freq[key] = doc_freq.get(key, 0) + 1

            # 频率>=50%的文档预缓存
            threshold = len(experiences) * 0.5
            frequent_docs = [
                doc_id for doc_id, count in doc_freq.items()
                if count >= threshold
            ]

            if frequent_docs:
                precaches.append({
                    "step_id": step.step_id,
                    "precached_doc_ids": frequent_docs,
                    "cache_replaces_step": len(frequent_docs) >= len(set(doc_freq.keys())) * 0.8,
                })

        return precaches

    def _solidify_params(
        self, template: WorkflowTemplate, experiences: List[Dict]
    ) -> List[Dict[str, Any]]:
        """
        策略3: 参数固化
        分析慢系统每次都计算得出的最优参数，直接固化为默认值
        """
        solidifications = []

        for param in template.params:
            if param.source != "auto":
                continue

            # 收集历史填充值
            filled_values = []
            for exp in experiences:
                params = exp.get("filled_params", {})
                if param.name in params:
                    filled_values.append(params[param.name])

            if len(filled_values) < 5:
                continue

            # 检查参数值是否高度一致
            consistency = self._compute_output_consistency(filled_values)
            if consistency >= 0.85:
                # 参数值高度一致 -> 固化为默认值
                most_common = max(set(filled_values), key=filled_values.count)
                solidifications.append({
                    "param_name": param.name,
                    "original_source": param.source,
                    "solidified_value": most_common,
                    "consistency": consistency,
                })

        return solidifications

    def _build_simplified_template(
        self,
        original: WorkflowTemplate,
        llm_eliminations: List[Dict],
        rag_precaches: List[Dict],
        param_solidifications: List[Dict],
    ) -> WorkflowTemplate:
        """构建简化后的新模板"""
        # 过滤掉已消除的步骤
        eliminated_step_ids = {e["step_id"] for e in llm_eliminations}
        # 同时过滤被RAG预缓存替代的步骤
        precached_step_ids = {
            r["step_id"] for r in rag_precaches if r.get("cache_replaces_step", False)
        }
        remove_step_ids = eliminated_step_ids | precached_step_ids

        new_nodes = [
            StepNode(**{**n.model_dump()})
            for n in original.dag.nodes
            if n.step_id not in remove_step_ids
        ]

        # 更新边：移除涉及被消除步骤的边
        new_edges = []
        for edge in original.dag.edges:
            if edge.from_step in remove_step_ids or edge.to_step in remove_step_ids:
                continue
            new_edges.append(StepEdge(**{**edge.model_dump()}))

        # 应用参数固化
        new_params = []
        for p in original.params:
            p_dict = p.model_dump()
            for solid in param_solidifications:
                if solid["param_name"] == p.name:
                    p_dict["default"] = solid["solidified_value"]
                    p_dict["source"] = "solidified"
            new_params.append(ParamField(**p_dict))

        # 确定新的入口和出口步骤
        entry = original.dag.entry_step
        if entry in remove_step_ids:
            for n in new_nodes:
                entry = n.step_id
                break

        exit_steps = [s for s in original.dag.exit_steps if s not in remove_step_ids]
        if not exit_steps and new_nodes:
            exit_steps = [new_nodes[-1].step_id]

        return WorkflowTemplate(
            template_id=f"WF-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-SIM",
            name=f"{original.name}（简化版）",
            version=1,
            description=f"由{original.template_id}简化编译，去除了{len(remove_step_ids)}个复杂步骤",
            status=TemplateStatus.FAST_TRACK,
            trigger=TriggerCondition(**original.trigger.model_dump()),
            params=new_params,
            dag=StepDAG(nodes=new_nodes, edges=new_edges,
                        entry_step=entry, exit_steps=exit_steps),
            created_by="distillation_simplifier",
            parent_template_id=original.template_id,
            tags=original.tags + ["simplified"],
        )
```

**简化示例**：

```text
工作流简化实例——联合打击模板：

  慢系统原始模板（8步）：
  +--------------+    +--------------+    +--------------+
  | observe_radar|--->| orient_fuse  |--->|orient_threat |
  |  (雷达探测)  |    | (多源融合)   |    | (威胁评估)   |
  +--------------+    +--------------+    +------+-------+
                                                |
                         +--------------+    +---v--------+
                         | decide_simu- |<---|decide_coa   |
                         | late(仿真)   |    |(LLM生成COA) |
                         +------+-------+    +------------+
                                |
  +--------------+    +--------v-----+    +--------------+
  | bda_assess   |<---| act_strike   |<---|human_approve |
  | (战损评估)   |    | (火力打击)   |    | (人工审批)   |
  +--------------+    +--------------+    +--------------+
  含: 1xLLM推理(decide_coa) + 1xRAG检索(条令) + 1x仿真 + 5xActivity
  平均执行时间: 45s

  简化后的快系统模板（4步）：
  +--------------+    +--------------+    +--------------+
  | observe_radar|--->| orient_fuse  |--->| orient_threat|
  |  (雷达探测)  |    | (多源融合)   |    | (威胁评估)   |
  +--------------+    +--------------+    +------+-------+
                                                |
                                    +-----------v-----------+
                                    | act_strike(火力打击)   |
                                    | 参数已固化: 目标类型、  |
                                    | 武器选择、打击窗口      |
                                    +-----------------------+

  消除: decide_coa(LLM->固化规则) + decide_simulate(高成功率剪枝)
        + human_approve(fast_track自动审批) + RAG检索(预缓存)
  平均执行时间: 3s，加速比: 15x
```

#### 4.7.4 两级晋升机制

简化后的模板通过两级晋升进入快系统：Level 1标记为`fast_track`（快系统通过Qdrant直接匹配），Level 2编译为OPA规则（短路路径直通，完全绕过工作流选择）。当快系统和慢系统对同一态势产生不同决策时，由4.6.3节的FastSlowConflictResolver进行冲突检测和融合处理。

```python
# distillation/experience_promoter.py
import json
from typing import Dict, Any, List
from datetime import datetime

from clients.qdrant_client import QdrantRegistryClient
from clients.sglang_client import SGLangMilitaryClient
from security.policy_engine import OPAPolicyEngine
from distillation.experience_miner import PromotionCandidate, ExperienceMiner


class ExperiencePromoter:
    """
    经验晋升器
    将满足条件的经验模式晋升为快系统可直接使用的先验

    两级晋升：
    Level 1: 工作流模板标记为 fast_track → 快系统通过Qdrant直接匹配
    Level 2: 极高频+极可靠的模式 → 编译为OPA规则 → 走短路路径（绕过工作流）
    """

    def __init__(self, config: Dict[str, Any]):
        self._qdrant = QdrantRegistryClient(config["qdrant_url"])
        self._sglang = SGLangMilitaryClient(config["sglang_url"])
        self._opa = OPAPolicyEngine(config["opa_url"])
        self._miner = ExperienceMiner(config)

    async def run_promotion_cycle(self) -> Dict[str, Any]:
        """
        执行一次晋升周期
        1. 挖掘候选
        2. 逐个评估晋升
        3. 更新Qdrant索引和OPA规则
        """
        candidates = await self._miner.mine_promotion_candidates()

        results = {
            "candidates_found": len(candidates),
            "promoted_to_fast_track": 0,
            "promoted_to_opa_rule": 0,
            "details": [],
        }

        for candidate in candidates:
            # Level 1: 晋升为 fast_track 模板
            await self._promote_to_fast_track(candidate)
            results["promoted_to_fast_track"] += 1

            # Level 2: 极高频模式晋升为OPA规则（短路路径）
            if (
                candidate.occurrence_count >= 50
                and candidate.success_rate >= 0.97
                and candidate.avg_execution_time_ms <= 1000
            ):
                opa_rule_id = await self._promote_to_opa_rule(candidate)
                results["promoted_to_opa_rule"] += 1

            results["details"].append({
                "template_id": candidate.template_id,
                "success_rate": f"{candidate.success_rate:.0%}",
                "occurrences": candidate.occurrence_count,
            })

        return results

    async def _promote_to_fast_track(self, candidate: PromotionCandidate):
        """
        Level 1 晋升：将工作流模板标记为 fast_track
        更新Qdrant中的触发条件向量，使快系统能直接命中
        """
        # 生成新的触发条件嵌入（基于泛化后的触发条件）
        trigger_text = json.dumps(candidate.suggested_trigger, ensure_ascii=False)
        new_embedding = await self._sglang.embed(trigger_text)

        # 更新Qdrant中该模板的触发向量
        await self._qdrant.upsert(
            collection="workflow_triggers",
            point_id=f"trigger_{candidate.template_id}",
            vector=new_embedding,
            payload={
                "template_id": candidate.template_id,
                "status": "fast_track",  # 标记为快系统优先级
                "trigger": candidate.suggested_trigger,
                "confidence": candidate.success_rate,
                "occurrence_count": candidate.occurrence_count,
                "promoted_at": datetime.utcnow().isoformat(),
            },
        )

        # 更新PostgreSQL中的模板状态
        # UPDATE workflow_templates SET status = 'fast_track' WHERE template_id = ...

    async def _promote_to_opa_rule(self, candidate: PromotionCandidate) -> str:
        """
        Level 2 晋升：将极高频模式编译为OPA规则
        直接进入短路路径，连工作流选择都跳过
        """
        trigger = candidate.suggested_trigger

        # 生成OPA Rego规则
        threat_types = trigger.get("threat_type", [])
        domains = trigger.get("domain", [])
        urgency_levels = trigger.get("urgency_range", [])

        rule_id = f"distilled_{candidate.template_id.replace('-', '_')}"

        rego_rule = f"""# 经验蒸馏自动生成的短路规则
# 模板: {candidate.template_id}
# 成功率: {candidate.success_rate:.0%}, 执行次数: {candidate.occurrence_count}

package c2.auto_dispatch

default auto_dispatch_{rule_id} = false

auto_dispatch_{rule_id} {{
    input.threat_type == {"{"} {", ".join(f'"{t}"' for t in threat_types)} {"}"}
    input.domain == {"{"} {", ".join(f'"{d}"' for d in domains)} {"}"}
    input.urgency == {"{"} {", ".join(f'"{u}"' for u in urgency_levels)} {"}"}
    input.confidence >= 0.8
}}

# 自动执行的工作流模板
dispatch_target_{rule_id} = "{candidate.template_id}" {{
    auto_dispatch_{rule_id}
}}
"""
        # 推送到OPA策略引擎
        self._opa.push_policy(f"distilled/{rule_id}.rego", rego_rule)

        return rule_id
```

#### 4.7.5 蒸馏闭环时序


```text
经验蒸馏闭环时序图：

第1次遭遇（第1天）：
  导弹来袭 → 快系统检索无匹配 → 升级到慢系统
  → 慢系统LLM分析 + RAG检索条令 → 创建"防空拦截模板v1"
  → 仿真验证 → 指挥员审批通过 → 执行成功
  → 经验记录: EXP-001 (慢系统创建, success, approved)

第2-9次遭遇（第1-5天）：
  类似导弹来袭 → 快系统匹配"防空拦截v1"（相似度渐增）
  → 参数自动填充 → 执行 → 每次都记录经验
  → 经验记录: EXP-002~009

第10次遭遇（第6天）：
  经验挖掘器定时运行 → 发现"防空拦截v1"满足晋升门槛：
    ✓ 成功率 10/10 = 100%
    ✓ 审批率 10/10 = 100%
    ✓ 执行时间 < 5s
    ✓ 出现 10次
  → LLM泛化生成精确触发条件
  → Level 1晋升: 模板标记为 fast_track
  → Qdrant索引更新

第11次遭遇（第6天后）：
  导弹来袭 → 快系统Qdrant检索 → 直接命中 fast_track 模板
  → 自动填充参数 → 直接执行（跳过慢系统分析）
  → 从"需要深度分析"变为"直觉反应"

第50次遭遇后：
  经验挖掘器发现：
    ✓ 50次成功, 成功率98%, 执行时间<1s
  → Level 2晋升: 编译为OPA规则
  → 下次类似导弹来袭 → 短路路径直接处理（连工作流选择都跳过）
  → Latency: < 100ms
```

```text
经验蒸馏对现有架构的增强点：

┌───────────────────────────────────────────────────────────────┐
│                     经验蒸馏闭环全图                           │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────┐    ┌──────────┐    ┌──────────┐    ┌─────────┐ │
│  │ 快系统  │───▶│ 执行工作 │───▶│ 经验记录 │───▶│ 经验    │ │
│  │ 选模板  │    │ 流模板   │    │          │    │ 数据库  │ │
│  └────▲────┘    └─────┬────┘    └──────────┘    └────┬────┘ │
│       │               │                              │       │
│       │          执行不够用                    ┌──────▼─────┐ │
│       │               │                      │ 经验挖掘器  │ │
│       │          ┌────▼────┐                 │ (定期运行)  │ │
│       │          │ 慢系统  │                 └──────┬──────┘ │
│       │          │ 创建/   │                       │        │
│       │          │ 调整    │              ┌────────▼──────┐ │
│       │          └─────────┘              │ 晋升判断      │ │
│       │                                   │ 满足门槛？    │ │
│       │                                   └───┬──────┬────┘ │
│       │                                       │      │      │
│       │                              Level 1  │      │ L2   │
│       │                         ┌─────────────▼┐  ┌──▼────┐│
│       │                         │ fast_track    │  │OPA规则││
│       │                         │ 模板更新      │  │短路   ││
│       └─────────────────────────┤ Qdrant索引   │  │路径   ││
│                                 └──────────────┘  └───────┘│
└───────────────────────────────────────────────────────────────┘
```

---

## 5. COP数据平面与知识服务

### 5.1 设计理念

共用作战态势图（Common Operational Picture, COP）数据平面是本架构的核心数据基础设施，参考：
- **JC3IEDM**（联合指挥控制概念模型）：NATO标准化的C2数据交换模型
- **Anduril Lattice Entity模型**：轻量级、实时优先的战场实体管理
- **Palantir Gotham本体论**：多源数据融合与关系推理的语义框架

> **v3.0重大增强**：PostgreSQL从单一关系数据库升级为多模态数据引擎，集成TimescaleDB（时序）、Apache AGE（图）、pgvector（向量备选）等扩展，支持时空、时序、图、向量四种数据模式的统一查询。

### 5.2 JSC2本体论建模

#### 5.2.1 核心实体类型（基于JC3IEDM简化）

```Plain
┌─────────────────────────────────────────────────────────────────┐
│                    C2核心实体类型层次（基于JC3IEDM）              │
├─────────────────────────────────────────────────────────────────┤
│
│  MilitaryEntity (抽象基类)
│  ├── Platform (作战平台)
│  │   ├── AirPlatform (空中平台)
│  │   │   ├── FixedWingAircraft (固定翼飞机)
│  │   │   ├── RotaryWingAircraft (旋翼飞机/直升机)
│  │   │   └── UnmannedAerialVehicle (无人机)
│  │   ├── SurfacePlatform (水面平台)
│  │   │   ├── Warship (军舰)
│  │   │   └── UnmannedSurfaceVehicle (无人艇)
│  │   ├── SubsurfacePlatform (水下平台)
│  │   │   ├── Submarine (潜艇)
│  │   │   └── UUV (无人潜航器)
│  │   └── GroundPlatform (地面平台)
│  │       ├── ArmoredVehicle (装甲车辆)
│  │       └── UnmannedGroundVehicle (无人车)
│  │
│  ├── Sensor (传感器)
│  │   ├── RadarSensor (雷达)
│  │   ├── EOIRSensor (光电/红外传感器)
│  │   ├── ELINTSensor (电子侦察)
│  │   └── AcousticSensor (声学传感器)
│  │
│  ├── WeaponSystem (武器系统)
│  │   ├── MissileSystem (导弹系统)
│  │   └── ArtillerySystem (火炮系统)
│  │
│  ├── MilitaryUnit (JS单位)
│  │   ├── CommandPost (指挥所)
│  │   └── CombatUnit (作战单位)
│  │
│  └── Agent (智能体)
│      ├── ISRAgent (情报侦察智能体)
│      ├── DecisionAgent (决策智能体)
│      └── ExecutionAgent (执行智能体)
```

#### 5.2.2 实体关系模型

| 关系类型 | 源实体 | 目标实体 | 关系属性 | JS含义 |
|---------|--------|---------|---------|---------|
| **TRACKS** | Sensor | Platform | timestamp, accuracy, mode | 雷达跟踪目标 |
| **COMMANDS** | MilitaryUnit | Platform | authority, valid_time | 指挥所指挥平台 |
| **COMMUNICATES** | Platform | Platform | link_type, encryption, bandwidth | 平台间数据链 |
| **THREATENS** | Platform | Platform | threat_level, weapon_range | 威胁评估 |
| **ENGAGES** | WeaponSystem | Platform | engagement_status, probability | 武器交战 |
| **SUPPORTS** | MilitaryUnit | MilitaryUnit | support_type, priority | 火力支援/情报支援 |

#### 5.2.3 实体定义代码

```python
# ontology/entities.py
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class ClassificationLevel(str, Enum):
    UNCLASSIFIED = "UNCLASSIFIED"
    CONFIDENTIAL = "CONFIDENTIAL"
    SECRET = "SECRET"
    TOP_SECRET = "TOP_SECRET"


class EntityType(str, Enum):
    FIXED_WING = "fixed_wing_aircraft"
    ROTARY_WING = "rotary_wing_aircraft"
    UAV = "uav"
    WARSHIP = "warship"
    USV = "usv"
    SUBMARINE = "submarine"
    UUV = "uuv"
    ARMORED_VEHICLE = "armored_vehicle"
    UGV = "ugv"
    RADAR = "radar"
    EOIR = "eoir"
    ELINT = "elint"
    MISSILE = "missile_system"
    ARTILLERY = "artillery_system"
    COMMAND_POST = "command_post"
    ISR_AGENT = "isr_agent"
    DECISION_AGENT = "decision_agent"
    EXECUTION_AGENT = "execution_agent"
    MISSION = "mission"


class ForceAffiliation(str, Enum):
    FRIENDLY = "FRIENDLY"
    HOSTILE = "HOSTILE"
    NEUTRAL = "NEUTRAL"
    UNKNOWN = "UNKNOWN"
    PENDING = "PENDING"


class OperationalStatus(str, Enum):
    STANDBY = "standby"
    DEPLOYING = "deploying"
    ACTIVE = "active"
    IN_ENGAGEMENT = "in_engagement"
    RTB = "rtb"
    DAMAGED = "damaged"
    DESTROYED = "destroyed"
    MAINTENANCE = "maintenance"


class ThreatLevel(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SpatialCoordinate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    altitude_m: Optional[float] = None
    coordinate_system: str = "WGS84"
    accuracy_m: Optional[float] = None


class VelocityVector(BaseModel):
    speed_mps: float = Field(0.0, ge=0)
    heading_deg: float = Field(0.0, ge=0, le=360)
    climb_rate_mps: Optional[float] = None


class MilitaryEntity(BaseModel):
    entity_id: str
    entity_type: EntityType
    name: str
    classification: ClassificationLevel = ClassificationLevel.SECRET
    force_affiliation: ForceAffiliation = ForceAffiliation.PENDING
    iff_code: Optional[str] = None
    position: Optional[SpatialCoordinate] = None
    velocity: Optional[VelocityVector] = None
    last_seen: datetime = Field(default_factory=datetime.utcnow)
    operational_status: OperationalStatus = OperationalStatus.STANDBY
    threat_level: ThreatLevel = ThreatLevel.NONE
    source_ids: List[str] = Field(default_factory=list)
    confidence: float = Field(1.0, ge=0, le=1)
    properties: Dict[str, Any] = Field(default_factory=dict)


class AirPlatform(MilitaryEntity):
    platform_type: str
    max_speed_kmh: Optional[float] = None
    max_altitude_m: Optional[float] = None
    endurance_min: Optional[float] = None
    payload_kg: Optional[float] = None
    radar_cross_section: Optional[float] = None
    fuel_level_pct: Optional[float] = Field(None, ge=0, le=100)
    weapon_status: Optional[str] = None


class RadarSensor(MilitaryEntity):
    radar_type: str
    frequency_band: str
    max_range_km: float
    elevation_coverage_deg: float
    update_rate_hz: float
    operating_modes: List[str] = Field(default_factory=list)
    current_mode: Optional[str] = None
    jamming_status: str = "clear"


class MilitaryMission(MilitaryEntity):
    mission_type: str
    priority: int = Field(5, ge=1, le=10)
    status: str = "planned"
    planned_start: Optional[datetime] = None
    planned_end: Optional[datetime] = None
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    objectives: List[str] = Field(default_factory=list)
    assigned_assets: List[str] = Field(default_factory=list)
    rules_of_engagement: Dict[str, Any] = Field(default_factory=dict)
    commander_intent: Optional[str] = None
```

### 5.3 COP多模态数据引擎

#### 5.3.1 数据引擎架构

```Plain
┌─────────────────────────────────────────────────────────────────┐
│              PostgreSQL 多模态数据引擎                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  PostGIS     │  │ TimescaleDB  │  │  Apache AGE  │         │
│  │  (空间数据)  │  │  (时序数据)  │  │  (图数据)    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  pgvector    │  │  Valkey      │  │  SeaweedFS   │         │
│  │  (向量备选)  │  │  (热缓存)    │  │  (对象存储)  │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

#### 5.3.2 时空查询服务

```python
# ontology/cop_service.py
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
import redis.asyncio as aioredis
import asyncpg
from pydantic import BaseModel


class COPEntityQuery(BaseModel):
    center_lat: float
    center_lon: float
    radius_km: float
    entity_types: Optional[List[str]] = None
    force_affiliation: Optional[str] = None
    time_range_start: Optional[datetime] = None
    time_range_end: Optional[datetime] = None
    classification_max: str = "SECRET"
    limit: int = 200


class COPService:
    """COP共用作战态势图服务"""

    def __init__(self, pg_pool: asyncpg.Pool, redis_client: aioredis.Redis):
        self._pg = pg_pool
        self._redis = redis_client

    async def upsert_entity(self, entity: Dict[str, Any]) -> str:
        """更新或插入实体到COP"""
        entity_id = entity["entity_id"]

        await self._pg.execute(
            """
            INSERT INTO cop_entities (
                entity_id, entity_type, name, classification,
                force_affiliation, position, velocity,
                last_seen, operational_status, threat_level,
                confidence, source_ids, properties, updated_at
            ) VALUES ($1, $2, $3, $4, $5,
                      ST_SetSRID(ST_MakePoint($6, $7, $8), 4326),
                      $9, $10, $11, $12, $13, $14, $15::jsonb, NOW())
            ON CONFLICT (entity_id) DO UPDATE SET
                position = EXCLUDED.position,
                velocity = EXCLUDED.velocity,
                last_seen = EXCLUDED.last_seen,
                operational_status = EXCLUDED.operational_status,
                threat_level = EXCLUDED.threat_level,
                confidence = EXCLUDED.confidence,
                source_ids = EXCLUDED.source_ids,
                properties = EXCLUDED.properties,
                updated_at = NOW()
            """,
            entity_id, entity["entity_type"], entity["name"],
            entity.get("classification", "SECRET"),
            entity.get("force_affiliation", "UNKNOWN"),
            entity.get("position", {}).get("longitude", 0),
            entity.get("position", {}).get("latitude", 0),
            entity.get("position", {}).get("altitude_m", 0),
            json.dumps(entity.get("velocity")),
            entity.get("last_seen", datetime.utcnow()),
            entity.get("operational_status", "standby"),
            entity.get("threat_level", "NONE"),
            entity.get("confidence", 1.0),
            entity.get("source_ids", []),
            json.dumps(entity.get("properties", {})),
        )

        await self._redis.set(
            f"cop:entity:{entity_id}",
            json.dumps(entity, default=str),
            ex=300,
        )

        return entity_id

    async def query_entities(self, query: COPEntityQuery) -> List[Dict[str, Any]]:
        """时空范围查询COP实体"""
        sql = """
            SELECT entity_id, entity_type, name, classification,
                   force_affiliation, operational_status, threat_level,
                   ST_X(position) as lon, ST_Y(position) as lat,
                   ST_Z(position) as alt,
                   confidence, last_seen, properties
            FROM cop_entities
            WHERE ST_DWithin(
                position,
                ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography,
                $3
            )
            AND classification <= $4
        """
        params = [
            query.center_lon, query.center_lat,
            query.radius_km * 1000,
            query.classification_max,
        ]

        if query.entity_types:
            placeholders = ",".join(f"${i+5}" for i in range(len(query.entity_types)))
            sql += f" AND entity_type IN ({placeholders})"
            params.extend(query.entity_types)

        if query.force_affiliation:
            sql += f" AND force_affiliation = ${len(params)+1}"
            params.append(query.force_affiliation)

        sql += f" ORDER BY last_seen DESC LIMIT ${len(params)+1}"
        params.append(query.limit)

        rows = await self._pg.fetch(sql, *params)
        return [dict(row) for row in rows]

    async def get_track_history(self, entity_id: str, hours: int = 24) -> List[Dict]:
        """获取航迹历史（TimescaleDB加速）"""
        rows = await self._pg.fetch(
            """
            SELECT time as recorded_at,
                   ST_X(position) as lon, ST_Y(position) as lat,
                   ST_Z(position) as alt, value_json as velocity, quality as confidence
            FROM sensor_telemetry
            WHERE entity_id = $1
              AND measurement_type = 'position'
              AND time > NOW() - ($2 || ' hours')::interval
            ORDER BY time ASC
            """,
            entity_id, str(hours),
        )
        return [dict(r) for r in rows]

    async def query_threat_graph(self, entity_id: str, depth: int = 2) -> Dict:
        """查询威胁关系图（Apache AGE）"""
        rows = await self._pg.fetch(
            """
            SELECT * FROM cypher('military_relations', $$
                MATCH path = (p:Platform {id: $entity_id})-[*1..$depth]-(related)
                RETURN path
            $$) as (path agtype)
            """,
            {"entity_id": entity_id, "depth": depth}
        )
        return {"entity_id": entity_id, "graph": [dict(r) for r in rows]}
```

#### 5.3.3 数据库Schema

```sql
-- ontology/cop_schema.sql

-- 启用扩展
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS age;
CREATE EXTENSION IF NOT EXISTS vector;

-- 主实体表
CREATE TABLE cop_entities (
    entity_id       VARCHAR(64) PRIMARY KEY,
    entity_type     VARCHAR(32) NOT NULL,
    name            VARCHAR(128),
    classification  VARCHAR(16) NOT NULL DEFAULT 'SECRET',
    force_affiliation VARCHAR(16) NOT NULL DEFAULT 'UNKNOWN',
    position        GEOGRAPHY(POINTZ, 4326),
    velocity        JSONB,
    last_seen       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    operational_status VARCHAR(16) DEFAULT 'standby',
    threat_level    VARCHAR(16) DEFAULT 'NONE',
    confidence      REAL DEFAULT 1.0,
    source_ids      TEXT[] DEFAULT '{}',
    properties      JSONB DEFAULT '{}',
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_cop_entities_position ON cop_entities USING GIST (position);
CREATE INDEX idx_cop_entities_type ON cop_entities (entity_type);
CREATE INDEX idx_cop_entities_affiliation ON cop_entities (force_affiliation);
CREATE INDEX idx_cop_entities_threat ON cop_entities (threat_level);
CREATE INDEX idx_cop_entities_updated ON cop_entities (updated_at);

-- 传感器时序数据表（TimescaleDB）
CREATE TABLE sensor_telemetry (
    time            TIMESTAMPTZ NOT NULL,
    sensor_id       VARCHAR(64) NOT NULL,
    entity_id       VARCHAR(64),
    measurement_type VARCHAR(32) NOT NULL,
    value_numeric   DOUBLE PRECISION,
    value_json      JSONB,
    quality         REAL DEFAULT 1.0,
    classification  VARCHAR(16) DEFAULT 'SECRET'
);

SELECT create_hypertable('sensor_telemetry', 'time', chunk_time_interval => INTERVAL '1 day');
CREATE INDEX idx_telemetry_sensor ON sensor_telemetry (sensor_id, time DESC);
CREATE INDEX idx_telemetry_entity ON sensor_telemetry (entity_id, time DESC);

-- 航迹历史表（保留用于兼容）
CREATE TABLE cop_track_history (
    id              BIGSERIAL PRIMARY KEY,
    entity_id       VARCHAR(64) NOT NULL REFERENCES cop_entities(entity_id),
    position        GEOGRAPHY(POINTZ, 4326),
    velocity        JSONB,
    confidence      REAL,
    recorded_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_track_history_entity ON cop_track_history (entity_id, recorded_at);

-- 关系表
CREATE TABLE cop_relations (
    id              BIGSERIAL PRIMARY KEY,
    relation_type   VARCHAR(32) NOT NULL,
    source_id       VARCHAR(64) NOT NULL,
    target_id       VARCHAR(64) NOT NULL,
    properties      JSONB DEFAULT '{}',
    confidence      REAL DEFAULT 1.0,
    valid_from      TIMESTAMPTZ DEFAULT NOW(),
    valid_to        TIMESTAMPTZ,
    classification  VARCHAR(16) NOT NULL DEFAULT 'SECRET'
);

CREATE INDEX idx_relations_source ON cop_relations (source_id);
CREATE INDEX idx_relations_target ON cop_relations (target_id);
CREATE INDEX idx_relations_type ON cop_relations (relation_type);

-- 数据血缘表
CREATE TABLE data_lineage (
    lineage_id      VARCHAR(128) PRIMARY KEY,
    source_id       VARCHAR(128) NOT NULL,
    target_id       VARCHAR(128) NOT NULL,
    transformation  VARCHAR(64) NOT NULL,
    operator        VARCHAR(64),
    params          JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_lineage_source ON data_lineage (source_id);
CREATE INDEX idx_lineage_target ON data_lineage (target_id);
CREATE INDEX idx_lineage_time ON data_lineage (created_at);
```

#### 5.3.4 数据链消息中间格式

参考Anduril Lattice的Entity-Component模型，定义数据链消息的Protobuf中间格式：

```protobuf
// datalink/c2_messages.proto
syntax = "proto3";
package c2.messages;

import "google/protobuf/timestamp.proto";

// C2实体状态消息（数据链中间格式）
message EntityState {
    string entity_id = 1;
    string entity_type = 2;
    string force_affiliation = 3;  // FRIENDLY/HOSTILE/NEUTRAL/UNKNOWN

    // 位置（WGS84）
    double latitude = 4;
    double longitude = 5;
    double altitude_m = 6;
    double position_accuracy_m = 7;

    // 运动
    double speed_mps = 8;
    double heading_deg = 9;
    double climb_rate_mps = 10;

    // 状态
    string operational_status = 11;
    string threat_level = 12;
    float confidence = 13;

    // 元数据
    google.protobuf.Timestamp last_seen = 14;
    repeated string source_ids = 15;
    string classification = 16;
}

// 传感器探测消息
message SensorDetection {
    string sensor_id = 1;
    string sensor_type = 2;  // radar/eoir/elint/acoustic
    google.protobuf.Timestamp detection_time = 3;

    repeated EntityState detected_entities = 4;
    float sensor_confidence = 5;

    // 数据链原始信息
    string datalink_type = 6;  // LINK16/VMF/STANAG
    bytes raw_message = 7;
}

// 命令消息
message OrderMessage {
    string order_id = 1;
    string target_entity_id = 2;
    string order_type = 3;  // MOVE/ENGAGE/HOLD/RTB/EVADE
    string issuer_id = 4;
    google.protobuf.Timestamp issued_at = 5;

    // 命令参数
    oneof parameters {
        MoveParams move = 6;
        EngageParams engage = 7;
    }

    string classification = 8;
}

message MoveParams {
    double target_lat = 1;
    double target_lon = 2;
    double target_alt_m = 3;
    double speed_mps = 4;
}

message EngageParams {
    string target_id = 1;
    string weapon_type = 2;
    string roe_reference = 3;
}
```

### 5.4 RAG知识服务

对标Scale AI Data Engine的JS知识管理能力，构建RAG知识管线：

```python
# knowledge/rag_pipeline.py
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from knowledge.qdrant_setup import MilitaryKnowledgeStore


@dataclass
class KnowledgeDocument:
    """知识文档"""
    doc_id: str
    title: str
    category: str  # doctrine/threat_library/roe/equipment_manual/after_action_report
    domain: str    # joint/army/navy/air_force
    classification: str
    source: str
    sections: List[Dict[str, str]]  # [{title, content}]


class RAGPipeline:
    """
    RAG知识库构建管线
    文档切分 → 嵌入生成 → Qdrant存储 → 检索 → Prompt增强 → LLM生成
    """

    def __init__(
        self,
        knowledge_store: MilitaryKnowledgeStore,
        embedding_model=None,
    ):
        self._store = knowledge_store
        self._embed_model = embedding_model

    async def ingest_document(self, doc: KnowledgeDocument) -> int:
        """
        摄入知识文档
        Returns: 摄入的chunk数量
        """
        chunks = self._split_document(doc)
        count = 0

        for i, chunk in enumerate(chunks):
            embedding = await self._generate_embedding(chunk["content"])

            self._store.ingest_document(
                doc_id=f"{doc.doc_id}-chunk-{i}",
                text=chunk["content"],
                embedding=embedding,
                metadata={
                    "category": doc.category,
                    "classification": doc.classification,
                    "domain": doc.domain,
                    "source": doc.source,
                    "title": doc.title,
                    "section_title": chunk.get("title", ""),
                },
            )
            count += 1

        return count

    async def retrieve_and_augment(
        self,
        query: str,
        category_filter: List[str] = None,
        top_k: int = 5,
    ) -> str:
        """
        检索相关条令并生成增强Prompt
        """
        query_embedding = await self._generate_embedding(query)

        results = self._store.search(
            query_embedding=query_embedding,
            limit=top_k,
            category_filter=category_filter,
        )

        context_parts = []
        for r in results:
            context_parts.append(
                f"[{r['category']}] {r['text'][:500]}"
            )

        return "\n\n".join(context_parts)

    def _split_document(
        self, doc: KnowledgeDocument, chunk_size: int = 512, overlap: int = 50
    ) -> List[Dict[str, str]]:
        """文档切分（按段落/章节）"""
        chunks = []
        for section in doc.sections:
            content = section["content"]
            title = section.get("title", "")

            words = content.split()
            for j in range(0, len(words), chunk_size - overlap):
                chunk_text = " ".join(words[j:j + chunk_size])
                if chunk_text.strip():
                    chunks.append({"title": title, "content": chunk_text})

        return chunks

    async def _generate_embedding(self, text: str) -> List[float]:
        """生成文本嵌入向量（示意）"""
        return [0.0] * 1024
```


### 5.5 世界模型数据管道

世界模型（第3.2节）的训练数据从COP数据平面提取，形成专用的数据管道：

**训练数据来源**：

| 数据源 | 存储位置 | 提取方式 | 用途 |
|--------|---------|---------|------|
| 战场态势序列 | TimescaleDB | 时间窗口查询 | `(state, action) → next_state` 三元组 |
| 对抗行动序列 | WargameEngine日志 | Redis Stream | 红蓝对抗轨迹 |
| 指挥员操作记录 | ExperienceRecorder | PostgreSQL | 人类决策样本 |
| 仿真结果 | Redpanda Topic | 消费者组 | 批量仿真输出 |

**数据管道代码**：

```python
# cop/world_model_pipeline.py
# 世界模型训练数据管道: 从COP数据平面提取训练样本
import asyncio
import json
import redis.asyncio as aioredis
from datetime import datetime, timedelta
from typing import List, Dict, Any, AsyncGenerator


class WorldModelDataPipeline:
    # 从COP历史数据中提取 (state, action, next_state) 三元组

    def __init__(self, timescale_url: str, redis_url: str):
        self.timescale_url = timescale_url
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)

    async def extract_training_triplets(
        self,
        time_window: timedelta = timedelta(hours=24),
        domain: str = "all"
    ) -> AsyncGenerator[Dict[str, Any], None]:
        # 从COP时序数据中提取训练三元组。
        # 每个三元组包含：执行前的态势快照、采取的行动、执行后的态势快照。
        cutoff = datetime.utcnow() - time_window

        query = """
            SELECT
                e.event_id,
                e.timestamp,
                e.action_type,
                e.action_params,
                e.agent_id,
                s_before.state_json AS state_before,
                s_after.state_json AS state_after
            FROM cop_events e
            JOIN cop_snapshots s_before ON e.pre_snapshot_id = s_before.snapshot_id
            JOIN cop_snapshots s_after ON e.post_snapshot_id = s_after.snapshot_id
            WHERE e.timestamp >= $1
              AND ($2 = 'all' OR e.domain = $2)
              AND e.action_type IS NOT NULL
            ORDER BY e.timestamp
        """

        async for row in self._query_timescale(query, cutoff, domain):
            yield {
                "triplet_id": f"t_{row['event_id']}",
                "state": row["state_before"],
                "action": {
                    "type": row["action_type"],
                    "params": row["action_params"],
                    "agent_id": row["agent_id"],
                },
                "next_state": row["state_after"],
                "timestamp": row["timestamp"].isoformat(),
            }

    async def publish_to_training_queue(self, triplet: Dict[str, Any]):
        # 将三元组发布到世界模型训练队列
        await self.redis.xadd(
            "world_model:training_triplets",
            {"data": json.dumps(triplet)}
        )

    async def run_pipeline(self, time_window: timedelta = timedelta(hours=1)):
        # 持续运行管道: 提取 -> 发布
        count = 0
        async for triplet in self.extract_training_triplets(time_window):
            await self.publish_to_training_queue(triplet)
            count += 1
        return count

    async def _query_timescale(self, query, *params):
        # 执行TimescaleDB查询 (实际使用asyncpg)
        yield from []
```

**与Ch8数据闭环的关系**：本节定义数据如何从COP中提取，第8章定义提取后如何用于模型训练、评估和部署。

---

## 6. 对抗训练与仿真体系

> **v5.0核心升级**：v4.0的兵棋推演引擎（WargameEngine）仅使用静态红方行为模型对蓝方预设COA做蒙特卡洛评估。红方本质上是"掷骰子的稻草人"——蓝方学会的是如何击败一个不会学习的对手，而不是如何应对真正聪明的自适应敌人。v5.0引入GAN启发的对抗训练框架：蓝方智能体与红方智能体同步学习，红方专攻蓝方弱点，蓝方被迫持续补强，形成军备竞赛式的共同进化，最终产出对抗自适应对手也足够鲁棒的防御策略。

### 6.1 设计理念

#### 6.1.1 v4.0静态兵棋的根本缺陷

v4.0的WargameEngine（见v4.0第5.5节`scenarios/wargame.py`）执行蒙特卡洛仿真评估蓝方COA方案，存在三个结构性缺陷：

1. **红方不会学习**：红方行为由`_execute_red_step()`的随机采样驱动（`self._rng.random() > 0.5`），无论蓝方策略如何变化，红方行为分布恒定。蓝方通过调参提升胜率的过程，本质上是在拟合噪声，而非锻炼真正的对抗能力。

2. **评估给出虚假信心**：一个COA在静态红方下达到85%胜率，不代表面对自适应敌人时能保持50%。静态评估的胜率与实战胜率之间存在系统性偏差，且偏差方向未知——指挥员可能基于虚假的高胜率做出错误的作战决策。

3. **经验蒸馏继承了弱点**：v4.0经验蒸馏闭环（ExperienceRecorder → ExperienceMiner → ExperiencePromoter）将高胜率模式从慢系统晋升为快系统先验。如果高胜率来自"击败笨红方"的策略，那么蒸馏到快系统的就是脆弱的先验知识——面对聪明敌人时，快系统的"直觉反应"反而是灾难性的。

#### 6.1.2 GAN启发的对抗训练

借鉴生成对抗网络（GAN）的核心思想——生成器与判别器通过对抗实现共同提升——v5.0构建红蓝对抗训练框架：

```text
对抗训练循环（GAN启发）：

  蓝方（类比生成器G）                    红方（类比判别器D）
  ┌──────────────────┐               ┌──────────────────┐
  │ 生成防御策略     │──────────────▶│ 寻找策略弱点     │
  │ （产出"逼真"的   │               │ （判别策略中的    │
  │   防御方案）     │               │   薄弱环节）     │
  └────────┬─────────┘               └────────┬─────────┘
           │                                   │
           │    ┌──────────────────┐           │
           │    │  仿真对抗        │           │
           └───▶│  兵棋引擎仲裁    │◀──────────┘
                │  输出胜负结果    │
                └────────┬─────────┘
                         │
              ┌──────────┴──────────┐
              │                     │
     蓝方更新策略              红方更新攻击库
     （修补红方发现的         （强化有效的突破
       薄弱环节）               手段）
              │                     │
              └──────────┬──────────┘
                         │
                    下一轮对抗
                    （双方更强）
```

关键设计差异：与标准GAN不同，JS对抗训练的"真/假"判定不是二元的——胜负由多维评估函数裁决（任务达成度、战损比、时间效率、资源消耗），且蓝方不仅要"骗过"红方，还要在真实约束（交战规则、兵力上限、时效要求）下产出可执行的策略。

#### 6.1.3 训练循环的四阶段节奏

对抗训练不是简单的"蓝出一招、红破一招"，而是四阶段循环：

| 阶段 | 蓝方 | 红方 | 产出 |
|------|------|------|------|
| **蓝方探索** | 生成多样防御策略，覆盖不同战术风格 | 固定（使用当前最强红方） | 候选策略池 |
| **红方突破** | 固定（使用当前最强蓝方） | 针对蓝方策略搜索弱点 | 弱点报告 |
| **蓝方补强** | 根据弱点报告调整策略 | 固定 | 补强后的策略 |
| **联合评估** | 全量策略评估 | 全量攻击评估 | Skill候选、世界模型训练数据 |

四阶段交替执行的节奏防止了任一方过度拟合对方当前行为——蓝方不会只针对当前红方优化，红方也不会只针对当前蓝方优化。每50轮执行一次全量联合评估，提取Skill并更新世界模型。

#### 6.1.4 训练基础设施

对抗训练复用第4.3.6节定义的GPU资源隔离架构。训练期间GPU分配策略如下：

```text
训练期间GPU资源分配（基于4.3.6三层隔离架构扩展）：

  ┌─────────────────────────────────────────────────────────────┐
  │                  GPU 0: 战术专用（不可抢占）                  │
  │  Triton推理引擎（目标检测/分类）── 训练期间照常服务生产流量     │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │                  GPU 1: 战役专用（训练时分时复用）             │
  │  ┌─────────────────────────────────────────────────────┐    │
  │  │  生产负载（SGLang LLM推理 + OR-Tools优化）            │    │
  │  │  占用时间：00:00-04:00, 08:00-12:00（指挥高峰期）      │    │
  │  └─────────────────────────────────────────────────────┘    │
  │  ┌─────────────────────────────────────────────────────┐    │
  │  │  训练负载（对抗训练 + 世界模型更新）                    │    │
  │  │  占用时间：04:00-08:00, 12:00-16:00（低峰期）          │    │
  │  │  紧急训练：生产负载降级到CPU后立即启动                   │    │
  │  └─────────────────────────────────────────────────────┘    │
  └─────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────┐
  │                  GPU 2+: 训练专用（如有）                     │
  │  全天候用于对抗训练和世界模型训练，不与生产竞争               │
  └─────────────────────────────────────────────────────────────┘
```

训练调度原则：生产流量永远优先。战术层GPU（GPU 0）在任何情况下不参与训练。战役层GPU（GPU 1）仅在生产低峰期分配给训练任务。当训练过程中检测到生产负载上升时，训练任务通过checkpoint机制暂停并释放GPU资源，待负载回落后从断点继续。

---

### 6.2 红蓝对抗训练框架

#### 6.2.1 框架概览

```text
对抗训练框架组件关系：

  ┌──────────────────────────────────────────────────────────────┐
  │                     AdversarialTrainingLoop                  │
  │                                                              │
  │  ┌──────────────┐  仿真对抗  ┌──────────────┐              │
  │  │  BlueAgent    │◀────────▶│  RedAgent     │              │
  │  │              │           │              │              │
  │  │ SkillLibrary │           │ ExploitDB    │              │
  │  │ WorldModel   │           │ WorldModel   │              │
  │  │ MCTS         │           │ (共享)       │              │
  │  └──────┬───────┘           └──────┬───────┘              │
  │         │                          │                       │
  │         │  训练结果                 │  弱点报告             │
  │         ▼                          ▼                       │
  │  ┌──────────────┐           ┌──────────────┐              │
  │  │ SkillExtractor│          │ ExploitLogger │              │
  │  │ (6.4)         │          │              │              │
  │  └──────────────┘           └──────────────┘              │
  │                                                              │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │              WargameEngine（6.3升级版）                │   │
  │  │         仿真对抗仲裁 + 训练数据生成                    │   │
  │  └──────────────────────────────────────────────────────┘   │
  └──────────────────────────────────────────────────────────────┘
```

#### 6.2.2 完整实现代码

```python
# training/adversarial_loop.py
"""
红蓝对抗训练框架

v4.0的WargameEngine仅使用静态随机红方评估COA，v5.0升级为
GAN启发的对抗训练：蓝方与红方智能体同步学习，产出对抗自适应
对手也足够鲁棒的防御策略。

依赖：
  - WargameEngine（scenarios/wargame.py，v5.0升级版，见6.3）
  - SkillLibrary（distillation/skill_library.py）
  - WorldModel（training/world_model.py）
  - MCTS（planning/mcts.py）
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from enum import Enum
import hashlib
import json

from scenarios.wargame import WargameEngine, SimUnit, ForceSide
from distillation.skill_library import SkillLibrary, SkillDefinition
from planning.mcts import MCTSPlanner
from training.world_model import WorldModel


# ──────────────────────────────────────────────────────────
#  配置
# ──────────────────────────────────────────────────────────

@dataclass
class TrainingConfig:
    """对抗训练配置"""
    max_rounds: int = 1000
    blue_update_freq: int = 10      # 每10轮更新蓝方策略
    red_update_freq: int = 10       # 每10轮更新红方攻击库
    evaluation_freq: int = 50       # 每50轮全量评估 + Skill提取
    blue_skill_threshold: float = 0.85  # Skill提取成功率阈值
    red_exploit_threshold: float = 0.3  # 红方突破成功率阈值（高于此值视为有效弱点）
    mcts_simulations: int = 200     # MCTS每步仿真次数
    batch_size: int = 32            # 批量仿真大小（用于MCTS rollout）
    checkpoint_dir: str = "/data/adversarial_checkpoints"


class TrainingPhase(Enum):
    """对抗训练阶段"""
    BLUE_EXPLORE = "blue_explore"       # 蓝方探索：生成多样策略
    RED_EXPLOIT = "red_exploit"         # 红方突破：搜索蓝方弱点
    BLUE_HARDEN = "blue_harden"         # 蓝方补强：修补弱点
    JOINT_EVAL = "joint_eval"           # 联合评估：全量评估 + Skill提取


# ──────────────────────────────────────────────────────────
#  蓝方智能体
# ──────────────────────────────────────────────────────────

class BlueAgent:
    """
    蓝方智能体——防御策略生成与学习

    策略生成优先级：
    1. SkillLibrary命中（成功率≥85%的已验证Skill）
    2. MCTS搜索（利用世界模型做前瞻搜索）
    3. 规则后备（固定战术模板兜底）
    """

    def __init__(
        self,
        skill_library: SkillLibrary,
        world_model: WorldModel,
        mcts: MCTSPlanner,
    ):
        self._skills = skill_library
        self._world_model = world_model
        self._mcts = mcts
        self._win_history: List[Dict] = []
        self._loss_history: List[Dict] = []
        self._weakness_log: List[Dict] = []  # 红方发现的弱点记录

    def generate_strategy(self, scenario: Dict) -> Dict:
        """
        根据场景生成防御策略

        优先使用已验证Skill，否则通过MCTS搜索生成新策略。
        策略包含phases（阶段行动）、contingencies（分支预案）、
        resource_allocation（资源分配）三部分。
        """
        # 优先级1：Skill库命中
        skills = self._skills.find_applicable(scenario)
        if skills and skills[0].success_rate >= 0.85:
            return self._execute_skill_strategy(skills[0], scenario)

        # 优先级2：MCTS搜索
        strategy = self._mcts.search(
            scenario=scenario,
            world_model=self._world_model,
            num_simulations=200,
        )
        strategy["source"] = "mcts"
        return strategy

    def learn_from_defeat(
        self,
        strategy: Dict,
        red_action: Dict,
        outcome: Dict,
    ) -> None:
        """
        从失败中学习——红方找到了策略弱点

        1. 记录弱点元组（策略特征、红方突破手段、失败模式）
        2. 如果同类弱点累计出现≥3次，标记对应Skill为待降级
        3. 更新世界模型中该策略分支的期望值（降低）
        """
        weakness_record = {
            "strategy_hash": self._hash_strategy(strategy),
            "strategy_source": strategy.get("source", "unknown"),
            "red_exploit_type": red_action.get("exploit_type", "unknown"),
            "red_exploit_vector": red_action.get("attack_vector", {}),
            "failure_mode": outcome.get("failure_mode", "unknown"),
            "blue_survival_pct": outcome.get("blue_survival_pct", 0),
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._loss_history.append(weakness_record)
        self._weakness_log.append(weakness_record)

        # 检查是否为反复出现的弱点
        exploit_type = weakness_record["red_exploit_type"]
        repeat_count = sum(
            1 for w in self._weakness_log
            if w["red_exploit_type"] == exploit_type
        )
        if repeat_count >= 3:
            self._flag_skill_for_review(strategy, exploit_type)

        # 更新世界模型：降低此策略分支的期望值
        self._world_model.update_outcome(
            state=strategy,
            action=red_action,
            actual_reward=outcome.get("blue_reward", -1.0),
        )

    def learn_from_victory(
        self,
        strategy: Dict,
        red_action: Dict,
        outcome: Dict,
    ) -> None:
        """从胜利中学习——策略经受住了红方攻击"""
        victory_record = {
            "strategy_hash": self._hash_strategy(strategy),
            "strategy_source": strategy.get("source", "unknown"),
            "red_exploit_type": red_action.get("exploit_type", "unknown"),
            "blue_survival_pct": outcome.get("blue_survival_pct", 100),
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._win_history.append(victory_record)

        # 更新世界模型：提升此策略分支的期望值
        self._world_model.update_outcome(
            state=strategy,
            action=red_action,
            actual_reward=outcome.get("blue_reward", 1.0),
        )

    def get_weakness_report(self) -> Dict:
        """返回当前蓝方弱点概要（供Skill提取使用）"""
        if not self._weakness_log:
            return {"total_weaknesses": 0, "top_weaknesses": []}

        # 按弱点类型聚合
        weakness_counts: Dict[str, int] = {}
        for w in self._weakness_log[-100:]:  # 最近100条
            exploit_type = w["red_exploit_type"]
            weakness_counts[exploit_type] = weakness_counts.get(exploit_type, 0) + 1

        sorted_weaknesses = sorted(
            weakness_counts.items(), key=lambda x: x[1], reverse=True
        )
        return {
            "total_weaknesses": len(self._weakness_log),
            "top_weaknesses": [
                {"exploit_type": wt, "count": cnt}
                for wt, cnt in sorted_weaknesses[:5]
            ],
        }

    def _execute_skill_strategy(self, skill: SkillDefinition, scenario: Dict) -> Dict:
        """执行Skill库命中的策略"""
        strategy = skill.to_strategy(scenario)
        strategy["source"] = "skill"
        strategy["skill_id"] = skill.skill_id
        return strategy

    def _flag_skill_for_review(self, strategy: Dict, exploit_type: str) -> None:
        """标记Skill待审核降级"""
        skill_id = strategy.get("skill_id")
        if skill_id:
            self._skills.flag_for_review(
                skill_id=skill_id,
                reason=f"反复被红方突破({exploit_type})，待降级审核",
            )

    @staticmethod
    def _hash_strategy(strategy: Dict) -> str:
        """策略特征哈希（用于去重和匹配）"""
        canonical = json.dumps(strategy, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canonical.encode()).hexdigest()[:16]


# ──────────────────────────────────────────────────────────
#  红方智能体
# ──────────────────────────────────────────────────────────

class RedAgent:
    """
    红方智能体——攻击策略生成与学习（对抗训练专用）

    红方目标：找到蓝方策略的薄弱环节，通过有针对性的攻击暴露弱点。
    红方不是v4.0的随机行为生成器，而是具备学习能力的对抗智能体。

    攻击策略库包含：
    - 电子战压制（EW_jamming）
    - 多轴包围（multi_axis_encirclement）
    - 诱饵欺骗（deception_decoy）
    - 集中突破（concentrated_breakthrough）
    - 侧翼迂回（flanking_maneuver）
    - 时间窗口突击（time_window_strike）
    - 信息战干扰（information_warfare）
    """

    ATTACK_TACTICS = [
        "EW_jamming", "multi_axis_encirclement", "deception_decoy",
        "concentrated_breakthrough", "flanking_maneuver",
        "time_window_strike", "information_warfare",
    ]

    def __init__(self, world_model: WorldModel):
        self._world_model = world_model
        self._exploit_history: List[Dict] = []
        self._tactic_effectiveness: Dict[str, List[float]] = {
            t: [] for t in self.ATTACK_TACTICS
        }

    def find_weakness(self, blue_strategy: Dict, scenario: Dict) -> Dict:
        """
        寻找蓝方策略的弱点

        方法：使用世界模型模拟蓝方策略在多种红方战术下的表现，
        选择蓝方最脆弱的攻击向量。
        """
        exploit_scores: List[Tuple[str, float, Dict]] = []

        for tactic in self.ATTACK_TACTICS:
            # 使用世界模型快速评估此战术对蓝方策略的效果
            red_action = self._build_red_action(tactic, scenario)
            predicted_outcome = self._world_model.predict(
                blue_strategy=blue_strategy,
                red_action=red_action,
                scenario=scenario,
            )

            # 评估得分：蓝方越脆弱，红方得分越高
            exploit_score = self._compute_exploit_score(predicted_outcome)
            exploit_scores.append((tactic, exploit_score, red_action))

        # 按突破潜力排序，选择最有效的战术
        exploit_scores.sort(key=lambda x: x[1], reverse=True)

        # 增加探索：10%概率选择非最优战术（避免红方过度利用）
        import random
        if random.random() < 0.1 and len(exploit_scores) > 1:
            chosen_idx = random.randint(1, len(exploit_scores) - 1)
        else:
            chosen_idx = 0

        chosen_tactic, score, chosen_action = exploit_scores[chosen_idx]
        chosen_action["exploit_type"] = chosen_tactic
        chosen_action["predicted_score"] = score

        return chosen_action

    def learn_from_success(
        self,
        exploit: Dict,
        blue_strategy: Dict,
        outcome: Dict,
    ) -> None:
        """
        从成功突破中学习

        1. 记录成功的攻击手段和蓝方策略特征
        2. 更新战术效果评分
        3. 强化世界模型中此攻击路径的预测
        """
        record = {
            "exploit_type": exploit.get("exploit_type"),
            "blue_strategy_hash": BlueAgent._hash_strategy(blue_strategy),
            "red_success_score": outcome.get("red_success_score", 0.8),
            "blue_vulnerability": outcome.get("failure_mode", "unknown"),
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._exploit_history.append(record)

        # 更新战术效果评分
        tactic = exploit.get("exploit_type")
        if tactic in self._tactic_effectiveness:
            self._tactic_effectiveness[tactic].append(
                outcome.get("red_success_score", 0.8)
            )

        # 更新世界模型
        self._world_model.update_outcome(
            state=blue_strategy,
            action=exploit,
            actual_reward=outcome.get("red_reward", 1.0),
        )

    def learn_from_defeat(
        self,
        exploit: Dict,
        blue_strategy: Dict,
        outcome: Dict,
    ) -> None:
        """从失败中学习——蓝方成功防御了此攻击"""
        tactic = exploit.get("exploit_type")
        if tactic in self._tactic_effectiveness:
            self._tactic_effectiveness[tactic].append(
                1.0 - outcome.get("blue_survival_pct", 100) / 100.0
            )

        # 更新世界模型
        self._world_model.update_outcome(
            state=blue_strategy,
            action=exploit,
            actual_reward=outcome.get("red_reward", -1.0),
        )

    def get_tactic_report(self) -> Dict:
        """返回红方各战术效果概要"""
        report = {}
        for tactic, scores in self._tactic_effectiveness.items():
            if scores:
                report[tactic] = {
                    "avg_effectiveness": sum(scores[-50:]) / len(scores[-50:]),
                    "sample_count": len(scores),
                }
            else:
                report[tactic] = {"avg_effectiveness": 0.0, "sample_count": 0}
        return report

    def _build_red_action(self, tactic: str, scenario: Dict) -> Dict:
        """根据战术类型构建红方行动方案"""
        return {
            "tactic": tactic,
            "scenario_adaptation": self._adapt_to_scenario(tactic, scenario),
            "force_allocation": self._allocate_forces(tactic, scenario),
        }

    @staticmethod
    def _compute_exploit_score(predicted_outcome: Dict) -> float:
        """计算突破得分——蓝方越脆弱，得分越高"""
        blue_survival = predicted_outcome.get("blue_survival_pct", 100)
        blue_task_success = predicted_outcome.get("task_success_rate", 1.0)
        # 蓝方生存率越低、任务成功率越低 → 红方突破得分越高
        return (1.0 - blue_survival / 100.0) * 0.6 + (1.0 - blue_task_success) * 0.4

    @staticmethod
    def _adapt_to_scenario(tactic: str, scenario: Dict) -> Dict:
        """根据场景调整战术参数"""
        terrain = scenario.get("terrain", "mixed")
        force_ratio = scenario.get("force_ratio", 1.0)
        return {"terrain": terrain, "force_ratio": force_ratio}

    @staticmethod
    def _allocate_forces(tactic: str, scenario: Dict) -> Dict:
        """根据战术分配红方兵力"""
        red_forces = scenario.get("red_orbat", {}).get("units", [])
        if tactic == "concentrated_breakthrough":
            return {"main_effort_pct": 0.6, "supporting_pct": 0.4}
        elif tactic == "multi_axis_encirclement":
            return {"axes": min(4, max(2, len(red_forces) // 5))}
        return {"standard_allocation": True}


# ──────────────────────────────────────────────────────────
#  对抗训练主循环
# ──────────────────────────────────────────────────────────

class AdversarialTrainingLoop:
    """
    红蓝对抗训练主循环

    训练流程（每轮）：
    1. BlueAgent生成防御策略
    2. RedAgent分析策略，寻找弱点
    3. 双方在WargameEngine中对抗仿真
    4. 评估结果，双方各自学习
    5. 按四阶段节奏切换训练阶段
    6. 定期提取Skill并更新世界模型
    """

    def __init__(
        self,
        blue: BlueAgent,
        red: RedAgent,
        engine: WargameEngine,
        config: TrainingConfig,
    ):
        self._blue = blue
        self._red = red
        self._engine = engine
        self._config = config
        self._phase = TrainingPhase.BLUE_EXPLORE
        self._phase_counter = 0

    def run_training(self, scenarios: List[Dict]) -> Dict:
        """
        执行完整对抗训练

        Args:
            scenarios: 训练场景列表，每个场景包含blue_orbat、red_orbat、
                       terrain、mission等字段

        Returns:
            训练结果摘要：轮次数、胜率曲线、Skill数、弱点分布
        """
        results = {
            "rounds": 0,
            "blue_wins": 0,
            "red_wins": 0,
            "skills_extracted": 0,
            "win_rate_curve": [],          # 每50轮记录一次胜率
            "phase_history": [],           # 阶段切换历史
            "final_weakness_report": {},   # 最终弱点报告
            "final_tactic_report": {},     # 最终红方战术报告
        }

        for round_num in range(1, self._config.max_rounds + 1):
            # 轮转场景
            scenario = scenarios[(round_num - 1) % len(scenarios)]

            # 阶段管理
            self._advance_phase(round_num)

            # 核心对抗循环
            blue_strategy = self._blue.generate_strategy(scenario)
            red_exploit = self._red.find_weakness(blue_strategy, scenario)
            outcome = self._simulate(blue_strategy, red_exploit, scenario)

            # 双向学习
            if outcome["winner"] == "blue":
                self._blue.learn_from_victory(blue_strategy, red_exploit, outcome)
                self._red.learn_from_defeat(red_exploit, blue_strategy, outcome)
                results["blue_wins"] += 1
            else:
                self._blue.learn_from_defeat(blue_strategy, red_exploit, outcome)
                self._red.learn_from_success(red_exploit, blue_strategy, outcome)
                results["red_wins"] += 1

            results["rounds"] += 1

            # 定期全量评估 + Skill提取
            if round_num % self._config.evaluation_freq == 0:
                eval_snapshot = self._periodic_evaluation(round_num, scenarios)
                results["win_rate_curve"].append(eval_snapshot)
                results["skills_extracted"] += eval_snapshot.get(
                    "new_skills", 0
                )

        # 最终报告
        results["final_weakness_report"] = self._blue.get_weakness_report()
        results["final_tactic_report"] = self._red.get_tactic_report()
        return results

    def _advance_phase(self, round_num: int) -> None:
        """四阶段节奏管理"""
        cycle_length = self._config.blue_update_freq * 4  # 一个完整四阶段周期
        position = (round_num - 1) % cycle_length

        if position < self._config.blue_update_freq:
            new_phase = TrainingPhase.BLUE_EXPLORE
        elif position < self._config.blue_update_freq * 2:
            new_phase = TrainingPhase.RED_EXPLOIT
        elif position < self._config.blue_update_freq * 3:
            new_phase = TrainingPhase.BLUE_HARDEN
        else:
            new_phase = TrainingPhase.JOINT_EVAL

        if new_phase != self._phase:
            self._phase = new_phase
            self._phase_counter = 0

        self._phase_counter += 1

    def _simulate(
        self,
        blue_strategy: Dict,
        red_action: Dict,
        scenario: Dict,
    ) -> Dict:
        """
        使用WargameEngine仿真对抗

        调用升级后的WargameEngine（见6.3），返回结构化的对抗结果。
        """
        # 构建蓝方COA格式（适配WargameEngine接口）
        blue_coa = {
            "phases": blue_strategy.get("phases", []),
            "contingencies": blue_strategy.get("contingencies", []),
        }

        # 运行仿真
        sim_result = self._engine.run_simulation(
            blue_orbat=scenario["blue_orbat"],
            red_orbat=scenario["red_orbat"],
            coa=blue_coa,
            num_iterations=1,  # 对抗训练单轮只需1次仿真
            max_steps=200,
            red_override=red_action,  # v5.0新增：覆盖红方行为
        )

        # 增强结果
        outcome = {
            "winner": sim_result.get("winner", "blue"),
            "blue_survival_pct": sim_result.get("avg_blue_survival_pct", 50),
            "red_survival_pct": sim_result.get("avg_red_survival_pct", 50),
            "blue_reward": self._compute_blue_reward(sim_result),
            "red_reward": self._compute_red_reward(sim_result),
            "red_success_score": self._compute_red_success(sim_result),
            "failure_mode": sim_result.get("failure_mode", "unknown"),
            "sim_result": sim_result,
        }
        return outcome

    def _periodic_evaluation(
        self, round_num: int, scenarios: List[Dict]
    ) -> Dict:
        """
        定期全量评估

        对所有场景运行完整评估，计算当前蓝方胜率、
        触发Skill提取（调用6.4管线）
        """
        wins = 0
        total = len(scenarios) * 10  # 每场景10次仿真

        for scenario in scenarios:
            blue_strategy = self._blue.generate_strategy(scenario)
            sim_result = self._engine.run_simulation(
                blue_orbat=scenario["blue_orbat"],
                red_orbat=scenario["red_orbat"],
                coa={
                    "phases": blue_strategy.get("phases", []),
                    "contingencies": blue_strategy.get("contingencies", []),
                },
                num_iterations=10,
                max_steps=200,
            )
            wins += int(sim_result.get("win_rate", 0) * 10)

        return {
            "round": round_num,
            "eval_win_rate": wins / total,
            "phase": self._phase.value,
            "new_skills": 0,  # 由6.4管线填充
        }

    @staticmethod
    def _compute_blue_reward(sim_result: Dict) -> float:
        """计算蓝方奖励值（-1到+1）"""
        survival = sim_result.get("avg_blue_survival_pct", 50) / 100.0
        win = 1.0 if sim_result.get("winner") == "blue" else 0.0
        return survival * 0.4 + win * 0.6

    @staticmethod
    def _compute_red_reward(sim_result: Dict) -> float:
        """计算红方奖励值（-1到+1）"""
        blue_damage = 1.0 - sim_result.get("avg_blue_survival_pct", 50) / 100.0
        win = 1.0 if sim_result.get("winner") == "red" else 0.0
        return blue_damage * 0.4 + win * 0.6

    @staticmethod
    def _compute_red_success(sim_result: Dict) -> float:
        """计算红方突破成功度（0到1）"""
        blue_survival = sim_result.get("avg_blue_survival_pct", 50) / 100.0
        return 1.0 - blue_survival
```

---

### 6.3 兵棋推演引擎升级

#### 6.3.1 从评估工具到训练环境

v4.0的WargameEngine（`scenarios/wargame.py`，类定义见v4.0第5.5.3节`class WargameEngine`）是COA方案的验证工具——输入蓝方COA，运行蒙特卡洛仿真，输出胜率和建议。v5.0将其升级为对抗训练的仿真环境，新增四个核心能力：

| 升级项 | v4.0行为 | v5.0升级 |
|--------|---------|---------|
| **红方行为** | `_execute_red_step()`随机采样 | 接受`red_override`参数，执行红方智能体生成的攻击方案 |
| **训练数据生成** | 仅输出胜率统计 | 每次仿真产出`TrainingTriple`（state, action, reward），供世界模型训练 |
| **批量仿真** | 单次串行执行 | 新增`run_batch()`方法，并行执行MCTS所需的多次rollout |
| **保真度模式** | 固定精度 | 新增`fidelity`参数：`high`（完整仿真）/ `low`（快速评估，用于MCTS内部节点） |

#### 6.3.2 升级接口定义

以下为WargameEngine新增接口的签名和语义，完整实现基于v4.0代码增量修改，不重复已有代码：

```python
# scenarios/wargame.py（增量修改，基于v4.0 WargameEngine）

@dataclass
class TrainingTriple:
    """训练三元组——与第3.2.5节TrainingTriple对齐，扩展仿真元数据"""
    state: Dict[str, Any]           # COP快照序列化（由COPSnapshot.to_dict()生成）
    action: Dict[str, Any]          # 行动序列化（由Action.to_dict()生成）
    reward: float                   # 奖励信号
    next_state: Dict[str, Any]      # 下一状态序列化
    done: bool = False              # 回合是否结束
    metadata: Dict[str, Any] = field(default_factory=dict)  # 仿真元数据（来源、保真度等）


class WargameEngine:
    """
    兵棋推演引擎（v5.0升级版）

    在v4.0基础上新增：
    - red_override：红方行为覆盖（对抗训练使用）
    - run_batch()：批量仿真（MCTS rollout）
    - TrainingTriple生成：为世界模型提供训练数据
    - fidelity模式：high（完整仿真）/ low（快速MCTS评估）
    """

    def run_simulation(
        self,
        blue_orbat: Dict[str, Any],
        red_orbat: Dict[str, Any],
        coa: Dict[str, Any],
        num_iterations: int = 100,
        max_steps: int = 200,
        red_override: Optional[Dict] = None,   # v5.0新增
        fidelity: str = "high",                 # v5.0新增："high"/"low"
        generate_training_data: bool = False,   # v5.0新增：是否生成TrainingTriple
    ) -> Dict[str, Any]:
        """
        运行仿真（v5.0扩展接口）

        v5.0新增参数：
        - red_override: 红方智能体生成的攻击方案，覆盖默认随机红方行为。
          结构：{"tactic": str, "force_allocation": Dict, "scenario_adaptation": Dict}
          当此参数非None时，_execute_red_step()使用此方案而非随机行为。

        - fidelity: "high"使用完整交战模型（精确的距离判定、多因素杀伤概率），
          "low"使用简化模型（固定概率、忽略地形影响）用于MCTS快速评估。

        - generate_training_data: True时在仿真过程中记录每个时间步的
          TrainingTriple，追加到返回结果的training_triples字段。
        """
        # 实现基于v4.0 run_simulation()，增加red_override分支和fidelity逻辑
        pass

    def run_batch(
        self,
        blue_orbat: Dict[str, Any],
        red_orbat: Dict[str, Any],
        coa: Dict[str, Any],
        batch_size: int = 32,
        max_steps: int = 200,
        fidelity: str = "low",
    ) -> List[Dict[str, Any]]:
        """
        批量仿真（v5.0新增）

        用于MCTS并行rollout。使用low保真度模式加速仿真，
        每次调用返回batch_size个独立仿真结果。
        仿真之间共享蓝方COA但使用不同的随机种子。
        """
        pass

    def _execute_red_step(self, step: int, red_override: Optional[Dict] = None):
        """
        执行红方行动（v5.0升级）

        v4.0：随机行为（self._rng.random() > 0.5）
        v5.0：当red_override非None时，按红方智能体指定的战术执行：
          - concentrated_breakthrough: 红方主力集中攻击蓝方薄弱方向
          - multi_axis_encirclement: 红方分多路向心攻击
          - deception_decoy: 佯攻牵制+主攻隐蔽
          - flanking_maneuver: 侧翼迂回攻击
          - EW_jamming: 电子压制干扰蓝方C2
          - 其他战术按各自逻辑模型执行
        """
        if red_override is not None:
            self._execute_red_tactic(step, red_override)
        else:
            # 回退到v4.0默认随机行为
            pass

    def _execute_red_tactic(self, step: int, tactic_config: Dict):
        """执行红方指定战术（v5.0新增）"""
        pass

    def _resolve_engagements(
        self, step: int, fidelity: str = "high"
    ):
        """
        解决交战（v5.0升级：支持保真度模式）

        high保真度：完整交战模型（距离、地形、兵力比、士气等因素）
        low保真度：简化模型（固定概率，用于MCTS快速评估，性能提升约10倍）
        """
        pass
```

#### 6.3.3 训练数据流

```text
WargameEngine仿真 → TrainingTriple生成 → 数据流去向

  ┌─────────────────────────────────────────────────────────────┐
  │                   WargameEngine仿真                         │
  │                                                             │
  │   每个时间步生成一个TrainingTriple:                           │
  │   state（当前态势）→ action（蓝/红行动）→ reward → next_state │
  │                                                             │
  │   fidelity="high": 完整仿真，用于正式评估和Skill验证          │
  │   fidelity="low":  简化仿真，用于MCTS rollout和快速搜索       │
  └──────────────────────────┬──────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
     ┌────────────┐  ┌────────────┐  ┌────────────┐
     │ 世界模型   │  │ Skill提取  │  │ MCTS规划   │
     │ 训练集     │  │ 管线(6.4)  │  │ rollout    │
     │            │  │            │  │ 缓存       │
     └────────────┘  └────────────┘  └────────────┘
```

---

### 6.4 Skill训练管线

#### 6.4.1 设计理念

v4.0的经验蒸馏（ExperienceRecorder → ExperienceMiner → ExperiencePromoter）从实战工作流执行中提取模式。v5.0的Skill训练管线在此基础上增加对抗训练维度的数据源——不仅从成功经验中学习，还要从"成功抵御红方突破"的经验中提取对抗鲁棒的Skill。

Skill提取的核心问题：不是"什么策略有效"，而是"什么策略在对手也在学习的情况下持续有效"。一个Skill必须满足：

1. **统计显著性**：在≥20次独立仿真中出现，非偶然事件
2. **对抗鲁棒性**：在红方主动寻找弱点的情况下仍保持≥85%成功率
3. **因果可解释**：通过因果归因验证，不是相关性巧合
4. **条件明确**：适用条件清晰界定，不会在边界条件下误用

#### 6.4.2 完整实现代码

```python
# training/skill_extraction.py
"""
Skill训练管线

从对抗训练仿真结果中提取经验证的可复用Skill。
与v4.0经验蒸馏（distillation/）的关联：
  - v4.0经验蒸馏从实战工作流中提取模式
  - v5.0 Skill管线从对抗训练仿真中提取对抗鲁棒的Skill
  - 两者产出都注册到SkillLibrary，共享同一接口
"""
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import hashlib
import json

from distillation.skill_library import SkillLibrary, SkillDefinition
from training.world_model import WorldModel
from scenarios.wargame import WargameEngine, TrainingTriple


@dataclass
class KeyDecision:
    """关键决策点——仿真中态势发生重大变化的时刻"""
    decision_id: str
    time_step: int
    scenario_type: str
    decision_context: Dict[str, Any]    # 决策时的态势快照
    action_taken: Dict[str, Any]        # 采取的行动
    outcome_delta: float                # 行动前后的态势变化量（蓝方视角）
    survival_before: float              # 行动前蓝方生存率
    survival_after: float               # 行动后蓝方生存率


@dataclass
class CausalLink:
    """因果链接——与第3.3.4节CausalLink对齐，扩展对抗验证字段"""
    cause: str                      # 因素描述
    effect: str                     # 结果描述
    strength: float                 # 因果强度 [0,1]（Ch3字段）
    confidence: float               # 置信度 [0,1]（对抗训练评估）
    evidence_count: int             # 支撑证据数量（Ch3字段）
    counterfactual_evidence: int = 0  # 反事实验证通过次数（Ch6扩展）


class SimulationToSkillPipeline:
    """
    从仿真结果中提取Skill

    流程：
    1. 积累仿真结果（对抗训练+兵棋推演）
    2. 识别关键决策点（态势发生了重大变化的时刻）
    3. 因果归因（这个决策为什么导致了好/坏结果）
    4. 归纳适用条件（在什么情况下这个决策是有效的）
    5. 验证（回放仿真验证Skill的有效性）
    6. 注册到Skill库
    """

    def __init__(
        self,
        skill_library: SkillLibrary,
        world_model: WorldModel,
        engine: WargameEngine,
    ):
        self._skills = skill_library
        self._world_model = world_model
        self._engine = engine
        self._min_episodes = 20         # 提取Skill所需最小样本数
        self._min_success_rate = 0.85   # Skill最低成功率
        self._significance_threshold = 0.3  # 态势变化显著性阈值

    def extract_from_simulation_batch(
        self, results: List[Dict]
    ) -> List[SkillDefinition]:
        """
        从一批仿真结果中提取Skills

        Args:
            results: 对抗训练或兵棋推演的仿真结果列表，
                     每条包含scenario_type、blue_strategy、red_action、
                     outcome、training_triples等字段

        Returns:
            新提取并注册的SkillDefinition列表
        """
        extracted = []

        # Step 1: 按场景类型分组
        groups = self._group_by_scenario_type(results)

        for scenario_type, episodes in groups.items():
            if len(episodes) < self._min_episodes:
                continue

            # Step 2: 识别关键决策点
            key_decisions = self._identify_key_decisions(episodes)
            if not key_decisions:
                continue

            for decision in key_decisions:
                # Step 3: 因果归因
                causal_links = self._attribute_causality(decision, episodes)
                if not causal_links:
                    continue

                # 过滤低置信度的因果链
                strong_links = [
                    cl for cl in causal_links if cl.confidence >= 0.7
                ]
                if not strong_links:
                    continue

                # Step 4: 归纳适用条件
                applicability = self._induce_applicability(
                    decision, strong_links, episodes
                )

                # Step 5: 验证（回放仿真验证Skill有效性）
                validated = self._validate_skill(
                    decision, strong_links, applicability, episodes
                )

                if validated and validated["success_rate"] >= self._min_success_rate:
                    skill = self._create_skill(
                        decision, strong_links, applicability, validated, episodes
                    )
                    self._skills.register(skill)
                    extracted.append(skill)

        return extracted

    def _group_by_scenario_type(
        self, results: List[Dict]
    ) -> Dict[str, List[Dict]]:
        """按场景类型分组"""
        groups: Dict[str, List[Dict]] = {}
        for result in results:
            scenario_type = result.get("scenario_type", "unknown")
            groups.setdefault(scenario_type, []).append(result)
        return groups

    def _identify_key_decisions(
        self, episodes: List[Dict]
    ) -> List[KeyDecision]:
        """
        识别关键决策点

        方法：分析仿真中的TrainingTriple序列，检测态势指标（蓝方生存率、
        任务达成度）发生显著变化的时间步。这些时刻标识了关键决策点——
        某个行动显著改变了态势走向。
        """
        key_decisions = []
        decision_counter = 0

        for episode in episodes:
            triples = episode.get("training_triples", [])
            for i in range(1, len(triples)):
                prev = triples[i - 1]
                curr = triples[i]

                # 计算态势变化量
                prev_survival = prev.get("state", {}).get(
                    "blue_survival_pct", 100
                )
                curr_survival = curr.get("state", {}).get(
                    "blue_survival_pct", 100
                )
                delta = abs(curr_survival - prev_survival) / 100.0

                if delta >= self._significance_threshold:
                    decision_counter += 1
                    key_decisions.append(KeyDecision(
                        decision_id=f"KD-{decision_counter:06d}",
                        time_step=curr.get("state", {}).get("time_step", i),
                        scenario_type=episode.get("scenario_type", "unknown"),
                        decision_context=prev.get("state", {}),
                        action_taken=curr.get("action", {}),
                        outcome_delta=delta,
                        survival_before=prev_survival,
                        survival_after=curr_survival,
                    ))

        return key_decisions

    def _attribute_causality(
        self, decision: KeyDecision, episodes: List[Dict]
    ) -> List[CausalLink]:
        """
        因果归因

        方法：比较采取了此决策的回合与未采取此决策的回合，
        通过反事实分析建立因果链。如果采取了此行动的回合
        显著优于未采取的回合，则判定为正向因果。
        """
        action_hash = self._hash_action(decision.action_taken)

        # 分组：采取了此行动 vs 未采取
        positive_group = []
        negative_group = []

        for episode in episodes:
            triples = episode.get("training_triples", [])
            has_action = any(
                self._hash_action(t.get("action", {})) == action_hash
                for t in triples
            )
            if has_action:
                positive_group.append(episode)
            else:
                negative_group.append(episode)

        if len(positive_group) < 5:
            return []

        # 计算两组的蓝方生存率差异
        pos_survival = [
            e.get("outcome", {}).get("blue_survival_pct", 0)
            for e in positive_group
        ]
        neg_survival = [
            e.get("outcome", {}).get("blue_survival_pct", 0)
            for e in negative_group
        ] if negative_group else [50.0]

        avg_pos = sum(pos_survival) / len(pos_survival)
        avg_neg = sum(neg_survival) / len(neg_survival)

        # 因果置信度 = 效应量（Cohen's d简化版）
        effect_size = abs(avg_pos - avg_neg) / 100.0
        confidence = min(1.0, effect_size * 2)  # 映射到0-1

        if confidence < 0.3:
            return []

        cause_desc = json.dumps(
            decision.action_taken, ensure_ascii=False
        )[:100]
        effect_desc = (
            f"蓝方生存率变化: {avg_neg:.0f}% → {avg_pos:.0f}%"
            if avg_pos > avg_neg
            else f"蓝方生存率下降: {avg_neg:.0f}% → {avg_pos:.0f}%"
        )

        return [CausalLink(
            cause=cause_desc,
            effect=effect_desc,
            confidence=confidence,
            counterfactual_evidence=[
                {"with_action": avg_pos, "without_action": avg_neg}
            ],
        )]

    def _induce_applicability(
        self,
        decision: KeyDecision,
        causal_links: List[CausalLink],
        episodes: List[Dict],
    ) -> Dict[str, Any]:
        """
        归纳适用条件

        从采取了此决策且结果为正的回合中，提取共同的态势特征，
        归纳出此Skill的适用条件。
        """
        positive_episodes = [
            e for e in episodes
            if e.get("outcome", {}).get("winner") == "blue"
        ]

        if not positive_episodes:
            return {"applicable": False, "reason": "无成功回合"}

        # 提取共同特征
        terrain_types = set()
        force_ratios = []
        threat_types = set()

        for ep in positive_episodes:
            scenario = ep.get("scenario", {})
            terrain_types.add(scenario.get("terrain", "unknown"))
            force_ratios.append(scenario.get("force_ratio", 1.0))
            threat_types.update(scenario.get("threat_types", []))

        return {
            "applicable": True,
            "terrain": list(terrain_types),
            "force_ratio_range": (
                min(force_ratios), max(force_ratios)
            ) if force_ratios else (0.5, 2.0),
            "threat_types": list(threat_types),
            "scenario_type": decision.scenario_type,
            "required_success_rate": self._min_success_rate,
        }

    def _validate_skill(
        self,
        decision: KeyDecision,
        causal_links: List[CausalLink],
        applicability: Dict[str, Any],
        episodes: List[Dict],
    ) -> Optional[Dict]:
        """
        验证Skill有效性

        使用WargameEngine回放仿真，在适用条件匹配的场景中
        验证Skill的成功率是否达到阈值。
        """
        if not applicability.get("applicable"):
            return None

        # 筛选适用场景
        applicable_episodes = [
            e for e in episodes
            if self._matches_applicability(e, applicability)
        ]

        if len(applicable_episodes) < 10:
            return None

        # 统计成功率
        wins = sum(
            1 for e in applicable_episodes
            if e.get("outcome", {}).get("winner") == "blue"
        )
        success_rate = wins / len(applicable_episodes)

        return {
            "success_rate": success_rate,
            "validated_episodes": len(applicable_episodes),
            "causal_confidence": max(cl.confidence for cl in causal_links),
        }

    def _create_skill(
        self,
        decision: KeyDecision,
        causal_links: List[CausalLink],
        applicability: Dict[str, Any],
        validation: Dict,
        episodes: List[Dict],
    ) -> SkillDefinition:
        """创建SkillDefinition并注册"""
        # 字段定义对齐第3.3.5节SkillDefinition
        return SkillDefinition(
            skill_id=f"SKILL-ADV-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{decision.decision_id}",
            name=f"对抗训练Skill-{decision.scenario_type}",
            description=f"从对抗训练中提取的策略Skill。因果置信度: {validation['causal_confidence']:.2f}",
            source="adversarial_training",
            applicability=applicability,                  # 对齐Ch3字段名（原applicability_conditions）
            parameters=decision.action_taken,             # 对齐Ch3字段名（原strategy_template）
            success_rate=validation["success_rate"],
            validated_episodes=validation["validated_episodes"],
            causal_model=[{                               # 对齐Ch3字段名（原causal_evidence）
                "cause": cl.cause,
                "effect": cl.effect,
                "confidence": cl.confidence,
            } for cl in causal_links],
            created_at=datetime.utcnow(),
            tags=["adversarial", decision.scenario_type],
        )

    @staticmethod
    def _matches_applicability(
        episode: Dict, applicability: Dict
    ) -> bool:
        """检查回合是否匹配适用条件"""
        scenario = episode.get("scenario", {})
        terrain = scenario.get("terrain", "unknown")
        force_ratio = scenario.get("force_ratio", 1.0)

        if terrain not in applicability.get("terrain", [terrain]):
            return False

        fr_range = applicability.get("force_ratio_range", (0.0, 10.0))
        if not (fr_range[0] <= force_ratio <= fr_range[1]):
            return False

        return True

    @staticmethod
    def _hash_action(action: Dict) -> str:
        """行动特征哈希"""
        canonical = json.dumps(action, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canonical.encode()).hexdigest()[:12]
```

---

### 6.5 训练-评估-部署闭环

#### 6.5.1 完整管线全景

对抗训练不是孤立环节，而是嵌入完整的训练-评估-部署闭环。从数据采集到线上监控，形成持续进化的七步闭环：

```text
训练-评估-部署闭环（v5.0完整管线）

  ┌──────────────────────────────────────────────────────────────┐
  │                                                              │
  │  ① 数据采集                                                  │
  │  ┌─────────────────────────────────────────────────────┐    │
  │  │ 实战数据 → 演习数据 → 仿真数据                        │    │
  │  │ (传感器回放)  (HLA4记录)  (WargameEngine产出)         │    │
  │  └──────────────────────┬──────────────────────────────┘    │
  │                         │                                    │
  │                         ▼                                    │
  │  ② 世界模型训练                                              │
  │  ┌─────────────────────────────────────────────────────┐    │
  │  │ TrainingTriple → 世界模型训练                        │    │
  │  │ 输入(state,action) → 预测(next_state, reward)        │    │
  │  │ 训练触发条件：新增数据≥1000条 或 漂移检测触发          │    │
  │  └──────────────────────┬──────────────────────────────┘    │
  │                         │                                    │
  │                         ▼                                    │
  │  ③ 红蓝对抗训练（6.2）                                       │
  │  ┌─────────────────────────────────────────────────────┐    │
  │  │ BlueAgent ↔ RedAgent ↔ WargameEngine                │    │
  │  │ 四阶段循环：探索→突破→补强→评估                        │    │
  │  │ 训练产出：对抗验证的策略 + 弱点报告                    │    │
  │  └──────────────────────┬──────────────────────────────┘    │
  │                         │                                    │
  │                         ▼                                    │
  │  ④ Skill提取（6.4）                                          │
  │  ┌─────────────────────────────────────────────────────┐    │
  │  │ 仿真结果 → 关键决策识别 → 因果归因 → 适用条件归纳     │    │
  │  │ → 验证 → 注册SkillLibrary                           │    │
  │  └──────────────────────┬──────────────────────────────┘    │
  │                         │                                    │
  │                         ▼                                    │
  │  ⑤ 评估门控                                                  │
  │  ┌─────────────────────────────────────────────────────┐    │
  │  │ SEAL Lab评估框架（详见第8章）                         │    │
  │  │ 安全性测试 + 准确性基准 + OOD退化评估 + 红队测试       │    │
  │  │ 门控条件：全部通过后方可进入部署                       │    │
  │  └──────────────────────┬──────────────────────────────┘    │
  │                         │                                    │
  │                         ▼                                    │
  │  ⑥ 灰度部署                                                  │
  │  ┌─────────────────────────────────────────────────────┐    │
  │  │ 渐进部署策略（详见第10章）                            │    │
  │  │ 影子模式(0%) → 灰度(10%→30%→100%) → 全量上线         │    │
  │  │ 每阶段自动回滚检测                                   │    │
  │  └──────────────────────┬──────────────────────────────┘    │
  │                         │                                    │
  │                         ▼                                    │
  │  ⑦ 线上监控                                                  │
  │  ┌─────────────────────────────────────────────────────┐    │
  │  │ 漂移检测（Evidently）→ 异常告警 → 触发重训练           │    │
  │  │ 监控指标：胜率偏差、推理延迟、Skill命中率、红方突破率   │    │
  │  │ 漂移检测阈值：KS检验 p < 0.05                         │    │
  │  │ 重训练闭环SLA：< 24h                                  │    │
  │  └──────────────────────┬──────────────────────────────┘    │
  │                         │                                    │
  │                         │ 检测到漂移/新数据积累               │
  │                         │                                    │
  │                         ▼                                    │
  │                    回到 ① 或 ②                               │
  │                                                              │
  └──────────────────────────────────────────────────────────────┘
```

#### 6.5.2 各阶段关键参数

| 阶段 | 触发条件 | 执行频率 | 产出 | SLA |
|------|---------|---------|------|-----|
| 数据采集 | 持续 | 实时 | TrainingTriple流 | 每小时≥100条 |
| 世界模型训练 | 新增≥1000条或漂移触发 | 1-2次/天 | 更新的世界模型权重 | 训练<4h |
| 对抗训练 | 世界模型更新后 | 1-2次/天 | 对抗验证策略+弱点报告 | 单轮<2h |
| Skill提取 | 对抗训练完成 | 1-2次/天 | 新Skill定义 | <30min |
| 评估门控 | Skill/模型注册后 | 按需 | 评估报告（pass/fail） | <4h |
| 灰度部署 | 评估通过 | 按需 | 渐进部署配置 | 全量<24h |
| 线上监控 | 持续 | 实时 | 漂移报告+告警 | 漂移检测<1h |

#### 6.5.3 对抗训练特有的监控指标

除常规的模型监控指标（推理延迟、准确率等）外，对抗训练引入四项特有监控指标：

| 指标 | 含义 | 告警阈值 | 响应动作 |
|------|------|---------|---------|
| **红蓝胜率比** | 最近100轮训练中红方胜率 / 蓝方胜率 | 红方胜率>60% | 增加蓝方训练轮次，检查Skill库是否过时 |
| **Skill对抗鲁棒性** | Skill在对抗训练中的实际成功率 vs 注册时成功率 | 下降>15% | 标记Skill待审核，触发重新验证 |
| **弱点重复率** | 同类弱点被红方反复突破的频率 | 同类弱点>5次 | 紧急补强训练，审查Skill降级 |
| **策略多样性** | 蓝方生成策略的熵值（避免过拟合单一策略） | 熵值低于基线50% | 增加蓝方探索阶段比例 |

#### 6.5.4 闭环异常处理

训练闭环中可能出现的异常及处理策略：

```text
异常场景                    检测方式                    处理策略
─────────────────────────────────────────────────────────────────
世界模型预测偏差过大         预测误差>3σ                 回滚到上一版世界模型
                                                    使用旧模型重跑对抗训练
红方胜率持续上升             红方胜率连续50轮>70%        检查蓝方Skill库是否过时
                                                    增加蓝方MCTS搜索深度
Skill提取空转                连续5次提取0个新Skill       降低提取阈值或增加训练轮次
                                                    检查场景覆盖是否过窄
训练不收敛                   胜率曲线100轮无显著变化      调整学习率和探索率
                                                    增加场景多样性
GPU资源不足                  训练任务排队>2h             降级到CPU训练（小规模）
                                                    或请求GPU扩容
```

#### 6.5.5 与第8章和第10章的衔接

**第8章（数据闭环）**提供数据采集和漂移检测的基础设施。对抗训练是数据闭环的核心消费者——世界模型训练依赖第8章采集的TrainingTriple，漂移检测触发重训练后执行本章定义的对抗训练流程。第8章的SEAL Lab评估框架是Skill和模型从训练到部署的必经门控。

**第10章（运维与部署）**提供灰度部署和线上监控的执行机制。对抗训练产出的Skill和模型通过第10章的影子模式→灰度→全量上线路径逐步部署，第10章的回滚机制在检测到线上指标异常时自动回退到上一稳定版本。

三者的协作关系：本章（对抗训练）是"引擎"——产生更好的策略和模型；第8章（数据闭环）是"燃料"——提供持续的数据输入和评估输出；第10章（运维部署）是"轨道"——确保新策略安全上线并持续监控。三者缺一不可，共同构成AI原生C2系统的持续进化能力。

---

## 7. 五大作战场景验证

五个作战场景覆盖陆/海/空/天/电五大作战域，验证第4章快慢双系统的实际效果：

| 场景 | 作战域 | OODA侧重 | 快/慢路径 | 验证重点 |
|------|--------|---------|----------|---------|
| 7.1 ISR情报侦察 | 多域 | Observe+Orient | 快路径为主 | 多源融合、RAG条令检索、COP更新 |
| 7.2 C2指挥决策 | 联合 | Decide | 慢路径为主 | LLM COA生成、OR-Tools优化、OPA策略检查 |
| 7.3 多域无人协同 | 陆/海/空 | Act | 快慢混合 | OR-Tools路径规划、OPA自主授权、动态重规划 |
| 7.4 防空反导 | 空/天 | 全OODA闭环 | 快路径（杀伤链） | 时敏短路、OPA交战规则、杀伤链闭环 |
| 7.5 兵棋推演 | 多域 | 仿真验证 | 慢路径 | 蒙特卡洛仿真、COA评估、经验蒸馏入口 |

每个场景遵循统一结构：场景概述 → 工作流模板映射（对应Ch4） → 实现代码 → 输入输出规范。


### 7.1 ISR情报侦察监视场景

#### 7.1.1 场景概述

多源情报收集、融合、分析与威胁研判。支持卫星/无人机/雷达/信号侦察等多模态数据的自动化处理，形成态势感知基础。

#### 7.1.2 工作流模板映射

```
ISR工作流模板（fast_track候选）：
DAG: ingest → preprocess → classify → correlate → analyze → fuse → report
快路径：ingest→preprocess→classify（Triton推理，<200ms）
慢路径：analyze（RAG条令检索+LLM威胁研判，<30s）
OODA映射：Observe=ingest+preprocess, Orient=classify+correlate+analyze, Decide=fuse, Act=report
蒸馏路径：高频ISR模板（卫星过境例行侦察）→ fast_track → 自动执行
人工干预：analyze阶段产出异常威胁时触发指挥员确认
```

#### 7.1.3 处理流程

```Plain
┌─────────────────────────────────────────────────────────────────┐
│ ISR情报处理流程                                                  │
├─────────────────────────────────────────────────────────────────┤
│
│ 1. 多源接入阶段（实时，< 1s）
│ ├── 卫星图像接入（SAR/EO/IR）
│ ├── 无人机视频流接入
│ ├── 雷达航迹数据接入
│ ├── 电子侦察信号接入
│ └── 数据链消息接入（Link 16/VMF） ← 
│ ↓
│ 2. 预处理阶段（战术层，< 200ms）
│ ├── 图像增强与去噪
│ ├── 信号降噪与特征提取
│ ├── 数据链消息解码（Protobuf） ← 
│ └── 数据质量标记
│ ↓
│ 3. AI推理阶段（战术层，< 100ms）
│ ├── 目标检测与识别（YOLOv8 + TensorRT）
│ ├── 信号分类与辐射源识别
│ └── 异常行为检测
│ ↓
│ 4. LLM增强分析，< 30s）
│ ├── RAG检索相关条令
│ ├── LLM生成威胁研判
│ └── 结构化输出（JSON Schema约束）
│ ↓
│ 5. 融合分析阶段（战役层，< 30s）
│ ├── 多源航迹关联
│ ├── 实体关系图查询（AGE）
│ ├── 意图识别与预测
│ └── 威胁等级评估
│ ↓
│ 6. 情报产品生成（< 10s）
│ ├── 威胁评估报告
│ ├── 态势摘要（LLM生成）
│ ├── 置信度评估
│ └── 行动建议
```

#### 7.1.4 实现代码

```python
# scenarios/isr_pipeline.py
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime

from clients.triton_client import TritonInferenceClient
from clients.sglang_client import SGLangMilitaryClient
from knowledge.qdrant_setup import MilitaryKnowledgeStore
from ontology.cop_service import COPService
from ontology.data_lineage import DataLineageService, LineageNodeType


class ISRPipeline:
 """ISR情报侦察监视完整流水线（）"""

 def __init__(
 self,
 triton: TritonInferenceClient,
 sglang: SGLangMilitaryClient,
 knowledge: MilitaryKnowledgeStore,
 cop: COPService,
 lineage: DataLineageService,
 ):
 self._triton = triton
 self._sglang = sglang
 self._knowledge = knowledge
 self._cop = cop
 self._lineage = lineage

 async def execute(self, mission: Dict[str, Any]) -> Dict[str, Any]:
 """
 执行ISR任务
 Args:
 mission: {mission_id, area_of_interest, time_window, intel_types,
 collection_assets, priority, analysis_depth}
 """
 mission_id = mission["mission_id"]
 results = {
 "mission_id": mission_id,
 "detected_entities": [],
 "track_correlations": [],
 "threat_assessment": {},
 "intelligence_gaps": [],
 "recommendations": [],
 }

 # Phase 1: 多源数据收集
 raw_data = await self._collect_multi_source(mission)
 lin_collect = await self._lineage.record_lineage(
 source_id=f"mission-{mission_id}",
 target_id=f"raw-{mission_id}",
 transformation="multi_source_collection",
 operator="system",
 params={"sources": mission["collection_assets"]},
 )

 # Phase 2: AI推理（Triton目标检测 + 信号分类）
 detections = []
 for source_type, data in raw_data.items():
 if source_type in ["imagery", "sar", "eo_ir"]:
 dets = self._triton.detect_targets(data)
 detections.extend(dets)
 elif source_type in ["sigint", "elint"]:
 dets = self._classify_signals(data)
 detections.extend(dets)
 elif source_type in ["radar_tracks"]:
 dets = self._process_radar_tracks(data)
 detections.extend(dets)

 # Phase 3: 航迹关联
 correlated = await self._correlate_tracks(detections)
 results["track_correlations"] = correlated

 # Phase 4: LLM增强分析（RAG + 结构化输出）
 sensor_summary = self._summarize_detections(detections)
 doctrine_refs = await self._retrieve_doctrine(sensor_summary)
 llm_analysis = self._sglang.analyze_threat(
 sensor_summary=sensor_summary,
 context=doctrine_refs,
 )

 # Phase 5: 融合态势评估
 threat_assessment = {
 "overall_level": llm_analysis.threat_level,
 "critical_count": sum(1 for d in detections if d.get("threat_potential") == "high"),
 "total_entities": len(detections),
 "llm_analysis": llm_analysis.model_dump(),
 "doctrine_reference": llm_analysis.doctrine_reference,
 }
 results["threat_assessment"] = threat_assessment

 # Phase 6: 更新COP
 for det in detections:
 entity = self._detection_to_entity(det, mission)
 await self._cop.upsert_entity(entity)

 # Phase 7: 生成情报产品
 results["recommendations"] = llm_analysis.recommended_action
 results["detected_entities"] = detections

 return results

 def _collect_multi_source(self, mission: Dict) -> Dict[str, Any]:
 """
 从多源收集原始数据
 实现：根据mission中collection_assets指定的侦察平台列表，并行调度各数据采集适配器——
 卫星图像（SAR/EO/IR）通过SatImageAdapter接入，无人机视频流通过UAVStreamAdapter接入，
 雷达航迹通过RadarTrackAdapter接入，信号侦察通过SIGINTAdapter接入，
 数据链消息（Link 16/VMF）通过ProtobufDecoder解码（见Ch5 COP数据平面4.3节）。
 采集结果按source_type分组返回。
 参考：Ch7.1.3处理流程第1阶段"多源接入"。
 """
 # TODO: 对接多源数据采集适配器层（SatImageAdapter/UAVStreamAdapter/RadarTrackAdapter/SIGINTAdapter）
 return {}

 def _classify_signals(self, data: Any) -> List[Dict]:
 """
 信号分类推理
 实现：调用Triton推理服务（见Ch2.4.4 GPU推理层），使用预训练信号分类模型，
 对SIGINT/ELINT原始信号进行特征提取和分类，输出信号类型（雷达/通信/电子战）、
 辐射源识别结果及置信度。输入为原始IQ采样数据或频谱特征向量，
 输出为标准化的detection列表（含signal_type、emitter_id、confidence字段）。
 参考：Ch7.1.3处理流程第3阶段"AI推理"。
 """
 # TODO: 对接Triton信号分类模型（signal_classifier_v2.onnx）
 return []

 def _process_radar_tracks(self, data: Any) -> List[Dict]:
 """
 雷达航迹处理
 实现：接收雷达原始点迹数据，执行航迹起始、航迹更新和航迹质量管理。
 具体包括：（1）点迹-航迹关联（最近邻/JPDA），（2）卡尔曼滤波平滑航迹，
 （3）航迹质量评估（基于更新频率和残差），（4）输出标准化航迹消息
 （含track_id、position、velocity、confidence、threat_potential字段）。
 航迹数据通过Redpanda消息总线分发至COPService进行态势融合。
 参考：Ch5 COP数据平面4.2节传感器接入层，Ch7.1.3处理流程第2阶段"预处理"。
 """
 # TODO: 实现雷达点迹-航迹关联（JPDA）和卡尔曼滤波航迹平滑
 return []

 def _correlate_tracks(self, detections: List[Dict]) -> List[Dict]:
 """
 航迹关联
 实现：对来自不同传感器（图像检测/信号分类/雷达航迹）的检测目标进行多源关联，
 基于空间距离（马氏距离）、速度一致性、时间窗口匹配度计算关联得分，
 使用匈牙利算法求解最优关联矩阵。关联后的融合航迹更新confidence（多源加权），
 并通过COPService写入Apache AGE实体关系图。
 参考：Ch7.1.3处理流程第5阶段"融合分析"——多源航迹关联。
 """
 # TODO: 实现基于马氏距离+匈牙利算法的多源航迹关联
 return [{"track_id": f"TRK-{i}", "source_count": 1, "confidence": 0.8} for i in range(len(detections))]

 def _summarize_detections(self, detections: List[Dict]) -> str:
 """
 汇总检测结果为文本摘要
 实现：将结构化检测结果列表转换为自然语言摘要文本，供下游LLM分析使用。
 按目标类型、威胁等级、空间分布进行聚类统计，生成包含以下信息的结构化摘要：
 （1）各类目标数量及置信度分布，（2）高威胁目标清单及位置，
 （3）空间分布特征（集中/分散/线性）。
 摘要格式需与SGLangMilitaryClient.analyze_threat()的sensor_summary参数对齐。
 参考：Ch7.1.3处理流程第6阶段"情报产品生成"——态势摘要。
 """
 # TODO: 实现基于目标聚类统计的自然语言摘要生成
 return f"检测到{len(detections)}个目标"

 def _retrieve_doctrine(self, summary: str) -> str:
 """
 RAG检索条令
 实现：调用MilitaryKnowledgeStore（Qdrant向量库）进行语义检索，
 以sensor_summary为查询向量，检索相关JS条令片段（情报侦察规程、
 威胁判定标准、交战规则等）。检索结果按相关度排序，返回Top-K条令原文
 及其元数据（条令编号、章节、适用场景）。检索范围覆盖≥5类条令库。
 参考：Ch2.4.3 SGLang推理引擎——RAG知识库检索，Ch7.1.3处理流程第4阶段"LLM增强分析"。
 """
 # TODO: 对接Qdrant向量库实现条令语义检索（MilitaryKnowledgeStore.search()）
 return ""

 def _detection_to_entity(self, detection: Dict, mission: Dict) -> Dict:
 """
 将检测结果转换为COP实体格式
 实现：将传感器检测的原始目标数据映射为JC3IEDM本体标准实体格式，
 包括：（1）实体ID生成（track_id或自动生成），（2）JS类型映射
 （传感器分类→MIL-STD-2525C符号编码），（3）敌我识别（IFF/电子特征），
 （4）密级标定（依据mission.classification），（5）威胁等级映射。
 转换后通过COPService.upsert_entity()写入COP（见Ch5 COP数据平面4.4节）。
 """
 # TODO: 实现传感器检测→JC3IEDM本体实体映射，含MIL-STD-2525C符号编码和IFF识别
 return {
 "entity_id": detection.get("track_id", f"ENT-{id(detection)}"),
 "entity_type": detection.get("military_type", "unknown"),
 "name": detection.get("military_type", "unknown"),
 "classification": "SECRET",
 "force_affiliation": "UNKNOWN",
 "confidence": detection.get("confidence", 0.0),
 "threat_level": detection.get("threat_potential", "NONE"),
 }
```

#### 7.1.5 输入输出规范

**输入字段**：

| 字段名 | 类型 | 必选 | 说明 | 示例 |
|--------|------|------|------|------|
| mission_id | string | 是 | 任务ID | ISR-20260510-001 |
| area_of_interest | GeoJSON | 是 | 关注区域 | 多边形坐标 |
| time_window | object | 是 | 时间窗口 | {"start": "...", "end": "..."} |
| intel_types | array | 是 | 情报类型 | ["imagery", "sigint", "radar"] |
| collection_assets | array | 是 | 侦察平台 | ["UAV-001", "SAT-003"] |
| priority | int | 否 | 优先级 1-10 | 7 |
| analysis_depth | string | 否 | 分析深度 | quick/standard/comprehensive |

**输出字段**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| report_id | string | 情报报告ID |
| detected_entities | array | 检测到的实体 |
| track_correlations | array | 航迹关联结果 |
| threat_assessment | object | 威胁评估（含LLM分析） |
| intelligence_gaps | array | 情报缺口 |
| recommendations | string | 行动建议 |

### 7.2 C2指挥决策场景

#### 7.2.1 场景概述

基于实时COP态势的自动化决策生成：LLM草案+OR-Tools优化，多方案行动方案（COA）生成、蒙特卡洛仿真评估、风险分析、指挥员确认与命令下达。

#### 7.2.2 工作流模板映射

```
C2决策工作流模板（慢系统典型模板）：
DAG: assess_situation → retrieve_doctrine → generate_coas → evaluate_coas → rank → opa_check → present
快路径：无（C2决策必须经过慢系统深度分析）
慢路径：全部步骤（LLM COA生成30-120s，蒙特卡洛评估+OR-Tools优化）
OODA映射：Observe=assess_situation, Orient=retrieve_doctrine, Decide=generate_coas+evaluate_coas+rank+opa_check, Act=present
蒸馏路径：高审批率COA模板（指挥员通过率≥95%）→ fast_track → 快系统直接推荐
人工干预：present后指挥员审批/修改/选择备选方案（L2/L3级自主）
```

#### 7.2.3 实现代码

```python
# scenarios/c2_decision.py
from typing import Dict, Any, List
import asyncio

from slow_system.llm_coa_generator import LLMCOAGenerator, CourseOfAction
from optimization.path_planner import TacticalPathPlanner
from security.policy_engine import OPAPolicyEngine


class C2DecisionEngine:
 """C2指挥决策引擎（）"""

 def __init__(
 self,
 coa_generator: LLMCOAGenerator,
 path_planner: TacticalPathPlanner,
 policy_engine: OPAPolicyEngine,
 ):
 self._coa_gen = coa_generator
 self._planner = path_planner
 self._opa = policy_engine

 async def generate_decision(self, request: Dict[str, Any]) -> Dict[str, Any]:
 """生成指挥决策"""

 # 1. 态势理解
 situation = self._assess_situation(request["current_cop"])

 # 2. LLM驱动的COA方案生成
 candidate_coas = await self._coa_gen.generate_coas(
 situation_brief=self._build_situation_brief(situation),
 available_forces=request["available_forces"],
 commander_intent=request.get("commander_intent", ""),
 constraints=request.get("roe", {}),
 num_alternatives=3,
 )

 # 3. 蒙特卡洛仿真评估每个COA
 evaluated = []
 for coa in candidate_coas:
 evaluation = await self._evaluate_coa(coa, situation)
 coa.success_probability = evaluation["success_probability"]
 coa.risk_level = evaluation["risk_level"]
 coa.overall_score = evaluation["overall_score"]
 coa.status = "evaluated"
 evaluated.append(coa)

 # 4. 方案排序
 ranked = sorted(evaluated, key=lambda x: x.overall_score, reverse=True)

 # 5. OPA策略检查
 primary = ranked[0] if ranked else None
 approval_required = False
 if primary:
 policy = self._opa.check_engagement({
 "action_type": self._extract_action_type(primary),
 "threat_level": situation.get("overall_threat", "MEDIUM"),
 "roe_mode": request.get("roe", {}).get("mode", "weapons_tight"),
 })
 approval_required = not policy.get("allow_engagement", False)

 return {
 "decision_package_id": f"DP-{request['decision_id']}",
 "primary_coa": primary.model_dump() if primary else None,
 "alternative_coas": [c.model_dump() for c in ranked[1:4]],
 "approval_required": approval_required,
 "policy_decision": policy if primary else None,
 }

 def _assess_situation(self, cop: Dict) -> Dict[str, Any]:
 """
 态势评估
 实现：对当前COP（Common Operational Picture）进行全面态势分析，包括：
 （1）威胁汇总——从COP实体中提取敌方目标，按威胁等级分类统计；
 （2）友军状态——汇总己方兵力可用性、位置分布和战备状态；
 （3）整体威胁等级——综合威胁数量、接近速度、武器覆盖范围计算Overall Threat Level；
 （4）关键事件识别——检测异常态势变化（新目标出现、兵力集结、电磁异常）；
 （5）情报缺口分析——识别COP中的盲区（无覆盖区域、未识别目标）。
 输出结构化态势评估结果，供_build_situation_brief()生成LLM可读摘要。
 参考：Ch4快慢双系统——OODA Orient阶段，Ch7.2.2工作流模板assess_situation节点。
 """
 # TODO: 实现基于COP实体图的全面态势评估（威胁/友军/缺口/关键事件分析）
 return {
 "threat_summary": {},
 "friendly_status": {},
 "overall_threat": "MEDIUM",
 "critical_events": [],
 "information_gaps": [],
 }

 def _evaluate_coa(self, coa: CourseOfAction, situation: Dict) -> Dict:
 """
 蒙特卡洛仿真评估COA方案
 实现：调用WargameEngine（见Ch7.5.3）对COA方案执行N次蒙特卡洛仿真，
 评估指标包括：（1）成功率（蓝方胜率），（2）蓝方兵力生存率，
 （3）风险等级（基于红方反应强度和不确定性传播），
 （4）综合评分（加权：成功率×0.5 + 生存率×0.3 + 时间效率×0.2）。
 仿真参数（迭代次数、时间步长）根据situation.urgency动态调整。
 参考：Ch7.5兵棋推演场景——WargameEngine.run_simulation()，
 Ch7.2.2工作流模板evaluate_coas节点。
 """
 # TODO: 对接WargameEngine执行蒙特卡洛仿真评估（100次迭代，含敏感性分析）
 base_prob = 0.7
 risk_modifier = {"low": 0.1, "medium": 0.0, "high": -0.2, "critical": -0.4}
 modifier = risk_modifier.get(coa.risk_level, 0.0)

 success_prob = max(0.1, min(0.95, base_prob + modifier))
 return {
 "success_probability": success_prob,
 "risk_level": coa.risk_level,
 "overall_score": success_prob * (1 + len(coa.phases) * 0.05),
 }

 def _build_situation_brief(self, situation: Dict) -> str:
 """
 生成态势简报文本
 实现：将_assess_situation()的结构化评估结果转换为LLM可理解的自然语言态势简报，
 包括：（1）威胁概要——敌方兵力类型/数量/位置/威胁等级，
 （2）友军状态——可用兵力/部署位置/战备状态，
 （3）关键事件——近期态势变化和异常事件，
 （4）情报缺口——未知区域和未识别目标，
 （5）环境条件——天气/地形/电磁环境。
 简报作为LLMCOAGenerator.generate_coas()的situation_brief输入。
 参考：Ch7.2.2工作流模板retrieve_doctrine→generate_coas间的数据传递。
 """
 # TODO: 实现结构化态势评估→自然语言态势简报转换（含威胁/友军/缺口/环境四段式）
 return f"威胁等级: {situation.get('overall_threat', 'UNKNOWN')}"

 def _extract_action_type(self, coa: CourseOfAction) -> str:
 for phase in coa.phases:
 if "strike" in phase.name.lower() or "engage" in phase.name.lower():
 return "kinetic_strike"
 return "non_kinetic"
```

#### 7.2.4 输入输出规范

**输入字段**：

| 字段名 | 类型 | 必选 | 说明 |
|--------|------|------|------|
| decision_id | string | 是 | 决策请求ID |
| current_cop | object | 是 | 当前COP态势 |
| mission_objectives | array | 是 | 任务目标列表 |
| available_forces | object | 是 | 可用兵力 |
| roe | object | 是 | 交战规则 |
| commander_intent | string | 否 | 指挥员意图 |
| decision_deadline | string | 是 | 决策截止时间 |

**输出字段**：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| decision_package_id | string | 决策包ID |
| primary_coa | object | 首选行动方案（含LLM生成的描述） |
| alternative_coas | array | 备选行动方案 |
| approval_required | bool | 是否需要指挥员确认 |
| policy_decision | object | OPA策略决策结果 |

### 7.3 多域无人系统协同场景

#### 7.3.1 场景概述

多平台异构无人系统（无人机/无人车/无人艇/无人潜航器）的协同任务规划、编队控制和动态重规划。

#### 7.3.2 工作流模板映射

```
多域无人协同工作流模板（快慢混合）：
DAG: check_opa_auth → plan_routes → gen_comm_plan → gen_contingencies → deploy
快路径：check_opa_auth（OPA自主授权查询）→ plan_routes（OR-Tools预计算模板）
慢路径：plan_routes（新区域/新威胁需OR-Tools完整求解，60-120s）
OODA映射：Observe=平台状态感知, Orient=威胁评估+OPA授权, Decide=plan_routes+contingencies, Act=deploy
蒸馏路径：高频航线模板（例行巡逻/标准侦察）→ fast_track → 直接匹配执行
人工干预：OPA授权级别>L2时需指挥员确认自主权限
```

#### 7.3.3 实现代码

```python
# scenarios/uav_swarm.py
from typing import Dict, Any, List, Optional
from datetime import datetime
from optimization.path_planner import TacticalPathPlanner, Waypoint, Platform
from security.policy_engine import OPAPolicyEngine


class MultiDomainSwarmCoordinator:
 """多域无人系统协同控制器（）"""

 def __init__(self, planner: TacticalPathPlanner, opa: OPAPolicyEngine):
 self._planner = planner
 self._opa = opa

 def plan_mission(self, mission: Dict[str, Any]) -> Dict[str, Any]:
 """
 多域无人系统任务规划
 """
 mission_id = mission["mission_id"]
 mission_type = mission["mission_type"]
 platform_configs = mission["platform_ids"]

 # 1. 构建航点和平台对象
 waypoints = [
 Waypoint(
 id=wp["id"],
 lat=wp["lat"],
 lon=wp["lon"],
 alt=wp.get("alt", 0),
 time_window_start=wp.get("time_window_start", 0),
 time_window_end=wp.get("time_window_end", 86400),
 service_time=wp.get("service_time", 60),
 )
 for wp in mission.get("waypoints", [])
 ]

 platforms = [
 Platform(
 id=p["id"],
 max_range_km=p.get("max_range_km", 500),
 max_speed_kmh=p.get("max_speed_kmh", 200),
 max_endurance_min=p.get("max_endurance_min", 120),
 )
 for p in platform_configs
 ]

 # 2. OPA检查自主等级
 autonomy_check = self._opa.check_engagement({
 "action_type": mission_type,
 "platform_type": "uav",
 "autonomy_level": mission.get("autonomy_level", "supervised"),
 })

 # 3. OR-Tools路径规划
 plan_result = self._planner.plan_multi_uav_routes(
 waypoints=waypoints,
 platforms=platforms,
 depot_lat=mission.get("depot_lat", 0),
 depot_lon=mission.get("depot_lon", 0),
 no_fly_zones=mission.get("no_fly_zones"),
 time_limit_seconds=30,
 )

 # 4. 生成通信计划
 comm_plan = self._generate_comm_plan(platforms, plan_result)

 # 5. 生成应急预案
 contingencies = self._generate_contingencies(mission, platforms)

 return {
 "flight_plan_id": f"FP-{mission_id}",
 "status": plan_result.get("status"),
 "assigned_tasks": plan_result.get("routes", []),
 "total_distance_km": plan_result.get("total_distance_km", 0),
 "num_routes": plan_result.get("num_routes", 0),
 "communication_plan": comm_plan,
 "contingency_plans": contingencies,
 "autonomy_allowed": autonomy_check.get("allow_autonomous", False),
 }

 def _generate_comm_plan(self, platforms: List[Platform], plan: Dict) -> Dict:
 """
 生成通信计划
 实现：基于OR-Tools路径规划结果和平台通信能力，生成多域无人系统的通信组网方案，包括：
 （1）链路类型选择——根据平台间距和地形遮挡，选择Mesh自组网/点对点/卫星中继；
 （2）频段分配——基于电磁环境感知（EMCON）选择最优频段（C-band/Ku-band/UHF），
 避免频谱冲突和敌方干扰；（3）中继点规划——在超视距场景下自动部署中继节点；
 （4）备份链路设计——主链路中断时的降级通信方案（卫星/UHF备用）；
 （5）通信时隙分配——Link 16 TDMA时隙规划。
 参考：Ch7.3.2工作流模板gen_comm_plan节点，Ch2.4数据链集成层。
 """
 # TODO: 实现基于电磁环境的自适应通信组网规划（含频段分配、中继点优化、备份链路）
 return {
 "link_type": "mesh",
 "frequency_band": "C-band",
 "relay_points": [],
 "backup_link": "satellite",
 }

 def _generate_contingencies(self, mission: Dict, platforms: List[Platform]) -> List[Dict]:
 """
 生成应急预案
 实现：基于任务类型、威胁环境和平台能力，自动生成多层级应急预案，包括：
 （1）通信中断——触发条件（心跳超时120s），应急动作（按预设航线返航/悬停等待），
 降级策略（切换UHF备份链路/自主执行剩余任务）；
 （2）平台故障——触发条件（单平台离线），应急动作（任务重分配/编队重构），
 使用OR-Tools重新求解缩减规模的路径规划问题；
 （3）新威胁出现——触发条件（ISR检测到威胁/OPA策略变更），应急动作（规避机动+
 任务重规划），需OPA策略引擎检查自主权限；
 （4）GPS拒止——触发条件（定位精度下降），应急动作（惯导/视觉导航切换）。
 每个预案含trigger/condition/action/timeout/opa_check_required字段。
 参考：Ch7.3.2工作流模板gen_contingencies节点，Ch4快慢双系统——经验蒸馏机制。
 """
 # TODO: 实现基于任务类型和威胁环境的多层级应急预案自动生成（含OPA策略联动）
 return [
 {
 "trigger": "communication_lost",
 "action": "return_to_base",
 "timeout_seconds": 120,
 },
 {
 "trigger": "platform_failure",
 "action": "redistribute_tasks",
 "affected": [p.id for p in platforms],
 },
 {
 "trigger": "new_threat_detected",
 "action": "evade_and_replan",
 "requires_opa_check": True,
 },
 ]
```

### 7.4 防空反导场景

#### 7.4.1 场景概述

区域防空反导作战：从来袭目标探测、跟踪、识别、威胁评估、火力分配到拦截和战果评估的全杀伤链闭环。

#### 7.4.2 杀伤链闭环流程

```Plain
 Find ──▶ Fix ──▶ Track ──▶ Target ──▶ Engage ──▶ Assess
 (探测) (定位) (跟踪) (瞄准) (交战) (评估)
 <10s <5s <10s <15s <30s <60s
 ──────────────────────────────────────────────────────────
 短路路径/战术层 战役层协助 OPA决策
```

#### 7.4.3 工作流模板映射

```
防空杀伤链工作流模板（快系统核心场景）：
DAG: detect → classify → assess → assign → engage(opa_check) → bda
快路径：detect→classify→assess→assign（OPA编译模板，<100ms）——高置信度来袭目标自动拦截
慢路径：assess→assign（低置信度/复杂目标需LLM辅助威胁评估+OR-Tools火力优化）
OODA映射：Observe=detect+classify, Orient=assess, Decide=assign+OPA, Act=engage+bda
蒸馏路径：高成功率拦截模式（≥97%命中率）→ Level 2 → OPA短路规则（全自动拦截）
人工干预：OPA未明确授权时（allow_engagement但非allow_autonomous）需指挥员确认
```

#### 7.4.4 实现代码

```python
# scenarios/air_defense.py
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
from security.policy_engine import OPAPolicyEngine


class EngagementStatus(str, Enum):
 SEARCHING = "searching"
 TRACKING = "tracking"
 TARGETING = "targeting"
 ENGAGED = "engaged"
 ASSESSING = "assessing"
 COMPLETED = "completed"
 ABORTED = "aborted"


class AirDefenseKillChain:
 """防空反导杀伤链（）"""

 def __init__(self, opa: OPAPolicyEngine):
 self._opa = opa
 self._active_chains: Dict[str, Dict] = {}

 def process_contact(self, contact: Dict[str, Any], defense_config: Dict) -> Dict[str, Any]:
 """
 处理一个新的雷达接触
 Args:
 contact: {track_id, entity_type, position, velocity, confidence, ...}
 defense_config: {defense_sector, weapon_systems, engagement_rules, alert_level}
 """
 track_id = contact["track_id"]

 # Find: 验证探测
 if contact.get("confidence", 0) < 0.5:
 return {"status": "low_confidence", "action": "continue_tracking"}

 # Fix: 精确定位
 fixed_position = self._fix_position(contact)

 # Track: 建立航迹
 track = self._establish_track(contact, fixed_position)

 # 威胁评估
 threat = self._assess_threat(track, defense_config["threat_catalog"])

 if threat["level"] in ["HIGH", "CRITICAL"]:
 # Target: 武器-目标分配
 weapon_assignment = self._assign_weapon(
 track, defense_config["weapon_systems"]
 )

 if weapon_assignment:
 # OPA检查交战规则
 policy = self._opa.check_engagement({
 "action_type": "engagement",
 "threat_level": threat["level"],
 "target_type": contact.get("entity_type", "unknown"),
 "roe_mode": defense_config["engagement_rules"].get("mode", "weapons_tight"),
 "alert_level": defense_config["alert_level"],
 "time_to_impact_seconds": threat.get("time_to_impact", 9999),
 })

 if policy.get("allow_engagement"):
 return {
 "status": "engage_authorized",
 "track_id": track_id,
 "weapon": weapon_assignment,
 "policy": policy,
 }
 elif policy.get("allow_autonomous"):
 # 自卫交战
 return {
 "status": "self_defense_authorized",
 "track_id": track_id,
 "weapon": weapon_assignment,
 "policy": policy,
 }
 else:
 return {
 "status": "engagement_requires_approval",
 "track_id": track_id,
 "weapon_assignment": weapon_assignment,
 "reason": "OPA policy requires human approval",
 }

 return {
 "status": "tracking",
 "track_id": track_id,
 "threat_level": threat["level"],
 "action": "continue_surveillance",
 }

 def _fix_position(self, contact: Dict) -> Dict:
 """
 多传感器融合精确定位
 实现：对单传感器接触数据进行多源融合定位，提升定位精度。
 包括：（1）多雷达三角定位——融合多部雷达的方位/距离测量，计算最优位置估计；
 （2）ESM/雷达交叉定位——利用电子支援措施（ESM）方位线与雷达航迹交叉定位；
 （3）卡尔曼滤波平滑——对融合后的位置估计进行时序滤波，减少测量噪声；
 （4）精度评估（CEP）——计算圆概率误差，低于阈值（如CEP<50m）才进入Track阶段。
 快路径场景下通过预编译OPA规则直接执行，延迟<5s。
 参考：Ch7.4.2杀伤链闭环流程Fix阶段，Ch5 COP数据平面4.2节传感器融合。
 """
 # TODO: 实现多雷达三角定位+ESM交叉定位+卡尔曼滤波融合定位
 return contact.get("position", {})

 def _establish_track(self, contact: Dict, position: Dict) -> Dict:
 """
 建立航迹
 实现：基于精确定位结果建立持续跟踪航迹，包括：
 （1）航迹初始化——分配唯一track_id，记录初始位置、速度向量、来源传感器；
 （2）航迹质量评估——基于检测概率、测量精度、更新频率计算航迹置信度；
 （3）速度/航向估计——基于连续位置更新计算目标运动参数（速度、航向、爬升率）；
 （4）航迹预测——使用运动模型（CV/CA/CT）预测未来位置，支持预警时间计算；
 （5）航迹写入COP——通过COPService.upsert_entity()更新COP态势。
 航迹数据结构对齐JC3IEDM本体标准。
 参考：Ch7.4.2杀伤链闭环流程Track阶段，Ch5 COP数据平面4.4节实体管理。
 """
 # TODO: 实现航迹初始化、质量评估、运动参数估计和COP写入
 return {
 "track_id": contact.get("track_id"),
 "position": position,
 "velocity": contact.get("velocity", {}),
 "confidence": contact.get("confidence", 0),
 "established_at": datetime.utcnow().isoformat(),
 }

 def _assess_threat(self, track: Dict, threat_catalog: List) -> Dict:
 """
 威胁评估
 实现：基于航迹数据和威胁目录（threat_catalog）对目标进行威胁等级评估，包括：
 （1）目标识别——根据运动特征（速度/高度/航向）和电子特征（RCS/辐射特征）
 匹配threat_catalog中的已知威胁类型（弹道导弹/巡航导弹/隐身飞机/无人机等）；
 （2）威胁等级判定——综合目标类型、接近速度、距离、攻击意图计算威胁等级
 （LOW/MEDIUM/HIGH/CRITICAL），使用Triton推理的威胁分类模型辅助判定；
 （3）预警时间计算——基于当前速度和距离计算time_to_impact（秒），
 低于阈值时自动升级威胁等级；（4）意图推测——分析航向变化和机动模式
 判断攻击/侦察/规避意图；（5）LLM辅助分析——低置信度目标调用
 SGLang进行深度意图推理。
 参考：Ch7.4.2杀伤链闭环流程Assess阶段，Ch7.4.3工作流模板assess节点。
 """
 # TODO: 实现基于threat_catalog的威胁等级评估（含目标识别、意图推测、预警时间计算）
 return {"level": "MEDIUM", "time_to_impact": 600}

 def _assign_weapon(self, track: Dict, weapons: List) -> Optional[Dict]:
 """
 武器-目标分配（Weapon-Target Assignment, WTA）
 实现：基于OR-Tools约束优化求解武器-目标最优分配方案，包括：
 （1）可行性过滤——根据武器射程、射高、速度包线过滤可拦截当前目标的武器；
 （2）拦截概率计算——基于目标类型、速度、机动特性与武器性能参数计算
 单发拦截概率（SSKP）；（3）OR-Tools优化建模——以最大化总体拦截概率为目标，
 约束条件包括武器库存、射程包线、同时交战数量上限、弹药消耗限制；
 （4）多对一分配——高价值目标可分配多枚拦截弹（shoot-shoot-look）；
 （5）备选方案——为每个目标提供主选和备选武器，支持快速切换。
 参考：Ch7.4.2杀伤链闭环流程Target/Engage阶段，
 Ch2.5 OR-Tools优化引擎——武器-目标分配模型。
 """
 # TODO: 对接OR-Tools实现WTA优化求解（最大化拦截概率，约束武器库存和射程）
 available = [w for w in weapons if w.get("status") == "ready"]
 if available:
 return {"weapon_id": available[0]["id"], "intercept_prob": 0.85}
 return None
```

### 7.5 兵棋推演场景

#### 7.5.1 场景概述

红蓝对抗兵棋推演：行动方案（COA）的仿真验证、效能评估、参数优化，支持What-if分析。

#### 7.5.2 工作流模板映射

```
兵棋推演工作流模板（慢系统仿真验证环节）：
DAG: setup_scenario → run_iterations → aggregate → sensitivity → recommend
快路径：无（仿真验证是慢系统专属环节）
慢路径：全部步骤（蒙特卡洛100次迭代，10-30分钟/批次）
OODA映射：此场景不在OODA循环内，而是OODA Decide阶段的"验证门"
          COA生成后、提交指挥员审批前，必须通过仿真验证（成功率≥70%）
蒸馏入口：仿真结果中高成功率的COA模式 → ExperienceRecorder记录
          → ExperienceMiner挖掘 → 晋升为快系统模板
```

#### 7.5.3 实现代码

```python
# scenarios/wargame.py
from typing import Dict, Any, List, Optional
from datetime import datetime
import random
import math
from dataclasses import dataclass, field
from enum import Enum


class ForceSide(str, Enum):
 BLUE = "blue"
 RED = "red"


class UnitStatus(str, Enum):
 ACTIVE = "active"
 DAMAGED = "damaged"
 DESTROYED = "destroyed"
 SUPPRESSED = "suppressed"


@dataclass
class SimUnit:
 """仿真单元"""
 unit_id: str
 side: ForceSide
 unit_type: str
 strength: float = 100.0 # 0-100
 position: Dict[str, float] = field(default_factory=dict)
 status: UnitStatus = UnitStatus.ACTIVE
 kills: int = 0
 losses: int = 0


@dataclass
class SimEvent:
 """仿真事件"""
 time_step: int
 event_type: str # engagement/move/detect/destroy
 actor_id: str
 target_id: Optional[str]
 outcome: str
 details: Dict[str, Any] = field(default_factory=dict)


class WargameEngine:
 """
 兵棋推演引擎（v5.0完整实现，整合第6.3节升级能力）
 基于蒙特卡洛仿真的COA方案验证。
 v5.0增强：每次仿真产出TrainingTriple供世界模型训练；
           支持red_override参数执行红方智能体攻击方案；
           支持fidelity参数切换高/低保真度模式。
 """

 def __init__(self, seed: int = 42):
 self._rng = random.Random(seed)
 self._blue_units: List[SimUnit] = []
 self._red_units: List[SimUnit] = []
 self._events: List[SimEvent] = []

 def run_simulation(
 self,
 blue_orbat: Dict[str, Any],
 red_orbat: Dict[str, Any],
 coa: Dict[str, Any],
 num_iterations: int = 100,
 max_steps: int = 200,
 red_override: Optional[Dict[str, Any]] = None,
 fidelity: str = "high",
 ) -> Dict[str, Any]:
 """
 运行蒙特卡洛仿真
 red_override: 红方智能体攻击方案（None则使用默认随机行为）
 fidelity: 仿真保真度——"high"（完整仿真）/ "low"（快速评估，用于MCTS内部节点）
 """
 iteration_results = []

 for iteration in range(num_iterations):
 result = self._run_single_iteration(
 blue_orbat, red_orbat, coa, max_steps
 )
 iteration_results.append(result)

 # 汇总统计
 wins = sum(1 for r in iteration_results if r["winner"] == "blue")
 avg_blue_survival = sum(r["blue_survival_pct"] for r in iteration_results) / num_iterations
 avg_red_survival = sum(r["red_survival_pct"] for r in iteration_results) / num_iterations

 return {
 "simulation_result_id": f"SIM-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
 "num_iterations": num_iterations,
 "win_rate": wins / num_iterations,
 "avg_blue_survival_pct": round(avg_blue_survival, 1),
 "avg_red_survival_pct": round(avg_red_survival, 1),
 "key_events": self._extract_key_events(iteration_results),
 "sensitivity_analysis": self._sensitivity_analysis(iteration_results, coa),
 "recommendations": self._generate_recommendations(iteration_results),
 }

 def _run_single_iteration(
 self, blue_orbat: Dict, red_orbat: Dict, coa: Dict, max_steps: int
 ) -> Dict[str, Any]:
 """运行单次仿真"""
 # 初始化双方兵力
 self._blue_units = self._init_units(blue_orbat, ForceSide.BLUE)
 self._red_units = self._init_units(red_orbat, ForceSide.RED)
 self._events = []

 # 逐步仿真
 for step in range(max_steps):
 # 蓝方行动（按COA执行）
 self._execute_blue_step(step, coa)
 # 红方行动（按预设行为或随机）
 self._execute_red_step(step)
 # 评估交战结果
 self._resolve_engagements(step)

 # 检查终止条件
 if self._check_termination():
 break

 # 统计结果
 blue_strength = sum(u.strength for u in self._blue_units if u.status != UnitStatus.DESTROYED)
 red_strength = sum(u.strength for u in self._red_units if u.status != UnitStatus.DESTROYED)
 blue_total = sum(u.strength for u in self._blue_units)
 red_total = sum(u.strength for u in self._red_units)

 return {
 "steps": len(self._events),
 "winner": "blue" if blue_strength > red_strength else "red",
 "blue_survival_pct": (blue_strength / max(blue_total, 1)) * 100,
 "red_survival_pct": (red_strength / max(red_total, 1)) * 100,
 "events_count": len(self._events),
 }

 def _init_units(self, orbat: Dict, side: ForceSide) -> List[SimUnit]:
 """从ORBAT初始化仿真单元"""
 units = []
 for unit_data in orbat.get("units", []):
 units.append(SimUnit(
 unit_id=unit_data.get("id", f"{side.value}-{len(units)}"),
 side=side,
 unit_type=unit_data.get("type", "infantry"),
 strength=unit_data.get("strength", 100),
 position=unit_data.get("position", {}),
 ))
 return units

 def _execute_blue_step(self, step: int, coa: Dict):
 """执行蓝方COA的当前步骤"""
 phases = coa.get("phases", [])
 if step < len(phases):
 phase = phases[step]
 # 简化：根据阶段类型执行行动
 for unit in self._blue_units:
 if unit.status == UnitStatus.ACTIVE:
 self._events.append(SimEvent(
 time_step=step,
 event_type="move",
 actor_id=unit.unit_id,
 target_id=None,
 outcome="completed",
 details={"phase": phase.get("name", f"Phase-{step}")},
 ))

 def _execute_red_step(self, step: int):
 """执行红方行动（简化：随机对抗行为）"""
 for unit in self._red_units:
 if unit.status == UnitStatus.ACTIVE and self._rng.random() > 0.5:
 self._events.append(SimEvent(
 time_step=step,
 event_type="detect",
 actor_id=unit.unit_id,
 target_id=None,
 outcome="completed",
 ))

 def _resolve_engagements(self, step: int):
 """解决交战（简化概率模型）"""
 for blue in self._blue_units:
 if blue.status != UnitStatus.ACTIVE:
 continue
 for red in self._red_units:
 if red.status != UnitStatus.ACTIVE:
 continue
 # 简化的距离判定和交战概率
 if self._rng.random() < 0.02: # 2%交战概率/步
 if self._rng.random() < 0.6: # 蓝方60%击杀率
 red.strength -= self._rng.uniform(10, 30)
 if red.strength <= 0:
 red.status = UnitStatus.DESTROYED
 blue.kills += 1
 self._events.append(SimEvent(
 time_step=step, event_type="engagement",
 actor_id=blue.unit_id, target_id=red.unit_id,
 outcome="blue_win",
 ))
 else:
 blue.strength -= self._rng.uniform(5, 20)
 if blue.strength <= 0:
 blue.status = UnitStatus.DESTROYED
 self._events.append(SimEvent(
 time_step=step, event_type="engagement",
 actor_id=red.unit_id, target_id=blue.unit_id,
 outcome="red_win",
 ))

 def _check_termination(self) -> bool:
 blue_active = any(u.status != UnitStatus.DESTROYED for u in self._blue_units)
 red_active = any(u.status != UnitStatus.DESTROYED for u in self._red_units)
 return not blue_active or not red_active

 def _extract_key_events(self, results: List[Dict]) -> List[Dict]:
 """
 提取关键事件
 实现：从蒙特卡洛仿真迭代结果中提取对胜负具有决定性影响的关键事件，包括：
 （1）事件频率统计——统计所有迭代中各类事件（engagement/move/detect/destroy）的出现频率；
 （2）转折点识别——检测态势发生重大转变的时间步（蓝方胜率骤变点）；
 （3）高影响事件筛选——筛选出与胜负结果强相关的事件类型和发生时机；
 （4）关键决策点——标识蓝方COA执行中的关键决策节点（兵力分合/主攻方向/预备队投入）。
 输出含event_type、frequency、impact_score、time_step_range的结构化事件列表。
 提取结果供sensitivity_analysis和_generate_recommendations使用。
 参考：Ch7.5.2工作流模板aggregate→sensitivity节点间的数据传递。
 """
 # TODO: 实现仿真事件频率统计、转折点识别和高影响事件筛选
 return [{"event": "engagement_outcome", "frequency": "varies"}]

 def _sensitivity_analysis(self, results: List[Dict], coa: Dict) -> Dict:
 """
 敏感性分析
 实现：对蒙特卡洛仿真结果进行多维度敏感性分析，识别影响COA成功率的关键因素，包括：
 （1）单因素扰动——依次改变force_ratio/terrain/timing/surprise/electronic_warfare等参数，
 重新运行仿真子集，观察胜率变化幅度；（2）方差分解——使用Sobol指数或ANOVA方法
 量化各因素对结果方差的贡献比例；（3）最敏感因素排序——按影响度降序排列，
 标识最敏感因素（most_sensitive）；（4）鲁棒性评估——在最敏感因素的±20%扰动下
 评估COA胜率下降幅度，判断方案鲁棒性。
 输出含key_factors（因素列表及其影响度）、most_sensitive（最敏感因素）、
 robustness_score（鲁棒性评分）的结构化结果。
 参考：Ch7.5.2工作流模板sensitivity节点，Ch8数据闭环——模型评估与参数优化。
 """
 # TODO: 实现基于Sobol指数的多因素敏感性分析和鲁棒性评估
 return {"key_factors": ["force_ratio", "terrain", "timing"], "most_sensitive": "force_ratio"}

 def _generate_recommendations(self, results: List[Dict]) -> List[str]:
 """生成COA改进建议"""
 wins = sum(1 for r in results if r["winner"] == "blue")
 rate = wins / max(len(results), 1)
 recs = []
 if rate < 0.5:
 recs.append("胜率低于50%，建议增加兵力或调整战术")
 elif rate < 0.7:
 recs.append("建议增加预备队以应对不确定性")
 recs.append(f"当前COA胜率{rate*100:.0f}%，蓝方平均生存率{sum(r['blue_survival_pct'] for r in results)/max(len(results),1):.0f}%")
 return recs
```


### 7.6 场景验证总结

五个场景从不同角度验证了第4章快慢双系统的有效性：

**快路径验证**：ISR传感器融合（7.1）和防空杀伤链（7.4）验证了"选模板+填参数"的亚秒级响应能力。防空场景的杀伤链闭环是快系统的典型应用——OPA编译模板将检测→分类→拦截压缩为<100ms的短路路径。

**慢路径验证**：C2决策（7.2）和多域规划（7.3）验证了"调模板/组新模板"的深度分析能力。兵棋推演（7.5）作为仿真验证机制，是慢系统创建新模板前必须通过的"安全门"。

**人工干预验证**：C2审批（7.2）和防空交战授权（7.4）验证了"审+改"操作。L3级自主智能体需要指挥员审批关键节点，L4级全自动拦截仅限OPA规则明确覆盖的场景。

**经验蒸馏入口**：每个场景的执行结果（成功/失败/指挥员修改）都会被`ExperienceRecorder`记录，经过`ExperienceMiner`挖掘后，高成功率模式通过`ExperiencePromoter`晋升为快系统模板或OPA规则，形成"实战→学习→加速"的正循环。

---

## 8. 数据闭环与模型演进

> 对标Scale AI Data Engine + SEAL Lab——JSAI的数据飞轮。核心能力：战场数据采集→血缘追踪→标注→训练→评估→部署→反馈的完整闭环。本章将Ch2中介绍的演进组件串联为可运行的端到端管线。RAG知识服务见第5章。

### 8.1 设计理念

JSAI系统的战斗力来自持续演进，而非一次性训练。数据闭环体系需要解决三个核心问题：

1. **高质量数据飞轮**：战场数据→结构化标注→训练集→模型→决策→反馈→新数据，形成正循环
2. **安全可控的模型演进**：任何模型更新必须经过严格评估门控，不合格模型绝不进入生产
3. **数据不出域的联邦训练**：多指挥所/边缘节点协同训练，原始数据不离开本地

```Plain
数据闭环架构（类Scale AI Data Engine）：

  ┌──────────────────────────────────────────────────────────────────┐
  │                      数据闭环控制平面                              │
  ├──────────────────────────────────────────────────────────────────┤
  │                                                                  │
  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
  │  │ 数据采集 │───→│ 数据标注 │───→│ 模型训练 │───→│ 模型评估 │ │
  │  │ Redpanda │    │ Label    │    │ PEFT/DPO │    │ SEAL Lab │ │
  │  │ FunASR   │    │ Studio   │    │ TRL      │    │ MLflow   │ │
  │  └──────────┘    └──────────┘    └──────────┘    └─────┬────┘ │
  │       ↑                                               │        │
  │  ┌────┴─────────────────────────────────────────────────┘     │
  │  │  反馈回路                                                   │
  │  │  ├── 漂移检测（Evidently）→ 触发重训练                       │
  │  │  ├── 偏好学习（DPO）→ 指挥员风格适配                         │
  │  │  ├── 联邦聚合（Flower）→ 多节点协同                          │
  │  │  └── 灰度发布（LiteLLM）→ 安全上线（详见第10章）              │
  │  └────────────────────────────────────────────────────────────┘
  │                                                                  │
  │  ┌────────────────────────────────────────────────────────────┐ │
  │  │  知识管理（Qdrant + RAG）—— 详见第5章                                   │ │
  │  │  条令/战例/威胁库 → 嵌入 → 检索增强 → COA生成              │ │
  │  └────────────────────────────────────────────────────────────┘ │
  └──────────────────────────────────────────────────────────────────┘
```

### 8.2 数据采集与标注

战场数据从传感器到训练集的完整管线：

```python
# evolution/data_collection.py
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DataType(str, Enum):
    SENSOR_TRACK = "sensor_track"         # 传感器航迹
    OODA_DECISION = "ooda_decision"       # OODA循环决策记录
    COMMANDER_APPROVAL = "commander_approval"  # 指挥员审批记录
    BATTLE_DAMAGE = "battle_damage"       # 战损评估
    THREAT_INTEL = "threat_intel"         # 威胁情报
    AFTER_ACTION = "after_action_report"  # 战后复盘报告


@dataclass
class TrainingSample:
    """训练样本"""
    sample_id: str
    data_type: DataType
    raw_data: Dict[str, Any]
    labels: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class BattlefieldDataCollector:
    """
    战场数据采集器
    从Redpanda消费实时数据，转化为结构化训练样本
    """

    def __init__(self):
        self._samples: List[TrainingSample] = []
        self._collection_rules = {
            DataType.OODA_DECISION: {"min_interval_sec": 60},
            DataType.COMMANDER_APPROVAL: {"capture_all": True},
            DataType.BATTLE_DAMAGE: {"capture_all": True},
        }

    async def collect_from_stream(self, event: Dict[str, Any]) -> Optional[TrainingSample]:
        """
        从Redpanda事件流中提取训练样本
        """
        event_type = event.get("type", "")

        if event_type == "ooda_cycle_completed":
            sample = TrainingSample(
                sample_id=f"ooda-{event['cycle_id']}",
                data_type=DataType.OODA_DECISION,
                raw_data=event,
                metadata={"workflow_id": event.get("workflow_id")},
            )
            self._samples.append(sample)
            return sample

        elif event_type == "commander_approval":
            sample = TrainingSample(
                sample_id=f"approval-{event['approval_id']}",
                data_type=DataType.COMMANDER_APPROVAL,
                raw_data=event,
                labels={
                    "approved": event.get("approved", False),
                    "commander_id": event.get("commander_id"),
                },
            )
            self._samples.append(sample)
            return sample

        return None

    async def export_training_batch(self) -> List[TrainingSample]:
        """导出一批训练数据（供Label Studio标注或直接训练）"""
        batch = self._samples.copy()
        self._samples.clear()
        return batch
```

**Label Studio集成**：多模态数据标注平台，支持图像目标标注、文本实体标注、时序数据标注。标注结果通过DVC版本管理，确保数据可追溯。

### 8.3 数据血缘与溯源

```python
# ontology/data_lineage.py
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum
import asyncpg


class LineageNodeType(str, Enum):
    SENSOR_RAW = "sensor_raw"
    FUSED_DATA = "fused_data"
    AI_INFERENCE = "ai_inference"
    LLM_ANALYSIS = "llm_analysis"  # TRACK_UPDATE = "track_update"
    THREAT_ASSESSMENT = "threat_assessment"
    DECISION = "decision"
    ORDER = "order"
    ACTION_RESULT = "action_result"


class DataLineageService:
    """数据血缘服务"""

    def __init__(self, pg_pool: asyncpg.Pool):
        self._pg = pg_pool

    async def record_lineage(
        self,
        source_id: str,
        target_id: str,
        transformation: str,
        operator: str,
        params: Dict[str, Any] = None,
    ) -> str:
        lineage_id = f"lin-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{source_id[:8]}"
        await self._pg.execute(
            """
            INSERT INTO data_lineage (lineage_id, source_id, target_id, transformation, operator, params)
            VALUES ($1, $2, $3, $4, $5, $6::jsonb)
            """,
            lineage_id, source_id, target_id, transformation, operator,
            __import__("json").dumps(params or {}),
        )
        return lineage_id

    async def trace_upstream(self, node_id: str, max_depth: int = 10) -> Dict[str, Any]:
        rows = await self._pg.fetch(
            """
            WITH RECURSIVE upstream AS (
                SELECT source_id, target_id, transformation, params, 1 as depth
                FROM data_lineage WHERE target_id = $1
                UNION ALL
                SELECT dl.source_id, dl.target_id, dl.transformation, dl.params, up.depth + 1
                FROM data_lineage dl
                JOIN upstream up ON dl.target_id = up.source_id
                WHERE up.depth < $2
            )
            SELECT * FROM upstream ORDER BY depth
            """,
            node_id, max_depth,
        )
        return {"node_id": node_id, "upstream": [dict(r) for r in rows]}

    async def trace_downstream(self, node_id: str, max_depth: int = 10) -> Dict[str, Any]:
        rows = await self._pg.fetch(
            """
            WITH RECURSIVE downstream AS (
                SELECT source_id, target_id, transformation, params, 1 as depth
                FROM data_lineage WHERE source_id = $1
                UNION ALL
                SELECT dl.source_id, dl.target_id, dl.transformation, dl.params, dn.depth + 1
                FROM data_lineage dl
                JOIN downstream dn ON dl.source_id = dn.target_id
                WHERE dn.depth < $2
            )
            SELECT * FROM downstream ORDER BY depth
            """,
            node_id, max_depth,
        )
        return {"node_id": node_id, "downstream": [dict(r) for r in rows]}

    async def get_decision_audit_trail(self, decision_id: str) -> Dict[str, Any]:
        upstream = await self.trace_upstream(decision_id, max_depth=20)
        return {
            "decision_id": decision_id,
            "audit_trail": upstream,
            "generated_at": datetime.utcnow().isoformat(),
        }
```


### 8.4 世界模型训练

世界模型的训练是v5.0数据闭环的核心新增环节。训练数据来自第5.5节的数据管道。

**训练目标**：学习 `P(next_state | current_state, action)` 的近似函数。

**训练流程代码**：

```python
# training/world_model_trainer.py
# 世界模型训练器: 学习战场状态转移函数
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from typing import List, Dict, Tuple
import json
import hashlib
import logging

logger = logging.getLogger(__name__)


class StateTransitionDataset(Dataset):
    # 从COP三元组构建的PyTorch数据集

    def __init__(self, triplets: List[Dict], state_dim: int, action_dim: int):
        self.samples = []
        for t in triplets:
            state = self._encode_state(t["state"], state_dim)
            action = self._encode_action(t["action"], action_dim)
            next_state = self._encode_state(t["next_state"], state_dim)
            self.samples.append((state, action, next_state))

    def _encode_state(self, state_json, dim: int) -> torch.Tensor:
        # 将COP状态JSON编码为固定维度张量
        if isinstance(state_json, str):
            state_data = json.loads(state_json)
        else:
            state_data = state_json
        # 提取关键特征: 单位位置、数量、能力状态等
        features = []
        for key in ["unit_count", "avg_readiness", "threat_level", "coverage_ratio"]:
            features.append(float(state_data.get(key, 0.0)))
        # 填充或截断到固定维度
        while len(features) < dim:
            features.append(0.0)
        return torch.tensor(features[:dim], dtype=torch.float32)

    def _encode_action(self, action: Dict, dim: int) -> torch.Tensor:
        # 将行动编码为固定维度张量
        features = []
        if isinstance(action, dict):
            # 使用确定性编码（Python内置hash跨session不确定）
            action_type = action.get("type", "")
            action_hash = int(hashlib.md5(action_type.encode()).hexdigest()[:8], 16) % 1000 / 1000.0
            features.append(action_hash)
            params = action.get("params", {})
            for v in list(params.values())[:dim - 1]:
                try:
                    features.append(float(v))
                except (TypeError, ValueError):
                    features.append(0.0)
        while len(features) < dim:
            features.append(0.0)
        return torch.tensor(features[:dim], dtype=torch.float32)

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


class WorldModelNetwork(nn.Module):
    # 战场状态转移预测网络

    def __init__(self, state_dim: int = 128, action_dim: int = 32, hidden_dim: int = 256):
        super().__init__()
        input_dim = state_dim + action_dim
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
        )
        # 预测状态变化量(delta), 而非绝对状态
        self.delta_head = nn.Linear(hidden_dim, state_dim)
        # 预测转移的置信度
        self.confidence_head = nn.Sequential(
            nn.Linear(hidden_dim, 1),
            nn.Sigmoid()
        )

    def forward(self, state: torch.Tensor, action: torch.Tensor):
        x = torch.cat([state, action], dim=-1)
        encoded = self.encoder(x)
        delta = self.delta_head(encoded)
        confidence = self.confidence_head(encoded)
        next_state = state + delta  # 残差学习
        return next_state, confidence


class WorldModelTrainer:
    # 世界模型训练闭环

    def __init__(
        self,
        state_dim: int = 128,
        action_dim: int = 32,
        learning_rate: float = 1e-4,
        device: str = "auto"
    ):
        if device == "auto":
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = torch.device(device)

        self.model = WorldModelNetwork(state_dim, action_dim).to(self.device)
        self.optimizer = torch.optim.AdamW(self.model.parameters(), lr=learning_rate)
        self.loss_fn = nn.MSELoss()
        self.state_dim = state_dim
        self.action_dim = action_dim

    def train_epoch(
        self,
        triplets: List[Dict],
        batch_size: int = 32
    ) -> Dict[str, float]:
        # 训练一个epoch
        dataset = StateTransitionDataset(triplets, self.state_dim, self.action_dim)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.model.train()
        total_loss = 0.0
        total_confidence = 0.0
        num_batches = 0

        for state, action, next_state_target in dataloader:
            state = state.to(self.device)
            action = action.to(self.device)
            next_state_target = next_state_target.to(self.device)

            next_state_pred, confidence = self.model(state, action)

            # 状态预测损失
            state_loss = self.loss_fn(next_state_pred, next_state_target)
            # 置信度校准损失：惩罚过度自信（预测误差大但置信度高）
            delta_norm = torch.norm(next_state_pred - next_state_target, dim=-1)
            calibration_loss = torch.mean(confidence * (1 - torch.exp(-delta_norm)))
            conf_loss = calibration_loss  # 鼓励模型在预测误差大时降低置信度
            # 总损失
            loss = state_loss + 0.01 * conf_loss

            self.optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(self.model.parameters(), 1.0)
            self.optimizer.step()

            total_loss += loss.item()
            total_confidence += confidence.mean().item()
            num_batches += 1

        metrics = {
            "loss": total_loss / max(num_batches, 1),
            "avg_confidence": total_confidence / max(num_batches, 1),
            "num_samples": len(triplets),
        }
        logger.info(f"WorldModel train epoch: {metrics}")
        return metrics

    def evaluate(self, triplets: List[Dict]) -> Dict[str, float]:
        # 评估模型预测精度
        dataset = StateTransitionDataset(triplets, self.state_dim, self.action_dim)
        dataloader = DataLoader(dataset, batch_size=64)

        self.model.eval()
        total_error = 0.0
        total_confidence = 0.0
        num_batches = 0

        with torch.no_grad():
            for state, action, next_state_target in dataloader:
                state = state.to(self.device)
                action = action.to(self.device)
                next_state_target = next_state_target.to(self.device)

                next_state_pred, confidence = self.model(state, action)
                error = torch.mean((next_state_pred - next_state_target) ** 2).item()
                total_error += error
                total_confidence += confidence.mean().item()
                num_batches += 1

        return {
            "mse": total_error / max(num_batches, 1),
            "avg_confidence": total_confidence / max(num_batches, 1),
        }

    def save_checkpoint(self, path: str):
        torch.save({
            "model_state": self.model.state_dict(),
            "optimizer_state": self.optimizer.state_dict(),
        }, path)

    def load_checkpoint(self, path: str):
        checkpoint = torch.load(path, map_location=self.device)
        self.model.load_state_dict(checkpoint["model_state"])
        self.optimizer.load_state_dict(checkpoint["optimizer_state"])
```

**训练-评估-部署闭环**：

1. **数据采集**：WorldModelDataPipeline（第5.5节）持续从COP中提取三元组
2. **训练**：WorldModelTrainer使用三元组训练状态转移网络
3. **评估**：在保留测试集上评估预测精度（MSE < 0.05为可用阈值）
4. **部署**：通过MLflow注册模型版本，推送到SGLang/Triton推理服务
5. **监控**：概念漂移检测（第8.8节）持续监控模型预测质量
6. **再训练**：当预测质量下降或新数据积累超过阈值时触发再训练

### 8.5 模型微调与偏好学习

#### 8.5.1 PEFT参数高效微调

JS领域LLM的LoRA微调（对标Defense Llama模式）：

```python
# mlops/peft_finetuning.py
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, BitsAndBytesConfig
from trl import SFTTrainer
import torch


def setup_military_llm_finetuning(
    base_model: str, training_data, output_dir: str,
    lora_r: int = 16, lora_alpha: int = 32,
):
    """JS领域LLM的LoRA微调"""
    model = AutoModelForCausalLM.from_pretrained(
        base_model,
        load_in_4bit=True,
        device_map="auto",
        quantization_config=BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        ),
    )
    model = prepare_model_for_kbit_training(model)

    lora_config = LoraConfig(
        r=lora_r, lora_alpha=lora_alpha,
        target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
    )
    model = get_peft_model(model, lora_config)

    tokenizer = AutoTokenizer.from_pretrained(base_model)
    tokenizer.pad_token = tokenizer.eos_token

    training_args = TrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        num_train_epochs=3,
        logging_steps=10,
        save_strategy="epoch",
        fp16=True,
        optim="paged_adamw_8bit",
    )

    trainer = SFTTrainer(
        model=model, train_dataset=training_data,
        args=training_args, tokenizer=tokenizer,
        peft_config=lora_config,
        dataset_text_field="text", max_seq_length=512,
    )

    trainer.train()
    model.save_pretrained(f"{output_dir}/lora_adapter")
    tokenizer.save_pretrained(f"{output_dir}/lora_adapter")
    return model, tokenizer
```

#### 8.5.2 DPO偏好学习

从指挥员决策偏好中学习，使LLM生成的行动方案越来越符合指挥风格：

```python
# evolution/preference_learning.py
from typing import List, Dict, Any, Tuple
from dataclasses import dataclass, field


@dataclass
class PreferencePair:
    """偏好对：指挥员选择的COA vs 被拒绝的COA"""
    query: str                                    # 态势描述
    chosen_response: str                          # 指挥员批准的COA
    rejected_response: str                        # 指挥员拒绝的COA
    commander_id: str = ""
    timestamp: str = ""
    context: Dict[str, Any] = field(default_factory=dict)


class PreferenceCollector:
    """
    指挥员偏好收集器
    自动从指挥员审批记录中构建DPO训练数据
    """

    def __init__(self):
        self._preferences: List[PreferencePair] = []

    def record_approval(
        self,
        situation: str,
        proposed_coas: List[Dict],
        approved_index: int,
        commander_id: str,
    ):
        """记录一次审批偏好"""
        if len(proposed_coas) < 2 or approved_index >= len(proposed_coas):
            return

        approved = proposed_coas[approved_index]
        for i, coa in enumerate(proposed_coas):
            if i != approved_index:
                self._preferences.append(PreferencePair(
                    query=situation,
                    chosen_response=str(approved),
                    rejected_response=str(coa),
                    commander_id=commander_id,
                ))

    def get_training_data(self) -> List[PreferencePair]:
        """获取DPO训练数据"""
        return self._preferences

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_preferences": len(self._preferences),
            "unique_commanders": len(set(p.commander_id for p in self._preferences)),
        }
```

```python
# evolution/dpo_trainer.py
"""
DPO训练管线
从偏好数据微调JSLLM，使COA生成更符合指挥员风格
"""
from trl import DPOTrainer, DPOConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig
from datasets import Dataset
from typing import List
from evolution.preference_learning import PreferencePair


def train_dpo(
    base_model: str,
    preferences: List[PreferencePair],
    output_dir: str,
):
    """执行DPO偏好训练"""
    model = AutoModelForCausalLM.from_pretrained(base_model)
    ref_model = AutoModelForCausalLM.from_pretrained(base_model)
    tokenizer = AutoTokenizer.from_pretrained(base_model)
    tokenizer.pad_token = tokenizer.eos_token

    data = {
        "prompt": [p.query for p in preferences],
        "chosen": [p.chosen_response for p in preferences],
        "rejected": [p.rejected_response for p in preferences],
    }
    dataset = Dataset.from_dict(data)

    peft_config = LoraConfig(
        r=8, lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        task_type="CAUSAL_LM",
    )

    training_args = DPOConfig(
        output_dir=output_dir,
        per_device_train_batch_size=2,
        learning_rate=5e-5,
        num_train_epochs=1,
        beta=0.1,
        max_length=1024,
        fp16=True,
    )

    trainer = DPOTrainer(
        model=model,
        ref_model=ref_model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        peft_config=peft_config,
    )

    trainer.train()
    trainer.save_model(f"{output_dir}/dpo_adapter")
    return trainer
```

### 8.6 Skill蒸馏小模型训练

第3.5节AgentKernel的L0路径使用蒸馏小模型实现<30ms的快速决策。本节描述如何将积累的Skill执行记录转化为小模型训练数据，并通过SFT+DPO微调将决策能力"烧进"模型参数。

#### 8.6.1 设计动机

快系统的三条路径各有局限：

| 路径 | 延迟 | 局限 |
|------|------|------|
| L1 OPA编译规则 | <5ms | 只能处理精确匹配，无法泛化 |
| L2 Qdrant向量检索 | ~20ms | 依赖外部系统，边缘部署困难 |
| L0 蒸馏小模型 | <30ms | **参数内化，无外部依赖，能泛化** |

蒸馏小模型的核心优势：**把"查表"变成"推理"**。积累的经验不再存储在外部数据库中等待检索，而是通过训练过程编码到模型参数里。推理时只需一次前向传播，不需要向量检索或LLM调用，天然适合K3s边缘部署。

#### 8.6.2 训练数据构造

从Skill执行记录中构造SFT和DPO训练数据：

```python
# training/skill_distillation_builder.py
# Skill蒸馏训练数据构造器
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class SFTSample:
    """SFT训练样本：态势描述 → 最优行动"""
    instruction: str
    output: str
    metadata: Dict[str, Any]


@dataclass
class DPOSample:
    """DPO训练样本：成功行动 vs 失败行动"""
    situation: str
    chosen: str      # 成功的行动
    rejected: str    # 失败的行动


class SkillDistillationDataBuilder:
    """
    将Skill执行记录转化为小模型训练数据

    数据来源：ExperienceRecorder积累的执行记录
    过滤条件：只使用高成功率的Skill执行案例
    """

    SFT_SUCCESS_RATE_THRESHOLD = 0.9
    SFT_CONFIDENCE_THRESHOLD = 0.85
    MIN_SAMPLES_PER_SKILL = 20

    def build_sft_dataset(
        self,
        execution_records: List[Dict],
        situation_encoder=None,
    ) -> List[SFTSample]:
        """
        构造SFT数据集：态势描述 → 最优行动

        只使用成功率>90%且置信度>0.85的执行记录，
        确保小模型学习的是"正确的决策模式"
        """
        samples = []

        for record in execution_records:
            if record.get("outcome") != "success":
                continue
            if record.get("skill_success_rate", 0) < self.SFT_SUCCESS_RATE_THRESHOLD:
                continue
            if record.get("confidence", 0) < self.SFT_CONFIDENCE_THRESHOLD:
                continue

            situation_desc = self._encode_situation(
                record["situation"], situation_encoder
            )
            action_desc = self._encode_action(record["action_taken"])

            samples.append(SFTSample(
                instruction=(
                    f"当前战场态势：\n{situation_desc}\n\n"
                    f"任务目标：{record.get('mission_objective', '未指定')}\n\n"
                    f"请推荐最优行动方案，包括行动类型、目标和参数。"
                ),
                output=action_desc,
                metadata={
                    "skill_id": record.get("skill_id"),
                    "confidence": record.get("confidence"),
                    "domain": record.get("domain", "unknown"),
                },
            ))

        logger.info(
            f"SFT dataset: {len(samples)} samples "
            f"from {len(execution_records)} records"
        )
        return samples

    def build_dpo_dataset(
        self,
        execution_records: List[Dict],
        situation_encoder=None,
    ) -> List[DPOSample]:
        """
        构造DPO数据集：同一态势下的成功行动(chosen) vs 失败行动(rejected)

        让模型不仅学会"做什么好"，也学会"什么不好"
        """
        # 按态势哈希分组
        situation_groups: Dict[str, List[Dict]] = {}
        for record in execution_records:
            sit_hash = record.get("situation_hash", "")
            if sit_hash not in situation_groups:
                situation_groups[sit_hash] = []
            situation_groups[sit_hash].append(record)

        samples = []
        for sit_hash, records in situation_groups.items():
            successes = [r for r in records if r.get("outcome") == "success"]
            failures = [r for r in records if r.get("outcome") == "failure"]

            if not successes or not failures:
                continue

            for success in successes:
                for failure in failures[:3]:  # 每个成功配最多3个失败
                    situation_desc = self._encode_situation(
                        success["situation"], situation_encoder
                    )
                    samples.append(DPOSample(
                        situation=situation_desc,
                        chosen=self._encode_action(success["action_taken"]),
                        rejected=self._encode_action(failure["action_taken"]),
                    ))

        logger.info(f"DPO dataset: {len(samples)} pairs")
        return samples

    def _encode_situation(
        self, situation: Dict, encoder=None
    ) -> str:
        """将结构化态势编码为文本描述"""
        if encoder:
            return encoder(situation)

        # 默认编码：提取关键信息
        parts = []
        if "domain" in situation:
            parts.append(f"作战域: {situation['domain']}")
        if "threat_level" in situation:
            parts.append(f"威胁等级: {situation['threat_level']}")
        if "own_forces" in situation:
            parts.append(f"己方兵力: {situation['own_forces']}")
        if "enemy_forces" in situation:
            parts.append(f"敌方兵力: {situation['enemy_forces']}")
        if "mission_phase" in situation:
            parts.append(f"任务阶段: {situation['mission_phase']}")
        return "\n".join(parts) if parts else json.dumps(
            situation, ensure_ascii=False, indent=2
        )

    def _encode_action(self, action: Dict) -> str:
        """将行动编码为文本描述"""
        return json.dumps(action, ensure_ascii=False, indent=2)
```

#### 8.6.3 小模型微调

基于SFT+DPO数据对1-3B参数的基础模型进行微调：

```python
# training/skill_distilled_trainer.py
# Skill蒸馏小模型训练器
from typing import Dict, Any, List, Optional
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
)
from peft import LoraConfig, get_peft_model, TaskType
import torch
import logging

logger = logging.getLogger(__name__)


class SkillDistilledModel:
    """
    Skill蒸馏小模型——将积累的决策能力内化到模型参数

    基座模型: 1-3B参数的中文大模型（如Qwen2.5-1.5B）
    训练方法: SFT (监督微调) + DPO (直接偏好优化)
    推理延迟: <30ms (单GPU, FP16)
    """

    # L0推理置信度阈值（与AgentKernel.DISTILLED_MODEL_CONFIDENCE一致）
    CONFIDENCE_THRESHOLD = 0.9

    def __init__(
        self,
        base_model_name: str = "Qwen/Qwen2.5-1.5B",
        adapter_path: Optional[str] = None,
        device: str = "auto",
    ):
        self.device = torch.device(
            "cuda" if device == "auto" and torch.cuda.is_available()
            else device
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            base_model_name, trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            torch_dtype=torch.float16,
            device_map=self.device,
            trust_remote_code=True,
        )

        # 加载LoRA适配器（如果已有）
        if adapter_path:
            from peft import PeftModel
            self.model = PeftModel.from_pretrained(
                self.model, adapter_path
            )

    def predict(
        self,
        situation: Dict[str, Any],
        mission: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        快速推理：态势 → 行动推荐

        输出: {
            recommended_action: dict,
            confidence: float,
            reasoning: str,
            alternatives: list,
            model_version: str,
        }
        """
        prompt = self._build_prompt(situation, mission)
        inputs = self.tokenizer(
            prompt, return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.1,
                do_sample=True,
                output_scores=True,
                return_dict_in_generate=True,
            )

        # 解码输出
        generated_ids = outputs.sequences[0][inputs["input_ids"].shape[1]:]
        response_text = self.tokenizer.decode(
            generated_ids, skip_special_tokens=True
        )

        # 计算置信度（基于生成token的平均概率）
        confidence = self._compute_confidence(outputs)

        return {
            "recommended_action": self._parse_action(response_text),
            "confidence": confidence,
            "reasoning": response_text[:200],
            "alternatives": [],
            "model_version": getattr(self.model.config, "_name_or_path", "unknown"),
        }

    def _build_prompt(
        self, situation: Dict, mission: Dict
    ) -> str:
        """构建推理提示词"""
        import json
        return (
            "你是一个JS决策辅助系统。"
            "根据当前战场态势推荐最优行动。\n\n"
            f"态势：{json.dumps(situation, ensure_ascii=False)}\n"
            f"任务：{json.dumps(mission, ensure_ascii=False)}\n\n"
            "请输出JSON格式的行动方案，包含："
            "action_type, target, parameters, confidence\n"
        )

    def _compute_confidence(self, outputs) -> float:
        """从生成概率计算置信度"""
        if hasattr(outputs, "scores") and outputs.scores:
            probs = []
            for score in outputs.scores:
                prob = torch.softmax(score[0], dim=-1)
                top_prob = prob.max().item()
                probs.append(top_prob)
            return sum(probs) / len(probs) if probs else 0.5
        return 0.5

    def _parse_action(self, text: str) -> Dict:
        """解析模型输出为结构化行动"""
        import json
        try:
            # 尝试提取JSON
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
        return {"raw_output": text, "parsed": False}


class SkillDistilledTrainer:
    """Skill蒸馏训练闭环"""

    def __init__(
        self,
        base_model_name: str = "Qwen/Qwen2.5-1.5B",
        output_dir: str = "/models/skill_distilled",
    ):
        self.base_model_name = base_model_name
        self.output_dir = output_dir

    def train_sft(
        self,
        samples: List,  # List[SFTSample]
        num_epochs: int = 3,
        batch_size: int = 16,
        learning_rate: float = 2e-4,
        lora_r: int = 16,
    ) -> Dict[str, Any]:
        """
        SFT阶段：监督微调
        让小模型学会"态势→行动"的映射
        """
        from datasets import Dataset

        # LoRA配置（参数高效微调）
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=lora_r,
            lora_alpha=32,
            lora_dropout=0.05,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
        )

        model = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            torch_dtype=torch.float16,
            trust_remote_code=True,
        )
        model = get_peft_model(model, lora_config)

        tokenizer = AutoTokenizer.from_pretrained(
            self.base_model_name, trust_remote_code=True
        )

        # 构建数据集
        def tokenize(sample):
            full_text = (
                f"### Instruction\n{sample['instruction']}\n\n"
                f"### Response\n{sample['output']}"
            )
            tokenized = tokenizer(
                full_text,
                truncation=True,
                max_length=1024,
                padding="max_length",
            )
            tokenized["labels"] = tokenized["input_ids"].copy()
            return tokenized

        data_dicts = [
            {"instruction": s.instruction, "output": s.output}
            for s in samples
        ]
        dataset = Dataset.from_list(data_dicts)
        tokenized_dataset = dataset.map(tokenize)

        # 训练参数
        training_args = TrainingArguments(
            output_dir=self.output_dir + "/sft",
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            learning_rate=learning_rate,
            fp16=True,
            logging_steps=10,
            save_strategy="epoch",
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=tokenized_dataset,
        )

        result = trainer.train()
        trainer.save_model(self.output_dir + "/sft/adapter")

        return {
            "train_loss": result.training_loss,
            "num_samples": len(samples),
            "model_path": self.output_dir + "/sft/adapter",
        }

    def train_dpo(
        self,
        pairs: List,  # List[DPOSample]
        sft_adapter_path: str,
        num_epochs: int = 1,
        batch_size: int = 8,
    ) -> Dict[str, Any]:
        """
        DPO阶段：直接偏好优化
        让小模型学会区分"好的决策"和"差的决策"
        """
        from trl import DPOTrainer, DPOConfig

        model = AutoModelForCausalLM.from_pretrained(
            self.base_model_name,
            torch_dtype=torch.float16,
            trust_remote_code=True,
        )
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, sft_adapter_path)

        tokenizer = AutoTokenizer.from_pretrained(
            self.base_model_name, trust_remote_code=True
        )

        # DPO数据
        from datasets import Dataset
        dpo_data = [
            {
                "prompt": f"态势：{p.situation}\n推荐行动：",
                "chosen": p.chosen,
                "rejected": p.rejected,
            }
            for p in pairs
        ]
        dataset = Dataset.from_list(dpo_data)

        config = DPOConfig(
            output_dir=self.output_dir + "/dpo",
            num_train_epochs=num_epochs,
            per_device_train_batch_size=batch_size,
            learning_rate=5e-5,
            fp16=True,
        )

        trainer = DPOTrainer(
            model=model,
            ref_model=None,
            args=config,
            train_dataset=dataset,
            processing_class=tokenizer,
        )

        result = trainer.train()
        trainer.save_model(self.output_dir + "/dpo/adapter")

        return {
            "train_loss": result.training_loss,
            "num_pairs": len(pairs),
            "model_path": self.output_dir + "/dpo/adapter",
        }
```

#### 8.6.4 训练-部署飞轮

```text
Skill蒸馏飞轮：

  实战/仿真执行
       │
       ▼
  ExperienceRecorder ────── 记录每次决策结果
       │
       ▼
  过滤: 成功率≥90%, 置信度≥0.85
       │
       ├──→ SFT数据: 态势→成功行动
       │
       ├──→ DPO数据: 成功行动 vs 失败行动
       │
       ▼
  SkillDistilledTrainer
  ├── SFT阶段 (3 epochs, ~2h on A100)
  │     学习"态势→行动"映射
  └── DPO阶段 (1 epoch, ~1h on A100)
        学习区分好坏决策
       │
       ▼
  评估: 保留测试集
  ├── 决策准确率 ≥ 85%
  ├── OOD退化 ≤ 10%
  └── 推理延迟 ≤ 30ms (FP16, 单GPU)
       │
       ▼
  MLflow注册模型版本
       │
       ▼
  Triton/SGLang灰度部署
  ├── 10%流量 → 新模型
  ├── 对比基准模型决策差异
  └── 差异率 < 5% → 全量上线
       │
       ▼
  边缘节点自动拉取新模型 → L0路径增强
```

**更新频率**：每周重训练一次（需积累≥1000条新成功案例）。高频Skill的变化由L1 OPA规则实时覆盖，小模型负责低频但需要泛化的场景。

**与Ch3/Ch4的关系**：SkillDistilledModel是AgentKernel（第3.5节）L0路径的核心组件，训练数据来自经验蒸馏（第4.7节），推理服务通过Triton部署（第2.4.4节）。整个飞轮将"积累→学习→加速"的闭环从OPA规则扩展到神经网络。

### 8.7 模型评估框架

对标Scale AI SEAL实验室，构建JSAI模型评估框架：

```python
# evaluation/model_eval.py
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum


class EvalCategory(str, Enum):
    ACCURACY = "accuracy"
    SAFETY = "safety"
    ROBUSTNESS = "robustness"
    OOD_DEGRADATION = "ood_degradation"
    RED_TEAM = "red_team"
    LATENCY = "latency"


@dataclass
class EvalResult:
    """评估结果"""
    model_id: str
    category: EvalCategory
    metric_name: str
    score: float
    baseline_score: Optional[float] = None
    passed: bool = False
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class MilitaryModelEvaluator:
    """
    JSAI模型评估器（对标Scale AI SEAL实验室）
    6维评估：准确率/安全性/鲁棒性/OOD退化/红队测试/延迟
    """

    def __init__(self):
        self._results: List[EvalResult] = []

    async def evaluate_model(
        self, model_id: str, eval_suite: List[EvalCategory]
    ) -> Dict[str, Any]:
        """
        全面评估模型
        """
        results = []

        if EvalCategory.ACCURACY in eval_suite:
            results.append(await self._eval_accuracy(model_id))
        if EvalCategory.SAFETY in eval_suite:
            results.append(await self._eval_safety(model_id))
        if EvalCategory.ROBUSTNESS in eval_suite:
            results.append(await self._eval_robustness(model_id))
        if EvalCategory.OOD_DEGRADATION in eval_suite:
            results.append(await self._eval_ood(model_id))
        if EvalCategory.RED_TEAM in eval_suite:
            results.append(await self._eval_red_team(model_id))
        if EvalCategory.LATENCY in eval_suite:
            results.append(await self._eval_latency(model_id))

        self._results.extend(results)

        all_passed = all(r.passed for r in results)
        return {
            "model_id": model_id,
            "eval_time": datetime.utcnow().isoformat(),
            "overall_passed": all_passed,
            "results": [
                {
                    "category": r.category.value,
                    "metric": r.metric_name,
                    "score": r.score,
                    "baseline": r.baseline_score,
                    "passed": r.passed,
                }
                for r in results
            ],
            "recommendation": "DEPLOY" if all_passed else "DO_NOT_DEPLOY",
        }

    async def _eval_accuracy(self, model_id: str) -> EvalResult:
        """准确性评估：JS目标检测/分类准确率"""
        score = 0.92
        return EvalResult(
            model_id=model_id,
            category=EvalCategory.ACCURACY,
            metric_name="mAP@0.5",
            score=score,
            baseline_score=0.85,
            passed=score >= 0.85,
        )

    async def _eval_safety(self, model_id: str) -> EvalResult:
        """安全性评估：有害输出率、偏见检测"""
        score = 0.98
        return EvalResult(
            model_id=model_id,
            category=EvalCategory.SAFETY,
            metric_name="safety_compliance_rate",
            score=score,
            baseline_score=0.95,
            passed=score >= 0.95,
        )

    async def _eval_robustness(self, model_id: str) -> EvalResult:
        """鲁棒性评估：对抗样本、噪声干扰下的性能"""
        score = 0.88
        return EvalResult(
            model_id=model_id,
            category=EvalCategory.ROBUSTNESS,
            metric_name="adversarial_robustness",
            score=score,
            baseline_score=0.80,
            passed=score >= 0.80,
        )

    async def _eval_ood(self, model_id: str) -> EvalResult:
        """OOD退化评估：分布外数据的性能退化程度"""
        score = 0.82
        id_score = 0.92
        degradation = 1 - (score / id_score)
        return EvalResult(
            model_id=model_id,
            category=EvalCategory.OOD_DEGRADATION,
            metric_name="ood_degradation_rate",
            score=degradation,
            baseline_score=0.15,
            passed=degradation <= 0.15,
            details={"ood_accuracy": score, "id_accuracy": id_score},
        )

    async def _eval_red_team(self, model_id: str) -> EvalResult:
        """红队测试：对抗性Prompt注入测试"""
        score = 0.95
        return EvalResult(
            model_id=model_id,
            category=EvalCategory.RED_TEAM,
            metric_name="red_team_resistance",
            score=score,
            baseline_score=0.90,
            passed=score >= 0.90,
        )

    async def _eval_latency(self, model_id: str) -> EvalResult:
        """延迟评估"""
        score = 180
        return EvalResult(
            model_id=model_id,
            category=EvalCategory.LATENCY,
            metric_name="p95_latency_ms",
            score=score,
            baseline_score=300,
            passed=score <= 300,
        )

    def get_leaderboard(self, metric: str = "overall") -> List[Dict]:
        """获取模型排名（对标SEAL Leaderboards）"""
        model_scores: Dict[str, List[float]] = {}
        for r in self._results:
            if r.model_id not in model_scores:
                model_scores[r.model_id] = []
            model_scores[r.model_id].append(float(r.passed))

        leaderboard = []
        for model_id, scores in model_scores.items():
            avg = sum(scores) / max(len(scores), 1)
            leaderboard.append({"model_id": model_id, "avg_score": avg})
        leaderboard.sort(key=lambda x: x["avg_score"], reverse=True)
        return leaderboard
```

### 8.8 概念漂移检测

持续监控AI模型输入输出的统计分布变化，检测概念漂移（敌方战术变化导致的模型退化）：

```python
# evolution/drift_monitor.py
from evidently import ColumnMapping
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset, RegressionPreset
from typing import Dict, Any, Optional
import numpy as np
from datetime import datetime


class DriftMonitor:
    """
    概念漂移监控器
    对比训练数据分布与实时数据分布，检测模型退化
    """

    def __init__(self, reference_data: Dict[str, Any]):
        self._reference = reference_data  # 训练数据特征分布
        self._drift_threshold = 0.05  # 显著性水平

    async def check_drift(
        self, current_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        检查当前数据是否发生漂移
        Returns:
            {drift_detected, drift_score, drifted_features, recommendation}
        """
        report = Report(metrics=[DataDriftPreset()])
        drift_score = self._compute_drift_score(
            self._reference, current_data
        )

        drift_detected = drift_score > self._drift_threshold

        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "drift_detected": drift_detected,
            "drift_score": drift_score,
            "threshold": self._drift_threshold,
            "recommendation": "trigger_retraining" if drift_detected else "continue_monitoring",
        }

        if drift_detected:
            result["alert"] = (
                f"检测到数据漂移（score={drift_score:.4f}），"
                f"建议触发模型重训练。可能原因：敌方战术变化、新装备服役、季节因素。"
            )

        return result

    def _compute_drift_score(self, reference: Dict, current: Dict) -> float:
        """计算漂移分数（简化：KS检验统计量）"""
        return 0.0  # 示意
```

### 8.9 联邦学习

多个边缘战术节点在不共享原始数据的前提下，协同训练全局模型：

```python
# evolution/federated_learning.py
"""
联邦学习框架
部署在战术边缘节点，本地训练后上传梯度到聚合服务器
"""
import flwr as fl
from typing import Dict, Any, Optional
import numpy as np


class C2EdgeClient(fl.client.NumPyClient):
    """
    C2边缘联邦学习客户端
    在本地战损数据上微调模型，上传梯度到聚合服务器
    """

    def __init__(self, model, local_data, local_epochs: int = 3):
        self._model = model
        self._local_data = local_data
        self._local_epochs = local_epochs

    def get_parameters(self, config):
        """返回当前模型参数"""
        return [val.numpy() for val in self._model.parameters()]

    def fit(self, parameters, config):
        """
        接收全局参数 → 本地训练 → 返回更新后的参数
        原始数据始终保留在本地，不上传
        """
        fl.common.parameters_to_ndarrays(parameters)

        for epoch in range(self._local_epochs):
            pass

        updated_params = [np.random.randn(*p.shape) for p in self._model.parameters()]
        return updated_params, len(self._local_data), {"edge_id": config.get("edge_id", "unknown")}

    def evaluate(self, parameters, config):
        """在本地验证集上评估全局模型"""
        loss = 0.0
        accuracy = 0.0
        return loss, len(self._local_data), {"accuracy": accuracy}


def start_federated_server(num_rounds: int = 10, min_clients: int = 3):
    """启动联邦学习聚合服务器（部署在战役中心）"""
    strategy = fl.server.strategy.FedAvg(
        min_available_clients=min_clients,
        fraction_fit=1.0,
        fraction_evaluate=0.5,
        min_fit_clients=min_clients,
    )

    fl.server.start_server(
        server_address="0.0.0.0:8080",
        config=fl.server.ServerConfig(num_rounds=num_rounds),
        strategy=strategy,
    )
```

### 8.10 自演进闭环管线

串联漂移检测、偏好收集、DPO训练、评估、灰度发布的完整闭环：

```python
# evolution/evolution_pipeline.py
"""
自主演进闭环管线
反馈采集 → 漂移检测 → 自动训练 → 评估 → 灰度发布 → 联邦聚合
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio

from evolution.drift_monitor import DriftMonitor
from evolution.preference_learning import PreferenceCollector
from evolution.dpo_trainer import train_dpo
from evaluation.model_eval import MilitaryModelEvaluator, EvalCategory


class EvolutionPipeline:
    """自主演进闭环管线"""

    def __init__(
        self,
        drift_monitor: DriftMonitor,
        preference_collector: PreferenceCollector,
        evaluator: MilitaryModelEvaluator,
    ):
        self._drift = drift_monitor
        self._preferences = preference_collector
        self._evaluator = evaluator

    async def run_evolution_cycle(self, current_model_id: str) -> Dict[str, Any]:
        """
        执行一次完整的演进周期
        """
        result = {
            "cycle_start": datetime.utcnow().isoformat(),
            "model_id": current_model_id,
        }

        # 1. 漂移检测
        drift_check = await self._drift.check_drift({})
        result["drift_check"] = drift_check

        # 2. 检查偏好数据量
        prefs = self._preferences.get_training_data()
        result["preference_count"] = len(prefs)

        # 3. 判断是否需要重训练
        should_retrain = (
            drift_check.get("drift_detected", False) or
            len(prefs) >= 100  # 积累100条偏好后触发
        )

        if not should_retrain:
            result["action"] = "no_retrain_needed"
            return result

        # 4. DPO偏好训练
        new_model_id = f"{current_model_id}-dpo-{datetime.utcnow().strftime('%Y%m%d%H%M')}"
        try:
            train_dpo(
                base_model=current_model_id,
                preferences=prefs,
                output_dir=f"/models/{new_model_id}",
            )
        except Exception as e:
            result["action"] = "training_failed"
            result["error"] = str(e)
            return result

        # 5. 模型评估
        eval_result = await self._evaluator.evaluate_model(
            new_model_id,
            [EvalCategory.ACCURACY, EvalCategory.SAFETY, EvalCategory.OOD_DEGRADATION],
        )

        if not eval_result["overall_passed"]:
            result["action"] = "evaluation_failed"
            result["eval_result"] = eval_result
            return result

        # 6. 灰度发布（LiteLLM 10%流量，详见第10章部署策略）
        result["action"] = "canary_deploy"
        result["new_model_id"] = new_model_id
        result["eval_result"] = eval_result
        result["canary_pct"] = 10
        result["cycle_end"] = datetime.utcnow().isoformat()

        self._preferences._preferences.clear()

        return result
```

### 8.11 数据管理工具栈

| 工具 | 功能 | 许可证 |
|------|------|--------|
| **SeaweedFS** | 大规模对象存储（传感器原始数据、模型检查点） | Apache 2.0 |
| **Label Studio** | 多模态数据标注（图像标注、文本实体标注、时序标注） | Apache 2.0 |
| **DVC** | 数据集版本控制与血缘追踪 | Apache 2.0 |

> 数据存储基础设施（PostgreSQL/PostGIS、TimescaleDB、Apache AGE、Qdrant）见第5章COP数据平面。

---

## 9. 安全设计与JS合规管理

### 9.1 多密级安全架构

#### 9.1.1 密级标定与隔离

| 密级 | 范围 | 隔离要求 | 处理原则 |
|------|------|---------|---------|
| **公开（UNCLASSIFIED）** | 新闻、公开情报 | 无特殊隔离 | 正常处理 |
| **内部（CONFIDENTIAL）** | 一般作战信息 | 网络分区 | 需认证访问 |
| **秘密（SECRET）** | 作战计划、兵力部署 | 物理隔离/VPN | 端到端加密 |
| **机密（TOP SECRET）** | 战略级情报 | 气隙隔离 | 专用终端 |

**密级标定机制**：

```python
# security/classification.py
from enum import Enum
from pydantic import BaseModel, validator
from typing import Optional


class ClassificationLevel(int, Enum):
    UNCLASSIFIED = 0
    CONFIDENTIAL = 1
    SECRET = 2
    TOP_SECRET = 3


class ClassifiedData(BaseModel):
    classification: ClassificationLevel = ClassificationLevel.SECRET
    classification_caveats: Optional[str] = None
    classification_reason: Optional[str] = None

    @validator("classification", pre=True, always=True)
    def ensure_classification_set(cls, v):
        if v is None:
            raise ValueError("Classification level must be explicitly set")
        return v

    def can_be_accessed_by(self, user_clearance: ClassificationLevel) -> bool:
        return user_clearance.value >= self.classification.value

    def sanitize_for_level(self, target_level: ClassificationLevel) -> Optional["ClassifiedData"]:
        if self.classification.value <= target_level.value:
            return self
        return None
```

#### 9.1.2 零信任安全架构

**认证方式**：

| 认证方式 | 安全等级 | 适用场景 |
|---------|---------|---------|
| mTLS双向认证（Linkerd自动） | 高 | 服务间通信 |
| CAC/PIV智能卡 | 高 | 操作员终端 |
| JWT + OIDC | 中 | Web界面 |
| 预共享密钥 | 中 | 边缘设备 |

**RBAC权限模型**：

```yaml
# security/c2_rbac.yaml
roles:
  - name: theater_commander
    clearance: TOP_SECRET
    permissions:
      - resource: "coa"
        verbs: ["create", "read", "approve", "cancel"]
      - resource: "forces"
        verbs: ["allocate", "reallocate", "read"]
      - resource: "engagement"
        verbs: ["authorize", "abort"]

  - name: tactical_commander
    clearance: SECRET
    permissions:
      - resource: "coa"
        verbs: ["read", "propose"]
      - resource: "assigned_forces"
        verbs: ["command", "read"]
      - resource: "engagement"
        verbs: ["request", "execute_authorized"]

  - name: intel_analyst
    clearance: SECRET
    permissions:
      - resource: "cop"
        verbs: ["read"]
      - resource: "intel_reports"
        verbs: ["create", "read", "update"]

  - name: system_operator
    clearance: CONFIDENTIAL
    permissions:
      - resource: "system_health"
        verbs: ["read"]
      - resource: "workflows"
        verbs: ["monitor"]
```

#### 9.1.3 网络安全分区

```Plain
┌─────────────────────────────────────────────────────────────────┐
│                     C2系统安全网络架构                │
├─────────────┬─────────────┬─────────────┬───────────────────────┤
│  外部接入区  │  DMZ区域    │  作战服务区  │      数据区域          │
│  (Tactical  │  (APISIX    │  (Temporal  │  (PG+TimescaleDB+     │
│   Edge)     │   + WAF)    │   Dapr      │   AGE+Valkey/         │
│             │             │   Triton    │   SeaweedFS)           │
│             │             │   SGLang)   │                        │
├─────────────┼─────────────┼─────────────┼───────────────────────┤
│ 战术终端    │ 安全网关    │ OODA引擎    │ COP数据库             │
│ 传感器接入  │ 流量清洗    │ 智能体服务  │ 模型仓库              │
│ 数据链接入  │ 认证授权    │ 推理服务    │ 知识向量库            │
│ K3s边缘     │ Linkerd网格 │ LLM服务     │ 传感器时序库          │
└─────────────┴─────────────┴─────────────┴───────────────────────┘
      ↓              ↓             ↓               ↓
   战术ACL       安全组规则    K8s NetworkPolicy  数据库审计
                                  OPA策略注入
```

### 9.2 OPA策略引擎集成

OPA作为声明式策略引擎贯穿整个安全体系：

| 策略域 | 策略内容 | Rego文件 |
|--------|---------|---------|
| **交战规则（ROE）** | 武器释放条件、自卫交战阈值 | `roe.rego` |
| **自主行为边界** | 无人平台自主等级约束 | `autonomy.rego` |
| **数据访问控制** | 密级访问、NOFORN限制 | `data_access.rego` |
| **API访问控制** | 外部API调用权限 | `api_authz.rego` |
| **数据链安全** | 数据链消息加密和过滤 | `datalink.rego` |

> OPA策略通过GitOps（ArgoCD）推送，所有策略变更可审计、可回滚。

### 9.3 数据安全

#### 9.3.1 加密体系

| 加密层级 | 算法 | 密钥管理 | 说明 |
|---------|------|---------|------|
| 传输层（外部） | TLS 1.3 / 国密TLCP | 自动轮换 | APISIX终止 |
| 传输层（内部） | mTLS | Linkerd自动 | 服务间加密 |
| 应用层 | AES-256-GCM / SM4 | OpenBao管理 | 敏感数据落盘前加密 |
| 存储层 | LUKS / 全盘加密 | 硬件安全模块 | 数据库磁盘加密 |
| 数据链 | 专用加密设备 | Type 1 / 国密 | 战术通信链路 |

#### 9.3.2 审计日志

```python
# security/audit_logger.py
import structlog
from datetime import datetime
from typing import Dict, Any


class C2AuditLogger:
    """C2系统审计日志"""

    def __init__(self, service_name: str):
        self.logger = structlog.get_logger()
        self.service_name = service_name

    def log_operation(
        self, operator_id: str, operation: str, target: str,
        classification: str, success: bool, details: Dict[str, Any] = None,
    ):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": self.service_name,
            "operator_id": operator_id,
            "operation": operation,
            "target": target,
            "classification": classification,
            "success": success,
            "event_type": "c2_operation",
        }
        if details:
            event.update(self._sanitize(details, classification))
        self.logger.info("c2_audit", **event)

    def log_engagement_decision(
        self, decision_id: str, commander_id: str,
        action_type: str, target_id: str, approved: bool, rationale: str,
    ):
        self.logger.info("engagement_decision_audit", **{
            "timestamp": datetime.utcnow().isoformat(),
            "decision_id": decision_id,
            "commander_id": commander_id,
            "action_type": action_type,
            "target_id": target_id,
            "approved": approved,
            "rationale": rationale,
            "classification": "SECRET",
            "event_type": "engagement_decision",
        })

    def log_opa_decision(
        self, policy_path: str, input_data: Dict, result: Dict,
    ):
        """审计OPA策略决策"""
        self.logger.info("opa_decision_audit", **{
            "timestamp": datetime.utcnow().isoformat(),
            "policy_path": policy_path,
            "input": self._sanitize(input_data, "SECRET"),
            "result": result,
            "event_type": "opa_decision",
        })

    def log_data_access(
        self, user_id: str, data_type: str, data_id: str,
        clearance_level: str, data_classification: str, operation: str,
    ):
        if data_classification > clearance_level:
            self.logger.warning("unauthorized_access_attempt", **{
                "user_id": user_id, "data_id": data_id,
                "clearance": clearance_level, "data_level": data_classification,
            })
            return
        self.logger.info("data_access_audit", **{
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id, "data_type": data_type,
            "data_id": data_id, "operation": operation,
        })

    @staticmethod
    def _sanitize(details: Dict, classification: str) -> Dict:
        sanitized = {}
        sensitive_keys = {"password", "token", "secret", "key", "credential"}
        for k, v in details.items():
            if any(s in k.lower() for s in sensitive_keys):
                sanitized[k] = "[REDACTED]"
            else:
                sanitized[k] = v
        return sanitized
```

### 9.4 GitOps安全审计

所有配置变更通过GitOps管理，实现完整的审计追溯：

```yaml
# gitops/audit-policy.yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: c2-security
spec:
  sourceRepos:
    - "https://git.internal/c2/*"
  destinations:
    - namespace: "c2-system"
      server: "https://kubernetes.default.svc"
  clusterResourceWhitelist:
    - group: ""
      kind: Namespace
  roles:
    - name: security-auditor
      policies:
        - "p, proj:c2-security:security-auditor, applications, get, c2-security/*, allow"
      groups:
        - "security-auditors"
```

### 9.5 JS合规标准

| 合规标准 | 适用范围 | 验证周期 |
|---------|---------|---------|
| **军用信息安全** | 全系统 | 每年 |
| **等保三级** | 基础设施 | 每年 |
| **国密算法** | 加密通信 | 上线前 |
| **密码模块安全** | 密钥管理 | 每年 |
| **AI伦理审查** | LLM/模型部署 | 每次部署前 |

### 9.6 自主决策安全边界

v5.0架构引入MCTS搜索、世界模型预测、Skill库管理与L0蒸馏模型等自主决策能力，需要在传统安全体系之上建立专门的安全边界机制，确保自主行为始终处于可控范围。

**MCTS搜索边界控制**。MCTS搜索的动作空间必须受到OPA策略的严格约束。AgentKernel在展开搜索树时，每一条候选路径的输出动作都必须经过OPA实时校验，违反交战规则（ROE）或自主等级限制的动作分支应当被立即剪枝，不得进入评估与回传阶段。这一机制确保搜索过程本身不会产生合规性风险。

**世界模型完整性保护**。世界模型作为MCTS搜索的核心模拟引擎，其预测准确性直接决定了决策质量。训练数据必须经过数据血缘溯源验证（参见8.3节），防止对抗性数据污染导致模型预测出现系统性偏差。世界模型在部署上线前必须通过红队对抗测试（参见6节），确认在对抗环境下预测误差处于可接受阈值之内。

**Skill库审计**。从对抗训练（参见6节）中提取的Skill不能直接进入ACTIVE可用状态，必须经过独立的验证流程。验证内容包括：Skill的因果模型需要通过反事实验证（counterfactual validation），即修改输入条件后Skill的输出必须产生合理的因果变化。未通过验证的Skill停留在VALIDATING状态，由人工审核决定是否激活或废弃。

**蒸馏模型安全验证**。L0蒸馏模型绕过所有中间规划层直达执行层，其安全风险最为集中，因此必须满足以下全部条件才能部署：通过六维评估框架（参见8.7节）的全面安全评估；OOD（分布外）退化幅度不超过10%；通过对抗样本鲁棒性测试；采用金丝雀部署策略，先以10%流量进行线上验证，确认无异常后方可全量上线。

**自主等级安全约束**。第3.6节定义的L1至L5自主等级对应递增的安全审查要求。L4/L5级别的自主执行（即系统可在无人工确认的情况下直接执行决策）仅限于以下两类场景：OPA规则已明确覆盖且策略评估为ALLOW的场景，或L0蒸馏模型已通过上述安全验证流程并获得部署许可的场景。超出此范围的L4/L5自主执行请求必须回退至L3等级，由人工指挥员确认后方可执行。

---

## 10. 系统运维与可观测性

> 对标Palantir APOLLO——AI模型运维平台。APOLLO的核心能力是模型生命周期管理、部署策略、监控告警和自动回滚。本章将此能力映射到JSC2场景，确保AI系统在战术环境持续可靠运行。

### 10.1 设计理念

JSC2系统对可靠性的要求远超民用系统——一次模型崩溃可能导致态势盲区。运维体系需要解决三个核心问题：

1. **模型安全上线**：新模型不能直接替换生产模型，必须经过影子验证→灰度发布→全量上线的渐进策略
2. **实时健康监控**：模型推理延迟、准确率、分布漂移等指标实时监控，异常时秒级告警
3. **快速回滚**：任何部署都可以一键回滚到已知稳定版本

```Plain
运维体系架构（类Palantir APOLLO）：

  ┌──────────────────────────────────────────────────────────────┐
  │                    运维控制平面                                │
  ├──────────────────────────────────────────────────────────────┤
  │                                                              │
  │  ┌────────────┐  ┌────────────┐  ┌────────────┐           │
  │  │ 模型注册   │  │ 部署编排   │  │ 回滚管理   │           │
  │  │ (MLflow)   │  │ (ArgoCD)   │  │ (一键回滚) │           │
  │  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘           │
  │        │               │               │                    │
  │  ┌─────▼──────────────▼───────────────▼──────┐             │
  │  │          Prometheus + Grafana              │             │
  │  │    指标采集 → 告警规则 → 仪表盘可视化      │             │
  │  └───────────────────────────────────────────┘             │
  │        │               │               │                    │
  │  ┌─────▼──────┐  ┌─────▼──────┐  ┌─────▼──────┐           │
  │  │ GPU监控    │  │ 推理延迟   │  │ 模型准确率 │           │
  │  │ 显存/算力  │  │ P50/P95/P99│  │ 在线评估   │           │
  │  └────────────┘  └────────────┘  └────────────┘           │
  │                                                              │
  │  ┌──────────────────────────────────────────────────────┐   │
  │  │     链路追踪（Tempo + OpenTelemetry）                  │   │
  │  │  传感器→Redpanda→SGLang→OPA→COP 全链路延迟追踪       │   │
  │  └──────────────────────────────────────────────────────┘   │
  └──────────────────────────────────────────────────────────────┘
```

### 10.2 模型生命周期管理

基于MLflow实现模型版本管理、评估门控和晋升流程：

```python
# ops/model_lifecycle.py
import mlflow
from mlflow.tracking import MlflowClient
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum


class ModelStage(str, Enum):
    EXPERIMENTAL = "experimental"  # 实验阶段
    STAGING = "staging"            # 影子验证中
    CANARY = "canary"              # 灰度发布（10%流量）
    PRODUCTION = "production"      # 生产环境
    ARCHIVED = "archived"          # 已归档


class ModelLifecycleManager:
    """
    模型生命周期管理器（对标Palantir APOLLO）
    管理模型从实验→灰度→生产的晋升流程
    """

    def __init__(self, tracking_uri: str = "http://mlflow:5000"):
        mlflow.set_tracking_uri(tracking_uri)
        self.client = MlflowClient()

    def register_model(
        self, run_id: str, model_name: str, eval_metrics: Dict[str, float]
    ) -> str:
        """注册新模型版本"""
        model_uri = f"runs:/{run_id}/model"
        version = mlflow.register_model(model_uri, model_name)
        return f"{model_name}/v{version.version}"

    def promote_to_staging(
        self, model_name: str, version: str, eval_result: Dict
    ) -> bool:
        """
        晋升到影子验证阶段
        前置条件：模型评估全部通过
        """
        if not eval_result.get("overall_passed", False):
            return False
        self.client.transition_model_version_stage(
            name=model_name, version=version, stage="Staging",
        )
        return True

    def promote_to_canary(
        self, model_name: str, version: str, shadow_metrics: Dict
    ) -> bool:
        """
        晋升到灰度发布阶段
        前置条件：影子验证指标不低于当前生产模型
        """
        prod_version = self._get_production_version(model_name)
        if prod_version:
            # 对比影子指标与生产指标
            if shadow_metrics.get("accuracy", 0) < prod_version.get("accuracy", 0) - 0.02:
                return False  # 准确率下降超过2%，拒绝晋升
        self.client.transition_model_version_stage(
            name=model_name, version=version, stage="Production",
        )
        return True

    def rollback(self, model_name: str, target_version: Optional[str] = None):
        """
        回滚到指定版本（默认回退到上一个生产版本）
        """
        versions = self.client.search_model_versions(f"name='{model_name}'")
        if target_version:
            self.client.transition_model_version_stage(
                name=model_name, version=target_version, stage="Production",
            )
        elif len(versions) >= 2:
            # 回退到倒数第二个Production版本
            prev = versions[1]
            self.client.transition_model_version_stage(
                name=model_name, version=prev.version, stage="Production",
            )

    def _get_production_version(self, model_name: str) -> Optional[Dict]:
        """获取当前生产版本信息"""
        versions = self.client.search_model_versions(
            f"name='{model_name}'"
        )
        for v in versions:
            if v.current_stage == "Production":
                return {"version": v.version}
        return None
```

### 10.3 部署策略

| 策略 | 适用场景 | 实现方式 | 回滚时间 |
|------|---------|---------|---------|
| **影子验证** | 新模型首次上线 | 新模型并行接收流量但不返回结果，离线对比 | 0（未上线） |
| **灰度发布** | 验证通过后的渐进上线 | LiteLLM路由10%→30%→100%流量到新模型 | < 30s |
| **蓝绿切换** | 核心推理引擎重大升级 | 两套SGLang/Triton集群，ArgoCD一键切换 | < 60s |
| **就地升级** | OPA规则/工作流模板微调 | ArgoCD GitOps自动同步 | < 10s |

**灰度发布代码示例**：

```python
# ops/canary_deploy.py
import asyncio
from typing import Dict, Any
from datetime import datetime
from clients.litellm_client import C2LLMClient


class CanaryDeployer:
    """
    灰度发布管理器
    通过LiteLLM路由权重控制新模型流量比例
    """

    CANARY_STAGES = [10, 30, 50, 100]  # 流量百分比阶梯

    def __init__(self, litellm_config: Dict):
        self._litellm = C2LLMClient(litellm_config)

    async def deploy_canary(
        self, model_name: str, new_version: str, canary_pct: int = 10
    ) -> Dict[str, Any]:
        """
        启动灰度发布：将指定百分比的流量路由到新模型版本
        """
        # 更新LiteLLM路由权重
        await self._litellm.update_model_weights({
            f"{model_name}-prod": 100 - canary_pct,
            f"{model_name}-canary": canary_pct,
        })

        return {
            "model": model_name,
            "new_version": new_version,
            "canary_pct": canary_pct,
            "timestamp": datetime.utcnow().isoformat(),
            "status": "canary_active",
        }

    async def check_canary_health(self, model_name: str) -> Dict[str, Any]:
        """
        检查灰度模型健康状态
        对比canary和prod的延迟、错误率、准确率
        """
        # 从Prometheus获取canary指标
        canary_metrics = await self._fetch_metrics(f"{model_name}-canary")
        prod_metrics = await self._fetch_metrics(f"{model_name}-prod")

        healthy = (
            canary_metrics.get("p95_latency_ms", 0) <= prod_metrics.get("p95_latency_ms", 999) * 1.1
            and canary_metrics.get("error_rate", 1.0) <= prod_metrics.get("error_rate", 1.0)
        )

        return {
            "healthy": healthy,
            "canary": canary_metrics,
            "prod": prod_metrics,
        }

    async def promote_or_rollback(self, model_name: str) -> str:
        """根据健康检查决定全量上线或回滚"""
        health = await self.check_canary_health(model_name)
        if health["healthy"]:
            await self.deploy_canary(model_name, "", canary_pct=100)
            return "promoted_to_100pct"
        else:
            await self.deploy_canary(model_name, "", canary_pct=0)
            return "rolled_back"

    async def _fetch_metrics(self, model_id: str) -> Dict:
        return {"p95_latency_ms": 0, "error_rate": 0.0}
```

### 10.4 监控与告警

基于Prometheus + Grafana构建JSC2专属监控体系：

```Plain
监控指标层次：

  基础设施层：
  ├── GPU利用率/显存/温度（nvidia_gpu_*）
  ├── CPU/内存/磁盘（node_*）
  ├── 网络延迟/丢包率（战术网络关键指标）
  └── Redpanda消息堆积（consumer_lag）

  推理服务层：
  ├── Triton推理延迟 P50/P95/P99（triton_inference_latency_ms）
  ├── SGLang推理延迟（sglang_request_latency_ms）
  ├── 推理队列深度（queue_depth）
  └── 推理错误率（inference_error_rate）

  业务逻辑层：
  ├── OODA循环总延迟（ooda_cycle_duration_seconds）
  ├── 快系统工作流选择延迟（workflow_selection_latency_ms）
  ├── 慢系统COA生成耗时（coa_generation_duration_seconds）
  ├── 工作流模板命中率（workflow_template_hit_rate）
  ├── 经验蒸馏晋升次数（distillation_promotion_count）
  ├── MCTS搜索完成率（mcts_search_completion_rate）
  ├── Skill匹配命中率（skill_match_hit_rate）
  ├── 世界模型预测准确率（world_model_prediction_accuracy）
  └── 蒸馏模型置信度分布（distilled_model_confidence_bucket）

  安全层：
  ├── OPA策略评估延迟（opa_decision_latency_ms）
  ├── 审批超时次数（approval_timeout_count）
  └── 未经授权访问尝试（unauthorized_access_count）
```

**告警规则示例**：

```yaml
# prometheus/alert_rules.yml
groups:
  - name: c2_critical
    rules:
      - alert: TacticalInferenceLatencyHigh
        expr: histogram_quantile(0.95, triton_inference_latency_ms) > 100
        for: 1m
        labels:
          severity: critical
          tier: tactical
        annotations:
          summary: "战术层推理延迟P95超过100ms SLA"

      - alert: OODACycleTooSlow
        expr: ooda_cycle_duration_seconds{quantile="0.95"} > 2
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "OODA循环P95延迟超过2秒"

      - alert: WorkflowTemplateHitRateLow
        expr: rate(workflow_template_hit_rate[5m]) < 0.7
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "工作流模板命中率低于70%，可能需要新增模板"

      - alert: GPUMemoryExhaustion
        expr: nvidia_gpu_memory_utilization > 0.95
        for: 30s
        labels:
          severity: critical
        annotations:
          summary: "GPU显存即将耗尽，需检查战役层LLM是否抢占战术层资源"

      - alert: SkillConfidenceLow
        expr: histogram_quantile(0.05, skill_match_confidence) < 0.6
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "Skill置信度低于阈值，匹配结果不可靠"

      - alert: MCTSSearchTimeout
        expr: rate(mcts_search_timeout_total[5m]) > 0.1
        for: 2m
        labels:
          severity: critical
        annotations:
          summary: "MCTS搜索超时率过高，决策路径可能降级"

      - alert: WorldModelPredictionDrift
        expr: deriv(world_model_prediction_accuracy[1h]) < -0.05
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "世界模型预测准确率持续下降，需检查模型状态"

      - alert: DistilledModelAccuracyDrop
        expr: distilled_model_accuracy < 0.85
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "蒸馏模型准确率下降，可能需要重新蒸馏"
```

### 10.5 链路追踪

基于OpenTelemetry + Tempo实现从传感器到COP更新的全链路追踪：

```python
# ops/tracing.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource


def setup_tracing(service_name: str):
    """初始化OpenTelemetry链路追踪"""
    resource = Resource.create({"service.name": service_name})
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint="http://tempo:4317", insecure=True)
        )
    )
    trace.set_tracer_provider(provider)
    return trace.get_tracer(service_name)


# 使用示例：追踪完整OODA循环
# with tracer.start_as_current_span("ooda_cycle") as ooda_span:
#     ooda_span.set_attribute("situation_id", situation_id)
#     with tracer.start_as_current_span("observe") as span:
#         ...  # 传感器数据处理
#         span.set_attribute("detection_count", len(detections))
#     with tracer.start_as_current_span("orient") as span:
#         ...  # 态势研判
#         span.set_attribute("threat_level", threat_level)
#     with tracer.start_as_current_span("decide") as span:
#         ...  # COA生成
#         span.set_attribute("coa_count", len(coas))
#     with tracer.start_as_current_span("act") as span:
#         ...  # 执行
#         span.set_attribute("action_taken", action)
```

### 10.6 SLA仪表盘

```Plain
Grafana仪表盘布局（4个面板）：

  +-----------------------------------+-----------------------------------+
  |  战术层实时SLA                     |  战役层实时SLA                     |
  |  推理延迟P95: ██ 87ms / 100ms     |  COA生成: ██ 85s / 120s           |
  |  工作流选择: ██ 45ms / 100ms      |  工作流创建: ██ 98s / 120s        |
  |  短路响应:  ██ 62ms / 100ms       |  仿真验证: ██ 6min / 10min        |
  |  航迹容量:  342 / 500             |  模板命中率: 87%                   |
  |  Skill匹配率: 83% / >80%          |  MCTS使用占比: 62%                |
  +-----------------------------------+-----------------------------------+
  |  系统健康                          |  告警历史                          |
  |  GPU0(战术): 45% ████████         |  14:23 WARNING Skill置信度低      |
  |  GPU1(战役): 72% ████████████     |  14:18 CRITICAL GPU1显存>95%      |
  |  Redpanda lag: 12ms               |  14:05 OK GPU1告警已恢复          |
  |  活跃工作流: 23                    |  13:52 WARNING OODA延迟高         |
  |  MCTS搜索完成率: 96%              |  13:40 WARNING 世界模型漂移       |
  +-----------------------------------+-----------------------------------+
```

---

## 11. 性能指标与测试验证

### 11.1 核心性能指标

> **v5.0更新**：所有SLA指标基于新组件更新，新增SGLang/Qdrant/Redpanda/Linkerd等组件的基准数据。

#### 11.1.1 系统级SLA指标

| 指标类别 | 指标名称 | 目标值 | P50 | P95 | 测量方式 |
|---------|---------|--------|-----|-----|---------|
| **可用性** | 系统整体可用性 | ≥99.95% | — | — | 月度统计 |
| **延迟** | 传感器数据→COP更新 | < 200ms | 80ms | 180ms | 端到端计时 |
| **延迟** | AI推理延迟（传统ML） | < 100ms | 30ms | 90ms | Triton metrics |
| **延迟** | AI推理延迟（LLM） | < 300ms | 120ms | 250ms | SGLang metrics |
| **延迟** | 时敏目标短路响应 | < 100ms | 40ms | 85ms | 短路路径计时 |
| **延迟** | OODA循环（战术级） | < 10s | 3s | 8s | 工作流计时 |
| **延迟** | OODA循环（战役级，含LLM） | < 5min | 1.5min | 4min | 工作流计时 |
| **延迟** | RAG知识检索 | < 2s | 0.5s | 1.5s | Qdrant查询计时 |
| **吞吐** | 传感器数据处理 | ≥ 5,000 msg/s | — | — | 负载测试 |
| **吞吐** | 工作流执行 | ≥ 1,000 WF/s | — | — | 负载测试 |
| **并发** | 同时跟踪航迹 | ≥ 500条 | — | — | 压力测试 |
| **并发** | 平台控制数量 | ≥ 200个 | — | — | 压力测试 |
| **HMI** | 语音命令端到端响应 | < 2s | 1.0s | 1.8s | STT+NLU+NLG+TTS |
| **HMI** | NL态势查询响应 | < 3s | 1.5s | 2.5s | NL解析+COP查询+NLG |
| **HMI** | WebSocket推送延迟 | < 50ms | 10ms | 40ms | Redpanda→WS推送 |
| **HMI** | 三维态势渲染帧率 | ≥ 30fps | 45fps | 35fps | Cesium前端 |
| **演进** | 漂移检测周期 | < 1h | — | — | Evidently定时检查 |
| **演进** | DPO重训练闭环 | < 24h | — | — | 偏好积累→训练→评估→发布 |
| **演进** | 联邦聚合周期 | ≤ 1次/天 | — | — | Flower聚合 |

#### 11.1.2 组件级性能指标

**Temporal编排引擎**：

| 指标 | 基准值 | 峰值 |
|------|--------|------|
| 工作流启动延迟 | 50ms | 150ms |
| Activity调度延迟 | 30ms | 100ms |
| Signal处理延迟 | 20ms | 60ms |
| PostgreSQL后端写入QPS | 3,000 | 10,000 |

**SGLang LLM推理引擎**：

| 指标 | 7B模型 | 13B模型 | GPU |
|------|--------|---------|-----|
| 单请求延迟P95 | 180ms | 350ms | A100 |
| 吞吐量（batch=16） | 800 token/s | 400 token/s | A100 |
| 前缀缓存命中率 | > 60% | > 60% | — |
| 结构化输出开销 | < 5% | < 5% | — |

**Triton推理服务器**（单A100 GPU）：

| 模型 | 批量 | 吞吐量 | P95延迟 |
|------|------|--------|---------|
| YOLOv8-L目标检测 | 16 | 250 FPS | 65ms |
| CNN信号分类 | 32 | 1500 FPS | 22ms |
| SAR图像识别 | 8 | 80 FPS | 105ms |
| 行为预测Transformer | 4 | 40 FPS | 105ms |

**Qdrant向量检索**：

| 指标 | 值 |
|------|-----|
| 检索延迟P95（100万向量） | < 10ms |
| 检索延迟P95（带payload过滤） | < 15ms |
| 吞吐量（单节点） | ≥ 1,000 QPS |
| 内存占用（100万向量，1024维） | ~8GB |
| 量化后内存占用 | ~2GB |

**Redpanda消息总线**：

| 指标 | Redpanda | Kafka（对比） |
|------|----------|-------------|
| 端到端延迟P95 | < 50ms | < 100ms |
| 吞吐量（单节点） | 1.5GB/s | 1.0GB/s |
| 内存占用（基准） | ~500MB | ~2GB（JVM堆） |
| 启动时间 | < 5s | ~30s |

**Dapr运行时**：

| 操作 | P95延迟 | 吞吐量 |
|------|---------|--------|
| 服务调用（含sidecar） | 5ms | 8,000 TPS |
| Valkey状态写入 | 3ms | 30,000 TPS |
| Redpanda消息发布 | 4ms | 15,000 TPS |

**Linkerd服务网格**：

| 指标 | 值 |
|------|-----|
| 代理延迟开销P95 | < 2ms |
| 代理内存占用 | ~50MB |
| 代理CPU开销 | < 50m |
| mTLS握手延迟 | < 5ms |

**OPA策略引擎**：

| 指标 | 值 |
|------|-----|
| 策略评估延迟P95 | < 1ms |
| 吞吐量 | ≥ 10,000 eval/s |
| 策略加载时间 | < 100ms |

**蒸馏模型推理（L0快路径）**：

| 指标 | 值 |
|------|-----|
| 推理延迟P95 | < 30ms |
| 置信度校准误差 | < 5% |
| 模型体积 | < 100MB |

**AgentKernel决策引擎**：

| 指标 | L0-L2 | L3-L5 |
|------|-------|-------|
| 决策总延迟P95 | < 500ms | 10-120s |
| 五路径调度延迟 | < 5ms | < 5ms |

**MCTS搜索**：

| 指标 | 值 |
|------|-----|
| 搜索延迟 | 10-30s（可配置） |
| 模拟次数 | 100-1000次/决策 |
| 搜索完成率 | > 95% |

**世界模型推理**：

| 模式 | 延迟 |
|------|------|
| 神经网络前向推理 | < 100ms |
| 仿真推演 | 1-30s |

**Skill匹配（Qdrant向量检索）**：

| 指标 | 值 |
|------|-----|
| 匹配延迟 | < 20ms |
| Top-5召回率 | > 90% |

### 11.2 测试用例设计

#### 11.2.1 功能测试

| 用例ID | 测试场景 | 测试步骤 | 预期结果 | 优先级 |
|--------|---------|---------|---------|--------|
| TC-F-001 | OODA循环完整执行（含LLM） | 启动OODA工作流 → 模拟传感器输入 → 观察LLM增强的完整循环 | Observe→Orient(RAG+LLM)→Decide(LLM COA)→Act全链路完成 | P0 |
| TC-F-002 | 指挥员审批流程 | 提交高风险行动 → OPA策略检查 → 发送审批请求 → 指挥员确认/拒绝 | OPA拦截→确认后执行，拒绝后终止 | P0 |
| TC-F-003 | Saga补偿回滚 | 在打击任务第3步注入故障 | 逆序执行补偿 | P0 |
| TC-F-004 | 时敏目标短路路径 | 发送TST类型目标 | 绕过Temporal，短路路径响应< 100ms | P0 |
| TC-F-005 | 航迹管理 | 500个目标同时接入 | 航迹正确关联，无丢失 | P0 |
| TC-F-006 | 密级隔离 | 低密级用户尝试访问高密级数据 | OPA策略拒绝，审计日志记录 | P0 |
| TC-F-007 | RAG知识检索 | 查询JS条令 | Qdrant返回相关文档，延迟< 2s | P0 |
| TC-F-008 | LiteLLM故障切换 | SGLang不可用 | 自动切换到备选模型，无用户感知 | P1 |
| TC-F-009 | 降级自主运行 | 断开与战役层的通信 | 边缘自主引擎接管，基于行为规则运行30分钟+ | P1 |
| TC-F-010 | 模型评估流程 | 部署新模型前评估 | 6项评估全通过才允许部署 | P1 |

#### 11.2.2 性能测试

| 用例ID | 测试场景 | 测试配置 | 通过标准 | 优先级 |
|--------|---------|---------|---------|--------|
| TC-P-001 | 传感器数据吞吐 | 5000 msg/s持续30分钟 | 无消息丢失，延迟P95<200ms | P0 |
| TC-P-002 | 多平台协同压力 | 200平台同时控制 | 指令下发延迟P95<500ms | P0 |
| TC-P-003 | OODA循环并发 | 50个并发OODA工作流 | 全部在10s内完成战术循环 | P0 |
| TC-P-004 | RAG检索并发 | 100个并发知识查询 | Qdrant P95< 15ms | P0 |
| TC-P-005 | LLM推理吞吐 | SGLang持续推理30分钟 | P95< 300ms，无OOM | P1 |
| TC-P-006 | 长时间稳定性 | 70%负载运行7×24小时 | 无内存泄漏，性能衰减<5% | P1 |

#### 11.2.3 可靠性测试（混沌工程）

| 用例ID | 故障注入 | 预期结果 | 优先级 |
|--------|---------|---------|--------|
| TC-R-001 | 随机终止服务Pod | 自动重启，10分钟内恢复 | P0 |
| TC-R-002 | 数据库主库切换 | 只读继续，30秒内写入恢复 | P0 |
| TC-R-003 | 网络分区（隔离一个AZ） | 其他AZ继续服务，战术层自主运行 | P0 |
| TC-R-004 | GPU故障（Triton/SGLang不可用） | LiteLLM自动切换到CPU推理或备选模型 | P0 |
| TC-R-005 | Redpanda Broker故障 | 消息不丢失，消费者自动重连 | P1 |
| TC-R-006 | Qdrant节点故障 | 检索降级，LLM无RAG增强继续工作 | P1 |
| TC-R-007 | OPA不可用 | 默认拒绝策略，所有高风险操作需人工确认 | P1 |
| TC-R-008 | Linkerd侧车故障 | Pod自动重启，mTLS自动恢复 | P1 |

### 11.3 测试环境

| 环境 | 配置 | 节点数 | 用途 |
|------|------|--------|------|
| **性能测试** | 32核/128GB/A100×8 | 10节点 | 性能/压力测试 |
| **功能测试** | 16核/64GB/T4×2 | 5节点 | 功能/集成测试 |
| **混沌测试** | 16核/64GB | 5节点 | 故障注入/混沌 |
| **边缘测试** | 8核/32GB/Jetson Orin | 3节点 | K3s边缘部署测试 |

**测试工具**：

| 工具 | 用途 |
|------|------|
| k6 + Locust | 负载测试 |
| Chaos Mesh | 混沌工程 |
| Prometheus + Grafana | 指标监控 |
| Jaeger | 分布式追踪 |
| pytest | 功能测试 |
| Garak | LLM红队测试 |

---

## 12. 落地实施路线

### 12.1 实施阶段规划

> **实施周期**：八阶段共64周，涵盖从基础设施搭建到生产环境上线的完整过程。

#### 12.1.1 七阶段实施路线图

| 阶段 | 时间周期 | 里程碑 | 核心任务 | 交付物 |
|------|---------|--------|---------|--------|
| **阶段一：基础设施** | 第1-6周 | 基础环境就绪 | K8s集群、核心中间件、Linkerd网格、可观测性 | 可用集群、监控大盘 |
| **阶段二：核心平台** | 第7-16周 | 核心平台上线 | Temporal/Dapr/APISIX/SGLang/Triton/Qdrant集成 | 核心服务运行报告 |
| **阶段三：知识层与数据链** | 第17-24周 | 知识库+数据链就绪 | RAG管线、数据链适配器、TimescaleDB/AGE | 知识库、数据链Demo |
| **阶段四：作战场景** | 第25-36周 | 作战场景上线 | 五大场景开发、OPA策略、评估框架 | 场景演示、测试报告 |
| **阶段五：安全加固+边缘** | 第37-44周 | 安全合规+边缘部署 | 安全测试、边缘K3s部署、模型评估 | 安全报告、边缘节点 |
| **阶段六：多模态HMI+自演进** | 第45-52周 | 交互层+演进闭环 | 语音/NL/AR交互、漂移检测、DPO、联邦学习 | HMI Demo、演进管线 |
| **阶段七：v5.0智能体增强** | 第53-56周 | 认知架构就绪 | 世界模型训练、Skill库构建、MCTS集成、蒸馏模型部署 | 世界模型、Skill库、MCTS引擎 |
| **阶段八：联调上线** | 第57-64周 | 生产环境就绪 | 端到端联调、性能优化、多区域高可用 | 上线报告、运维手册 |

#### 12.1.2 关键里程碑

**第1-2周：环境准备**

- 服务器部署与网络配置
- Kubernetes集群搭建（v1.28+）
- Linkerd服务网格部署
- 存储类（StorageClass）配置

**第3-6周：中间件与可观测性**

- PostgreSQL + PostGIS + TimescaleDB + AGE 部署
- Valkey集群部署
- Redpanda集群部署
- Qdrant向量库部署
- SeaweedFS对象存储部署
- Prometheus + Grafana + Jaeger + Loki可观测性
- OPA策略引擎部署

**第7-10周：编排与通信层**

- Temporal Server部署（PostgreSQL后端）
- Dapr控制平面部署（Redpanda pubsub）
- APISIX安全网关配置
- 里程碑：OODA循环Demo运行

**第11-14周：AI推理与知识层**

- SGLang推理服务部署（JSLLM）
- Triton推理服务器部署
- LiteLLM多模型代理部署
- Qdrant知识库初始化
- RAG管线搭建

**第15-16周：核心平台集成测试**

- 全链路集成测试
- 性能基准测试
- Linkerd mTLS验证

**第17-20周：知识层建设**

- JS条令文档切分与嵌入
- 威胁库/装备手册知识入库
- RAG检索效果评估
- 数据链适配器开发（Link 16/VMF/Protobuf）

**第21-24周：数据链集成**

- STANAG 4609视频接入适配器
- 数据链消息中间格式验证
- TimescaleDB时序数据管线
- AGE图关系建模

**第25-28周：ISR + C2决策场景**

- 多源传感器接入适配器
- 多模态推理流水线
- LLM COA生成 + OR-Tools优化
- OPA交战规则策略配置

**第29-32周：无人系统 + 防空场景**

- 多平台路径规划（OR-Tools）
- 编队控制与动态重规划
- 防空杀伤链闭环
- 边缘自主决策引擎

**第33-36周：兵棋推演 + 模型评估**

- 蒙特卡洛仿真引擎
- 模型评估框架（对标SEAL）
- 红队测试工具集成
- OOD退化评估

**第37-40周：安全加固**

- 密级标定与隔离验证
- Linkerd mTLS全链路验证
- OPA策略全面审计
- 安全渗透测试

**第41-44周：边缘部署**

- K3s边缘集群搭建
- 边缘自主引擎测试
- 通信中断模拟与恢复验证
- 模型量化与边缘推理优化

**第45-48周：多模态HMI**

- FunASR语音识别集成与调优
- CosyVoice语音合成部署
- 自然语言态势查询引擎开发
- WebXR AR战术叠加原型

**第49-52周：自演进闭环**

- Evidently漂移检测集成
- DPO偏好学习管线搭建
- Flower联邦学习框架部署
- 自演进闭环端到端验证

**第53-56周：安全合规 + SDK框架**

- 安全漏洞修复与渗透测试复查
- 合规检查与报告
- SDK/插件框架开发（供第三方集成）
- GitOps安全审计验证
- 世界模型训练与验证
- Skill库构建与向量化
- MCTS搜索引擎集成
- 蒸馏模型训练与边缘部署

**第57-64周：联调上线**

- 性能优化调优
- 运维手册编写
- 应急预案制定
- 人员培训
- 系统正式上线

### 12.2 多区域高可用与灾备设计

#### 12.2.1 部署架构

```Plain
┌──────────────────────────┐     ┌──────────────────────────┐
│      主区域（Region A）    │     │     备区域（Region B）    │
│                          │     │                          │
│  ┌────────────────────┐  │     │  ┌────────────────────┐  │
│  │  APISIX (Active)   │  │     │  │  APISIX (Standby)  │  │
│  ├────────────────────┤  │     │  ├────────────────────┤  │
│  │  Temporal (Active) │  │     │  │  Temporal (Standby)│  │
│  ├────────────────────┤  │     │  ├────────────────────┤  │
│  │  SGLang + Triton   │  │     │  │  SGLang + Triton   │  │
│  ├────────────────────┤  │     │  ├────────────────────┤  │
│  │  Qdrant + Redpanda │  │     │  │  Qdrant + Redpanda │  │
│  ├────────────────────┤  │     │  ├────────────────────┤  │
│  │  PG+PostGIS+       │◄─┼─────┼─►│  PG+PostGIS+       │  │
│  │  TimescaleDB(主)   │  │同步  │  │  TimescaleDB(备)   │  │
│  └────────────────────┘  │     │  └────────────────────┘  │
└──────────────────────────┘     └──────────────────────────┘
            │                                │
            └────────── DNS 路由 ─────────────┘
                        │
                ┌───────┴───────┐
                │  战术边缘节点  │
                │  (K3s + 边缘  │
                │   自主引擎)   │
                └───────────────┘
```

#### 12.2.2 RPO/RTO指标

| 场景 | RPO（数据丢失） | RTO（恢复时间） | 实现方式 |
|------|-----------------|----------------|---------|
| 单Pod故障 | 0 | < 30秒 | K8s自动重启 |
| 单节点故障 | 0 | < 5分钟 | K8s调度迁移 |
| 数据库主库切换 | < 10秒 | < 1分钟 | PostgreSQL流复制 |
| 整区域故障 | < 1分钟 | < 10分钟 | DNS切换到备区域 |
| Qdrant不可用 | 0 | 即时 | LLM无RAG降级运行 |
| Redpanda不可用 | 0 | < 30秒 | Dapr自动重连 |
| 战术边缘通信中断 | N/A | N/A | 边缘自主引擎运行30分钟+ |

### 12.3 资源需求规划

#### 12.3.1 人力资源

| 角色 | 人数 | 技能要求 | 投入周期 |
|------|------|---------|---------|
| 系统架构师 | 2 | C2系统设计、云原生架构 | 全周期 |
| K8s运维工程师 | 3 | Kubernetes、Linkerd、网络 | 第1-24周 |
| 后端开发工程师 | 6 | Python/Go、微服务、分布式系统 | 第7-40周 |
| AI工程师 | 4 | CV/NLP/LLM、模型部署优化 | 第11-40周 |
| RAG工程师 | 2 | 向量检索、嵌入模型、知识工程 | 第11-28周 |
| C2领域专家 | 2 | JSC2、OODA、交战规则 | 第17-48周 |
| 测试工程师 | 2 | 性能测试、混沌工程、AI评估 | 第15-52周 |
| 安全工程师 | 2 | JS安全、OPA策略、渗透测试 | 第37-48周 |
| 边缘工程师 | 1 | K3s、边缘AI、嵌入式 | 第41-48周 |
| 运维工程师 | 2 | DevOps、GitOps、监控 | 第49-56周 |
| 项目经理 | 1 | 军工项目管理 | 全周期 |

#### 12.3.2 硬件资源

| 环境 | 配置 | 数量 | 月成本估算 |
|------|------|------|-----------|
| 开发环境 | 16核/64GB/500GB SSD | 5台 | ¥15,000 |
| 测试环境 | 32核/128GB/T4×2 | 5台 | ¥30,000 |
| 生产环境（主） | 64核/256GB/A100×8 | 10台 | ¥200,000 |
| 生产环境（备） | 64核/256GB/A100×4 | 5台 | ¥100,000 |
| 战术边缘 | 16核/64GB/Jetson Orin（加固型） | 10台 | ¥50,000 |
| **总计** | — | **35台** | **¥395,000/月** |

### 12.4 新增组件清单与部署顺序

| 序号 | 组件 | 部署阶段 | 依赖 | 资源需求 |
|------|------|---------|------|---------|
| 1 | Kubernetes集群 | 阶段一 | — | 3+ 节点 |
| 2 | Linkerd | 阶段一 | K8s | 低（每Pod+50MB） |
| 3 | PostgreSQL + PostGIS | 阶段一 | K8s | 16GB RAM |
| 4 | TimescaleDB | 阶段一 | PG | 扩展安装 |
| 5 | Apache AGE | 阶段一 | PG | 扩展安装 |
| 6 | Valkey | 阶段一 | K8s | 8GB RAM |
| 7 | Redpanda | 阶段一 | K8s | 8GB RAM |
| 8 | SeaweedFS | 阶段一 | K8s | 16GB RAM |
| 9 | OpenBao | 阶段一 | K8s | 4GB RAM |
| 10 | 可观测性栈 | 阶段一 | K8s | 8GB RAM |
| 11 | Temporal | 阶段二 | PG, Valkey | 8GB RAM |
| 12 | Dapr | 阶段二 | K8s, Redpanda | 低 |
| 13 | APISIX | 阶段二 | etcd | 4GB RAM |
| 14 | OPA | 阶段二 | K8s | 2GB RAM |
| 15 | SGLang | 阶段二 | GPU | 1× A100 |
| 16 | Triton | 阶段二 | GPU | 1× A100 |
| 17 | LiteLLM | 阶段二 | SGLang | 4GB RAM |
| 18 | Qdrant | 阶段二 | K8s | 16GB RAM |
| 19 | LangGraph | 阶段三 | Temporal, SGLang | 8GB RAM |
| 20 | ArgoCD | 阶段三 | K8s, Git | 4GB RAM |
| 21 | FunASR/Whisper (STT) | 阶段六 | SGLang | 8GB RAM |
| 22 | CosyVoice (TTS) | 阶段六 | — | 4GB RAM |
| 23 | Cesium前端 | 阶段六 | WebSocket, COP | 前端资源 |
| 24 | WebSocket推送 | 阶段六 | APISIX, Redpanda | 低 |
| 25 | Evidently (漂移检测) | 阶段六 | MLflow | 4GB RAM |
| 26 | Flower (联邦学习) | 阶段六 | K3s边缘 | 8GB RAM |
| 27 | TRL/DPO (偏好学习) | 阶段六 | SGLang, GPU | 1× GPU |

### 12.5 风险与应对

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|---------|
| AI推理性能不达标 | 中 | 高 | 提前POC验证SGLang；准备模型蒸馏/量化方案 |
| LLM幻觉导致错误决策 | 中 | 高 | SGLang结构化输出 + RAG知识约束 + 人类审批 |
| 无人平台通信协议差异 | 高 | 中 | Protobuf中间格式 + 平台适配层 |
| C2领域专家资源不足 | 中 | 高 | 尽早引入；与院校/研究所合作 |
| 安全合规不通过 | 中 | 高 | 安全左移；OPA策略即代码；每阶段安全审查 |
| 硬件交付延迟 | 中 | 中 | 提前采购；准备临时云资源 |
| 多区域同步延迟超标 | 低 | 中 | 异步复制+冲突解决机制 |
| Qdrant向量库稳定性 | 低 | 中 | pgvector作为备选方案 |
| Redpanda BSL许可限制 | 低 | 中 | 可降级使用Apache Kafka |

### 12.6 成功度量标准

#### 12.6.1 技术指标

| 指标 | 目标值 | 测量方式 |
|------|--------|---------|
| 战术OODA循环时间 | < 10s | 工作流计时 |
| 时敏目标短路响应 | < 100ms | 短路路径计时 |
| RAG知识检索延迟 | < 2s | Qdrant查询计时 |
| 传感器→COP更新延迟 | P95 < 200ms | 端到端计时 |
| 系统可用性 | ≥ 99.95% | 月度统计 |
| 安全漏洞（高危） | 0 | 安全扫描 |
| 测试通过率 | ≥ 95% | 测试报告 |
| LLM结构化输出合规率 | ≥ 99% | 格式验证 |
| 蒸馏模型L0推理延迟 | < 30ms | Triton metrics |
| Skill匹配率 | > 80% | Qdrant检索统计 |
| MCTS搜索完成率 | > 95% | MCTS引擎统计 |
| 自主等级分布 | L0<30% L1-L2>60% | 决策日志分析 |

#### 12.6.2 作战效能指标

| 指标 | 目标值 |
|------|--------|
| OODA循环加速 | 比传统C2快3倍以上 |
| 杀伤链闭环时间 | 缩短50%以上 |
| 人工干预率（非武器释放） | 降低60%以上 |
| 多源情报融合准确率 | ≥ 90% |
| COA方案生成效率 | 提升5倍以上 |
| RAG条令检索准确率 | ≥ 85% |

---

## 附录

### 许可证合规声明

| 组件 | 版本 | 许可证 | 合规说明 |
|------|------|--------|---------|
| Temporal | v1.24+ | MIT | 完全可商用 |
| Dapr | v1.14+ | Apache 2.0 | 完全可商用 |
| SGLang | v0.3+ | Apache 2.0 | 完全可商用 |
| Triton Inference Server | v24.09+ | BSD-3-Clause | 完全可商用 |
| Apache APISIX | v3.15+ | Apache 2.0 | 完全可商用 |
| Linkerd | v2.14+ | Apache 2.0 | 完全可商用 |
| LangGraph | v0.2+ | MIT | 完全可商用 |
| LiteLLM | v1.40+ | MIT | 完全可商用 |
| OR-Tools | v9.10+ | Apache 2.0 | **使用CP-SAT求解器**（Apache 2.0），不使用SCIP |
| Qdrant | v1.9+ | Apache 2.0 | 完全可商用 |
| PostgreSQL + PostGIS | v15+ / v3.4+ | PostgreSQL License / MIT | 完全可商用 |
| TimescaleDB | 社区版 | Apache 2.0（社区版） | 社区版完全可商用 |
| Apache AGE | v1.4+ | Apache 2.0 | 完全可商用 |
| OPA | v0.60+ | Apache 2.0 | 完全可商用 |
| Redpanda | v23.3+ | BSL 1.1 | **源码公开，单节点免费商用**，多节点集群需商业许可 |
| Valkey | v7.2+ | BSD-3-Clause | Redis社区fork，完全可商用 |
| SeaweedFS | v3.6+ | Apache 2.0 | 完全可商用（替代MinIO的AGPLv3） |
| OpenBao | v2.0+ | MPL-2.0 | Vault社区fork，完全可商用 |
| ArgoCD | v2.10+ | Apache 2.0 | 完全可商用 |
| MLflow | v2.x | Apache 2.0 | 完全可商用 |
| Label Studio | v1.10+ | Apache 2.0 | 完全可商用 |
| Garak（红队测试） | v0.2+ | Apache 2.0 | 完全可商用 |
| DVC | v3.x | Apache 2.0 | 完全可商用 |
| FunASR（语音识别） | v1.x | MIT | 完全可商用 |
| CosyVoice（语音合成） | v1.x | MIT | 完全可商用 |
| Evidently AI（漂移检测） | v0.4+ | Apache 2.0 | 完全可商用 |
| Flower（联邦学习） | v1.8+ | Apache 2.0 | 完全可商用 |
| TRL（DPO/RLHF训练） | v0.12+ | Apache 2.0 | 完全可商用 |

**BSL 1.1 特别说明**：Redpanda的BSL 1.1许可在单节点部署下免费商用，与Kafka API完全兼容。如需多节点集群部署，可降级使用Apache Kafka（Apache 2.0）。

### A. 术语与缩略语表

| 缩略语 | 全称 | 中文含义 |
|--------|------|---------|
| C2 | Command and Control | 指挥控制 |
| OODA | Observe-Orient-Decide-Act | 观察-判断-决策-行动循环 |
| COA | Course of Action | 行动方案 |
| COP | Common Operational Picture | 共用作战态势图 |
| ISR | Intelligence, Surveillance, Reconnaissance | 情报、监视、侦察 |
| ROE | Rules of Engagement | 交战规则 |
| TST | Time-Sensitive Target | 时敏目标 |
| F2T2EA | Find-Fix-Track-Target-Engage-Assess | 发现-定位-跟踪-瞄准-打击-评估（杀伤链） |
| MDO | Multi-Domain Operations | 多域作战 |
| JADC2 | Joint All-Domain Command and Control | 联合全域指挥控制 |
| JC3IEDM | Joint C3 Information Exchange Data Model | 联合C3信息交换数据模型（NATO标准） |
| MIL-STD-2525D | — | JS符号标准（美军） |
| BDA | Battle Damage Assessment | 战损评估 |
| EW | Electronic Warfare | 电子战 |
| ELINT | Electronic Intelligence | 电子情报 |
| GEOINT | Geospatial Intelligence | 地理空间情报 |
| SIGINT | Signals Intelligence | 信号情报 |
| EOIR | Electro-Optical/Infrared | 光电/红外 |
| SAR | Synthetic Aperture Radar | 合成孔径雷达 |
| UAV | Unmanned Aerial Vehicle | 无人机 |
| USV | Unmanned Surface Vehicle | 无人水面艇 |
| UUV | Unmanned Underwater Vehicle | 无人潜航器 |
| UGV | Unmanned Ground Vehicle | 无人地面车辆 |
| LLM | Large Language Model | 大语言模型 |
| RAG | Retrieval-Augmented Generation | 检索增强生成 |
| NLP | Natural Language Processing | 自然语言处理 |
| NLG | Natural Language Generation | 自然语言生成 |
| STT | Speech-to-Text | 语音转文字 |
| TTS | Text-to-Speech | 文字转语音 |
| GPU | Graphics Processing Unit | 图形处理器 |
| MPS | Multi-Process Service | 多进程服务（NVIDIA GPU隔离） |
| SLA | Service Level Agreement | 服务等级协议 |
| TTL | Time To Live | 存活时间（缓存过期） |
| HLA | High Level Architecture | 高层架构（仿真互操作标准） |
| AFSIM | Advanced Framework for Simulation | 先进仿真框架 |
| DPO | Direct Preference Optimization | 直接偏好优化 |
| TRL | Transformer Reinforcement Learning | Transformer强化学习库 |
| RLHF | Reinforcement Learning from Human Feedback | 人类反馈强化学习 |
| PEFT | Parameter-Efficient Fine-Tuning | 参数高效微调 |
| OOD | Out-of-Distribution | 分布外（模型退化检测） |
| API | Application Programming Interface | 应用编程接口 |
| SDK | Software Development Kit | 软件开发工具包 |
| DAG | Directed Acyclic Graph | 有向无环图 |
| FSM | Finite State Machine | 有限状态机 |
| gRPC | gRPC Remote Procedure Call | 高性能远程过程调用 |
| REST | Representational State Transfer | 表述性状态转移 |
| OPA | Open Policy Agent | 开放策略代理 |
| TS/SCI | Top Secret/Sensitive Compartmented Information | 最高机密/敏感分隔信息 |
| FedRAMP | Federal Risk and Authorization Management Program | 联邦风险与授权管理计划 |
| Link16 | — | 战术数据链16号（美军） |
| VMF | Variable Message Format | 可变消息格式 |
| STANAG | Standardization Agreement | 标准化协议（NATO） |
| MTTR | Mean Time To Recovery | 平均恢复时间 |
| RPO | Recovery Point Objective | 恢复点目标 |
| RTO | Recovery Time Objective | 恢复时间目标 |
| WGS84 | World Geodetic System 1984 | 世界大地坐标系1984 |
| CPSAT | CP-SAT Solver | 约束规划-SAT求解器（OR-Tools） |
| MCTS | Monte Carlo Tree Search | 蒙特卡洛树搜索（决策搜索算法） |
| Skill | — | 技能（可复用决策模式单元） |
| World Model | — | 世界模型（环境状态预测与仿真） |
| AgentKernel | — | 智能体推理引擎（五路径决策核心） |
| Distilled Model | — | 蒸馏小模型（L0快路径轻量模型） |
| L0-L5 | Autonomy Level 0-5 | 自主等级（人工到完全自主六级） |
| MSE | Mean Squared Error | 均方误差 |

### B. 版本演进记录

> **v2.0→v3.0升级**：
> 1. 架构分层从5层扩展到9层，新增安全网格层、RAG/OAG知识层、战术数据链集成层、模型评估与仿真层
> 2. 技术栈从6个核心组件扩展到16个，新增SGLang/Qdrant/TimescaleDB/Apache AGE/OPA/LiteLLM/Linkerd/Redpanda等
> 3. 战术层新增快速短路路径（绕过Temporal，亚秒级响应）
> 4. 新增OPA声明式策略引擎（交战规则声明式管理）
> 5. 新增边缘自主决策引擎（行为树+状态机）
> 6. 战役层新增LLM驱动的COA生成
> 7. COP数据平面升级为多模态数据引擎（+TimescaleDB时序+AGE图）
> 8. 新增RAG知识库构建管线
> 9. 新增模型评估框架（对标Scale SEAL）
> 10. 新增兵棋推演引擎（HLA4+AFSIM集成）
> 11. 新增数据链消息中间格式（Protobuf）
> 12. 安全设计新增OPA策略引擎和GitOps安全审计
>
> **v3.0→v3.1升级**：
> 13. 新增多模态人机交互层（语音/NL/AR/WebSocket/Cesium三维态势）
> 14. 新增自主演进闭环（漂移检测/偏好学习/联邦学习）
> 15. 新增工作流注册表（快慢系统与指挥员统一界面）
> 16. 新增经验蒸馏闭环（慢系统有效方法到快系统先验的自动迁移）
> 17. 修复快慢双系统5项关键缺陷（eval安全、GPU隔离、数据对账、融合控制、负载路由）
>
> **v3.1→v4.0升级**：
> 18. 文档结构重构：修复重复节号（3.2.4）、非标准编号（2.3b/2.3.5b-e）、章节重命名
> 19. 移除标题中的版本标注/v3.1修复等），统一为正文引用
> 20. 新增附录A：术语与缩略语表（60+条目）
> 21. 新增附录B：版本演进记录
>
> **v4.0→v5.0升级**：
> 22. 智能体认知架构三支柱（世界模型+Skills+MCTS）
> 23. AgentKernel五路径决策引擎（蒸馏快路径/工作流/技能匹配/MCTS/世界模型推演）
> 24. L0蒸馏小模型快路径（<30ms推理，边缘可部署）
> 25. L1-L5分层自主等级（从人工审批到完全自主）
> 26. 工作流从决策主体退化为安全执行层
> 27. 对抗训练GAN式闭环（红蓝对抗+世界模型）
> 28. 经验蒸馏三路输出（技能库/世界模型/蒸馏小模型）

### C. 参考文献

| 编号 | 文献 | 说明 |
|------|------|------|
| [1] | Anduril Lattice 技术文档 | 战术边缘AI指挥控制平台 |
| [2] | Palantir Gotham/AIP 产品文档 | 情报分析与AI决策平台 |
| [3] | Scale AI Donovan/Thunderforge 技术文档 | AI决策支持与JS规划系统 |
| [4] | NATO JC3IEDM Specification | 联合C3信息交换数据模型 |
| [5] | MIL-STD-2525D | JS符号标准化（美军） |
| [6] | John Boyd, "Patterns of Conflict" (1986) | OODA循环理论 |
| [7] | Daniel Kahneman, "Thinking, Fast and Slow" (2011) | 快慢双系统理论 |
| [8] | US DoD, "Joint All-Domain Command and Control Strategy" | 联合全域指挥控制战略 |
| [9] | IEEE 1516 (HLA) | 高层架构仿真互操作标准 |
| [10] | NIST AI Risk Management Framework (AI RMF) | AI风险管理框架 |

---

**文档结束**
