# Why

将已验证的个人项目阶段开发流程提炼为可复用模板，让新项目和已有仓库采用可追溯的设计、审查、实现与验收流程，同时保留各自技术栈和授权边界。

# What Changes

- 提供通用协作规则、六个角色契约、项目技能和本地 OpenSpec schema。
- 用可填写项目上下文隔离业务背景、命令、时区和交付规则。
- 提供标准库接入脚本：默认预览、整批冲突预检、相同内容幂等、显式排除与路径边界检查。
- 保留模板 MIT 通知，导出流程而不导出本工具包 Git、README、初始化历史或稳定规范。
- 提供配置与引用验证、接入行为测试、使用说明和归档记录。

# Capabilities

## New Capabilities
- `workflow-template`: 通用阶段工作流及安全接入合同。

## Modified Capabilities
无。

# Impact

新仓库 V:/OpenSpec-Workflow-Kit，远程 https://github.com/Ysuestc/OpenSpec-Workflow-Kit。仅读取原工作流；不修改原项目，也不复制原始压缩包内部资料。PyYAML 仅为工具包开发检查依赖。

# Success Criteria

- 通用载荷不包含原项目业务、技术栈、固定分支或继承的推送授权。
- schema 和初始化 change 通过 OpenSpec 1.14.1 严格校验，技能与本地引用有效。
- 接入行为测试证明预览无写入、冲突前置停止、幂等、排除及路径边界。
- 新目标项目可识别 schema 并创建四类制品；不包含工具包构建历史。
- 完成验收后归档，并按当前用户明确授权提交推送到指定远程。

# Non-goals

业务系统开发、多 agent 运行器、自动 CI、第三方消息集成、部署及全局 CLI 安装。
