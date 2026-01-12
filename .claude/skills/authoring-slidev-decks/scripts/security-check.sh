#!/usr/bin/env bash
set -euo pipefail

INPUT="${1:-}"

# Allowlist patterns (tight on purpose)
ALLOW_PATTERNS=(
  '^python3? (\./)?\.claude/skills/authoring-slidev-decks/scripts/(init_slidev_project|validate|slidev_introspect|apply_patch|render_deck|read_slide|list_slides|audit|export)\.py(\s|$)'
  '^npm (install|ci)(\s|$)'
  '^npm run (dev|build|export)(\s|$)'
  '^pnpm (dev|build)(\s|$)'
  '^npx --no-install slidev (dev|build|export)(\s|$)'
  '^ls(\s|$)'
  '^pwd(\s|$)'
  '^cat (\.\/)?(deck\.json|llm\/out\/.*\.json|slides\.md|slides\/.*\.md)(\s|$)'
  '^mkdir -p'
)

# Blocklist (obvious footguns)
DENY_PATTERNS=(
  '(^|\s)rm(\s|$)'
  '(^|\s)mv(\s|$)'
  '(^|\s)cp(\s|$)'
  '(^|\s)chmod(\s|$)'
  '(^|\s)chown(\s|$)'
  '(^|\s)curl(\s|$)'
  '(^|\s)wget(\s|$)'
  '(^|\s)git\s+push(\s|$)'
)

for p in "${DENY_PATTERNS[@]}"; do
  if [[ "$INPUT" =~ $p ]]; then
    echo "Blocked command by security policy: $INPUT" >&2
    exit 2
  fi
done

for p in "${ALLOW_PATTERNS[@]}"; do
  if [[ "$INPUT" =~ $p ]]; then
    exit 0
  fi
done

echo "Blocked command (not in allowlist): $INPUT" >&2
exit 3
