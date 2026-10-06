# Verification

- Result: PASS
- Environment: Windows、Python 3.11.7、PyYAML 6.0.1、Node.js 24.19.0、OpenSpec 1.14.1。
- Scope: 通用模板、接入行为、配置与引用、临时消费者。

## Commands

| Command / Check | Exit code | Result | Evidence |
|---|---|---|---|
| python -X utf8 scripts/validate_kit.py | 0 | PASS | schema、技能、模板、依赖图、本地引用与载荷引用闭包有效。 |
| skill-creator/scripts/quick_validate.py .agents/skills/openspec-workflow | 0 | PASS | Skill is valid。 |
| python -X utf8 -m unittest discover -s tests -v | 0 | PASS | 14 项，13 项通过、1 项因 WinError 1314 无符号链接创建权限而跳过；真实 Windows junction 检查通过。 |
| openspec schema validate workflow-spec-driven | 0 | PASS | 本地 schema 有效。 |
| openspec validate bootstrap-workflow-kit --strict | 0 | PASS | 六项需求与场景的 change 有效。 |
| openspec status / instructions apply --json | 0 | PASS | 识别四类制品和任务跟踪；制品存在不作为验收证据。 |
| 临时消费者接入与 CLI 检查 | 0 | PASS | 预览无目录；载荷仅为显式 22 文件；schema 识别、四类 instructions、严格 change 校验和任务完成状态通过。 |
| git diff --cached --check 与实际候选 diff 审查 | 0 | PASS | 格式检查无问题；文件清单均属于本次构建。 |

符号链接实际创建测试为环境限制下的未执行子检查；结果保留为 skipped，未声称通过。没有依赖该测试修改主机权限。没有独立审查或自动 CI。

## Acceptance mapping

- 可配置与授权隔离：通用载荷读取目标项目上下文，无源项目业务和固定技术栈；本次用户授权仅在 bootstrap 记录。
- 过程证据：角色、skill 和 processing 模板明确 SELF_REVIEW / NOT_RUN，不以制品存在判验收。
- 接入安全：行为测试覆盖默认预览、前后清单冲突、目录/父文件冲突、排除、未知排除、幂等、内容与修改时间、根许可证和 Git 保留、源目录拒绝、预览后变化及 Windows junction。
- CLI 可用性：模板直接接入临时消费者，验证本地 schema、四类制品指令、严格格式与任务状态。
- 导出范围：只导出 22 个工作流文件，changes 与 specs 初始为空，不导出工具包构建记录或根 README / LICENSE。
- 交付：依据当前用户授权在验收后同步稳定规范、归档，再提交推送至指定远程。

## Archive preparation

任务完成，方案和实现均为明确自审，无未解决阻断项。将 workflow-template delta 的六项 ADDED Requirements 同步为 stable spec，其他规范不变。源为 changes/bootstrap-workflow-kit，目标为 changes/archive/2026-10-06-bootstrap-workflow-kit；归档前检查目标不存在且路径位于当前项目 changes 内。

归档、提交和推送是验收后的交付，实际结果以归档记录、Git 历史和最终交付消息为准。

## Post-archive checks

- OpenSpec archive bootstrap-workflow-kit --yes：退出码 0，同步 6 项 ADDED Requirements，归档日期为 Asia/Shanghai 的 2026-10-06。
- 归档时提示 Purpose 少于 50 字符，已补全具体目标和边界，同步稳定规范及归档 delta。
- OpenSpec validate --specs --strict：退出码 0，1 个 stable spec 通过，0 失败。
- OpenSpec schema validate workflow-spec-driven：退出码 0。
- validate_kit.py：退出码 0，30 个 Markdown、38 处本地引用及导出引用闭包通过；README 指向实际 archive。
