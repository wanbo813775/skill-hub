---
name: alibaba-java-guidelines
description: 基于阿里巴巴 Java 开发手册编写、修改和审查 Java/Spring 代码、MySQL 表与 SQL、接口契约、测试及技术设计文档。当用户要求按阿里巴巴开发规范实现、重构、审查或编写 Java 后端相关文档时使用；不用于与 Java 后端无关的通用写作或纯前端任务。
---

# 阿里巴巴 Java 开发规范

以用户的实际任务为主线，在开发、修改、审查 Java 后端代码或编写技术文档时，应用《阿里巴巴 Java 开发手册》的工程规则。

## 规范基线

本 Skill 基于手册 1.7.0 “嵩山版”（2020-08-03）整理，保留三级约束语义：

- **强制**：在适用且不与更高优先级要求冲突时必须遵守。
- **推荐**：默认采用；偏离时应有明确的工程理由。
- **参考**：作为设计和取舍的检查项，不机械执行。

不要把规范级别直接当作缺陷严重程度。代码审查的严重程度应由实际的正确性、安全、数据和可用性影响决定。

## 工作方式

1. 先读取项目的 `AGENTS.md`、README、构建文件、格式化/静态检查配置和已有代码惯例，确认 JDK、Spring、ORM 和 MySQL 版本。
2. 只读取与当前任务相关的参考文件，不要一次加载全部规范。
3. 实现时先保证用户要求和现有公开契约，再在适用范围内落实规范；不为了套用规范而扩大修改范围。
4. 完成后运行项目现有的格式化、编译、静态检查和相关测试。规范无法通过工具验证时，说明人工检查结果和未验证项。

## 按任务加载参考

- Java 命名、常量、格式、OOP 和日期时间：读取 [references/java-basics.md](references/java-basics.md)。
- 集合、并发、控制语句和通用性能规则：读取 [references/collections-concurrency.md](references/collections-concurrency.md)。
- Javadoc、注释、前后端 API 契约和接口文档：读取 [references/api-documentation.md](references/api-documentation.md)。
- 错误码、异常和日志：读取 [references/exceptions-logging.md](references/exceptions-logging.md)。
- 单元测试和安全性：读取 [references/testing-security.md](references/testing-security.md)。
- MySQL 建表、索引、SQL 和 ORM：读取 [references/mysql.md](references/mysql.md)。
- 应用分层、依赖管理、系统设计和技术方案文档：读取 [references/architecture-design.md](references/architecture-design.md)。

## 处理冲突和时效性

- 用户明确要求和仓库内的有效约定优先于本规范；发现冲突时要指出差异和影响。
- 对于与 JDK 8、旧 ORM/模板引擎、旧 MySQL 或 2020 年工程环境绑定的条目，先根据当前版本核实，不使用已过时 API 替换现代做法。
- 涉及安全、隐私、日志留存或无障碍的要求时，本规范不代替现行法律、组织政策或最新安全标准。

## 输出要求

- **开发/修改**：交付可运行的实现，并简要说明对实际决策有影响的规范；不罗列无关条款。
- **代码审查**：每个问题给出文件位置、观察到的行为、实际影响、对应规范级别和可执行修复建议。
- **技术文档**：根据系统复杂度表达边界、模块关系、关键流程、数据结构、异常路径、非功能需求、取舍与验证方案；只在能提高理解度时增加图。
