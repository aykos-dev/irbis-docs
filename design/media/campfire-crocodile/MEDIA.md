# campfire-crocodile — media

No canvas board for Crocodile (roadmap 29b, owner 2026-10-20). Look and feel follows the campfire boards
(`CampLobby`, `ImpReveal`, `MafEnd`) and `campTheme`. Everything except the tile art and the word packs is drawn in code.

| File | What | Used on | Format / size | Status |
|---|---|---|---|---|
| Crocodile tile glyph | tile image for CampHub grid + lobby picker (like the other game tiles) | CampHub, CampLobby | inline SVG 24×24 glyph, campTheme colour | needed · placeholder OK? (glyph drawn in code) |
| Word card | word on the describer's phone (hold-to-reveal like Imposter) | describer turn | existing `SecretCard` | exists |
| Turn timer ring | countdown ring / bar | turn screen | react-native-svg + Reanimated | needed · drawn in code |
| Companion avatars ×6 | player avatars on the score list | turn, scores | SVG in app (`companion*`) | exists |
| Win confetti | small coloured rects | final scores | drawn in code (Mafia) | exists |
| Guessed / time-up / win sounds | short cue on guess, timer end, winner | turn, final | .m4a | needed? — reuse lessons Kenney CC0 clips (`src/shared/sounds`) or haptics only |
| Word packs ×3 | animals, movie heroes, famous people — uz/ru/en | describer card | JSON in `design/media/campfire-crocodile/packs/` | needed · Claude drafts, owner review |
