# Brief active-trip-3-irbis-web — public live trip page

- Spec: features/active-trip.md · ACs in this brief: AC5 (web)
- Repo / branch: irbis-web · `feat/active-trip` from `main`
- Depends on: api brief active-trip-1 (`GET /v1/live/{token}`, operationId `liveGet`) → copy irbis-api
  `feat/active-trip` `openapi.json` the way gen:api expects, then `npm run gen:api`

## Files
- Touch: new route group `src/app/(public)/layout.tsx` + `src/app/(public)/t/[token]/page.tsx` (thin) ·
  `src/features/live-trip/` (`LiveTripView.tsx`, hook) · messages en/ru/uz namespace `live`
- Read for patterns: `src/app/(auth)/layout.tsx` (a layout without the admin shell), `src/shared/api/client.ts`
  + `session.ts` (make sure the public page never triggers the admin refresh / login redirect on 404),
  `shared/components/ui` (Badge, Skeleton, ErrorState, Button)
- Copy: `irbis-docs/features/briefs/active-trip-copy.md` → `live.*`

## Behaviour
- No login, no admin sidebar. `metadata.robots = { index: false, follow: false }`. Locale from `Accept-Language`
  (uz/ru/en, default en) — no locale switcher.
- Shows `live.title` {displayName}, `live.place` {placeNames[locale] ?? uz}, `live.backBy` (Asia/Tashkent HH:mm),
  status Badge (on_trip teal, late orange, alerted red, back_safe green; colour + label), `live.last` {min} or
  `lastNone`, `live.openMaps` link (mapsUrl, new tab, rel noopener) when present, footer.
- Refetch every 60 s (TanStack `refetchInterval`). Status `ended` → only `live.ended` + footer (no place time or
  location). 404 → `live.notFound`. Other error → ErrorState `error` + `retry`. Loading skeleton. Mobile-first
  (contacts open it on phones), tokens only.

## API
| GET | /v1/live/{token} | — | LiveTripDto | 404 LIVE_NOT_FOUND, 429 |

## testIDs
`live.status` `live.place` `live.backby` `live.last` `live.maps` `live.notfound` `live.ended`

## Approved packages
none

## Done when
- [ ] tests: on_trip render, ended hides location, 404 not found, error + retry; one axe check
- [ ] `npm run check` green; `npm run build` passes (new route); commit on `feat/active-trip`
