# Agent Skill Hub（智能体技能中心）

一个用 GitHub 统一维护、检索和安装 Agent Skills 的仓库。同一份 `SKILL.md` 尽可能同时供以下客户端使用：

- OpenAI Codex
- Claude Code
- DeepSeek Harness（DSH）

仓库里的 Skill 是可执行指令，安装前应像审查代码一样审查其 `SKILL.md`、脚本和引用资源。

## 当前 Skills

| 名称 | 用途 |
|---|---|
| `alibaba-java-guidelines` | 基于阿里巴巴 Java 开发手册编写、修改和审查 Java 代码、MySQL 设计与技术文档。 |

## 仓库结构

```text
skill-hub/
├── registry.json              # Skill 索引
├── skills/                    # Skill 源码，一份源码供多个客户端使用
│   └── <skill-name>/
│       ├── SKILL.md           # 唯一必需入口
│       ├── manifest.yaml      # Skill Hub 元数据
│       ├── agents/            # 可选的客户端元数据
│       └── references/        # 按需读取的参考资料
├── scripts/
│   ├── skill                  # 完整 CLI
│   ├── skill.sh               # 兼容入口
│   ├── install.sh             # 简化安装入口
│   ├── install-cli.sh         # 从 GitHub 安装全局 CLI
│   ├── list.sh                # 简化查询入口
│   └── validate.sh            # 简化校验入口
└── .github/workflows/
    └── validate-skills.yml
```

每个 Skill 必须位于 `skills/<skill-name>/SKILL.md`，并在 YAML frontmatter 中只依赖跨平台共有的必需字段：

```yaml
---
name: example-skill
description: 说明这个 Skill 能做什么，以及 Agent 应在什么情况下使用它。
---
```

## 远程安装（推荐）

不需要克隆本仓库。先安装全局 CLI：

```bash
curl -fsSL https://raw.githubusercontent.com/wanbo813775/skill-hub/main/scripts/install-cli.sh | bash
```

如果终端提示 `skill` 命令不存在，将 `~/.local/bin` 加入 `PATH`：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

之后可以在任意目录运行：

```bash
skill list
skill search 阿里巴巴
skill install alibaba-java-guidelines --target codex
```

`skill` 会自动从 GitHub 读取最新索引，并只安装选中的 Skill。以后更新时运行：

```bash
skill update alibaba-java-guidelines --target codex
```

重新执行 CLI 安装命令即可更新 `skill` 命令本身。

## 本地仓库开发

克隆仓库后，可直接运行内置 CLI 来开发和校验 Skill：

```bash
./scripts/skill list
./scripts/skill search 阿里巴巴
./scripts/skill info alibaba-java-guidelines
./scripts/skill validate
```

安装到当前用户：

```bash
./scripts/skill install alibaba-java-guidelines --target codex
./scripts/skill install alibaba-java-guidelines --target claude
./scripts/skill install alibaba-java-guidelines --target deepseek
./scripts/skill install alibaba-java-guidelines --target all
```

安装到某个项目：

```bash
./scripts/skill install alibaba-java-guidelines \
  --target all \
  --scope project \
  --project-dir /path/to/project
```

目标目录：

| 目标客户端 | 用户级 | 项目级 |
|---|---|---|
| Codex | `~/.agents/skills` | `<project>/.agents/skills` |
| Claude Code | `~/.claude/skills` | `<project>/.claude/skills` |
| DeepSeek Harness | `~/.dsh/skills` | `<project>/.dsh/skills` |

已有同名目录时，安装器默认拒绝覆盖。确认需要替换时使用 `update`，或在 `install` 上显式传入 `--force`：

```bash
./scripts/skill update alibaba-java-guidelines --target codex
```

卸载需要显式确认：

```bash
./scripts/skill uninstall alibaba-java-guidelines --target codex --yes
```

## 新增 Skill

1. 新建 `skills/<name>/SKILL.md`；只有真正需要时才增加 `scripts/`、`references/` 或 `assets/`。
2. 新建 `manifest.yaml`，记录版本、作者、目标客户端和标签。
3. 在 `registry.json` 中登记相同的名称、版本、路径和目标客户端。
4. 执行 `./scripts/skill validate <name>`。
5. 提交代码；GitHub Actions 会再次校验整个仓库。

名称必须使用小写字母、数字和连字符，最长 64 个字符。`description` 应同时说明 Skill 做什么以及何时使用。

## 兼容性原则

- 共享层只依赖 `SKILL.md` 的 `name` 和 `description`。
- 客户端专属配置放在独立目录中，不能改变其他客户端理解核心 Skill 的方式。
- 详细规则按需放入 `references/`，避免把所有内容塞进入口文件。
- 可重复、需要确定性的操作才放入 `scripts/`，并在提交前真实运行验证。

当前路径约定参考 [OpenAI Skills 文档](https://learn.chatgpt.com/docs/build-skills)、[Claude Agent Skills 文档](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) 和 [DeepSeek Harness Skills 文档](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md)。

## 开源许可

[MIT](LICENSE)
