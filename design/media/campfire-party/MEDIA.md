# campfire-party — media

| File | What | Used on | Format / size | Status |
|---|---|---|---|---|
| Companion avatars ×6 | fox, ibex, bear, marmot, eagle, panda (neutral) | clue order, vote list, Who am I list, WYR voter avatars | SVG, in app (`companion*`) | exists |
| `irbisDefault.ts` | Irbis mascot, neutral (canvas `9ebec15…`) | hint bubble on ImpReveal, ImpVote, WYR | SVG, in app | exists |
| `hero-lake.jpg` | Lake illustration (canvas `2ea0b85…`) | ImpReveal secret-word card backdrop | JPG, in app `src/assets/images/places/` | exists |
| Game icons ×4 | Imposter, Who am I?, Would you rather (+ Mafia) | lobby game picker, game headers | inline SVG from CampHub/CampLobby boards | exists (canvas vectors) |
| "SHH…" imposter card | dark card, no illustration on the board | ImpImposter | drawn in code | exists (canvas layout) |
| "?" hidden character card | drawn in code | WhoAmI | drawn in code | exists (canvas layout) |
| `wyr-drumroll` | short drumroll when WYR bars fill (note `n_c_wyr`) | WYR reveal | sound, ≤1.5 s, .mp3/.wav | needed — needs a sound package (ask) or placeholder: haptic only |
| Campfire badge emblems ×5 | Poker Face, Sharp Detective, Life Saver, Mind Reader, Campfire Host (hexagon + glyph) | CampHub badges card, badge unlock | inline hexagon in code / final art | needed only if badges are in scope (placeholder OK: canvas hexagon + glyph) |
| Content packs | Imposter word packs, Who am I characters, WYR questions — uz / ru / en | all three games | bundled JSON in app | needed — text, not art (ask who writes) |

Owner art (2026-10-20), not in the app yet (badges come with `campfire-party-2`): `badge-poker-face.png`, `badge-life-saver.png`, `badge-campfire-host.png`. Still missing: Sharp Detective, Mind Reader.
