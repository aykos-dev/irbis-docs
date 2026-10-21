# Media — trip-plan

Screen: `TripPlan` (canvas). Canvas asset ids from `design/assets.md`. Companion and place SVGs are final
(onboarding 2026-10-17, levels 2026-10-18). Gear rows and the contact avatar are drawn with tokens + the shared
`Icon` set (no image files on the board).

| File | What | Used on | Format / size | Status (exists · needed · placeholder OK) |
|---|---|---|---|---|
| place hero by type (canvas `2ea0b851…` lake, shared `PlaceHero`) | Place illustration in the trail card | TripPlan trail card | SVG | exists · final |
| `companionFox.ts` (canvas `d1b0d619…`) | Current user's companion, neutral | TripPlan header | SVG | exists · final |
| gear row icons (water, layer, first-aid, map, sun, headlamp, filter) | Line icons in the checklist | TripPlan gear list | shared `Icon` set | exists if `Icon` has them · else placeholder OK (generic check icon) |
| contact initial avatar | Circle with the contact's first letter | Emergency contact row | tokens, no file | exists (drawn) |
