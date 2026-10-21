# Media — profile

Screens: `Profile` / `ProfileDark`, `EditProfile`, `Settings`, `Notifs`, `AccGuestProfile` (canvas). Canvas asset ids
from `design/assets.md`. Owner decisions already on record: companion and Irbis SVGs are final (onboarding 2026-10-17,
levels 2026-10-18); badge and league emblems do not exist as files yet.

| File | What | Used on | Format / size | Status (exists · needed · placeholder OK) |
|---|---|---|---|---|
| user photo (runtime) | Uploaded profile photo | Profile header, EditProfile | JPEG/WebP, server re-encodes to 512×512 square | needed · user-supplied · initials fallback exists |
| `companionFox.ts` (canvas `d1b0d619…`) | L3 fox companion, neutral | Profile avatar badge, guest profile | SVG | exists · final |
| `irbisExcited.ts` (canvas `28945aeb…`) | Irbis excited / waving | Settings Irbis Plus row | SVG | exists · final |
| `irbisSleepy.ts` (canvas `bdd9780b…`) | Irbis sleepy | Notifs empty state | SVG | exists · final |
| avatar initials (`TK`) | Initials fallback when no photo | Profile header, EditProfile | drawn in code (circle + text) | exists on canvas · final |
| badge showcase: 4 emblems + "All 23" | Profile badge showcase tiles | Profile | inline SVG hex 64×64 | needed · placeholder OK (generic hex + glyph; real art with `badges`) |
| Granite league emblem | League tier chip "Granite · #7" | Profile | inline SVG 22×22 | needed · placeholder OK (code-drawn gem; real art with `leagues`) |
| stat glyphs: peak, lake, cave, boot, mountain, pin | Stats row icons | Profile | inline SVG 22×22 | exists on canvas · final · draw in code |
| `verified` shield, share, settings, chevrons, camera, toggles | Row/header icons | Profile, EditProfile, Settings, Notifs | inline SVG 22–26 px | exists on canvas · final · draw in code |
| backpack colour swatches | 6 colour dots | EditProfile | drawn in code | exists on canvas · final |
| notification category glyphs | Conditions, duels, Top Shots, groups, spots, feed, streaks | Notifs rows | inline SVG 22×22 | exists on canvas · final · draw in code (rows ship empty until those features emit) |

No sound, video, or animation assets are needed for this feature.

If a missing item is approved as a placeholder, it is recorded as a known issue in `STATUS.md` and replaced when its
source feature (`badges`, `leagues`) ships.
