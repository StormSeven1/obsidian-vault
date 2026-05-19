# Palantir Target Workbench API - Create Target Intel Target

- 原始链接：https://www.palantir.com/docs/gotham/api/target-workbench-v2-resources/targets/create-target-intel-target
- 来源类型：Palantir API documentation
- 本地保存状态：Markdown + HTML structured API note; extracted via web.open
- 研究价值：核验目标情报附着/Intel on Target API。

## 核心要点

- Endpoint: PUT /api/v2/targetWorkbench/targets/{targetRid}/createTargetIntel。
- 用于 Create Intel on Target by RID。
- domain enum 包含 SIGINT、OSINT、IMINT、ELINT、HUMINT、ALL_SOURCE、GEOINT 等。
- OAuth2 scope: api:target-write。

## 本地摘录 / 结构化正文

Endpoint: PUT /api/v2/targetWorkbench/targets/{targetRid}/createTargetIntel

Purpose: Create Intel on Target by RID.

OAuth2 scope: api:target-write.

Request body: CreateTargetIntelTargetRequest with fields such as id, name, description, domain, validTime, location, confidence, intelType, source.

Domain enum values: SIGINT, OSINT, IMINT, ELINT, HUMINT, OTHER, ALL_SOURCE, GEOINT, OPIR, FMV, COMINT.

Response body: EmptySuccessResponse.

Error examples include TargetNotFound and permission denied.

---

> 注：本文件为离线研究快照。美国陆军/DoD/DVIDS 类材料通常为公有领域或官方公开资料；企业官网、API 文档与媒体页面仅保留研究摘要和短摘录，建议以原始链接核验全文。
