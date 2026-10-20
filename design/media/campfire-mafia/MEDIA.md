# campfire-mafia — media

Owner (2026-10-19): app icon = final canvas asset `68fc129c…`; 3 extra role glyphs drawn in canvas style as
placeholders (Q8).

| File | What | Used on | Format / size | Status |
|---|---|---|---|---|
| Role glyphs ×8 | crown (Boss), hat (Mafia), glass (Detective), cross (Doctor), moon (Maniac), heart (Lover), shield (Bodyguard), person (Civilian) — paths in `MafSetup.dc.html` | setup rows, role card, host list, game over | inline 24×24 SVG paths | exists · final (canvas) |
| Role glyphs ×3 | Sniper (crosshair), Journalist (notepad), Immortal (infinity) | same | PNG @1x–3x 40 px, black → `tintColor` (`role-*.png`, cleaned) | exists · final (owner 2026-10-20) |
| Role colours ×11 | Boss #8F1F1F, Mafia #D93636, Detective #1F74C7, Doctor #2E8B57, Maniac #6A4FE8, Lover #C93A6B, Bodyguard #0C807A, Civilian #5E6E74 (canvas); Sniper #B5651D, Journalist #8A6D1F, Immortal #4E7D8C (new) | role chips, icons | colours in mafia role table | 8 exist · 3 placeholder |
| Companion avatars ×6 | fox, ibex, bear, marmot, eagle, panda | host list, out list, game over | SVG in app (`companion*`) | exists |
| Game-over confetti | small coloured rects (MafEnd `.cf`) | game over header | drawn in code | exists (canvas layout) |
| `irbis-icon.svg` (canvas `68fc129c…`) | Irbis app icon: teal tile, ridge, Irbis | Android launcher (mipmap ×5, round, adaptive), iOS AppIcon | SVG → PNG via macOS `qlmanage`/`sips` | exists · final |
| Night/day narration audio | "App voice" narrator (MafSetup) | — | — | out of scope (host reads, Q1) |
| XP / Life Saver badge row (MafEnd) | — | — | — | out of scope (no XP / badges) |
| Role card art ×11 | chibi animal per role on the role colour (`rolecard-*.png`) | role card under "You are" (glyphs stay elsewhere) | JPG @1x–3x 144×192, app `src/assets/images/campfire/` | exists · final (owner 2026-10-20) |
