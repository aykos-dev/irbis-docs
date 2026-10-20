# Brief campfire-crocodile-1-irbis-app — tile, protocol v5, settings, packs, pick, secret word

- Spec: features/campfire-crocodile.md · ACs in this slice: AC1, AC2, AC3, AC8
- Repo / branch: irbis-app · `feat/campfire-crocodile` (create from `main`; slices stack on it). Not from `feat/campfire-xo`.
- Depends on: campfire-core/party/mafia on main (gameReducer, GameWaiting, lobby picker + settings, GameTile,
  campTheme, SecretCard, useSecureScreen, usedStore, packs/index.ts)

## Files
- New: `src/features/campfire-core/games/croc/` — `CrocScreen.tsx` (phase switch), `CrocPick.tsx` (host list /
  waiting), `CrocSecret.tsx` (describer card: SecretCard + rule + Skip + Start), `CrocGlyph.tsx` (tile glyph),
  `__tests__/`. Packs: copy `irbis-docs/design/media/campfire-crocodile/packs/croc-{animals,heroes,famous}.json`
  → `games/packs/` unchanged.
- Edit: `games/packs/index.ts` (`game: 'croc'` in the schema, word items; export croc packs), `games/gameReducer.ts`
  (new `croc` branch, range `{ min: 3, max: 15 }` incl. host — host plays), `protocol/codec.ts` (`PROTOCOL_VERSION`
  3 → 5; the host picks the describer locally, no message; add client msgs `crocStart`, `crocSkip`, `crocGuessed` with `{ round,
  turnNo }`; croc `game.public` schema; per-seat `secret` for croc), host room/server + `join/playerClient.ts`
  (route the croc messages to the reducer, send the secret only to the describer), lobby settings (timer + packs),
  `campTheme.ts` (`GameId` + `'croc'` colour), `components/GameTile.tsx`, CampHub + lobby picker, `GameWaiting.tsx`
  (render `CrocScreen` for `game === 'croc'`), host room persistence, `src/shared/i18n/{en,ru,uz}/camp.json`.
- Read for patterns: how `imposter` sends a per-seat secret + uses `usedStore` (no repeats per pack), how `mafia`
  settings live in the lobby, how `rather` sends client messages to the host reducer. Tests that assert protocol 3
  may change expected 3 → 5 only — list each edited test in the summary; no other test edits.
- Find things with `graphify explain/query` in irbis-app first if available; else grep narrowly.

## Behaviour
- AC1 — Tile "Crocodile" (`camp.hub.game.croc`, `camp.lobby.game.croc`), `CrocGlyph` (simple croc head / jaw,
  campTheme stroke). Lobby settings when croc is picked: timer chips 30/60/90 (default 60), pack checkboxes (default
  all 3, at least 1 — unticking the last is blocked). Start disabled with `croc.needThree` when < 3 connected incl.
  host, or with `croc.needPack` if no pack. Older protocol phone → existing "Update Irbis to join this room".
- State: `public = { phase: 'pick', turnNo: 0, durationSec, totals: { guessed: 0, skipped: 0, turns: 0 } }`;
  host keeps `packs`, `word`, `describerSeatId` privately.
- AC2 — phase `pick`: host phone shows `croc.pickTitle` + all connected seats (avatar + nickname, host included,
  `croc.pick.<seatId>`); tap → `turnNo`+1, draw a word, phase `ready`, `describerSeatId` set. Non-host phones:
  `croc.choosing` (`croc.waiting`).
- AC3 — phase `ready`: describer gets `secret { word, pack }` (the host never puts the word in `public` here) and
  sees SecretCard (hold to reveal, `useSecureScreen`) with word, pack name, rule `croc.rule`, buttons Skip
  (`croc.skip` → new word, `totals.skipped`+1) and Start (`croc.start` → phase `running`). In this slice `running` renders
  the same describer card / showing view; the timer and Guessed! come in slice 2. Others: `croc.showing` with the describer avatar.
  Word pick: random from ticked packs, skip words already used for that pack (`usedStore`), reset the pack when
  empty. Messages with an old `turnNo` or from a non-describer are ignored.
- AC8 — packs validated by the schema test (60 items each, unique ids, uz/ru/en). No sounds anywhere.

## Copy (`camp.json`, add; match existing key style)
| key | en | ru | uz |
|---|---|---|---|
| games.croc | Crocodile | Крокодил | Timsoh |
| croc.meta | 3–15 · mime | 3–15 · пантомима | 3–15 · pantomima |
| croc.needThree | Crocodile needs 3+ players | Для «Крокодила» нужно 3+ игрока | «Timsoh» uchun 3+ o'yinchi kerak |
| croc.needPack | Pick at least one pack | Выберите хотя бы один набор | Kamida bitta to'plamni tanlang |
| croc.timer | Turn time | Время хода | Navbat vaqti |
| croc.seconds | {{n}} s | {{n}} с | {{n}} s |
| croc.packs | Word packs | Наборы слов | So'z to'plamlari |
| croc.pickTitle | Who shows next? | Кто показывает? | Kim ko'rsatadi? |
| croc.choosing | The host is choosing who shows | Ведущий выбирает, кто показывает | Boshlovchi kim ko'rsatishini tanlayapti |
| croc.showing | {{name}} is showing | Показывает {{name}} | {{name}} ko'rsatyapti |
| croc.rule | Show it, don't say it — no words, no sounds | Покажи, не говори — без слов и звуков | Ko'rsating, aytmang — so'zsiz va ovozsiz |
| croc.skip | Skip | Другое слово | Boshqa so'z |
| croc.start | Start | Старт | Boshlash |
| croc.guessed | Guessed! | Угадали! | Topildi! |

## testIDs · QA events
`camp.hub.game.croc` · `camp.lobby.game.croc` · `croc.settings.timer.<30|60|90>` · `croc.settings.pack.<id>` ·
`croc.pick` · `croc.pick.<seatId>` · `croc.waiting` · `croc.card` · `croc.skip` · `croc.start` ·
`camp_game_started { game:'croc', players }` · `croc_pick { turnNo }` · `croc_skip { turnNo, pack }` — no words, no names.

## Approved packages
none

## Done when
- [ ] tests: range 3–15 + Start reasons; pick → ready with secret only on the describer's view (not in public);
      skip draws a new word + counts; no repeat until pack empty, then reset; stale turnNo / non-describer ignored;
      packs schema (3 × 60); protocol 5 rejects 3; CrocPick host vs. guest render with the room mocked
- [ ] `npm run check` green (output in summary), committed on `feat/campfire-crocodile`, reply ≤ 10 lines
