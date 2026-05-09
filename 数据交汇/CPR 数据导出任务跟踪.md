
## 当前运行中的任务

  

### 任务一：001/002 数据集导出（batch_export.py）

  

- **PID**: 954803

- **脚本**: `/mnt/local4t/storm/CPRExport/docs/batch_export.py`

- **输出目录**: `/mnt/local4t/storm/CPRExport/export_output/`

- **日志**: `/mnt/local4t/storm/CPRExport/export_output/export.log`

- **策略**: 从 4470 个 CPR 文件中均匀采样 344 个，按目标大小/文件数控制导出量

- **注意**: 该任务也在导出 003 数据，但因 ch 31 数据稀疏，003 部分不会达标（由任务二补充）

  

| 子数据集 | 目标大小 | 目标文件数 | 备注 |

|----------|----------|------------|------|

| 001 雷达回波 | 20 GB | 20 | ch 1 |

| 001 雷达航迹 | 2 GB | 10 | ch 2 |

| 002 雷达回波 | 22 GB | 21 | ch 11 |

| 002 雷达航迹 | 1.8 GB | 8 | ch 12 |

| 003 原始航迹 | 10 GB | 10 | ch 31（采样不足，由任务二覆盖） |

| 003 分类航迹 | 11 GB | 10 | ch 31（采样不足，由任务二覆盖） |

  

### 任务二：003 数据集专用导出（export_003.py）

  

- **PID**: 1069255

- **脚本**: `/mnt/local4t/storm/CPRExport/docs/export_003.py`

- **输出目录**: `/mnt/local4t/storm/CPRExport/export_003/`

- **日志**: `/mnt/local4t/storm/CPRExport/export_003/export_003.log`

- **策略**: 全量遍历所有 4470 个 CPR 文件，只提取 ch 31 数据，达标即停

- **特性**: 导出时实时修正 TRACK_EXT 异常时间戳

  

| 子数据集 | 目标大小 | 目标文件数 | 备注 |

|----------|----------|------------|------|

| 003 原始航迹 | 10 GB | 10 | TRACK_* from ch 31，时间戳已修正 |

| 003 分类航迹 | 11 GB | 10 | BIRD_TRACK from ch 31 |

  

---

  

## 进度查看命令

  

### 1. 检查进程是否存活

  

```bash

# 任务一

ps -p 954803 -o pid,etime,%cpu,rss,cmd --no-headers

  

# 任务二

ps -p 1069255 -o pid,etime,%cpu,rss,cmd --no-headers

  

# 如果无输出，说明进程已结束

```

  

### 2. 查看实时日志

  

```bash

# 任务一日志

tail -20 /mnt/local4t/storm/CPRExport/export_output/export.log

  

# 任务二日志

tail -20 /mnt/local4t/storm/CPRExport/export_003/export_003.log

```

  

### 3. 查看已导出数据量

  

```bash

# 任务一各数据集大小

du -sh /mnt/local4t/storm/CPRExport/export_output/*/

  

# 任务二 003 各子目录大小

du -sh /mnt/local4t/storm/CPRExport/export_003/2022ZD0116409-003-威海外场岸基对空雷达观测数据/*/

```

  

### 4. 一键查看全部状态

  

```bash

echo "=== 进程状态 ===" && \

ps -p 954803,1069255 -o pid,etime,%cpu,cmd --no-headers 2>/dev/null || echo "  (部分进程已结束)" && \

echo "" && \

echo "=== 任务一 (001/002) ===" && \

tail -3 /mnt/local4t/storm/CPRExport/export_output/export.log && \

du -sh /mnt/local4t/storm/CPRExport/export_output/*/ && \

echo "" && \

echo "=== 任务二 (003) ===" && \

tail -3 /mnt/local4t/storm/CPRExport/export_003/export_003.log && \

du -sh /mnt/local4t/storm/CPRExport/export_003/2022ZD0116409-003-威海外场岸基对空雷达观测数据/*/

```

  

