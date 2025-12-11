# 日志管理指南

## 日志文件位置

所有日志文件存储在 `logs/` 目录下：

```
logs/
├── access.log         # API 访问日志（当前）
├── access.log.1       # API 访问日志（备份1）
├── access.log.2       # API 访问日志（备份2）
├── app.log            # 应用日志（当前）
├── app.log.1          # 应用日志（备份1）
├── error.log          # 错误日志（当前）
└── error.log.2025-12-09  # 错误日志（按天备份）
```

## 日志类型

### 1. 访问日志 (access.log)
记录所有 API 请求

**轮转策略**：
- 单个文件最大 **10MB**
- 保留最近 **30 个备份文件**
- 自动压缩旧文件

**示例**：
```
2025-12-10 18:30:15 - uvicorn.access - INFO - 127.0.0.1:55432 - "GET /api/v1/task/ HTTP/1.1" 200 OK
```

### 2. 错误日志 (error.log)
记录所有错误和异常

**轮转策略**：
- **每天午夜**自动轮转
- 保留最近 **30 天**的日志
- 旧文件自动归档

**示例**：
```
2025-12-10 18:30:15 - app - ERROR - Database connection failed
```

### 3. 应用日志 (app.log)
记录应用程序事件

**轮转策略**：
- 单个文件最大 **10MB**
- 保留最近 **10 个备份文件**

**示例**：
```
2025-12-10 18:30:15 - app - INFO - [启动] AGVC System v0.1.0
```

## 日志级别

- **DEBUG**: 详细调试信息
- **INFO**: 常规信息（默认）
- **WARNING**: 警告信息
- **ERROR**: 错误信息
- **CRITICAL**: 严重错误

## 容量管理

### 自动清理

日志文件会**自动管理**，不需要手动清理：

| 日志类型 | 最大单文件 | 保留数量 | 最大总容量 |
|---------|----------|---------|-----------|
| access.log | 10MB | 30 个 | ~300MB |
| error.log | 不限 | 30 天 | 取决于错误量 |
| app.log | 10MB | 10 个 | ~100MB |

**总计**: 约 **400-500MB**

### 手动清理

如需手动清理旧日志：

```bash
# Windows
rd /s /q logs
mkdir logs

# Linux/Mac
rm -rf logs/
mkdir logs
```

## 查看日志

### 实时查看（Windows PowerShell）
```powershell
Get-Content logs\access.log -Wait -Tail 50
```

### 查找特定时间的日志
```powershell
Select-String -Path logs\access.log -Pattern "2025-12-10 18:"
```

### 统计错误数量
```powershell
(Select-String -Path logs\error.log -Pattern "ERROR").Count
```

## 日志分析

### 最常访问的端点
```bash
# 统计 API 访问频率
grep "GET\|POST\|PUT\|DELETE" logs/access.log | cut -d'"' -f2 | sort | uniq -c | sort -rn | head -10
```

### 响应时间分析
```bash
# 查找慢请求（响应时间 > 1秒）
grep "HTTP/1.1\" [0-9]* [1-9][0-9][0-9][0-9]" logs/access.log
```

## 配置修改

如需修改日志配置，编辑 `app/core/logging_config.py`：

```python
# 修改文件大小限制（默认 10MB）
maxBytes=20 * 1024 * 1024,  # 改为 20MB

# 修改保留数量（默认 30 个）
backupCount=60,  # 改为保留 60 个

# 修改轮转周期（默认每天）
when='midnight',  # 可改为 'H'（每小时）, 'D'（每天）, 'W0'（每周一）
```

## 生产环境建议

1. **定期归档**: 将旧日志移至长期存储
2. **监控日志大小**: 设置磁盘空间告警
3. **日志分析工具**: 考虑使用 ELK Stack 或 Grafana Loki
4. **敏感信息**: 确保日志中不包含密码等敏感数据

## 故障排查

### 日志文件权限错误
```bash
# 确保 logs 目录有写入权限
chmod 755 logs/
```

### 日志文件过大
```bash
# 立即触发轮转（手动创建新文件）
mv logs/access.log logs/access.log.backup
# 重启服务器将自动创建新的 access.log
```

## 禁用日志（不推荐）

如果需要临时禁用文件日志，注释掉 `app/main.py` 中的：

```python
# setup_logging()  # 注释此行
```

但仍会在控制台显示日志。
