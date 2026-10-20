# campfire-xo — media

No canvas board for X and O (roadmap 29a, owner sketch). Everything below except the tile art can be drawn in code.

| File | What | Used on | Format / size | Status |
|---|---|---|---|---|
| X and O marks | X (two strokes) and O (ring), drawn in with a short stroke animation | board cells | react-native-svg + Reanimated, campTheme colours | needed · drawn in code (no file) |
| Winning line | stroke across the 3 winning cells | board, end of each game | react-native-svg + Reanimated | needed · drawn in code |
| Board grid | 3×3 grid, rounded lines | board | drawn in code | needed · drawn in code |
| XO game tile art | tile image for CampHub grid + lobby picker (like the other game tiles) | CampHub, CampLobby | inline SVG 24×24 glyph or tile illustration | needed · placeholder OK? (glyph drawn in code) |
| Companion avatars ×6 | player avatars on the score bar | board, score | SVG in app (`companion*`) | exists |
| Win confetti | small coloured rects (as Mafia game over) | final score screen | drawn in code | exists (Mafia) |
| Move / win / draw sounds | short tap, win, draw | board | .m4a | needed? — reuse lessons Kenney CC0 sounds or haptics only (owner) |
