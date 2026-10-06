---
name: openspec-workflow
description: 在采用此模板的仓库中创建或继续 OpenSpec 阶段变更，组织方案、角色审查、受控实现、验证、规范同步与归档，并在当前用户授权范围内交付。
---

# OpenSpec Workflow

读取 [AGENTS](../../../AGENTS.md)、[项目上下文](../../../docs/project-context.md) 和 [工作流](../../../docs/workflow.md)，只加载相关能力与当前 change。

1. 根据实际请求判断是在准备方案还是已授权实现，选择或继续匹配的 change；不从模板推断权限。
2. 读取当前状态及最新证据，按 [schema](../../../openspec/schemas/workflow-spec-driven/schema.yaml) 维护四类制品和 [过程模板](../../../openspec/schemas/workflow-spec-driven/templates/processing/)。
3. 按需承担 [协调](../../roles/coordinator.md)、[设计](../../roles/designer.md)、[方案审查](../../roles/spec-reviewer.md)、[实现](../../roles/implementer.md)、[实现审查](../../roles/code-reviewer.md)、[验证归档](../../roles/verifier-archiver.md) 职责。
4. 在明确范围内连续工作，逐项提供真实验证证据；必要输入缺失时记录问题并继续独立工作，不伪造通过。
5. 验收后同步稳定规范并归档；提交、推送、部署或外部消息只执行用户已经授权的动作，报告实际结果。

默认单助手顺序承担角色，自审如实标明。用户明确要求多 agent 才使用现有协作工具，不假定任何产品专用注册或运行器已安装。

CLI 不可用时按模板手动维护，说明检查方式和限制。遵循实际项目技术栈、分支、时区与验证命令，不安装全局工具或修改无关配置。
