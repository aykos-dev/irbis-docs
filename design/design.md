# Irbis — Design tokens (source of truth)

From the canvas boards **Design system** (`canvas/Main.dc.html`), **Irbis mascot** (`canvas/Irbis.dc.html`),
**Companion evolution line** (`canvas/Companions.dc.html`) and **Bottom nav** (`canvas/Nav.dc.html`), snapshot
2026-10-16. Mirrored verbatim by:
- `irbis-app/src/shared/constants/{colors,typography,spacing}.ts`
- `irbis-web/src/shared/styles/tokens.css`

New visual values are added **here first**, then mirrored in the same change. Values marked *(derived)* were read
off screen boards rather than the design-system board — confirm when the feature that uses them starts.

## Colour

### Core
| Token | Hex | Use |
|---|---|---|
| `teal` | `#1CB0A8` | Glacier teal — brand, peak type, active nav border, Go ring accent. **Not** for white text. |
| `teal-700` | `#0C807A` | Primary button fill (white text), links, active nav label |
| `teal-700-edge` | `#075B56` | Primary button 4 px bottom shadow |
| `teal-icon-edge` | `#0E8A83` | App-icon tile shadow |
| `teal-tint` | `#E3F7F5` | Tinted surfaces, active nav pill |
| `orange` | `#FF9F1C` | Sunrise orange — secondary button, trail type, backpack |
| `orange-edge` | `#CC7A00` | Orange button shadow |
| `on-orange` | `#3A2200` | Text on orange |
| `orange-tint` | `#FFF1DA` | Orange tinted surfaces |
| `sky` | `#4CA9FF` | Lake type |
| `purple` | `#7B61FF` | Cave type |
| `pine` | `#3DAA5C` | Camping type, Go ring |
| `stone` | `#8A979C` | Neutral icon |
| `red` | `#FF4B4B` | Safety red — Not now ring |
| `red-700` | `#D93636` | Danger / SOS button fill (white text) |
| `red-700-edge` | `#A12121` | Danger button shadow |
| `gold` | `#FFC800` | Completed place, Caution ring |
| `gold-edge` | `#D9A500` | Completed node shadow |
| `on-gold` | `#6E4E00` | Text / icon on gold |

### Surfaces and text
| Token | Light | Dark |
|---|---|---|
| `bg` | `#F7F7F2` | `#131D22` |
| `card` | `#FFFFFF` | `#1C2A30` |
| `line` | `#E5E5DC` | `#2B3B42` *(derived: nav)* |
| `ink` (headings) | `#1F2A2E` | `#F1F5F4` |
| `body` | `#3C4A4F` | *(derived — confirm)* |
| `muted` | `#5E6E74` | `#9AA8AD` |
| `soft` (dividers) | `#EEF0E8` | *(derived — confirm)* |
| `nav-active-bg` / `-border` / `-fg` | `#E3F7F5` / `#1CB0A8` / `#0C807A` | `#123B3A` / `#1CB0A8` / `#5FD6CE` |
| `disabled-bg` / `disabled-fg` | `#E5E5DC` / `#6B787D` | *(derived — confirm)* |

### Condition status (always colour + icon + label)
| Status | Chip bg | Chip fg | Ring | Icon |
|---|---|---|---|---|
| Go | `#DFF6E7` | `#1B6B3E` | `#3DAA5C` solid 5 px | check |
| Caution | `#FFF1BF` | `#6E4E00` | `#FFC800` solid 5 px | warning triangle |
| Not now | `#FFE1E1` | `#B32424` | `#FF4B4B` solid 5 px | circled × |
| Seasonal lock | `#ECEEEF` | `#56646A` | `#AEB8BC` dashed 5 px, node `#C9D1D4` | lock |
Completed place: gold node `#FFC800` with a star, shadow `#D9A500` — the **shape** changes, not only the colour.

### Place types
| Type | Colour |
|---|---|
| Peak | `#1CB0A8` |
| Lake | `#4CA9FF` |
| Cave | `#7B61FF` |
| Camping | `#3DAA5C` |
| Trail | `#FF9F1C` |

