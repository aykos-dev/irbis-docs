# Brief campfire-xo-2-irbis-app — next game, score, disconnect, final score, sounds

- Spec: features/campfire-xo.md · ACs in this slice: AC4, AC5, AC6, AC7, AC8
- Repo / branch: irbis-app · `feat/campfire-xo` (slice 1 committed there)
- Depends on: brief campfire-xo-1-irbis-app

## Files
- New: `games/xo/XoScoreBar.tsx`, `games/xo/XoFinal.tsx`, `src/shared/sounds/` (moved player), tests.
- Edit: `games/xo/*`, `games/gameReducer.ts` (xo next / pause / end / play again), `protocol/codec.ts` (`xoNext`),
  host server + `join/playerClient.ts`, `src/features/lessons/*` (import path only), `camp.json` ×3.
- Move: `src/features/lessons/sounds.ts` → `src/shared/sounds/sounds.ts` (`git mv`; same API `load/play/muted`
  + mute toggle). Update lessons imports and any test `jest.mock` paths for it (path-only edits allowed; list them).
  Clip assets stay in `src/assets/sounds/`. If qaLog event name `lesson_audio_error` is used by lessons tests,
  keep it; xo failures may use the same logger with stage prefixed `xo_`.
- Read for patterns: `games/mafia/GameOver.tsx` (confetti, host Lobby / Play again, players "Waiting for the host"),
  how Mafia handles End confirm, seat drop/reconnect and host remove in the reducer.

## Behaviour
- AC4 — When `result` is set, both phones show "Next game" (`xo.next`). Either tap (host local, joiner sends
  `xoNext { round, gameNo }`; ignore stale gameNo or no result) → empty board, `gameNo`+1, swap `xSeatId`/`oSeatId`,
  `turn:'x'`, `result:null`. Header shows "Game <n>" (`xo.game`).
- AC5 — `XoScoreBar` at the top: per player avatar (SeatAvatar), nickname, current mark, wins (`xo.score.<seatId>`);
  centre "Draws <d>" (`xo.draws`). State persisted with the host room (12 h resume restores board + score).
- AC6 — Joiner seat disconnected → `paused:true`; host sees "Waiting for <name>…" (`xo.paused`), all cells disabled,
  moves ignored; reconnect same seat → `paused:false`, same board/turn/score. Host drop → existing reconnecting
  state on joiner. Third phone mid-series → existing "Game in progress" message. Host removes joiner → `ended`.
- AC7 — Host header "End" (`xo.end`) → confirm "End the series?" (End / Keep playing) → `ended { games, draws,
  score }` → both phones `XoFinal` (`xo.final`): title "Final score"; line: you won → "You win the series {{a}}–{{b}}",
  other won → "{{name}} wins the series {{a}}–{{b}}", equal → "It's a tie {{a}}–{{a}}" (a = viewer's wins first;
  tie uses the same number twice); "Draws {{d}} · Games {{n}}" (games = finished games); confetti unless tie. Host:
  "Play again" (`xo.play-again`: score 0, draws 0, gameNo 1, host X, round + 1) and "Lobby" (`xo.lobby`); joiner:
  "Waiting for the host". Joiner has no End.
- AC8 — On a result: win → `sounds.play('complete')` on the winner's phone, `'wrong'` on the other; draw →
  `'correct'` on both. Header mute button (`xo.mute`, speaker icon, a11y label) toggles the shared mute. Call
  `sounds.load()` when XoScreen mounts. Audio errors never break the game.

## Copy (`camp.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| xo.next | Next game | Следующая игра | Keyingi o'yin |
| xo.game | Game {{n}} | Игра {{n}} | {{n}}-o'yin |
| xo.draws | Draws {{d}} | Ничьи: {{d}} | Durang: {{d}} |
| xo.waiting | Waiting for {{name}}… | Ждём {{name}}… | {{name}} kutilmoqda… |
| xo.end | End | Завершить | Tugatish |
| xo.endConfirm | End the series? | Завершить серию? | Seriyani tugatasizmi? |
| xo.keepPlaying | Keep playing | Играть дальше | Davom etish |
| xo.final | Final score | Итоговый счёт | Yakuniy hisob |
| xo.youWinSeries | You win the series {{a}}–{{b}} | Вы выиграли серию {{a}}–{{b}} | Seriyani siz yutdingiz {{a}}–{{b}} |
| xo.theyWinSeries | {{name}} wins the series {{a}}–{{b}} | {{name}} выигрывает серию {{a}}–{{b}} | {{name}} seriyani yutdi {{a}}–{{b}} |
| xo.tie | It's a tie {{a}}–{{b}} | Ничья {{a}}–{{b}} | Durang {{a}}–{{b}} |
| xo.finalStats | Draws {{d}} · Games {{n}} | Ничьи {{d}} · Игр {{n}} | Durang {{d}} · O'yinlar {{n}} |
| xo.mute / xo.unmute | Mute sounds / Turn sounds on | Выключить звук / Включить звук | Ovozni o'chirish / Ovozni yoqish |
Reuse existing keys for "Play again", "Lobby", "Waiting for the host" (Mafia game over) if present.

## testIDs · QA events
`xo.next` · `xo.game` · `xo.score.<seatId>` · `xo.draws` · `xo.paused` · `xo.mute` · `xo.end` · `xo.final` ·
`xo.play-again` · `xo.lobby` · `xo_next { gameNo }` · `xo_paused { paused }` · `camp_game_ended { game:'xo', games, draws }`

## Approved packages
none

## Done when
- [ ] tests: next swaps marks + X first + stale ignored; score/draws carry; pause on drop, moves ignored, resume
      same state; remove → ended; end → final lines (win/lose/tie); play again resets; sound clip per outcome +
      mute respected (sounds mocked); lessons tests still green after the move
- [ ] `npm run check` green (output in summary), committed on `feat/campfire-xo`, reply ≤ 10 lines
