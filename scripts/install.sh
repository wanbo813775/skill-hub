#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"

if [[ $# -lt 1 ]]; then
  echo "用法：$0 <skill> [codex|claude|deepseek|all] [其他选项]" >&2
  exit 2
fi

SKILL_NAME="$1"
TARGET="${2:-codex}"
if [[ $# -ge 2 ]]; then
  shift 2
else
  shift 1
fi

exec "$SCRIPT_DIR/skill" install "$SKILL_NAME" --target "$TARGET" "$@"
