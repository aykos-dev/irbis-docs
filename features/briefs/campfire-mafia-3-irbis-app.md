# Brief campfire-mafia-3-irbis-app — win check + game over

- Spec: features/campfire-mafia.md · ACs in this slice: AC6
- Repo / branch: irbis-app · `feat/campfire-mafia`
- Depends on: campfire-mafia-2 (MafiaScreen, out/back, phases)

## Files
- New: `games/mafia/winCheck.ts` (pure), `mafia/WinSheet.tsx`, `mafia/GameOver.tsx` (+ small confetti), tests.
- Edit: `games/gameReducer.ts` (mafia `end { winner }`, `playAgain`), `MafiaScreen.tsx`, `camp.json` ×3.
- Read for patterns: `mafia/HostControl.tsx`, `games/components/SeatAvatar.tsx`, campfire-party round restart code.

## Behaviour
- AC6 — `winCheck(roles, out)` after every markOut / markBack on the host, in order:
  1. maniac alive and alive ≤ 2 → `maniac`; 2. no boss/mafia and no maniac alive → `town`;
  3. alive (boss+mafia) ≥ alive others → `mafia`; else null.
  On a non-null result (and not already dismissed for this exact out-set) host gets WinSheet `maf.winQ.<team>` with
  `maf.endGame` (→ end with that winner) / `maf.keepPlaying` (dismiss). Host End game with no match → confirm
  `maf.endNoWinner` → winner `none`. End → `game.public.ended = { winner, roles: all seats' roleIds }` (the only
  time players get others' roles). Every phone (host too) shows GameOver (MafEnd): `maf.overLine` with the phase
  label, `maf.win.<winner>`, `maf.survived` (alive count), `maf.everyone` list: avatar, nickname (+ " (you)"
  for own via existing copy if present), fate (`maf.alive`/`maf.killed`/`maf.exiled`), role chip; out rows opacity
  0.6. Confetti (a few coloured rects, Reanimated, ≤ 1.5 s) only when winner ≠ none; heavy haptic on show. No XP or
  badge rows. Host buttons `maf.lobby` (back to lobby, existing flow) and `maf.playAgain` (same counts + reveal
  setting, new deal over the currently connected non-host seats, round + 1; re-check the AC1 disabled reasons,
  if they fail go to setup instead). Players see `maf.waitHost`.

## Copy (`camp.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| maf.winQ.town | Town wins? | Победа города? | Shahar yutdimi? |
| maf.winQ.mafia | Mafia wins? | Победа мафии? | Mafiya yutdimi? |
| maf.winQ.maniac | Maniac wins? | Победа маньяка? | Manyak yutdimi? |
| maf.endGame | End game | Завершить игру | O'yinni tugatish |
| maf.keepPlaying | Keep playing | Продолжить | Davom etish |
| maf.endNoWinner | End without a winner? | Завершить без победителя? | G'olibsiz tugatilsinmi? |
| maf.overLine | GAME OVER · {{phase}} | ИГРА ОКОНЧЕНА · {{phase}} | O'YIN TUGADI · {{phase}} |
| maf.win.town | Town wins! | Город победил! | Shahar yutdi! |
| maf.win.mafia | Mafia wins! | Мафия победила! | Mafiya yutdi! |
| maf.win.maniac | Maniac wins! | Маньяк победил! | Manyak yutdi! |
| maf.win.none | Game over | Игра окончена | O'yin tugadi |
| maf.survived | {{s}} players survived | Выжило игроков: {{s}} | {{s}} o'yinchi omon qoldi |
| maf.everyone | Everyone's role | Роли всех игроков | Hammaning roli |
| maf.lobby | Lobby | Лобби | Lobbi |
| maf.playAgain | Play again | Сыграть ещё | Yana o'ynash |
| maf.waitHost | Waiting for the host | Ждём ведущего | Boshlovchi kutilmoqda |

## testIDs · QA events
`maf.win-sheet` · `maf.over` · `maf.play-again` · `maf.lobby` · `maf_win_suggested { winner }` ·
`camp_game_ended { game:'mafia', rounds, winner }`

## Approved packages
none

## Done when
- [ ] tests: winCheck table (each rule + order + null), keep playing doesn't re-ask for same out-set, end without
      winner, ended payload reaches players with all roles, play again re-deals and round + 1
- [ ] `npm run check` green (output in summary), committed on `feat/campfire-mafia`, reply ≤ 10 lines
