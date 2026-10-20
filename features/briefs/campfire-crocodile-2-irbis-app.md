# Brief campfire-crocodile-2-irbis-app — timer, turn end, disconnect, end + summary

- Spec: features/campfire-crocodile.md · ACs in this slice: AC4, AC5, AC6, AC7
- Repo / branch: irbis-app · `feat/campfire-crocodile` (slice 1 committed on it)
- Depends on: brief campfire-crocodile-1-irbis-app (croc branch in gameReducer, protocol v5, CrocScreen, packs)

## Files
- New: `games/croc/CrocTimer.tsx` (ring + seconds, react-native-svg + Reanimated), `games/croc/CrocResult.tsx`,
  `games/croc/CrocSummary.tsx`, tests in `games/croc/__tests__/`.
- Edit: `games/gameReducer.ts` (croc: start, guessed, timeUp, cancel on describer drop/remove, end, playAgain,
  host-resume), `games/croc/CrocScreen.tsx`, host room/server (host-side timer that dispatches `timeUp`; route
  `crocGuessed`; `End` for croc), `join/playerClient.ts`, `src/shared/i18n/{en,ru,uz}/camp.json`.
- Read for patterns: Mafia `GameOver.tsx` (confetti, Play again / Lobby / "Waiting for the host"), XO-style host
  End confirm via `ConfirmSheet`, how seat drop/remove/reconnect reaches the reducer (Mafia / Imposter presence).

## Behaviour
- AC4 — `crocStart` (or the host describer tapping Start) → phase `running`, `public.remainingMs = durationSec*1000`
  stamped when broadcast. Every phone counts down locally from the received `remainingMs` (no clock sync); the
  host's timer is the only one that ends the turn (dispatches `timeUp` for the current `turnNo`). Ring + seconds
  (`croc.timer`) on all phones; last 10 s in the campTheme warning colour; light haptic on each of the last 5 s.
  Skip still allowed while running (new word, timer keeps going). Describer sees `croc.guessed` button (≥ 44 pt).
- AC5 — `crocGuessed` from the describer (stale `turnNo` ignored, and ignored once the turn ended) → phase
  `result { kind:'guessed', word }`, `totals.guessed`+1, success haptic on all phones; time-up → `result
  { kind:'timeUp', word }`, heavy haptic. `totals.turns`+1 in both. Result view (`croc.result`) shows title + word
  in the viewer's locale for ~3 s, then phase `pick` (host can also tap Next to go earlier — host only).
- AC6 — describer seat disconnects or is removed during `ready`/`running` → `result { kind:'cancelled', word }`
  with `croc.left` (word not counted, `turns` unchanged) → `pick`. Reconnected seat is pickable again. New seat
  joining mid-game: guesser, listed in pick. Host app restart: state restored from the saved room; a turn in
  `running` resumes in `ready` with the same describer and word (timer restarts on Start). Fewer than 3 connected:
  game continues.
- AC7 — host `croc.end` (any phase) → `ConfirmSheet` `croc.endConfirm` → phase `ended` on all phones:
  `CrocSummary` (`croc.summary`): `croc.over`, `croc.totals`, Mafia confetti. Host: `croc.play-again` (totals 0,
  same settings, turnNo 0, phase `pick`) and `croc.lobby` (existing back-to-lobby); others `croc.waitingHost`.

## Copy (`camp.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| croc.timeUp | Time's up! | Время вышло! | Vaqt tugadi! |
| croc.wordWas | The word: {{word}} | Слово: {{word}} | So'z: {{word}} |
| croc.left | {{name}} left — the word is not counted | {{name}} вышел(а) — слово не засчитано | {{name}} chiqib ketdi — so'z hisoblanmaydi |
| croc.next | Next | Дальше | Keyingisi |
| croc.end | End | Завершить | Tugatish |
| croc.endConfirm | End the game? | Завершить игру? | O'yinni tugatasizmi? |
| croc.over | Game over | Игра окончена | O'yin tugadi |
| croc.totals | Words guessed {{g}} · Skipped {{s}} · Turns {{t}} | Угадано {{g}} · Пропущено {{s}} · Ходов {{t}} | Topildi {{g}} · O'tkazildi {{s}} · Navbatlar {{t}} |
| croc.playAgain | Play again | Играть ещё | Yana o'ynash |
| croc.lobby | Lobby | Лобби | Lobbi |
| croc.waitingHost | Waiting for the host | Ждём ведущего | Boshlovchini kutyapmiz |

(Reuse existing keys for Play again / Lobby / Waiting for the host if they already exist in camp.json.)

## testIDs · QA events
`croc.timer` · `croc.guessed` · `croc.result` · `croc.next` · `croc.end` · `croc.summary` · `croc.play-again` ·
`croc.lobby` · `croc_start { turnNo, durationSec }` · `croc_turn_end { turnNo, kind }` ·
`camp_game_ended { game:'croc', guessed, skipped, turns }` — no words, no names.

## Approved packages
none

## Done when
- [ ] tests: start sets remainingMs; guessed and timeUp totals; stale turnNo / after-result guessed ignored;
      describer drop → cancelled, turns unchanged; host resume running → ready same word; end → ended totals;
      play again resets; CrocSummary host vs. guest buttons; timer warning colour under 10 s (fake timers)
- [ ] `npm run check` green (output in summary), committed on `feat/campfire-crocodile`, reply ≤ 10 lines
