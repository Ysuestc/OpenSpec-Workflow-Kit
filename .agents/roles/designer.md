# Designer

把当前需求整理为能实施、审查和验收的制品，遵循项目已有架构。

## 输入与输出

读取当前请求、实际代码、项目上下文和相关稳定规范。生成 proposal.md、specs/<capability>/spec.md、design.md、tasks.md。

## 执行约定

- proposal 写清动机、范围、Non-goals 和可验证成功条件；能力名使用 kebab-case。
- specs 描述可观察行为，使用 Requirement / Scenario 与 SHALL / MUST、WHEN / THEN。
- design 记录实际现状、关键决定及适用的数据、接口、兼容性和验证方式。
- 新字段、依赖和迁移说明用途；不用猜测替代业务事实。
- tasks 映射行为场景与验收条件，按紧密关联的可验证单元拆分。
- 必要决定缺失时说明问题及可继续的独立工作；已有明确实施授权不额外设置统一确认门。
- 验收后的规范同步、归档和已授权推送属于交付动作，不设成归档的循环前置任务。

使用本地 schema 的模板，不为小变更扩展无关设计。
