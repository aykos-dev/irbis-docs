# D{n} · {what goes wrong, one line}

| | |
|---|---|
| Status | Open · found YYYY-MM-DD |
| Severity | 3 - Medium |
| Cases | TC-NNN[, STD-XXX@screen] — the retest re-runs exactly these |
| Found | run [YYYY-MM-DD_HHMM](../../runs/YYYY-MM-DD_HHMM/run.md) · build irbis-app {sha} · {device} |

**Title:** [Area / Sub-area] - {wrong behaviour, present tense, ~60–95 chars}

*Reference: features/{slug}.md AC{n}: "{the broken AC text, word for word}"* {(QA reading, owner to confirm) — only when it rests on an open question}

**Steps to Reproduce**
1. {state setup}
2. …

**Actual:** {one paragraph — exact strings, QA event values} · proof: `../../runs/…/proof/TC-NNN/{shot}.png`

**Expected:** {one assertable statement}

**Cause in code:** `{repo}/{file}:{line}` — {one line} | not located

## Retests
<!-- newest first, one line each:
- YYYY-MM-DD · ✅ Fixed / ❌ Not fixed / ⏸ Not reached · irbis-app {sha} · {device} · run [..](../../runs/../run.md)
-->
