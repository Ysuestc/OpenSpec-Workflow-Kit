# Context

参考流程已存在于原项目，但其中项目背景、技术栈、分支和初始业务设计确认条件不能作为通用约束。用户明确要求创建独立模板仓库并推送；该授权仅用于本次构建交付。

当前环境为 Windows、Python 3.11、PyYAML 6.0.1。使用可用的 Node.js 24 与 OpenSpec 1.14.1 本地缓存执行验证，不安装全局工具。

# Goals / Non-Goals

目标：可读的通用契约、真实的过程记录、可验证接入行为及局部配置。
非目标：运行器、业务代码、自动部署或消费者项目的 Git 变更。

# Decisions

1. 六个角色作为 Markdown 职责契约，默认单助手顺序执行；自审明确标识。
2. 技能入口保持简洁并通过相对引用加载上下文、流程和角色；不携带外部产品专用注册格式。
3. schema 为 workflow-spec-driven，保留 proposal / specs / design / tasks 四类原生制品；processing 是手动过程记录模板。
4. scripts/apply_template.py 使用标准库和显式文件清单。先预检所有输出，再创建目录和写入；默认仅展示 CREATE / SAME / CONFLICT / EXCLUDED。
5. 已有不同内容、目录、符号链接或越过目标根的路径阻断整批写入；相同文件保持原修改时间。--exclude 只能排除明确的清单路径，不提供强制覆盖。
6. 排除工具包 README、Git、测试、脚本、bootstrap 历史及 stable specs。目标根许可证保留，源 MIT 通知输出为 docs/workflow-kit-LICENSE。
7. scripts/validate_kit.py 使用 PyYAML 检查 schema、frontmatter、依赖图、模板和 Markdown 本地链接；unittest 验证有意义的接入行为。开发依赖不进入导出项目。
8. 验收前任务只要求完成实现、审查、验证与归档准备；验收后的规范同步、归档和推送单独记录，避免循环前置。

# Risks / Trade-offs

- 预检避免确定性冲突导致部分写入，但不提供并发锁或文件系统事务；接入时不得同时修改目标文件。
- 既有 AGENTS 或 OpenSpec 配置需人工合并并显式排除，脚本不猜测合并策略。
- 符号链接目录即使指向根内也拒绝，简化路径安全和跨平台行为。
- CLI artifact 状态不代表业务验收；额外过程记录依赖助手维护。

# Validation Strategy

运行 Python 行为测试、技能验证、模板与链接检查、OpenSpec schema/change 严格校验；将载荷应用到临时新项目，验证其 schema 与制品指令。自审记录真实检查，交付前核对文件清单、原仓库状态与目标远程。

# Delivery

本次用户已授权在 V:/OpenSpec-Workflow-Kit 创建和推送，使用 main 普通推送至明确远程。消费者项目不继承该约定；原仓库保持不变。归档按 Asia/Shanghai 项目环境日期 2026-10-06。
