# Weekly path ("This Month's Path") — layout notes from canvas (so dev agents never open the canvas HTML)

Base 390 × 844 (Home.dc.html / HomeDark.dc.html). Colours are canvas values; map to `design/design.md` tokens where one
exists (bg #F7F7F2, card #FFF, line #E5E5DC, ink #1F2A2E, body #3C4A4F, muted #5E6E74, soft #EEF0E8, teal-700 #0C807A).
Feature changes vs canvas: title "This Month's Path"; 3 place nodes + chest (canvas has 7 + chest); header = companion
+ XP only (no flame/boot/gems); no "Autumn Colors" card; swap buttons "Keep plan" + "See place". Canvas text styles:
h2 900/22, h3 800/16, small 700/13 muted, caption 900/12 uppercase .08em → use the design.md tokens.

## Header (padding 14/16/10, bg = screen bg, bottom border 2 line, space-between)
- Left: companion avatar 44 px circle, bg = level tint (L3 #FFE9D9), border 3 level colour (#F2802E), art 44 px with
  6 px top offset, clipped. Tap → Level screen.
- Right: XP stat (gap 4, 900 16 px ink): bolt 24 px #FFC800, fill `M13.5 1.5L4 14h7l-1.5 8.5L20 9.5h-7z` + "1,240".

## Intro card (section padding 16/16/0; card padding 16, gap 14, radius 20, border 2 + bottom 4)
- Row (space-between, align top, gap 12): title "This Month's Path" (h2) + subtitle (small, gap 3).
- Info button 40 × 40, radius 12, border 2 line, card bg, muted glyph 20 px: `<circle cx=12 cy=12 r=9/>` +
  `M12 11v6M12 7.5v.3` (stroke 2.6, round). a11y "How the path is built".
- Weather strip (row, gap 8): 3 pills Fri/Sat/Sun, flex 1, column centred, gap 2, padding 8/4, radius 14, bg soft
  #EEF0E8. Contents: day caption 11 px · glyph 30 px · temp h3 ("22°") · condition small 12 px ("Sunny").
  Bad day (storm) pill: bg #FFE1E1, day + condition text #B32424, temp stays ink.

## Weather glyphs (24 × 24)
- sun (#FFB800): `<circle cx=12 cy=12 r=4.5/>` filled + stroke 2 `M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.3 5.3l1.4 1.4M17.3 17.3l1.4 1.4M5.3 18.7l1.4-1.4M17.3 6.7l1.4-1.4`
- storm: cloud fill #7D8B90 `M7 16h10a4 4 0 0 0 .5-8 5.5 5.5 0 0 0-10.6 1.5A3.3 3.3 0 0 0 7 16z` + bolt fill #FFB800
  `M12.5 13.5l-2.2 4.2h2.4l-1 4.3 4-5.6h-2.4l1.1-2.9z`
- partly cloudy / wind: sun `<circle cx=9 cy=9 r=4/>` fill #FFB800 + cloud fill #B9C3CC
  `M8 19h9a3.5 3.5 0 0 0 .4-7 4.8 4.8 0 0 0-9.2 1.3A2.9 2.9 0 0 0 8 19z`

## Path section (margin-top 8, relative, height 520 for 3 + chest; nodes absolutely positioned by centre)
- Canvas: centres zig-zag x 150 → 230 → 270 → 190 → 110 …, vertical spacing ~110–120. Adapted (3 + chest), centres:
  n1 (150, 70) · n2 (260, 195) · n3 (140, 320) · chest (210, 450). Line (SVG viewBox 0 0 390 520, behind nodes):
  `M150 70 C150 130 260 125 260 195 C260 265 140 250 140 320 C140 390 210 380 210 450`
  stroke line colour (#E5E5DC / dark #2B3B42), width 10, round cap, dasharray `2 18` (dotted), no fill.
- Labels sit on the opposite side from the screen edge: node x < 195 → label right (left = ring right + 12, align
  start); else label left, right-aligned, ending at ring left − 12. Width 120–150, column gap 5: name h3, status chip,
  optional reason line (small, e.g. "Storm Saturday"). Label top ≈ ring top + 14–24.

## Nodes
- Ring (outer) 96 px (current/next node 104), border 7 in status colour, bg = screen bg; core 72 px (78 on 104),
  circle, bg = place-type colour, white glyph 34 px (38 on 104), shadow `0 6px 0` type edge (lake #2F86D6, trail
  #CC7A00, camp #2B8545, peak #0E8A83). Badge 30 px circle bottom-right (−2, −2), border 3 screen bg, glyph 16 px.
- Status → ring / badge / badge glyph / chip (bg, text) light:
  - Go: #3DAA5C / #3DAA5C / white check `M5 12.5l4.5 4.5L19 7.5` (stroke 3.4) / #DFF6E7, #1B6B3E, "Go · Sat"
  - Caution: #FFC800 / #FFC800 / #5C4000 `M12 6v7M12 17.5v.3` / #FFF1BF, #6E4E00, wind icon
    `M3 9h11a3 3 0 1 0-3-3M3 14h15a3 3 0 1 1-3 3`, "Caution · wind"
  - Not now: #FF4B4B / #D93636 / white × `M7 7l10 10M17 7L7 17` / #FFE1E1, #B32424, icon circle r9 +
    `M8.5 8.5l7 7M15.5 8.5l-7 7`, "Not now"; core opacity .55
  - Seasonal lock: ring border 6 **dashed** #AEB8BC, no badge; core #C9D1D4, glyph #56646A (padlock 32 px
    `<rect x=5 y=11 w=14 h=10 rx=2.5/>` + `M8.5 11V8a3.5 3.5 0 0 1 7 0v3`), shadow #AEB8BC; chip #ECEEEF / #56646A,
    "Opens in May"
- Chip: height 26, padding 0/9, radius 999, 800 12 px, gap 4, icon 14 px (stroke 2.6).
- Done (gold): no ring border, ring 76 / core 70, core #FFC800, star #7A5800 34 px fill
  `M12 2.5l2.9 6 6.6.8-4.9 4.5 1.3 6.5L12 17l-5.9 3.3 1.3-6.5L2.5 9.3l6.6-.8z`, shadow `0 6px 0 #D9A500`;
  chip bg #FFF6D6 text #7A5800 "Done · +40 XP".
- START bubble above the first not-done node (bottom touches ring top): padding 8/14, radius 12, card bg, border 2
  line, 900 15 px, letter-spacing .06em, #0C807A; tail 20 × 10 `M0 0 L10 10 L20 0` fill card, stroke line 2, margin −2.
- Not-now mascot: worried Irbis (`Mascot kind="worried"`, umbrella) 100 px, on the label side right of the label:
  top-left = node centre + (172, −78), i.e. it hangs to the screen edge beside the chip.

## Smart swap card (under the Not-now node, full width: left/right 16, gap from node ~20)
- Card padding 14, gap 12, radius 20, border 2 + bottom 4, **border colour #4CA9FF**.
- Head row (gap 8): swap icon 22 px #1F74C7 stroke `M4 8h13l-3-3M20 16H7l3 3` + caption "SMART SWAP" #1F74C7.
- Body row (gap 12, centre): place photo 72 × 72 radius 16 cover; column gap 4: "Try {place} instead" (h3), reason
  (small), Go chip.
- Buttons row gap 10: "Keep plan" white button (flex 1; card bg, #0C807A text, border 2 line, shadow 0 4 line) ·
  "See place" primary (flex 1.4; #0C807A, shadow #075B56). Canvas btn: min-h 48, radius 14 → use design.md button.

## Chest node (last)
- Tile 88 × 76, radius 20, bg #FF9F1C, shadow `0 6px 0 #CC7A00`, glyph 54 × 46 (viewBox 0 0 48 40):
  `<rect x=4 y=14 w=40 h=24 rx=5 fill=#8C5A33/>` · `M4 18 Q4 4 24 4 Q44 4 44 18Z` fill #A86B3C ·
  `<rect x=4 y=16 w=40 h=5 fill=#FFC800/>` · `<rect x=20 y=14 w=8 h=12 rx=2 fill=#FFC800/>`.
- Label (right side, width 136): "Monthly chest" (h3) + "1 / 3 · Check in at all 3 places" (small).

## Dark mode (HomeDark)
- Tokens: bg #131D22, card #1C2A30, line #2B3B42, ink #F1F5F4, body #D5DEDD, muted #9AA8AD, soft #22323A,
  gold #3D3310 / gold text #FFD95A; white button text #5FD6CE.
- Chips: Go #173F2A / #7BE0A2 · Caution #463A10 / #FFD95A · Not now #4A1C1F / #FF9A9A · Lock #2B3940 / #B8C4C8 ·
  Done #3D3310 / #FFD95A. Storm pill bg #4A1C1F, text #FF9A9A, temp = ink.
- Ring/badge/core/chest hexes are unchanged on the canvas; note `n_homedk` asks for brighter ring tints keeping
  3:1 on #131D22 (lighten #FF4B4B / #AEB8BC if they fail) — every status keeps icon + label.

## Motion (`n_home`)
- Tap a node: bounce (scale 1 → 1.1 → 1, spring) + popover anchored to the node.
- Node becomes done: flips to gold + coin shower (Reanimated placeholder OK).
- Not-now node: worried Irbis sways under the umbrella with rain particles (loop; off with reduce-motion).
- Chest open animation on `POST /v1/path/chest/open` (open-chest art still needed — see MEDIA.md).
- Canvas weather-shield pulse on the streak is dropped (no streak in this header).
