# Brief <slug>-<n>-<repo> — <slice name, e.g. "sign-up + log-in">

<!-- 60–80 lines max. Everything the dev agent needs for THIS slice and nothing else; it reads only
     ../<repo>/RULES.md, this brief and the files listed under "Files". Written by the main session from the spec. -->

- Spec: features/<slug>.md · ACs in this slice: AC1, AC3 (2–5 ACs)
- Repo / branch: <repo> · `feat/<slug>` (create from main if missing; slices stack on it)
- Depends on: brief <slug>-<n-1>-… (merged on the branch) | none

## Files
- Touch: `src/features/<slug>/…` (new) · `src/app/navigation/…` (edit: add route X)
- Read for patterns (don't change): `src/features/health/…` (reference feature)

## Behaviour (the ACs, concrete)
- AC3 — … exact rule, numbers, limits …

## API (for app/web: the generated hooks to use · for api: endpoints to add)
| Method | Path | Request | Response | Errors (code → status) |
|---|---|---|---|---|

## Copy (i18n keys, en / ru / uz)
| key | en | ru | uz |
|---|---|---|---|

## testIDs · QA events
`…` · `event_name { prop }`

## Approved packages
none | `<pkg>@<version>`

## Done when
- [ ] tests for each AC above (1–3 each), `npm run check` green, committed on the branch
- [ ] (api) `npm run openapi:export` committed · (app) build only if asked
