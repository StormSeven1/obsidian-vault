# AI Native C2 / NGC2 / Palantir / Anduril 一手资料包索引

生成日期：2026-05-19

说明：本资料包优先收录可直接下载的 PDF 原文。对没有公开 PDF 的官方网页、API 文档和行业报道，已在最后一节列出“需要浏览器另存 PDF/继续核验”的链接。本包用于研究 AI-native C2、NGC2、Lattice、Palantir Target Workbench、IBCS/IBCS-M、C-UAS 评估与陆军转型。

## A. 已下载 PDF 文件

| 本地文件 | 原始来源 | 主要内容 / 研究价值 |
|---|---|---|
| `pdfs/Army_NGC2_Muddy_Boots.pdf` | https://www.armyupress.army.mil/Portals/7/nco-journal/images/2026/April/next-gen/Next-Generation-Command-and-Control_Muddy%20Boots_UA.pdf | Army University Press / NCO Journal 对 NGC2 的可读性介绍。重点：whole-stack modernization、Transport / Integration / Data / Applications 四层、4th ID Ivy Sting 实践。 |
| `pdfs/Army_Communicator_NGC2_Faster_Better.pdf` | https://www.lineofdeparture.army.mil/Portals/144/PDF/Journals/Army-Communicator/Fall-Winter-2025/NGC2-Faster-Better.pdf | Army Communicator 对 NGC2 的官方阐释。重点：指挥员如何重新获得 C2 优势、多路径通信、数据可用性、快速决策。 |
| `pdfs/Fort_Carson_Ivy_Mass_2026_Environmental_Assessment.pdf` | https://home.army.mil/carson/download_file/view/30635bc5-525d-4ee5-b8b9-82762525cf0c/1440 | Ivy Mass 2026 训练演习的环境评估材料。用于核验 Ivy Mass 的训练背景、地点与规模，不是技术架构白皮书。 |
| `pdfs/Palantir_Target_Workbench.pdf` | https://www.palantir.com/assets/xrfr7uokpv1b/1IqzwzpemtBSm98TNCczao/49bbc30cbec4d2d4d189ab27bd07376c/Palantir_Target_Workbench___1_.pdf | Palantir 官方 Target Workbench PDF。重点：目标从识别到执行和评估的生命周期、Kanban 式 targeting workflow、目标情报附着、协作审批、效应器配对。 |
| `pdfs/Palantir_Gotham_AI_Enabled_Operations.pdf` | https://www.palantir.com/assets/xrfr7uokpv1b/3A0y10xksgXENvRMNaAsUu/ed8f7f1ed534c0101f64536a85f7297b/Gotham_AI-Enabled_Operations_White_Paper.pdf | Palantir Gotham AI-enabled operations 白皮书。重点：大规模数据整合、AI 辅助态势理解、COA 建议、人机协同决策与行动反馈。 |
| `pdfs/Palantir_Edge_AI_Autonomy.pdf` | https://www.palantir.com/assets/xrfr7uokpv1b/5KtW43WegiCHFLT7IJi3Tg/d24fd27f752b0647a7ac5fd73bfd409f/Navy_Edge_AI_Autonomy_White_Paper.pdf | Palantir Edge AI + Autonomy 白皮书。重点：断连/低带宽/边缘环境中的模型部署、AI 模型运营、异构平台部署和持续交付。 |
| `pdfs/Palantir_Edge_AI.pdf` | https://www.palantir.com/assets/xrfr7uokpv1b/SobaEwwQdZKESeUTytnNP/82aa2096b43f063f32f421717a5f50aa/Whitepaper_-_Palantir_Edge_AI.pdf | Palantir Edge AI 白皮书。重点：低带宽、低功耗、边缘自治决策、传感器 AI、模型管理与部署。 |
| `pdfs/Palantir_JADC2.pdf` | https://www.palantir.com/assets/xrfr7uokpv1b/5T6DHvz26j39revZgsTQ4z/c7dfca2ed64671b30917fd4740ca55ce/general-Munitions-JADC2-native_2.pdf | Palantir JADC2 方案材料。重点：多域数据融合、AI/ML、munition/readiness/C2 数据汇聚与联合全域作战。 |
| `pdfs/Palantir_AIDP_AUSA.pdf` | https://www.palantir.com/assets/xrfr7uokpv1b/7JAWiSA6yA5MLDAD1AsX7l/c256437b1c29bad5747633123957b4b7/AIDP_AUSA__2_-updated2.pdf | Palantir AIDP 材料。重点：陆军情报数据平台、情报/目标数据融合背景。 |
| `pdfs/Palantir_TITAN_AUSA.pdf` | https://www.palantir.com/assets/xrfr7uokpv1b/7kEyhuSSUmfQtsGfIwIWZ4/01f49e667d8ff762dd22ad729c670294/AUSA_Titan__1_.pdf | Palantir TITAN 材料。重点：Tactical Intelligence Targeting Access Node、传感器到目标到火力链路。 |
| `pdfs/Palantir_Distributed_Maritime_Operations_Decision_Support.pdf` | https://www.palantir.com/assets/xrfr7uokpv1b/7fMgurDhYT5hMjrjDGTZW5/88bd42f31bc65c93861fe97c1a5af3ec/Navy_-_Distributed_Maritime_Operations-_Decision_Support.pdf | 分布式海上作战决策支持材料。重点：开放 API、分布式作战、海军场景下的决策支持与数据集成。 |
| `pdfs/Palantir_Secure_Collaboration.pdf` | https://www.palantir.com/assets/xrfr7uokpv1b/4JWbqPQ8d6vYcNijOVqD0D/2857507783a328b6ddb6aef1ffc5fac4/Palantir_for_Secure_Collaboration__1_.pdf | Palantir 安全协作材料。重点：跨组织/跨密级协作、访问控制、联合作战数据共享。 |
| `pdfs/Anduril_Lattice_OS_2022.pdf` | https://sldinfo.com/wp-content/uploads/2022/10/2022-slick-Lattice-OS-AUS.pdf | Anduril Lattice OS 公开 PDF。虽然较早，但系统性展示 Lattice OS 的传感器融合、AI 辅助 C2、多域任务管理与边缘自治理念。 |
| `pdfs/Army_IBCS_Paradigm_Shifts.pdf` | https://www.lineofdeparture.army.mil/Portals/144/PDF/Journals/ADA/2024-E/Paradigm-Shifts_UA.pdf | IBCS 架构范式转变材料。重点：解耦传感器、效应器和 C2 节点，理解 any sensor / best effector 的技术逻辑。 |
| `pdfs/DoD_IAMD_SAR_2021.pdf` | https://www.esd.whs.mil/Portals/54/Documents/FOID/Reading%20Room/Selected_Acquisition_Reports/FY_2021_SARS/22-F-0762_IAMD_SAR_2021.pdf | DoD Selected Acquisition Report。重点：IAMD/IBCS 项目采办背景、项目结构、里程碑和风险。 |
| `pdfs/DSCA_Denmark_IBCS_Patriot_25_51.pdf` | https://media.defense.gov/2025/Aug/29/2003790440/-1/-1/1/PRESS%20RELEASE%20-%20DENMARK%2025-51%20CN.PDF | DSCA 对丹麦 IBCS-enabled Patriot 的 FMS 通告。用于核验 IBCS 国际化、盟友防空体系扩展。 |
| `pdfs/DSCA_Denmark_IBCS_IFPC_25_75.pdf` | https://media.defense.gov/2025/Dec/05/2003837761/-1/-1/1/PRESS%20RELEASE%20-%20DENMARK%2025-75%20CN.PDF | DSCA 对丹麦 IBCS + IFPC 相关 FMS 通告。用于理解 IBCS 与更多防空/反导系统组合输出。 |
| `pdfs/DoD_Army_Transformation_and_Acquisition_Reform.pdf` | https://media.defense.gov/2025/May/01/2003702281/-1/-1/1/ARMY-TRANSFORMATION-AND-ACQUISITION-REFORM.PDF | DoD/Army 转型与采办改革文件。重点：快速采办、裁撤旧能力、反无人机/防空/电子战/网络等优先方向。 |
| `pdfs/Army_Transformation_in_Contact.pdf` | https://www.armyupress.army.mil/Portals/7/military-review/Archives/English/Online-Exclusive/2024/Transformation-in-Contact/Transformation-in-Contact-UA.pdf | Transformation in Contact 文章。重点：接触中转型、C2 网络简化、人机集成编队。 |
| `pdfs/Army_Deliberate_Transformation.pdf` | https://www.armyupress.army.mil/Portals/7/military-review/Archives/English/Online-Exclusive/2024/Deliberate-Transformation/Deliberate-Transformation-UA.pdf | Deliberate Transformation 文章。重点：需求、预算、采办机制如何适应快速技术迭代。 |
| `pdfs/Army_Decision_Dominance_Operationalized_Data.pdf` | https://www.armyupress.army.mil/Portals/7/military-review/Archives/English/January-February-2025/Decision-Dominance/Decision-Dominance-UA.pdf | Operationalized Data / Decision Dominance。重点：数据作战化、决策优势、C2 数据基础设施。 |
| `pdfs/DoD_Establishment_JIATF_401.pdf` | https://media.defense.gov/2025/Aug/28/2003790021/-1/-1/0/ESTABLISHMENT-OF-JOINT-INTERAGENCY-TASK-FORCE-401.PDF | JIATF-401 建立文件。重点：C-sUAS 组织、快速采购、测试训练与标准化背景。 |
| `pdfs/JIATF_401_CUAS_Testing_Evaluation_Criteria.pdf` | https://media.defense.gov/2026/Apr/29/2003922024/-1/-1/1/JIATF-401-PUBLISHES-TESTING-AND-EVALUATION-CRITERIA-TO-INFORM-FUTURE-DEMONSTRATIONS-AND-EXERCISES.PDF | C-UAS 测试与评估共同标准。重点：系统验收、测试数据标准化、未来演示与演习评估。 |
| `pdfs/JIATF_401_Physical_Protection_Critical_Infrastructure.pdf` | https://media.defense.gov/2026/Jan/30/2003868750/-1/-1/0/JIATF-401-GUIDE-FOR-PHYSICAL-PROTECTION-OF-CRITICAL-INFRASTRUCTURE.PDF | JIATF-401 对关键基础设施反无人机保护的指南。重点：非技术措施、分层防护、外围思维。 |

