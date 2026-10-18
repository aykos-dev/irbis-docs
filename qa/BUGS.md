# Defects — all features

Built by `scripts/qa/case/bugs.py index`. Open first, then by severity. Retest open ones with `/qa-retest open`.

| Ref | Severity | Defect | Status |
|---|---|---|---|
| [auth/D1](auth/bugs/D1_deeplink-intent-filter/D1_deeplink-intent-filter.md) | 2 - High | irbis:// deep links do not open the app (no Android intent-filter) | Open · found 2026-10-17 |
| [onboarding/D2](onboarding/bugs/D2_welcome_font2/D2_welcome_font2.md) | 2 - High | Meet Irbis at font scale 2.0: Get started and I already have an account are pushed off-screen and unreachable | Closed · not retested (owner dropped font-scale QA, 2026-10-17) |
| [places/D1](places/bugs/D1_empty-state-blank/D1_empty-state-blank.md) | 2 - High | Explore empty state renders blank: no text, no Reset filters button | Fixed · retest 2026-10-17 |
| [conditions/D1](conditions/bugs/D1_explore-offline-no-cache/D1_explore-offline-no-cache.md) | 3 - Medium | Explore shows a connection error offline instead of the cached list with condition chips | Withdrawn · not a defect (owner 2026-10-18: Explore needs no offline) |
| [health/D2](health/bugs/D2_wrapped-chip-overflows-card/D2_wrapped-chip-overflows-card.md) | 3 - Medium | Status chip runs past the card when its label wraps | Fixed · retest 2026-10-17 |
| [onboarding/D1](onboarding/bugs/D1_merge-skipped-after-first-device-merge/D1_merge-skipped-after-first-device-merge.md) | 3 - Medium | Guest onboarding choices are not merged on sign-up/log-in once any earlier merge happened on the device | Closed · not an app defect · retest 2026-10-17 |
| [places/D2](places/bugs/D2_not-found-back-dead/D2_not-found-back-dead.md) | 3 - Medium | Place not-found screen: Back does nothing after a cold deep link | Fixed · retest 2026-10-18 |
| [health/D1](health/bugs/D1_api-chip-red-when-db-down/D1_api-chip-red-when-db-down.md) | 4 - Low | API chip turns red when only the database is down | Fixed · retest 2026-10-17 |
| [onboarding/D3](onboarding/bugs/D3_font_change_restarts/D3_font_change_restarts.md) | 4 - Low | Changing the system font size mid-onboarding restarts the flow at Meet Irbis | Fixed · not retested (owner dropped font-scale QA, 2026-10-17) |
| [places/D3](places/bugs/D3_uz-level-lock-overflow/D3_uz-level-lock-overflow.md) | 4 - Low | Uzbek level-card lock text runs past the card edge | Fixed · retest 2026-10-18 |
