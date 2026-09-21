# Agent Skill Hub（智能体技能中心）

一个用 GitHub 统一维护、检索和安装 Agent Skills 的仓库。同一份 `SKILL.md` 尽可能同时供以下客户端使用：

- OpenAI Codex
- Claude Code
- DeepSeek Harness（DSH）

仓库里的 Skill 是可执行指令，安装前应像审查代码一样审查其 `SKILL.md`、脚本和引用资源。

## 仓库结构

```text
skill-hub/
├── registry.json              # Skill 索引
├── skills/                    # Skill 源码，一份源码供多个客户端使用
│   └── spring-boot-review/
│       ├── SKILL.md           # 唯一必需入口
│       ├── manifest.yaml      # Skill Hub 元数据
│       ├── agents/            # 可选的客户端元数据
│       └── references/        # 按需读取的参考资料
├── scripts/
│   ├── skill                  # 完整 CLI
│   ├── skill.sh               # 兼容入口
│   ├── install.sh             # 简化安装入口
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

## 使用

直接运行仓库内的 CLI：

```bash
./scripts/skill list
./scripts/skill search spring
./scripts/skill info spring-boot-review
./scripts/skill validate
```

安装到当前用户：

```bash
./scripts/skill install spring-boot-review --target codex
./scripts/skill install spring-boot-review --target claude
./scripts/skill install spring-boot-review --target deepseek
./scripts/skill install spring-boot-review --target all
```

安装到某个项目：

```bash
./scripts/skill install spring-boot-review \
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
./scripts/skill update spring-boot-review --target codex
```

卸载需要显式确认：

```bash
./scripts/skill uninstall spring-boot-review --target codex --yes
```

如果希望像系统命令一样使用，可以自行创建软链接：

```bash
ln -s "$(pwd)/scripts/skill" /usr/local/bin/skill
skill list
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
