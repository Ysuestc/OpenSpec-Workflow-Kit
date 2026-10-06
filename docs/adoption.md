# 接入指南

## 新项目

预览 scripts/apply_template.py 的目标路径和文件清单，再使用 --apply 写入。目标可以尚不存在；预览不会创建它。

填写项目上下文后，按实际项目修改 config 的 context / rules。默认中文正文和标准 OpenSpec 标记，可以按团队语言调整。schema 名称不必包含项目名。

## 已有仓库

1. 检查现有 AGENTS.md、项目上下文、OpenSpec 配置和已有 schema。
2. 运行预览，查看冲突。发现任意冲突时整个写入操作会在修改前停止。
3. 将现有规则和模板人工合并；不要抹掉原有技术栈、授权范围或 schema。
4. 对已合并文件使用 --exclude；可重复传入精确目标路径。
5. 执行 --apply，再验证新技能、schema 和引用。

例如已有 AGENTS.md 和 config 时：

```bash
python scripts/apply_template.py ../ExistingProject --exclude AGENTS.md --exclude openspec/config.yaml
python scripts/apply_template.py ../ExistingProject --exclude AGENTS.md --exclude openspec/config.yaml --apply
```

保留旧 config 时，当前 change 可明确选择 --schema workflow-spec-driven；是否改默认 schema 由项目决定。相同内容的文件会跳过，重复接入不会刷新这些文件。

接入脚本不会覆盖目录、符号链接、Windows 目录联接、根 README / LICENSE、Git 配置或不属于模板的文件；拒绝指向工具包自身或其内部目录的目标。

脚本执行整批预检，没有并发锁或事务回滚；接入期间保持目标文件不变。

## 导出内容

导出 AGENTS.md、docs/project-context.md、docs/workflow.md、docs/lessons.md、角色、技能、config 和 schema 模板。MIT 通知放在 docs/workflow-kit-LICENSE，保留模板许可，不更换目标项目许可证。

不导出工具包自身的 stable specs、changes、Git 历史、测试或验证脚本。目标项目的 specs 和 changes 目录只在实际写入时准备。

## 工具与其他助手

项目技能目录遵循 .agents/skills 约定。只支持 AGENTS.md 的助手也可从工作流入口读取角色；其他产品的运行时注册需要其自身适配，本模板没有预配置自动编排。

没有 CLI 时手动维护四类制品与过程记录。格式检查、行为测试和独立审查是不同证据，不互相替代。