## B. 未能直接作为 PDF 下载、但强烈建议继续保存/另存 PDF 的一手网页

| 来源 | 链接 | 重点 |
|---|---|---|
| U.S. Army | https://www.army.mil/article/287180/army_announces_next_generation_command_and_control_ngc2_prototype_award | NGC2 原型合同授予 Team Anduril，确认 PEO C3N、4th ID、开放模块化和四层架构。 |
| U.S. Army | https://www.army.mil/article/288233/army_announces_additional_competitive_award_for_next_generation_command_and_control_ngc2_prototyping_efforts | 第二条 NGC2 原型竞争线，理解 4th ID / 25th ID 并行原型。 |
| U.S. Army | https://www.army.mil/article/288651/its_about_lethal_formations_ivy_division_launches_army_prototype_for_next_gen_command_and_control | Ivy Division 启动 NGC2 原型，强调 Ivy Sting/Ivy Mass 逐步增加复杂性、DDIL/电磁干扰场景。 |
| U.S. Army | https://www.army.mil/article/290401/4th_infantry_division_showcases_ivy_sting_4_a_leap_forward_in_command_and_control | Ivy Sting 4 官方报道，核验 NGC2 持续演训进展。 |
| U.S. Army CAC | https://usacac.army.mil/Article-Library/View-Content?ArtMID=575&ArticleID=2308 | MCCoE 在 Ivy Sting 5 做 C2 评估，适合研究“演训反馈驱动迭代”。 |
| U.S. Army | https://www.army.mil/article/290501/army_leaders_discuss_operationalizing_ngc2 | NGC2 operationalizing 讨论，说明 NGC2 如何改变陆军作战。 |
| U.S. Army | https://www.army.mil/article/290032/ngc2_at_the_tactical_edge_enabling_predictive_logistics_for_decision_dominance | NGC2 at tactical edge，说明 NGC2 与预测性后勤、四层技术栈。 |
| Anduril | https://www.anduril.com/news/how-anduril-and-the-army-are-rewriting-fire-missions-with-ngc2 | Ivy Sting 1：Lattice Mesh + Palantir Target Workbench 支撑从总部到炮线的 targeting process。 |
| Anduril | https://www.anduril.com/news/how-ngc2-is-expanding-the-battlefield-network-at-ivy-sting-2 | Ivy Sting 2：更多节点、传感器、士兵接入统一 mesh network。 |
| Anduril | https://www.anduril.com/news/scaling-next-generation-command-and-control-from-prototype-to-fight | Ivy Sting 5：跨军种/跨密级 sensor-to-effector kill chain，无人工数据重录。 |
| Anduril | https://www.anduril.com/news/anduril-awarded-usd99-6m-for-u-s-army-next-generation-command-and-control-prototype | Anduril 官方合同说明，强调与士兵 touchpoints 和 operational environments at scale。 |
| Anduril | https://www.anduril.com/lattice/command-and-control | Lattice for C2 官方产品页，说明 AI-powered battle management platform、thousands of sensors/effectors、kill chain acceleration。 |
| Anduril | https://www.anduril.com/news/anduril-selected-for-u-s-army-s-integrated-battle-command-system-maneuver-program | IBCS-M 官方来源：Lattice 成为 Counter-UAS missions 的 next-generation fire control platform。 |
| Anduril | https://www.anduril.com/news/jiatf-401-selects-lattice-as-enterprise-tactical-command-and-control-platform-for-c-uas | JIATF-401 选择 Lattice 作为企业级 C-UAS 战术 C2 平台。 |
| Palantir API Docs | https://www.palantir.com/docs/gotham/api/target-workbench-v2-resources/targets/target-basics | Target Workbench API - Target basics。 |
| Palantir API Docs | https://www.palantir.com/docs/gotham/api/target-workbench/targetBoard/create-target-board | Target Board 创建 API。 |
| Palantir API Docs | https://www.palantir.com/docs/gotham/api/target-workbench-v2-resources/targets/set-target-column-target | 目标 Column / 状态流转 API。 |
| Palantir API Docs | https://www.palantir.com/docs/gotham/api/target-workbench-v2-resources/targets/create-target-intel-target | Target Intel 创建 API。 |
| Palantir | https://www.palantir.com/defense/sdk/ | Palantir Defense OSDK，研究 Defense Ontology + API/SDK 扩展生态。 |
| Northrop Grumman | https://www.northropgrumman.com/what-we-do/missile-defense/integrated-battle-command-system-ibcs | IBCS 官方产品页。 |
| U.S. Army | https://www.army.mil/article/291023/ibcs_and_the_future_of_offensive_and_defensive_integrated_fires | IBCS 与 offensive / defensive integrated fires 的最新官方阐释。 |
| U.S. Army | https://www.army.mil/article/278092/us_army_receives_first_complete_ibcs_delivery | IBCS 首套完整交付，核验 plug-and-fight / best weapon 相关说法。 |
| U.S. Army | https://www.army.mil/article/265686/army_integrated_air_and_missile_defense_system_achieves_full_rate_production | IBCS 达到 full-rate production。 |

