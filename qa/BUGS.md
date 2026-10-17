# Defects — all features

Built by `scripts/qa/case/bugs.py index`. Open first, then by severity. Retest open ones with `/qa-retest open`.

| Ref | Severity | Defect | Status |
|---|---|---|---|
| [auth/D1](auth/bugs/D1_deeplink-intent-filter/D1_deeplink-intent-filter.md) | 2 - High | irbis:// deep links do not open the app (no Android intent-filter) | Open · found 2026-10-17 |
| [health/D2](health/bugs/D2_wrapped-chip-overflows-card/D2_wrapped-chip-overflows-card.md) | 3 - Medium | Status chip runs past the card when its label wraps | Fixed · retest 2026-10-17 |
| [health/D1](health/bugs/D1_api-chip-red-when-db-down/D1_api-chip-red-when-db-down.md) | 4 - Low | API chip turns red when only the database is down | Fixed · retest 2026-10-17 |
