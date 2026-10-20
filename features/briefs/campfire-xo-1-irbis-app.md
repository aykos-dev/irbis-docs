# Brief campfire-xo-1-irbis-app — tile, protocol v4, board, turns, win/draw

- Spec: features/campfire-xo.md · ACs in this slice: AC1, AC2, AC3
- Repo / branch: irbis-app · `feat/campfire-xo` (create from `main`; slices stack on it)
- Depends on: campfire-core/party/mafia on main (gameReducer, GameWaiting, lobby picker, GameTile, campTheme)

## Files
- New: `src/features/campfire-core/games/xo/` — `xoRules.ts` (pure: `LINES`, `findWin(board)`, `isFull`),
  `XoScreen.tsx` (board + header), `XoBoard.tsx` (grid, cells, marks, winning line — react-native-svg + Reanimated),
  `XoGlyph.tsx` (tile glyph), `__tests__/`.
- Edit: `campTheme.ts` (`GameId` + `'xo'` colour), `components/GameTile.tsx` (xo case), `games/gameReducer.ts`
  (new `xo` branch + range `{ min: 2, max: 2 }`), `protocol/codec.ts` (`PROTOCOL_VERSION` 3 → 4, `xoMove` schema,
  xo `game.public` schema), host server/room + `join/playerClient.ts` (route `xoMove` to the reducer, expose xo view),
  `games/GameWaiting.tsx` (render `XoScreen` for `game === 'xo'`), CampHub + lobby picker (tile selectable),
  host room persistence, `src/shared/i18n/{en,ru,uz}/camp.json`.
- Read for patterns: how `rather` (votes from players → host reducer → public state) and `mafia` are wired end to
  end; existing tests that assert protocol version 3 (editing expected 3 → 4 is part of this spec — list each
  edited test in the summary; no other test edits).
- Find things with `graphify explain/query` in irbis-app first if available; else grep narrowly.

## Behaviour
- AC1 — Tile "X and O" (`camp.hub.game.xo`, `camp.lobby.game.xo`) with `XoGlyph` (an X and an O, campTheme stroke).
  Seats must be exactly 2 incl. host; otherwise Start disabled with `xo.needTwo` (follow how other games show the
  range reason). v3 phone → existing "Update Irbis to join this room".
- AC2 — Start: `public = { board: Array(9).fill(null), xSeatId: hostSeat, oSeatId: joinerSeat, turn: 'x',
  result: null, score: { [host]: 0, [joiner]: 0 }, draws: 0, gameNo: 1, paused: false }`. Move (host taps locally,
  joiner sends `xoMove { round, gameNo, cell }`): accept only if sender's mark === turn, cell in 0..8 and empty,
  `gameNo` current, `result` null, not paused; else ignore (no crash, no state change). Accepted → place mark, flip
  turn, broadcast. Header `xo.turn`: "Your turn" / "<name>'s turn" + small mark. Cells ≥ 44 pt, disabled when not
  your turn. Mark draws in ~200 ms (stroke dash) + light haptic on the phone that placed it and on the other phone.
- AC3 — After each accepted move: `findWin` over 8 lines → `result { kind:'win', mark, line }`, winner's score + 1;
  else full → `result { kind:'draw' }`, draws + 1. Winning line stroked across the 3 cells. Banner `xo.result`:
  "You win!" / "<name> wins!" / "Draw". Board locks. (Next game button + score bar come in slice 2; until then show
  the banner only.)

## Copy (`camp.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| games.xo (match existing game-name key style) | X and O | Крестики-нолики | X va O |
| xo.needTwo | X and O is for 2 players | Крестики-нолики — игра для двоих | X va O ikki kishilik o'yin |
| xo.yourTurn | Your turn | Ваш ход | Sizning navbatingiz |
| xo.theirTurn | {{name}}'s turn | Ходит {{name}} | {{name}} navbati |
| xo.youWin | You win! | Вы победили! | Siz yutdingiz! |
| xo.theyWin | {{name}} wins! | {{name}} побеждает! | {{name}} yutdi! |
| xo.draw | Draw | Ничья | Durang |
| xo.cell | Cell {{n}}, {{state}} | Клетка {{n}}, {{state}} | Katak {{n}}, {{state}} |
| xo.empty | empty | пусто | bo'sh |

## testIDs · QA events
`camp.hub.game.xo` · `camp.lobby.game.xo` · `xo.board` · `xo.cell.<0-8>` · `xo.turn` · `xo.result` ·
`camp_game_started { game:'xo', players:2 }` · `xo_move { gameNo, cell, mark }` · `xo_result { gameNo, kind, mark? }`

## Approved packages
none (react-native-svg + Reanimated already installed)

## Done when
- [ ] tests: `findWin` all 8 lines + no-win; draw; reducer start state; out-of-turn / taken cell / old gameNo /
      after result ignored; win adds score; Start disabled with ≠ 2 seats; protocol 4 rejects v3; screen shows
      turn text and banner with the room mocked
- [ ] `npm run check` green (output in summary), committed on `feat/campfire-xo`, reply ≤ 10 lines
