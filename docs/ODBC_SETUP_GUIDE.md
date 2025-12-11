# PostgreSQL ODBC 配置指南

本文档说明如何配置 Windows ODBC 数据源以连接到 AGVC PostgreSQL 数据库。

## 目录

1. [数据库连接信息](#数据库连接信息)
2. [ODBC 驱动程序安装](#odbc-驱动程序安装)
3. [32位/64位识别](#32位64位识别)
4. [ODBC 数据源配置](#odbc-数据源配置)
5. [LabVIEW 配置](#labview-配置)
6. [其他应用程序配置](#其他应用程序配置)
7. [故障排除](#故障排除)

---

## 数据库连接信息

### AGVC PostgreSQL 数据库参数

| 参数 | 值 | 说明 |
|------|-----|------|
| **服务器地址** | `localhost` | 本地主机 |
| **端口** | `5432` | PostgreSQL 默认端口 |
| **数据库名称** | `agvc` | AGVC 系统数据库 |
| **用户名** | `agvc` | 数据库用户 |
| **密码** | `36274806` | 数据库密码 |
| **SSL 模式** | `disable` | 本地连接不需要 SSL |

### 连接字符串

**ODBC DSN 连接**：
```
DSN=PostgreSQL35W;
```

**ODBC 完整连接字符串**（无 DSN）：
```
Driver={PostgreSQL Unicode};
Server=localhost;
Port=5432;
Database=agvc;
Uid=agvc;
Pwd=36274806;
```

**PostgreSQL 标准连接字符串**：
```
postgresql://agvc:36274806@localhost:5432/agvc
```

---

## ODBC 驱动程序安装

### 下载 PostgreSQL ODBC 驱动

**官方下载地址**：
https://www.postgresql.org/ftp/odbc/versions/msi/

### 选择正确的版本

#### 32位驱动（用于 32位应用程序）
```
psqlodbc_xx_xx_xxxx-x86.msi
```

**适用于**：
- LabVIEW 32位
- Excel 32位
- Access 32位
- 其他 32位应用程序

#### 64位驱动（用于 64位应用程序）
```
psqlodbc_xx_xx_xxxx-x64.msi
```

**适用于**：
- LabVIEW 64位
- Excel 64位
- Power BI Desktop
- 其他 64位应用程序

### 安装步骤

1. 下载对应位数的 MSI 文件
2. 双击运行安装程序
3. 选择默认安装路径
4. 完成安装

**⚠️ 重要**：
- 如果不确定，可以同时安装 32位和 64位驱动
- 两个版本可以共存，不会冲突

---

## 32位/64位识别

### Windows ODBC 管理器位置

Windows 系统有**两个**独立的 ODBC 数据源管理器：

| 位数 | 管理器路径 | 快速打开方式 |
|------|-----------|-------------|
| **32位** | `C:\Windows\SysWOW64\odbcad32.exe` | Win+R → `C:\Windows\SysWOW64\odbcad32.exe` |
| **64位** | `C:\Windows\System32\odbcad32.exe` | Win+R → `odbcad32.exe` |

### 检查应用程序位数

#### LabVIEW
1. 打开 LabVIEW
2. 帮助 → 关于 LabVIEW
3. 查看版本号是否有 **(64-bit)** 标识
   - 有 **(64-bit)** → 使用 64位 ODBC
   - 没有 → 使用 32位 ODBC

#### Excel / Office
1. 打开 Excel
2. 文件 → 帐户 → 关于 Excel
3. 查看版本号
   - 有 **(64-bit)** → 使用 64位 ODBC
   - 没有 → 使用 32位 ODBC

#### 使用 PowerShell 检查已安装的驱动

```powershell
# 检查 32位 ODBC 驱动
Get-OdbcDriver -Platform "32-bit" | Where-Object {$_.Name -like "*PostgreSQL*"}

# 检查 64位 ODBC 驱动
Get-OdbcDriver -Platform "64-bit" | Where-Object {$_.Name -like "*PostgreSQL*"}
```

---

## ODBC 数据源配置

### 步骤 1: 打开对应位数的 ODBC 管理器

**对于 32位应用程序**（如 LabVIEW 32位）：
```
Win+R → C:\Windows\SysWOW64\odbcad32.exe
```

**对于 64位应用程序**：
```
Win+R → odbcad32.exe
```

### 步骤 2: 添加新的数据源

1. 选择 **"系统 DSN"** 标签（推荐）
   - 系统 DSN：所有用户可用
   - 用户 DSN：仅当前用户可用

2. 点击 **"添加"** 按钮

3. 选择驱动程序：
   - **PostgreSQL Unicode(x64)** （64位）
   - **PostgreSQL Unicode** （32位）
   - 或 **PostgreSQL ANSI**

4. 点击 **"完成"**

### 步骤 3: 配置连接参数

在 PostgreSQL ODBC Driver Setup 窗口中填写：

#### 基本设置（左侧）

| 字段 | 填写内容 | 必填 |
|------|---------|------|
| **Data Source** | `AGVC` | ✅ 是 |
| **Database** | `agvc` | ✅ 是 |
| **Server** | `localhost` | ✅ 是 |
| **User Name** | `agvc` | ✅ 是 |
| **Port** | `5432` | ✅ 是 |
| **Password** | `36274806` | ✅ 是 |

#### 扩展设置（右侧）

| 字段 | 填写内容 | 说明 |
|------|---------|------|
| **Description** | `AGVC Database Connection` | 可选，描述此连接 |
| **SSL Mode** | `disable` | 本地连接不需要 SSL |

### 配置截图示例

```
┌──────────────────────────────────────────────────────┐
│ PostgreSQL ANSI ODBC Driver (psqlODBC) Setup         │
├──────────────────────────────────────────────────────┤
│                                                       │
│ Data Source:  PostgreSQL35W                          │
│ Database:     agvc                                   │
│ Server:       localhost                              │
│ User Name:    agvc                                   │
│                                                       │
│ Port:         5432                                   │
│ Password:     36274806                               │
│                                                       │
│ Description:  AGVC Database Connection               │
│ SSL Mode:     disable                                │
│                                                       │
│ [Datasource]  [Global]              [Test]  [Save]  │
└──────────────────────────────────────────────────────┘
```

### 步骤 4: 测试连接

1. 点击 **"Test"** 按钮

2. **预期结果**：
   ```
   Connection successful
   ```

3. 如果测试成功，点击 **"Save"** 保存配置

### 步骤 5: 验证数据源

在 ODBC 管理器的系统 DSN 列表中，应该能看到：

| 名称 | 驱动程序 |
|------|---------|
| PostgreSQL35W | PostgreSQL Unicode (或 ANSI) |

---

## LabVIEW 配置

### 连接方式 1: 使用 DSN

在 LabVIEW 的 **DB Tools Open Connection.vi** 中：

**连接字符串**：
```
DSN=PostgreSQL35W;
```

**VI 配置**：
```
┌────────────────────────────────┐
│ DB Tools Open Connection       │
├────────────────────────────────┤
│ connection string:             │
│ DSN=PostgreSQL35W;             │
│                                │
│ user name:  [留空]             │
│ password:   [留空]             │
│                                │
│ → connection out               │
└────────────────────────────────┘
```

**说明**：
- 用户名和密码已在 DSN 中保存，无需再次输入
- 如果需要覆盖，可在 VI 中输入

### 连接方式 2: 完整连接字符串（不使用 DSN）

**连接字符串**：
```
Driver={PostgreSQL Unicode};Server=localhost;Port=5432;Database=agvc;Uid=agvc;Pwd=36274806;
```

**VI 配置**：
```
┌────────────────────────────────┐
│ DB Tools Open Connection       │
├────────────────────────────────┤
│ connection string:             │
│ Driver={PostgreSQL Unicode};   │
│ Server=localhost;              │
│ Port=5432;                     │
│ Database=agvc;                 │
│ Uid=agvc;                      │
│ Pwd=36274806;                  │
│                                │
│ user name:  [留空]             │
│ password:   [留空]             │
│                                │
│ → connection out               │
└────────────────────────────────┘
```

### LabVIEW 示例程序

#### 连接并查询数据

```
┌─────────────────────────────────────────┐
│ 1. DB Tools Open Connection.vi          │
│    connection string: DSN=PostgreSQL35W;│
│    → connection out                      │
│                                          │
│ 2. DB Tools Select Data.vi               │
│    connection in: [来自步骤1]            │
│    SQL Statement: SELECT * FROM agv      │
│    → data (Recordset)                    │
│                                          │
│ 3. DB Tools Close Connection.vi          │
│    connection in: [来自步骤1]            │
└─────────────────────────────────────────┘
```

### 常见错误处理

#### 错误 1: "驅動程式和應用程式架構不相符"

**原因**: LabVIEW 和 ODBC 驱动位数不匹配

**解决**:
1. 确认 LabVIEW 位数（32位或64位）
2. 在对应位数的 ODBC 管理器中配置 DSN
3. 重启 LabVIEW

#### 错误 2: "找不到数据源名称"

**原因**: DSN 名称错误或未配置

**解决**:
1. 检查 DSN 名称是否正确（区分大小写）
2. 确认在正确位数的 ODBC 管理器中配置了 DSN

#### 错误 3: "连接超时"

**原因**: PostgreSQL 未运行

**解决**:
```bash
# 检查 Docker 容器状态
docker ps | findstr postgres

# 启动容器
docker-compose up -d postgres
```

---

## 其他应用程序配置

### Excel

#### 连接步骤

1. 打开 Excel
2. **数据** → **获取数据** → **从其他源** → **从 ODBC**
3. 选择数据源：`PostgreSQL35W`
4. 点击 **确定**
5. 选择要导入的表

#### Power Query M 语言

```m
let
    Source = Odbc.DataSource("dsn=PostgreSQL35W", [HierarchicalNavigation=true]),
    agvc_Database = Source{[Name="agvc",Kind="Database"]}[Data],
    public_Schema = agvc_Database{[Name="public",Kind="Schema"]}[Data],
    agv_Table = public_Schema{[Name="agv",Kind="Table"]}[Data]
in
    agv_Table
```

### Access

1. 打开 Access
2. **外部数据** → **ODBC 数据库**
3. 选择 **链接到数据源**
4. 选择 **机器数据源**
5. 选择 `PostgreSQL35W`
6. 选择要链接的表

### Power BI Desktop

1. **获取数据** → **ODBC**
2. DSN: `PostgreSQL35W`
3. 选择表并加载

### Python

#### 使用 pyodbc

```python
import pyodbc

# 方法 1: 使用 DSN
conn = pyodbc.connect('DSN=PostgreSQL35W')

# 方法 2: 完整连接字符串
conn = pyodbc.connect(
    'Driver={PostgreSQL Unicode};'
    'Server=localhost;'
    'Port=5432;'
    'Database=agvc;'
    'Uid=agvc;'
    'Pwd=36274806;'
)

# 查询数据
cursor = conn.cursor()
cursor.execute("SELECT * FROM agv")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
```

### C# / .NET

```csharp
using System.Data.Odbc;

string connectionString = "DSN=PostgreSQL35W;";

using (OdbcConnection conn = new OdbcConnection(connectionString))
{
    conn.Open();

    OdbcCommand cmd = new OdbcCommand("SELECT * FROM agv", conn);
    OdbcDataReader reader = cmd.ExecuteReader();

    while (reader.Read())
    {
        Console.WriteLine(reader["name"]);
    }
}
```

---

## 故障排除

### 问题 1: 找不到 ODBC 驱动

**症状**: 在 ODBC 管理器中看不到 PostgreSQL 驱动

**解决**:
1. 确认已安装 PostgreSQL ODBC 驱动
2. 检查是否在正确位数的管理器中查看
3. 重新安装驱动程序

### 问题 2: 测试连接失败

**检查清单**:

- [ ] PostgreSQL 容器是否运行？
  ```bash
  docker ps | findstr postgres
  ```

- [ ] 端口 5432 是否开放？
  ```bash
  netstat -an | findstr 5432
  ```

- [ ] 用户名密码是否正确？
  - 用户名: `agvc`
  - 密码: `36274806`

- [ ] 数据库名称是否正确？
  - 数据库: `agvc`

### 问题 3: 架构不匹配错误

**错误信息**: `驅動程式和應用程式架構不相符`

**解决步骤**:

1. **确认应用程序位数**
   ```
   LabVIEW: 帮助 → 关于 LabVIEW
   Excel: 文件 → 帐户 → 关于 Excel
   ```

2. **在对应位数的管理器中配置**
   - 32位应用 → `C:\Windows\SysWOW64\odbcad32.exe`
   - 64位应用 → `C:\Windows\System32\odbcad32.exe`

3. **重新创建 DSN**
   - 删除旧的 DSN
   - 在正确位数的管理器中重新添加

### 问题 4: SSL 错误

**错误信息**: `SSL error` 或 `SSL connection error`

**解决**:
- 确保 SSL Mode 设置为 `disable`
- 本地连接不需要 SSL

### 问题 5: 编码问题（中文乱码）

**解决**:
1. 使用 **PostgreSQL Unicode** 驱动（而非 ANSI）
2. 在高级设置中：
   - Client Encoding: `UTF8`
   - Server Encoding: `UTF8`

### 验证配置的 PowerShell 脚本

```powershell
# 检查 DSN 是否存在（32位）
Write-Host "=== 32位 DSN ===" -ForegroundColor Yellow
Get-OdbcDsn -Platform "32-bit" | Where-Object {$_.Name -eq "PostgreSQL35W"} | Format-Table

# 检查 DSN 是否存在（64位）
Write-Host "`n=== 64位 DSN ===" -ForegroundColor Yellow
Get-OdbcDsn -Platform "64-bit" | Where-Object {$_.Name -eq "PostgreSQL35W"} | Format-Table

# 测试连接（需要修改为对应位数）
Write-Host "`n=== 测试连接 ===" -ForegroundColor Yellow
try {
    $conn = New-Object System.Data.Odbc.OdbcConnection("DSN=PostgreSQL35W")
    $conn.Open()
    Write-Host "✓ 连接成功！" -ForegroundColor Green
    $conn.Close()
} catch {
    Write-Host "✗ 连接失败: $($_.Exception.Message)" -ForegroundColor Red
}
```

---

## 快速参考

### 数据库信息

```
服务器: localhost
端口:   5432
数据库: agvc
用户:   agvc
密码:   36274806
```

### ODBC 管理器路径

```
32位: C:\Windows\SysWOW64\odbcad32.exe
64位: C:\Windows\System32\odbcad32.exe
```

### DSN 名称

```
PostgreSQL35W
```

### 连接字符串

```
# DSN 方式
DSN=PostgreSQL35W;

# 完整方式
Driver={PostgreSQL Unicode};Server=localhost;Port=5432;Database=agvc;Uid=agvc;Pwd=36274806;
```

### 常用查询

```sql
-- 查看所有表
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';

-- 查看 AGV 数据
SELECT * FROM agv;

-- 查看任务数据
SELECT * FROM task;

-- 查看端口数据
SELECT * FROM eqp_port;
```

---

## 安全注意事项

⚠️ **生产环境建议**：

1. **不要在连接字符串中明文保存密码**
   - 使用 DSN 存储凭据
   - 或使用环境变量

2. **限制网络访问**
   - 生产环境修改 PostgreSQL 监听地址
   - 使用防火墙限制访问

3. **使用 SSL 连接**
   - 生产环境启用 SSL
   - 配置 SSL 证书

4. **定期更换密码**
   - 使用强密码
   - 定期更新凭据

---

## 附录

### PostgreSQL ODBC 驱动版本历史

| 版本 | 发布日期 | 备注 |
|------|---------|------|
| 13.x | 2021+ | 支持 PostgreSQL 13+ |
| 12.x | 2020 | 支持 PostgreSQL 12 |
| 11.x | 2019 | 支持 PostgreSQL 11 |

### 支持的操作系统

- Windows 11
- Windows 10
- Windows Server 2019/2022
- Windows 8.1（需要旧版本驱动）

### 相关链接

- **PostgreSQL ODBC 官网**: https://odbc.postgresql.org/
- **驱动下载**: https://www.postgresql.org/ftp/odbc/versions/msi/
- **官方文档**: https://odbc.postgresql.org/docs/

---

**文档版本**: 1.0
**最后更新**: 2025-12-10
**维护者**: AGVC 团队