---

  

## 判断任务是否完成

  

### 任务一完成标志

  

- 进程不存在（`ps -p 954803` 无输出）

- 日志末尾出现 `导出完成!` 和各子数据集结果

- 或出现 `所有子数据集已达标，提前停止！`

- 生成汇总文件: `/mnt/local4t/storm/CPRExport/export_output/export_summary.json`

  

```bash

# 检查是否完成

grep "导出完成" /mnt/local4t/storm/CPRExport/export_output/export.log

```

  

### 任务二完成标志

  

- 进程不存在（`ps -p 1069255` 无输出）

- 日志末尾出现 `导出完成!` 或 `两个子数据集均已达标，提前停止！`

- 生成汇总文件: `/mnt/local4t/storm/CPRExport/export_003/export_003_summary.json`

  

```bash

# 检查是否完成

grep "导出完成\|已达标" /mnt/local4t/storm/CPRExport/export_003/export_003.log

```

  

---

  

## 导出完成后的操作

  

### 1. 任务一完成后：修复 003 原始航迹时间戳

  

任务一导出的 003 原始航迹数据存在异常时间戳（TRACK_EXT 包约 46% 无效），需要后处理修复：

  

```bash

python3 /mnt/local4t/storm/CPRExport/docs/fix_timestamps.py \

  /mnt/local4t/storm/CPRExport/export_output/2022ZD0116409-003-威海外场岸基对空雷达观测数据/对空雷达原始航迹数据/

```

  

> 注：任务二的 003 数据不需要此步骤（导出时已实时修正）。

  

### 2. 最终数据集组装

  

- **001/002 数据集**: 直接使用任务一的输出 (`export_output/` 下对应目录)

- **003 数据集**: 使用任务二的输出 (`export_003/` 下的目录)，时间戳已修正

  

### 3. 校验导出数据

  

使用校验脚本检查数据完整性和内容：

  

```bash

# 校验任务一输出（汇总模式，跳过详情）

python3 /mnt/local4t/storm/CPRExport/docs/validate_dataset.py \

  /mnt/local4t/storm/CPRExport/export_output --no-detail

  

# 校验任务二输出

python3 /mnt/local4t/storm/CPRExport/docs/validate_dataset.py \

  /mnt/local4t/storm/CPRExport/export_003 --no-detail

  

# 查看某个文件的详细内容样本

python3 /mnt/local4t/storm/CPRExport/docs/validate_dataset.py \

  /path/to/某文件.dat --samples 5

```

  

### 4. 输出 JSON 校验报告（可选）

  

```bash

python3 /mnt/local4t/storm/CPRExport/docs/validate_dataset.py \

  /mnt/local4t/storm/CPRExport/export_output --json export_output_report.json

  

python3 /mnt/local4t/storm/CPRExport/docs/validate_dataset.py \

  /mnt/local4t/storm/CPRExport/export_003 --json export_003_report.json

```

  

---

  

## 脚本清单

  

| 脚本 | 用途 | 依赖 web 后端 |

|------|------|---------------|

| `docs/batch_export.py` | 001/002/003 定量批量导出 | 是（cpr_parser.py） |

| `docs/export_003.py` | 003 专用全量导出 + 时间戳修正 | 是（cpr_parser.py） |

| `docs/validate_dataset.py` | 校验 DAT 文件内容完整性 | **否（完全独立）** |

| `docs/fix_timestamps.py` | 后处理修复异常时间戳 | **否（完全独立）** |

| `docs/gather_stats.py` | 通过 API 收集数据统计 | 是（需启动 web 服务） |

  

> 导出脚本（batch_export / export_003）依赖 `web/backend/cpr_parser.py` 作为 Python 模块，

> 但**不需要启动 web 服务**。运行时需 `cd` 到 `web/backend` 目录。

>

> 校验和修复脚本完全独立，任何人都可以直接运行。