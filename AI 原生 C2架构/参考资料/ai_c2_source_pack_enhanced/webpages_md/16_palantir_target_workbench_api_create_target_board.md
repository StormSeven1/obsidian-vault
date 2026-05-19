# Palantir Target Workbench API - Create Target Board

- 原始链接：https://www.palantir.com/docs/gotham/api/target-workbench/targetBoard/create-target-board
- 来源类型：Palantir API documentation
- 本地保存状态：Markdown + HTML structured API note; extracted via web.open
- 研究价值：核验 Target Board、默认列、RID、security 字段。

## 核心要点

- Endpoint: POST /api/gotham/v1/twb/targetBoard。
- 默认创建 columns：IDENTIFIED TARGET, PRIORITIZED TARGET, IN COORDINATION, IN EXECUTION, COMPLETE。
- Response 返回 targetBoardRid。
- Request body 包含 name、description、highPriorityTargetList、configuration、security。

## 本地摘录 / 结构化正文

Endpoint: POST /api/gotham/v1/twb/targetBoard

By default, creates a TargetBoard with default columns: IDENTIFIED TARGET, PRIORITIZED TARGET, IN COORDINATION, IN EXECUTION, COMPLETE. Returns the RID of the created TargetBoard.

Request body: CreateTargetBoardRequestV2 with fields including name, description, highPriorityTargetList, configuration, and security. Security mutation details can override system default security when creating/updating data.

Response body: CreateTargetBoardResponseV2 with targetBoardRid, the unique resource identifier of a Target Board.

---

> 注：本文件为离线研究快照。美国陆军/DoD/DVIDS 类材料通常为公有领域或官方公开资料；企业官网、API 文档与媒体页面仅保留研究摘要和短摘录，建议以原始链接核验全文。
