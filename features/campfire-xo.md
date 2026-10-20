# campfire-xo

- Status: Approved
- Surfaces: app only (no api, no web: the game runs on the host phone over the campfire-core room; no XP, no badges)
- Related ADRs: ADR-001 (guest-first: offline games need no account)
- Requirements: ROADMAP 29a (owner 2026-10-20): X and O duel, host + 1 joiner, 3×3, 3 in a row, next game, running
  score until the host ends. No canvas board and no Product Overview section — this spec is the source.
  Look and feel: campfire boards (`CampLobby`, `MafEnd`, `WYR`) and `campTheme`.
- Builds on: `campfire-core` + `campfire-party` + `campfire-mafia` (all on irbis-app `main` at f7290a3).
  Branch: irbis-app `feat/campfire-xo` from `main`.

## Goal
Two phones in a Campfire room (host + 1 joiner) play X and O on a shared 3×3 board. After each game either player
taps "Next game", symbols swap, and the score carries on until the host ends the series and both phones see the
final score.

## Local protocol changes (no API)
- `PROTOCOL_VERSION` 3 → **4** (a v3 phone gets the existing "Update Irbis to join this room").
- Host → all: `game { game: 'xo', round, public }` — `public` `{ board: (x|o|null)[9], xSeatId, oSeatId, turn: x|o,
  result: null | { kind: win|draw, mark?, line?: [a,b,c] }, score: { [seatId]: wins }, draws, gameNo, paused,
  ended?: { games, draws, score } }`.
- Client → host: `xoMove { round, gameNo, cell: 0..8 }`, `xoNext { round, gameNo }`.
- State in the pure `gameReducer` (new `xo` branch) on the host; saved with the host room (resume 12 h).

## Data model changes
None on the server. App: none new (mute reuses the lessons mute key).

## Acceptance criteria
- **AC1** — **Tile + start:** "X and O" tile (code-drawn X/O glyph, own `campTheme` colour) in the CampHub games
  grid and the lobby game picker. Seat range exactly 2 (host + 1 joiner). With any other count, Start is disabled
  with "X and O is for 2 players". Protocol v4.
- **AC2** — **Board + turns:** 3×3 board on both phones, same state. Game 1: host is X, X moves first. Only the
  phone whose turn it is can tap a free cell; the host ignores a move that is out of turn, on a taken cell, for an
  old `gameNo` or after the game ended. Header "Your turn" / "<nickname>'s turn" with the mark. Placed marks draw in
  (≈200 ms) + light haptic. No turn timer.
- **AC3** — **Win / draw:** after each move the host checks the 8 lines (3 rows, 3 columns, 2 diagonals). Three
  of a mark → winning line drawn over the cells, banner "You win!" (winner) / "<nickname> wins!" (other phone),
  winner +1. Full board, no line → "Draw", draws +1. Board locks.
- **AC4** — **Next game:** the result stays until **either** player taps "Next game". New empty board, `gameNo`+1,
  X and O swap every game (draws included); X always moves first. Header shows "Game <n>".
- **AC5** — **Score bar:** top of the board: each player's avatar, nickname, current mark and wins; centre
  "Draws <d>". Kept across games until the host ends; survives host app restart (room resume 12 h).
- **AC6** — **Disconnect:** joiner drops → host board freezes with "Waiting for <nickname>…" (cells disabled);
  the same seat reconnects to the same board, turn and score. Host drops → existing "reconnecting…" state on the
  joiner. A third phone joining mid-series gets the existing "Game in progress" message. Host removes the joiner
  → series ends (AC7 screen).
- **AC7** — **End + final score:** host "End" → confirm "End the series?" → both phones: "Final score",
  "<nickname> wins the series <a>–<b>" / "You win the series <a>–<b>" / "It's a tie <a>–<a>", "Draws <d> · Games
  <n>", small confetti on a win (Mafia game-over confetti). Host: "Play again" (score 0–0, game 1, host X) and
  "Lobby"; joiner: "Waiting for the host". The joiner has no End button.
- **AC8** — **Sounds + mute:** the lessons sound player moves from `src/features/lessons/sounds.ts` to
  `src/shared/sounds/` (lessons imports updated, behaviour unchanged). X and O plays: win → `complete` clip on the
  winner's phone, `wrong` on the other; draw → `correct` on both. Mute button on the board header toggles the same
  mute setting lessons use. Audio failure never breaks the game (logged, silent).

### QA events (app, dev/staging builds)
`camp_game_started { game: 'xo', players: 2 }` · `xo_move { gameNo, cell, mark }` · `xo_result { gameNo, kind,
mark? }` · `xo_next { gameNo }` · `xo_paused { paused }` · `camp_game_ended { game: 'xo', games, draws }` — no
nicknames.

### testIDs (app)
`camp.hub.game.xo` · `camp.lobby.game.xo` · `xo.board` · `xo.cell.<0-8>` · `xo.turn` · `xo.score.<seatId>` ·
`xo.draws` · `xo.result` · `xo.next` · `xo.paused` · `xo.mute` · `xo.end` · `xo.final` · `xo.play-again` · `xo.lobby`

### Required UI states
- [ ] Loading (waiting for the first `game` message → existing GameWaiting)
- [ ] Empty (Start disabled with reason when seats ≠ 2)
- [ ] Error (host lost → existing reconnecting state; room closed → CampHub)
- [ ] Offline: works with no internet; no OfflineBanner on campfire screens
- [ ] Keyboard: none; safe areas; haptics (move, win); press states; cells ≥ 44 pt
- [ ] Dark campfire theme (`campTheme`) + design tokens + shared components only

## Media
`design/media/campfire-xo/MEDIA.md`: X/O marks, grid, winning line, tile glyph drawn in code (tile glyph is a
placeholder → STATUS known issue); sounds reuse the lessons Kenney CC0 clips (Q4).

## Waivers
- Phone-to-phone play is not unit-testable end to end: tests cover the `xo` reducer (turns, illegal moves, 8 lines,
  draw, swap, score, pause/resume, end) and the screens with the room mocked; the owner tests on two phones.

## Out of scope
- Bigger boards, more than 2 players, spectators, pass-and-play, AI opponent, turn timer, XP / badges.

## Assumptions
- Q1 (owner, 2026-10-20): exactly 2 phones (host + 1 joiner); Start disabled otherwise.
- Q2 (owner, 2026-10-20): game 1 host is X; X always moves first; X/O swap every game, draws included.
- Q3 (owner, 2026-10-20): result stays until either player taps "Next game".
- Q4 (owner, 2026-10-20): tile glyph drawn in code; reuse the lessons sounds (respect the lesson mute).
- Q5 (owner, 2026-10-20): no turn timer.
- Q6 (owner, 2026-10-20): disconnect pauses; same seat resumes the same board and score; host can End any time.
- Code in `irbis-app/src/features/campfire-core/games/xo/` (same as party/mafia); sounds module moves to
  `src/shared/sounds/` because features never import each other (main session).
- Clip mapping (win/lose/draw) and a mute button on the board are main-session picks (main session).

## Open questions
- none
