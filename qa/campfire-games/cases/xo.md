# X and O — test cases (campfire-xo AC1–AC8 + campfire-core multi-player)

Build: `feat/campfire-xo` (protocol v4). Players: **A** = emulator-5554 host, **B** = emulator-5556 joiner or
**bot_1** as the joiner (so moves and illegal moves can be scripted). Board cells `xo.cell.0`…`xo.cell.8`.

| id | title | AC | players | steps | expected |
|---|---|---|---|---|---|
| XO-01 | Tile in hub + picker | AC1 | A | CampHub, lobby picker | `camp.hub.game.xo`, `camp.lobby.game.xo` present (glyph manual) |
| XO-02 | Start needs exactly 2 | AC1 | A alone; A + 2 bots | Select X and O | Start disabled "X and O is for 2 players" with 1 and 3 seats |
| XO-03 | Game 1: host X, X first | AC2 | A + bot_1 | Start | Host turn "Your turn" X; `game.public.xSeatId` = host; bot sees "<host>'s turn" |
| XO-04 | Out-of-turn move ignored | AC2 | A + bot_1 | bot sends xoMove on X's turn | Board unchanged |
| XO-05 | Taken cell ignored | AC2 | A + bot_1 | host plays 4; bot sends xoMove cell 4 | Board unchanged, still O's turn |
| XO-06 | Stale gameNo / after end ignored | AC2 | A + bot_1 | bot sends xoMove with old gameNo; after a win, bot sends move | Ignored |
| XO-07 | Win lines (8) | AC3 | A + bot_1 | Play each of rows 0-1-2, 3-4-5, 6-7-8, cols, diagonals across games | `result {kind: win, line}` correct; banner "You win!" / "<nick> wins!"; score +1; board locks |
| XO-08 | Draw | AC3 | A + bot_1 | Fill board without line | "Draw", draws +1 |
| XO-09 | Next game swaps X/O | AC4 | A + bot_1 / B | Either taps Next game after win and after draw | gameNo+1, marks swap (draws too), X moves first, "Game n" |
| XO-10 | Next game from joiner + double tap | AC4 | bot_1 | bot sends xoNext twice | Only one new game |
| XO-11 | Score bar | AC5 | A + B | After games, read score bar | avatar, nickname, mark, wins; "Draws d" |
| XO-12 | Joiner drops → pause; reconnect | AC6 | A + bot_1 | bot mute 12 s; reconnect with token | Host "Waiting for bot_1…", cells disabled; after reconnect same board/turn/score |
| XO-13 | Third phone mid-series | AC6 | A + bot_1 + bot_2 | bot_2 hello | "Game in progress" (no seat in the game) |
| XO-14 | Host removes joiner → series ends | AC6, AC7 | A + bot_1 | Remove bot_1 | Final score screen |
| XO-15 | End + final score | AC7 | A + B | Host End → "End the series?" → confirm | Both phones "Final score", winner line, "Draws d · Games n"; host Play again (0–0, game 1, host X) + Lobby; joiner "Waiting for the host", no End |
| XO-16 | Host app killed and resumed | AC5 | A + bot_1 | force-stop mid-series, reopen → Resume | Score and board kept |
| XO-17 | Real joiner UI (B) | AC2 | A + B | Play a game on both emulators | Both boards same state; turn header correct — manual |
| XO-18 | Mute button | AC8 | A | Tap `xo.mute` | Toggles (sound itself manual) |
| XO-19 | Version mismatch | AC1 | bot v5 | hello with v 5 on v4 host | `rejected version` |
