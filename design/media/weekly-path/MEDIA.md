# Media — weekly-path

App screens: Home, HomeDark (canvas). Animations from canvas note `n_home`.

| File | What | Used on | Format / size | Status (exists · needed · placeholder OK) |
|---|---|---|---|---|
| Irbis worried (umbrella) | Mascot on the "Not now" node | Home node | SVG | exists in app (`Mascot kind="worried"`) |
| Companion neutral (current level) | User marker on the path | Home | `CompanionArt` (levels) | exists in app |
| Place-type glyphs (peak, lake, cave, camp, trail, waterfall, canyon) | Node core icon | Home nodes | inline SVG | exists in app (`placeTypes`) |
| Status icons (Go check, Caution !, Not now ×, lock) | Status ring + chip | Home nodes | inline SVG | exists in app (`StatusChip`) |
| Weather glyphs (sun, storm, wind…) | Weekend weather strip | Home header | inline SVG | exists in app · placeholder (conditions) |
| Path line + node rings, gold completed node with star | Winding path, node states | Home | inline SVG / views from canvas | exists on canvas (inline) |
| Header glyphs: flame, boot, XP bolt, gem | Stats row | Home header | inline SVG from canvas | exists on canvas (inline) |
| Weekly chest — closed / progress / open | Last node | Home | SVG ~64 px | closed on canvas (inline); **open chest needed** |
| Chest-open animation | Chest opening + reward | Home | Lottie or Reanimated | **needed** · placeholder OK: Reanimated |
| Coin shower | Node turns gold | Home | Lottie or Reanimated | **needed** · placeholder OK: Reanimated |
| Rain particles + worried sway | "Not now" node | Home | Reanimated | placeholder OK: Reanimated |
| Node bounce + popover | Tap a node | Home | Reanimated | code only |
