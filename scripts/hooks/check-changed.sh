#!/usr/bin/env bash
# Stop hook: run `npm run check` in every sibling repo that has changes vs main.
# Blocks "done" (exit 2) once if a check fails; the second stop attempt is allowed so it can't loop forever.
input="$(cat)"
[[ "$(jq -r '.stop_hook_active // false' <<<"$input")" == "true" ]] && exit 0

root="$(cd "$(dirname "$0")/../../.." && pwd)"
failed=0
for repo in irbis-api irbis-web irbis-app; do
  dir="$root/$repo"
  [[ -f "$dir/package.json" ]] || continue
  jq -e '.scripts.check' "$dir/package.json" >/dev/null 2>&1 || continue
  base="$(git -C "$dir" rev-parse --verify -q main >/dev/null && echo main || echo HEAD)"
  if [[ -z "$(git -C "$dir" status --porcelain)" ]] && [[ -z "$(git -C "$dir" log --oneline "$base"..HEAD 2>/dev/null)" ]]; then
    continue
  fi
  if ! out="$(cd "$dir" && npm run --silent check 2>&1)"; then
    failed=1
    echo "[$repo] npm run check FAILED:" >&2
    tail -n 40 <<<"$out" >&2
  fi
done
if [[ $failed -eq 1 ]]; then
  echo "Not done: fix the failures above (do not edit tests to pass), or report them to the user." >&2
  exit 2
fi
exit 0
