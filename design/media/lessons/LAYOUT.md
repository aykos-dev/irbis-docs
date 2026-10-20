# Lessons — layout notes from canvas (so dev agents never open the canvas HTML)

Base 390 × 844. Colours below are canvas values; map to `design/design.md` tokens where one exists (teal #1CB0A8 /
#0C807A, line #E5E5DC, ink #1F2A2E, bg #F7F7F2); new ones live in the feature's style file, dark mode = token pairs.

## LessonsHub
- Header (padding 16/16/0): title "Lessons" (h1) left; right: heart (#FF4B4B, 24 px) + hearts number (900, 16 px).
  No streak flame (→ `streaks`).
- Daily goal card (margin 0 16, padding 14, radius 20, border 2 + bottom 4, gap 14): ring 72 px (r 32, stroke 9, track
  #FFE6C2, progress #FF9F1C, round cap, starts at 12 o'clock) with "n/3" centred (900, 19 px); text "Daily goal ·
  3-minute lessons" (900, 17 px) + line (secondary); Irbis default mascot 60 px on the right.
- Tier card (margin 0 16, radius 22, border 2 + bottom 4): header row (padding 12/14, gap 12) tinted with the tier
  `colour` at ~15 % over the card; left square 40 px radius 12 in tier `colour` holding the tier's first lesson glyph
  (white); caption "TIER 1" (12 px, uppercase, letter-spacing .08em, 900) for keys 1–5, "FIRST AID" for `first-aid`;
  title (h2); right pill (28 px, radius 99, white, 12 px 900): "done / total" or ✓ "Done".
- Lessons grid: 3 columns, gap 8, padding 14/10/16. Node 84 px: ring r 38 stroke 6 (done = solid #FFC800; not done =
  track line colour); inner circle 60 px at 12 px inset, glyph colour bg, white 30 px glyph, shadow 0 4 0 rgba(0,0,0,.18);
  title under it (h3, centred, wraps). START pill above the node (top −10, #0C807A, white, 11 px 900, letter-spacing .06em).
- Glyph circle colours: compass #1CB0A8 · leaf #3DAA5C · padlock #FF9F1C · cloud #4CA9FF · paw #8C5A33 ·
  first-aid #D93636 · mountain #F2802E · waves #4CA9FF · avalanche #6B8FB3 · bolt #FF9F1C.

## Glyph paths (24 × 24, stroke currentColor, width 2, round caps/joins, no fill)
- compass: `<circle cx=12 cy=12 r=9/>` `<path d="M15.5 8.5 13.5 13.5 8.5 15.5 10.5 10.5Z"/>`
- leaf: `M5 19C5 10 10 5 19 5c0 9-5 14-14 14Z` · `M5 19 13 11`
- padlock: `<rect x=5 y=11 width=14 height=10 rx=2/>` · `M8 11V8a4 4 0 0 1 8 0v3`
- cloud: `M7 18h10a4 4 0 0 0 .5-8A6 6 0 0 0 6 9.5 4.3 4.3 0 0 0 7 18Z`
- paw: circles (7,9) (10.5,5.5) (14.5,5.5) (18,9) r 1.8 · `M12 11c-3 0-5.5 3.5-5.5 6a2.5 2.5 0 0 0 3.5 2.3 5 5 0 0 1 4 0A2.5 2.5 0 0 0 17.5 17c0-2.5-2.5-6-5.5-6Z`
- first-aid: `<rect x=3 y=6 width=18 height=14 rx=2/>` · `M9 6V4h6v2M12 10v6M9 13h6`
- mountain: `M2 20 9 7l4 7 2-3 7 9Z` · waves: `M2 9c2.5-2 4.5-2 7 0s4.5 2 7 0 4.5-2 6 0M2 15c2.5-2 4.5-2 7 0s4.5 2 7 0 4.5-2 6 0`
- avalanche: `M2 20 10 6l10 14Z` + circles (16,8) (19,12) r 1.5 · bolt: `M13 2 4 14h7l-1 8 9-12h-7Z`

## Quiz icons (24 × 24)
- close: stroke `M6 6l12 12M18 6L6 18` width 3, colour #8A979C, hit area 40 px
- heart (fill #FF4B4B): `M12 21s-8-5.2-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z`;
  broken overlay (wrong state): stroke white 2 `M12 7.5l-1.5 4 3 2-1.5 4`
- check: stroke `M5 12.5l4.5 4.5L19 7.5` width 3.4 · cross: stroke `M7 7l10 10M17 7L7 17` width 3.4

## Quiz
- Top row (padding 16/16/0, gap 12): close · progress bar (flex, 16 px, radius 99, track #E5E5DC, fill #1CB0A8 with
  inset bottom shadow 0 −4 0 rgba(0,0,0,.12)) · heart 26 px + number (900, 17 px) · speaker toggle (mute, 40 px).
- Body (padding 22/20/0, gap 14): chip (30 px, radius 99, glyph-colour tint bg, dark text, 13 px 900, glyph 16 px)
  "<tier title> · <lesson title>"; prompt (900, 24 px, lh 1.25); optional image (radius 16, full width, max 200 px
  tall, contain); hint row: companion 72 px + bubble (padding 10/14, radius 16, border 2 line, white, 800 15 px).
- Options (padding 18/20/0, gap 10): button with key circle "A"–"D" + text, wraps. States: idle white / border line /
  ink; picked #E3F7F5 / #1CB0A8 / #0B5B57; correct #DFF6E7 / #2E8B57 / #154F2E; wrong pick #FFE1E1 / #D93636 / #8F1F1F.
- Footer: Check (chunky button, 4 px bottom shadow; enabled #0C807A / shadow #075B56; disabled #E5E5DC / #6B787D),
  padding 16/20/28, top border 2.
- Correct sheet (bg #DFF6E7, padding 18/20/28, gap 12): circle 44 px #237A4A + check; "Nicely done!" (900, 22 px,
  #154F2E); explanation (700, 15 px, lh 1.45); Continue (#237A4A, shadow #165434).
- Wrong sheet (bg #FFE1E1): circle #D93636 + cross; "Not quite — you lost a heart" (#8F1F1F); "Correct answer:"
  (800, 15 px) + correct option text (bold) + wrongExplanation ?? explanation (#6B1717); Got it (#D93636, shadow #A12121).
  In practice mode the title is "Not quite" (no heart lost).
