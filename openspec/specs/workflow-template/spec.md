# workflow-template Specification

## Purpose
为新项目和已有仓库提供可配置、可追溯的阶段开发流程，统一方案、审查、实施、验证与规范归档，同时通过显式文件清单接入来保护既有内容，并保留目标项目的技术栈、验证方式和当前用户授权边界。

## Requirements

### Requirement: Project-local configurable workflow
The kit SHALL provide project-local workflow rules, six role contracts, a discoverable skill, a custom schema and processing templates without prescribing a business domain or technology stack.

#### Scenario: Adopt into a project with its own stack
- **WHEN** a maintainer adopts the template into a project
- **THEN** project context supplies the actual stack, verification commands, timezone and delivery conventions
- **AND** no source project's approvals or remote write permissions are inherited

### Requirement: Evidence-based stages
The workflow MUST distinguish artifact presence from review, implementation and acceptance evidence, and MUST identify self-review.

#### Scenario: Artifacts exist before checks run
- **WHEN** all design artifacts exist but necessary checks have not run
- **THEN** those checks remain NOT_RUN and the phase is not treated as accepted
- **AND** self-review is labeled SELF_REVIEW

### Requirement: Preview and conflict preflight
The application helper SHALL preview without writing by default and MUST check all planned outputs before applying.

#### Scenario: Preview a missing destination
- **WHEN** the helper runs without --apply for a nonexistent destination
- **THEN** it reports planned outputs without creating files or the destination directory

#### Scenario: Existing conflicting file
- **WHEN** a planned output has different existing content, a directory or a symlink
- **THEN** application fails before any planned files are written
- **AND** existing content remains intact

### Requirement: Idempotent selective application
The application helper SHALL skip identical files and SHALL support explicit exclusions for manual integration.

#### Scenario: Repeat an identical application
- **WHEN** the template is applied again without content changes
- **THEN** identical files and their modification times remain unchanged

#### Scenario: Preserve a manually integrated file
- **WHEN** a maintainer excludes an exact known output path
- **THEN** that output is not written and other nonconflicting outputs may be applied

### Requirement: Payload and path isolation
The helper MUST export only the explicit workflow payload, preserve the destination root license, and reject unsafe destination paths.

#### Scenario: Create a clean project workflow
- **WHEN** the payload is applied to an empty destination
- **THEN** workflow files and empty specs and changes directories are created
- **AND** the kit's Git data, README, scripts, tests, construction history and stable specs are absent
- **AND** the MIT notice is written separately under docs

#### Scenario: Unsafe source or linked destination
- **WHEN** the destination is the kit source, inside the kit source, or contains a symlink on an output path
- **THEN** application fails without writing outside the intended destination

### Requirement: Acceptance precedes archive delivery
The workflow SHALL synchronize completed delta specifications and archive after acceptance, and SHALL perform external delivery only within current user authorization.

#### Scenario: Archive after verified implementation
- **WHEN** implementation tasks and necessary checks are complete with no unresolved blocker
- **THEN** the coordinator may record acceptance and the archiver synchronizes specifications and archives
- **AND** archive or push is not a circular prerequisite for completing pre-archive tasks
