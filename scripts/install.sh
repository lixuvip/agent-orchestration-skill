#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
KNOWN_SKILLS=("agent-orchestration" "agy-second-opinion")
SKILL_NAME="agent-orchestration"
TARGET_ROOT="${CODEX_SKILLS_DIR:-${CODEX_HOME:-${HOME}/.codex}/skills}"
INSTALL_HELPER="${SCRIPT_DIR}/install_skill.py"

ALLOW_DIRTY=0
DRY_RUN=0
RESTORE=0

usage() {
  cat <<'EOF'
Usage: ./scripts/install.sh [--skill NAME] [--allow-dirty] [--dry-run] [--restore]

Default skill: agent-orchestration
Optional independent skill: agy-second-opinion

  --skill NAME   Install or restore exactly one known skill.
  --allow-dirty  Explicitly install an uncommitted development skill.
  --dry-run      Validate and print the planned action without changing files.
  --restore      Restore the retained previous copy for the selected skill.
EOF
}

is_known_skill() {
  local candidate="$1"
  local known
  for known in "${KNOWN_SKILLS[@]}"; do
    if [[ "${candidate}" == "${known}" ]]; then return 0; fi
  done
  return 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skill)
      shift
      if [[ $# -eq 0 ]]; then
        echo "--skill requires a value" >&2
        exit 2
      fi
      SKILL_NAME="$1"
      ;;
    --allow-dirty) ALLOW_DIRTY=1 ;;
    --dry-run) DRY_RUN=1 ;;
    --restore) RESTORE=1 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
  shift
done

if ! is_known_skill "${SKILL_NAME}"; then
  echo "Unknown skill: ${SKILL_NAME}" >&2
  echo "Known skills: ${KNOWN_SKILLS[*]}" >&2
  exit 2
fi
if [[ ! -f "${INSTALL_HELPER}" ]]; then
  echo "Missing install helper: ${INSTALL_HELPER}" >&2
  exit 1
fi

SOURCE_DIR="${REPO_ROOT}/skills/${SKILL_NAME}"
TARGET_DIR="${TARGET_ROOT}/${SKILL_NAME}"

if [[ "${RESTORE}" -eq 1 ]]; then
  args=(python3 "${INSTALL_HELPER}" --target-root "${TARGET_ROOT}" --skill-name "${SKILL_NAME}" --restore)
  if [[ "${DRY_RUN}" -eq 1 ]]; then args+=(--dry-run); fi
  "${args[@]}"
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
  echo "Dirty skill source refused for ${SKILL_NAME}. Pass --allow-dirty for a development install." >&2
  exit 2
fi

python3 "${SCRIPT_DIR}/validate.py"
python3 "${SCRIPT_DIR}/smoke_test.py"
python3 "${SCRIPT_DIR}/forward_test.py"
python3 "${SCRIPT_DIR}/protocol_test.py"
python3 "${SCRIPT_DIR}/automation_test.py"
python3 "${SCRIPT_DIR}/routing_test.py"
python3 "${SCRIPT_DIR}/scale_test.py"
python3 "${HOME}/.codex/skills/.system/skill-creator/scripts/quick_validate.py" "${SOURCE_DIR}"
git -C "${REPO_ROOT}" diff --check

args=(
  python3 "${INSTALL_HELPER}"
  --source-dir "${SOURCE_DIR}"
  --target-root "${TARGET_ROOT}"
  --skill-name "${SKILL_NAME}"
  --source-commit "${SOURCE_COMMIT}"
)
if [[ "${SOURCE_DIRTY}" -eq 1 ]]; then args+=(--source-dirty --allow-dirty); fi
if [[ "${DRY_RUN}" -eq 1 ]]; then args+=(--dry-run); fi
"${args[@]}"

if [[ "${DRY_RUN}" -eq 0 ]]; then
  diff -qr "${SOURCE_DIR}" "${TARGET_DIR}"
  echo "Installed ${SKILL_NAME} to ${TARGET_DIR}"
fi

echo "Source commit: ${SOURCE_COMMIT}"
echo "Restart Codex if the selected skill does not appear immediately."
