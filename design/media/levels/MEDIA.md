# Media — levels

Screens: `Level`, `LevelUp`, `Companions` (canvas). Canvas asset ids from `design/assets.md`.
Owner (2026-10-18, Q10–Q11): canvas companion SVGs final; full-colour L2–L7 already in `design/media/onboarding/companion-l*.svg`;
fox/ibex poses exported here; missing poses + Lottie ship as a Reanimated placeholder (STATUS known issue).

| File | What | Used on | Format / size | Status (exists · needed · placeholder OK) |
|---|---|---|---|---|
| `companionPanda.ts` (app, canvas `44b792e4…`) | L1 panda cub "Bao", neutral | Level, Companions, LevelUp | SVG | exists · in app |
| canvas `d4c16d0e…` | L2 marmot, neutral, full colour | Level, Companions, LevelUp | SVG | exists · final · `onboarding/companion-l2.svg` |
| `companionFox.ts` (app, canvas `d1b0d619…`) | L3 fox, neutral | Level, Companions, LevelUp | SVG | exists · in app |
| canvas `dba7b962…` | L4 ibex, neutral, full colour | Level (next-companion silhouette), Companions | SVG | exists · final · `onboarding/companion-l*.svg` |
| canvas `ffe22771…` | L5 brown bear, neutral | Level, Companions | SVG | exists · final · `onboarding/companion-l*.svg` |
| canvas `55d73e65…` | L6 golden eagle, neutral | Level, Companions | SVG | exists · final · `onboarding/companion-l*.svg` |
| canvas `09bfc86c…` | L7 snow leopard, neutral | Level, Companions | SVG | exists · final · `onboarding/companion-l*.svg` |
| `levelup-hand-l3.svg` (canvas `50d9950e…`) | L3 fox handing over the backpack | LevelUp (L3→L4 outgoing) | SVG | exists · final |
| `levelup-catch-l4.svg` (canvas `0c1003d2…`) | L4 ibex catching the backpack | LevelUp (L3→L4 incoming) | SVG | exists · final |
| `levelup-hand-l1`, `-l2`, `-l4`, `-l5`, `-l6` | Outgoing companion handing over the backpack (panda, marmot, ibex, bear, eagle) | LevelUp | SVG | needed · placeholder (neutral art) |
| `levelup-catch-l2`, `-l3`, `-l5`, `-l6`, `-l7` | Incoming companion catching the backpack (marmot, fox, bear, eagle, snow leopard) | LevelUp | SVG | needed · placeholder (neutral art) |
| `levelup-evolution.json` | Evolution 3 s, skippable after 1 s: old glows → hands backpack → white flash → new catches + pose (canvas note `n_lvlup`) | LevelUp | Lottie (one per transition, or one with swappable layers) | needed · placeholder (Reanimated sequence) |
| `backpack-placeholder.svg` (`design/media/onboarding/`) | Orange backpack passing between companions | LevelUp | SVG | placeholder (from onboarding) |
| Level frame shapes ×7 (circle, rounded square, shield, hexagon, octagon, gem, star) | Companion frame per level, colour + dark shadow | Level, Companions, LevelUp | drawn in code (react-native-svg) from canvas clip-paths | exists on canvas · final |
| Requirement glyphs (XP bolt, first-aid cross, boot) | Requirement row icons | Level | drawn in code from canvas paths | exists on canvas · final |
| Sunburst + confetti | LevelUp background | LevelUp | drawn in code | exists on canvas · final |
