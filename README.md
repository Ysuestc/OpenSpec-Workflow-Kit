# OpenSpec Workflow Kit

一套可接入新项目或已有仓库的 OpenSpec 工作流模板：方案 → 方案审查 → 实现 → 实现审查 → 验证 → 规范同步与归档。

包含六个角色契约、项目技能、本地 schema、制品与过程模板，以及不会覆盖现有文件的接入脚本。项目名称、技术栈、验证命令、时区和交付授权由使用者配置。

## 快速接入

需要 Python 3.10+。接入脚本仅使用标准库。

```bash
git clone https://github.com/Ysuestc/OpenSpec-Workflow-Kit.git
cd OpenSpec-Workflow-Kit
python scripts/apply_template.py ../YourProject
python scripts/apply_template.py ../YourProject --apply
```

第一条 Python 命令只预览；第二条在没有冲突时写入。它不复制本工具包的 README、Git 历史、测试、脚本、初始化记录或稳定规范，也不覆盖项目根许可证；模板许可证单独保存为 docs/workflow-kit-LICENSE。

接入已有仓库时先看 [接入指南](docs/adoption.md)。冲突需要合并，可用 --exclude 排除已经人工合并的文件；没有强制覆盖选项。接入不会初始化 Git、修改远程、自动提交或启动 agent。

随后补充 [项目上下文](docs/project-context.md)，核对 [OpenSpec 配置](openspec/config.yaml)，向助手描述阶段需求：

> 使用 $openspec-workflow，先为当前需求创建 proposal、specs、design 和 tasks。

用户已经要求实现时，流程在明确范围内连续完成；用户只要求方案时，保留设计阶段。模板不会把另一个项目的确认或推送权限带入新项目。

## 文件入口

- [AGENTS.md](AGENTS.md)：通用协作规则。
- [工作流](docs/workflow.md)：角色、状态、授权、审查、验证和归档。
- [项目技能](.agents/skills/openspec-workflow/SKILL.md)：可显式调用的入口。
- [本地 schema](openspec/schemas/workflow-spec-driven/schema.yaml)：四类制品及依赖。
- [过程模板](openspec/schemas/workflow-spec-driven/templates/processing/)：状态、审查与验证记录。
- [接入指南](docs/adoption.md)：新项目、已有仓库和冲突处理。

角色契约可以由一个助手顺序执行，独立审查需要实际独立审查者。仓库没有自动多 agent 运行器、定时通知、CI 门控或业务 AI SDK。

## OpenSpec CLI

本版本使用 OpenSpec 1.14.1 验证。CLI 需要 Node.js 20.19+；验证环境使用 Node.js 24。CLI 是辅助工具，没有 CLI 时可按同一模板手动维护并说明验证边界。

```bash
npx --yes --package=@fission-ai/openspec@1.14.1 openspec schema validate workflow-spec-driven
npx --yes --package=@fission-ai/openspec@1.14.1 openspec new change add-your-capability
npx --yes --package=@fission-ai/openspec@1.14.1 openspec status --change add-your-capability
```

CLI 只报告制品状态，不代替审查、用户确认或测试证据。过程记录由助手基于 [过程模板](openspec/schemas/workflow-spec-driven/templates/processing/) 创建。

## 验证工具包

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_kit.py
python -m unittest discover -s tests -v
```

PyYAML 仅用于工具包的 YAML 与技能格式检查；接入脚本和导出的流程没有 Python 第三方运行依赖。

## 许可证与来源

[MIT](LICENSE)。通用流程从个人项目实践中提炼，按 [OpenSpec 官方格式](https://github.com/Fission-AI/OpenSpec/blob/main/docs/customization.md) 和 [项目技能说明](https://learn.chatgpt.com/docs/build-skills) 组织；不包含原始参考项目的内部资料。

本次构建记录见 [初始化变更](openspec/changes/archive/2026-10-06-bootstrap-workflow-kit/proposal.md)，其历史不会导出到接入项目。