## C. 下载失败或未纳入的说明

- `Northrop_IBCS_Full_Rate_Production.pdf`（Northrop 投资者 PDF）下载失败，建议直接打开来源页面另存：`https://investor.northropgrumman.com/node/40531/pdf`
- HTML 网页因当前下载工具限制未直接抓取为本地 HTML/PDF，已在 B 节列出链接。建议用浏览器“打印为 PDF”批量保存。
- 媒体报道（Reuters/Yahoo、DefenseScoop、Business Insider 等）未放入本包，建议后续作为“争议与第三方验证”单独整理。

## D. 建议阅读路径

1. 先读 NGC2：`Army_NGC2_Muddy_Boots.pdf`、`Army_Communicator_NGC2_Faster_Better.pdf`，再看 Army/Anduril 的 NGC2/Ivy Sting 网页。
2. 再读 Palantir：`Palantir_Target_Workbench.pdf`、TWB API 文档、`Palantir_Gotham_AI_Enabled_Operations.pdf`。
3. 再读 Anduril：`Anduril_Lattice_OS_2022.pdf`、Lattice C2 官方页、Ivy Sting 1/2/5 新闻。
4. 然后看 IBCS/IBCS-M：`Army_IBCS_Paradigm_Shifts.pdf`、IBCS 官方页、Anduril IBCS-M 新闻。
5. 最后看转型与评估：Army Transformation、Decision Dominance、JIATF-401 评估标准。


## E. B 节网页的本地 Markdown / HTML 快照

本增强版资料包新增：

- `webpages_md/`：B 节网页的 Markdown 快照或研究摘要
- `webpages_html/`：同内容的离线 HTML 包装版
- `web_snapshot_index.md`：网页快照索引

说明：U.S. Army / U.S. Government 页面尽量保存正文摘录；Anduril、Palantir、Northrop 等企业网页因 JavaScript、版权和动态文档限制，保存的是结构化研究摘要、短摘录和原始链接，建议以原始链接核验全文。
