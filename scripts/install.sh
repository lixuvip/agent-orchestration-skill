#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_NAME="agent-orchestration"
SOURCE_DIR="${REPO_ROOT}/skills/${SKILL_NAME}"
TARGET_ROOT="${CODEX_SKILLS_DIR:-${CODEX_HOME:-${HOME}/.codex}/skills}"
TARGET_DIR="${TARGET_ROOT}/${SKILL_NAME}"
INSTALL_HELPER="${SCRIPT_DIR}/install_skill.py"

ALLOW_DIRTY=0
DRY_RUN=0
RESTORE=0

usage() {
  cat <<'EOF'
Usage: ./scripts/install.sh [--allow-dirty] [--dry-run] [--restore]

  --allow-dirty  Explicitly install an uncommitted development skill.
  --dry-run      Validate and print the planned install without changing files.
  --restore      Swap the current installation with the retained previous version.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --allow-dirty)
      ALLOW_DIRTY=1
      ;;
    --dry-run)
      DRY_RUN=1
      ;;
    --restore)
      RESTORE=1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
  shift
done

if [[ ! -f "${INSTALL_HELPER}" ]]; then
  echo "Missing install helper: ${INSTALL_HELPER}" >&2
  exit 1
fi

if [[ "${RESTORE}" -eq 1 ]]; then
  restore_args=(
    python3 "${INSTALL_HELPER}"
    --target-root "${TARGET_ROOT}"
    --skill-name "${SKILL_NAME}"
    --restore
  )
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    restore_args+=(--dry-run)
  fi
  "${restore_args[@]}"
  exit 0
fi

if [[ ! -f "${SOURCE_DIR}/SKILL.md" ]]; then
  echo "Missing skill source: ${SOURCE_DIR}/SKILL.md" >&2
  exit 1
fi

SOURCE_COMMIT="$(git -C "${REPO_ROOT}" rev-parse HEAD)"
SOURCE_DIRTY=0
if [[ -n "$(git -C "${REPO_ROOT}" status --porcelain -- "skills/${SKILL_NAME}")" ]]; then
  SOURCE_DIRTY=1
fi

if [[ "${SOURCE_DIRTY}" -eq 1 && "${ALLOW_DIRTY}" -ne 1 ]]; then
  echo "Dirty skill source refused. Commit the skill or pass --allow-dirty for a development install." >&2
  exit 2
fi

python3 "${SCRIPT_DIR}/validate.py"
python3 "${SCRIPT_DIR}/smoke_test.py"
python3 "${SCRIPT_DIR}/forward_test.py"
python3 "${SCRIPT_DIR}/protocol_test.py"
python3 "${SCRIPT_DIR}/automation_test.py"
python3 "${SCRIPT_DIR}/routing_test.py"
python3 "${HOME}/.codex/skills/.system/skill-creator/scripts/quick_validate.py" "${SOURCE_DIR}"
git -C "${REPO_ROOT}" diff --check

install_args=(
  python3 "${INSTALL_HELPER}"
  --source-dir "${SOURCE_DIR}"
  --target-root "${TARGET_ROOT}"
  --skill-name "${SKILL_NAME}"
  --source-commit "${SOURCE_COMMIT}"
)
if [[ "${SOURCE_DIRTY}" -eq 1 ]]; then
  install_args+=(--source-dirty --allow-dirty)
fi
if [[ "${DRY_RUN}" -eq 1 ]]; then
  install_args+=(--dry-run)
fi

"${install_args[@]}"

if [[ "${DRY_RUN}" -eq 1 ]]; then
  exit 0
fi

diff -qr "${SOURCE_DIR}" "${TARGET_DIR}"

echo "Installed ${SKILL_NAME} to ${TARGET_DIR}"
echo "Source commit: ${SOURCE_COMMIT}"
echo "Source dirty: ${SOURCE_DIRTY}"
echo "Restart Codex if the skill does not appear immediately."
