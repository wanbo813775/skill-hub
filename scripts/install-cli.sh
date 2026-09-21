#!/usr/bin/env bash
set -euo pipefail

SOURCE_URL="${SKILL_HUB_CLI_URL:-https://raw.githubusercontent.com/wanbo813775/skill-hub/main/scripts/skill}"
BIN_DIR="${SKILL_HUB_BIN_DIR:-${HOME}/.local/bin}"
DESTINATION="${BIN_DIR}/skill"

if ! command -v curl >/dev/null 2>&1; then
  echo "错误：需要 curl 才能下载 Skill Hub CLI。" >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "错误：需要 Python 3 才能运行 Skill Hub CLI。" >&2
  exit 1
fi

mkdir -p "$BIN_DIR"
TEMP_FILE="$(mktemp "${BIN_DIR}/.skill.XXXXXX")"
cleanup() {
  rm -f -- "$TEMP_FILE"
}
trap cleanup EXIT

curl --fail --silent --show-error --location "$SOURCE_URL" --output "$TEMP_FILE"
chmod 755 "$TEMP_FILE"
python3 "$TEMP_FILE" --help >/dev/null
mv -f -- "$TEMP_FILE" "$DESTINATION"
trap - EXIT

echo "已安装 Skill Hub CLI：$DESTINATION"
case ":${PATH}:" in
  *":${BIN_DIR}:"*) ;;
  *)
    echo "请将以下内容加入 shell 配置后重新打开终端："
    echo "export PATH=\"${BIN_DIR}:\${PATH}\""
    ;;
esac
echo "现在可以运行：skill list"
