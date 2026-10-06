# Change Status

- Change: bootstrap-workflow-kit
- Current stage: ARCHIVED
- Review mode: SELF_REVIEW
- Scope authorization: 当前用户要求在独立仓库提炼工作流模板，可实现模板、脚本、验证和说明。
- Delivery authorization: 当前用户明确授权推送至 https://github.com/Ysuestc/OpenSpec-Workflow-Kit。
- Timezone: Asia/Shanghai
- Updated at: 2026-10-06

## Decisions and blockers

无未解决阻断项。原项目只读，消费者上下文可配置；本次 Git 授权不进入通用载荷。符号链接测试受主机权限限制跳过，真实 junction 检查通过，边界见 verification.md。

## Transitions

| Time | From | To | Evidence |
|---|---|---|---|
| 2026-10-06 | INIT | DESIGNING | 核对用户请求、原工作流、目标空目录与空远程。 |
| 2026-10-06 | DESIGNING | REVIEWING_SPEC | proposal、specs、design、tasks 完成。 |
| 2026-10-06 | REVIEWING_SPEC | IMPLEMENTING | 方案自审通过，见 spec-review.md。 |
| 2026-10-06 | IMPLEMENTING | REVIEWING_CODE | 模板和脚本完成，已检查实际暂存 diff。 |
| 2026-10-06 | REVIEWING_CODE | VERIFYING | code-review.md 记录修复和已接受限制，无阻断。 |
| 2026-10-06 | VERIFYING | DONE | 行为测试、引用、技能、schema、change 和临时消费者验证完成。 |
| 2026-10-06 | DONE | ARCHIVED | OpenSpec 同步 6 项需求并归档；源 change 已移除。 |

## Delivery

稳定规范 openspec/specs/workflow-template/spec.md 已同步 6 项需求，变更已归档到当前目录。Git 交付按本次用户已有授权执行，结果以实际提交和最终交付消息为准。
