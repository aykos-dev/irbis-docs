#!/usr/bin/env bash
# Launch Claude Code from the brain repo with all three code repos attached.
cd "$(dirname "$0")/.." || exit 1
exec claude --add-dir ../irbis-api ../irbis-web ../irbis-app "$@"
