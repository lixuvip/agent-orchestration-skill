#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_NAME="agent-orchestration"
SOURCE_DIR="${REPO_ROOT}/skills/${SKILL_NAME}"
TARGET_ROOT="${CODEX_SKILLS_DIR:-${CODEX_HOME:-${HOME}/.codex}/skills}"
TARGET_DIR="${TARGET_ROOT}/${SKILL_NAME}"

if [[ ! -f "${SOURCE_DIR}/SKILL.md" ]]; then
  echo "Missing skill source: ${SOURCE_DIR}/SKILL.md" >&2
  exit 1
fi

mkdir -p "${TARGET_ROOT}"
rm -rf "${TARGET_DIR}"
cp -R "${SOURCE_DIR}" "${TARGET_DIR}"

echo "Installed ${SKILL_NAME} to ${TARGET_DIR}"
echo "Restart Codex if the skill does not appear immediately."