### Levels / companions (badge frame colour, edge, tint, text, frame shape)
| L | Name | Companion | Colour | Edge | Tint | Text | Frame |
|---|---|---|---|---|---|---|---|
| 1 | Wanderer | Panda cub | `#58B368` | `#3E8E4D` | `#E4F5E7` | `#2D6E3A` | circle |
| 2 | Burrower | Marmot | `#C98B4E` | `#A06A33` | `#F7EADB` | `#7A4E1F` | rounded square (44 px) |
| 3 | Pathfinder | Fox | `#F2802E` | `#C9601A` | `#FFE9D9` | `#9A4510` | shield |
| 4 | Ridge Walker | Ibex | `#1CB0A8` | `#0E8A83` | `#DDF5F3` | `#0C6E69` | hexagon |
| 5 | Mountain Guardian | Brown bear | `#4C7BD9` | `#335FB8` | `#E3ECFB` | `#2A4F9A` | octagon |
| 6 | Sky Watcher | Golden eagle | `#7B61FF` | `#5B42DB` | `#ECE8FF` | `#4B33C4` | gem |
| 7 | Snow Legend | Snow leopard | `#E5A800` | `#B88600` | `#FFF6D6` | `#7A5800` | star |
Difficulty boots colour: `#7A4E2D` (inactive boot at 18 % opacity).

### Mascot palette
Fur `#EDF0F3` · rosettes `#8E99A6` · backpack `#FF9F1C`. Mood backdrops: excited `#E3F7F5`, proud `#FFF1DA`,
worried `#E2F0FF`, sleepy `#EEEAFF`, sad-but-cute `#F0F1F2`.

## Typography — Nunito (weights 600, 700, 800, 900)
| Token | Size / line-height | Weight | Notes |
|---|---|---|---|
| `stat` | 48 / 1.0 | 900 | tabular numbers (elevation, XP) |
| `h1` | 28 / 1.15 | 900 | ink |
| `h2` | 22 / 1.2 | 900 | ink |
| `h3` | 17 / 1.25 | 800 | ink |
| `body` | 15 / 1.45 | 700 | body colour |
| `small` | 13 / 1.35 | 700 | muted |
| `caption` | 12, letter-spacing .08em, UPPERCASE | 900 | muted |
| `button` | 17 / 1.15, letter-spacing .05em, UPPERCASE | 900 | |
| `nav-label` | 11 | 800 | |
App: bundle Nunito `.ttf` (Regular 600 is not used; ship SemiBold 600, Bold 700, ExtraBold 800, Black 900) and select
by family name (`Nunito-Black` …), never `fontWeight`.

## Shape and spacing
- Radii: `16` (buttons, small tiles) · `20` (cards) · `24` (large cards, sheets) · `999` (chips, pills). App icon 24–30.
- Cards: 2 px `line` border, **4 px bottom edge**, radius 20.
- Buttons: min-height **54**, padding 8 × 20, radius 16, **4 px bottom shadow** in the edge colour;
  pressed = shadow 0 and translate y +4. Variants: primary (teal-700), secondary (orange), white (card + line border,
  teal-700 text), danger (red-700), disabled (no shadow). Labels wrap to 2 lines, never truncate.
- Chips: height 28, padding 0 × 10, radius 999, 13 / 800.
- Place type dot 44; path node 64 with 5 px drop shadow `rgba(0,0,0,.18)`; condition ring 72 around a 54 node.
- Spacing scale (px): 4 · 6 · 8 · 10 · 12 · 14 · 16 · 18 · 20 · 22 · 24 · 28 · 32 · 44 · 48 · 56 — screen padding 22–24.
- Icons: 2.5 px stroke, round caps and joins, 20 px default (inline SVG on the canvas → `shared/components/Icon`).
- Touch targets ≥ 44 pt.
- Mascot on a card: 88 (`sizes.mascotCard`, added by M0 `health`).
- Skeleton pulse: opacity 1 ↔ 0.5, 900 ms per half-cycle *(added by M0 — confirm)*.
- Press feedback: scale 0.97 + opacity 0.9, 150 ms (engineering standards §1).
- `maxFontSizeMultiplier` per typography token: not set yet — decide with the first text-heavy feature.

## Motion
Press 150 ms (and the 4 px press-down), enter/exit 200–250 ms, layout 300 ms; easing out-cubic in, in-cubic out.
Canvas notes add feature motions (e.g. waypoint ring fill + "+10 XP" chip floating up, reveal line 0.6 s) — listed in
each feature's spec.

## Art and media
Inventory and which images exist vs. still needed: `design/assets.md`. Art for a feature is requested from the
owner at the start of that feature (badges, league emblems, mascot animations, …) and stored under
`design/media/<slug>/` before it is copied into the app.
