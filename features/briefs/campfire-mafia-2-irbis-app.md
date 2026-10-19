# Brief campfire-mafia-2-irbis-app — role card, narrator control, player view

- Spec: features/campfire-mafia.md · ACs in this slice: AC3, AC4, AC5
- Repo / branch: irbis-app · `feat/campfire-mafia`
- Depends on: campfire-mafia-1 (roles.ts, RoleGlyph, mafia reducer, deal, copy)

## Files
- New: `games/mafia/MafiaScreen.tsx` (host vs player body), `mafia/RoleCard.tsx`, `mafia/HostControl.tsx`,
  `mafia/PlayerSheet.tsx` (host action sheet), `mafia/OutList.tsx`, tests.
- Edit: `games/gameReducer.ts` (mafia actions: ready, phaseNext, markOut, markBack), game route (Mafia body replaces
  `GameWaiting`), `camp.json` ×3.
- Read for patterns: `games/components/SecretCard.tsx`, `useSecureScreen.ts`, `games/components/SeatAvatar.tsx`,
  `imposter/ImposterScreen.tsx` (host bar, haptics), `campTheme.ts`.

## Behaviour
- AC3 — Player (non-host) role screen (MafRole): `maf.cardHeader`, `maf.seat` (seat number + own nickname),
  `maf.roleReady`, `maf.readyHint`. `SecretCard` covered/hold; revealed: `maf.youAre`, role name (role colour,
  glyph), `maf.teamLine` with team word, then 3 lines: `maf.role.<id>.night`, `maf.team.<team>.day`,
  `maf.team.<team>.win`. `useSecureScreen()` on. Button `maf.imReady` (r = readyCount, n = playerCount) → sends
  `mafReady { round }` once → shows `maf.readyDone`. Card stays on screen for the whole game.
- AC4 — Host screen (no card): title `maf.narrator`, phase label (`maf.night`/`maf.day`), line `maf.hostLine` with
  alive counts by team. List of all players: SeatAvatar, nickname, role chip (colour + name), status `maf.alive` /
  `maf.killed` / `maf.exiled`, `maf.readyTick` badge while phase is Night 1. Tap → sheet: in a night phase
  `maf.markKilled`, in a day phase `maf.markExiled`; for an out player only `maf.markBack`. Phase button: night n →
  `maf.startDay` (n), day n → `maf.startNight` (n+1). Existing End game button stays.
  Reducer: markOut adds `{seatId, reason, phase, roleId if revealOut}`; markBack removes it.
- AC5 — Player header: phase label + `maf.aliveLine`; `maf.outTitle` list of out players: avatar, nickname, fate
  (`maf.killed`/`maf.exiled`), role chip if `roleId` present. Own seat out → banner `maf.youreOut` with fate +
  heavy haptic (once per transition); removed on Back.

## Copy (`camp.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| maf.cardHeader | MAFIA · {{n}} PLAYERS | МАФИЯ · ИГРОКОВ: {{n}} | MAFIYA · {{n}} O'YINCHI |
| maf.seat | Seat {{k}} · {{name}} | Место {{k}} · {{name}} | {{k}}-o'rin · {{name}} |
| maf.roleReady | Your role is ready | Ваша роль готова | Rolingiz tayyor |
| maf.readyHint | Hold the card to look. Make sure nobody can see your screen. | Удерживайте карту, чтобы посмотреть. Убедитесь, что никто не видит экран. | Ko'rish uchun kartani bosib turing. Ekraningizni hech kim ko'rmayotganiga ishonch hosil qiling. |
| maf.youAre | YOU ARE THE | ВАША РОЛЬ | SIZNING ROLINGIZ |
| maf.teamLine | TEAM {{team}} | КОМАНДА: {{team}} | JAMOA: {{team}} |
| maf.imReady | I'm ready · {{r}} / {{n}} | Я готов · {{r}} / {{n}} | Tayyorman · {{r}} / {{n}} |
| maf.readyDone | Ready · {{r}} / {{n}} | Готово · {{r}} / {{n}} | Tayyor · {{r}} / {{n}} |
| maf.narrator | Mafia · narrator | Мафия · ведущий | Mafiya · boshlovchi |
| maf.night | Night {{n}} | Ночь {{n}} | {{n}}-tun |
| maf.day | Day {{n}} | День {{n}} | {{n}}-kun |
| maf.hostLine | Alive {{a}} / {{n}} · Mafia {{mafia}} · Town {{town}} · Solo {{solo}} | В игре {{a}} / {{n}} · Мафия {{mafia}} · Город {{town}} · Одиночка {{solo}} | Tirik {{a}} / {{n}} · Mafiya {{mafia}} · Shahar {{town}} · Yakka {{solo}} |
| maf.aliveLine | {{a}} / {{n}} alive | В игре: {{a}} / {{n}} | {{a}} / {{n}} tirik |
| maf.alive | alive | в игре | tirik |
| maf.killed | killed · Night {{n}} | убит(а) · ночь {{n}} | o'ldirildi · {{n}}-tun |
| maf.exiled | exiled · Day {{n}} | изгнан(а) · день {{n}} | quvildi · {{n}}-kun |
| maf.outTitle | Out | Выбыли | Chiqqanlar |
| maf.youreOut | You're out — {{fate}}. Stay quiet, no hints! | Вы выбыли — {{fate}}. Молчите, без подсказок! | Siz chiqdingiz — {{fate}}. Jim turing, ishora bermang! |
| maf.readyTick | Ready | Готов | Tayyor |
| maf.markKilled | Killed at night | Убит(а) ночью | Tunda o'ldirildi |
| maf.markExiled | Exiled by day | Изгнан(а) днём | Kunduzi quvildi |
| maf.markBack | Back in game | Вернуть в игру | O'yinga qaytarish |
| maf.startDay | Start Day {{n}} | Начать день {{n}} | {{n}}-kunni boshlash |
| maf.startNight | Start Night {{n}} | Начать ночь {{n}} | {{n}}-tunni boshlash |

## testIDs · QA events
`maf.card` · `maf.ready` · `maf.host` · `maf.player.<seatId>` · `maf.sheet.killed|exiled|back` · `maf.phase-next` ·
`maf.end` · `maf.out-banner` · `maf_ready { ready, players }` · `maf_phase { kind, n }` · `maf_out { reason, phase }`
· `maf_back {}`

## Approved packages
none

## Done when
- [ ] tests: card lines per role/team, ready count + single send, host sees roles / players don't receive others'
      roles, sheet options by phase, out/back reducer, phase stepping, revealOut off hides roleId, own-out banner
- [ ] `npm run check` green (output in summary), committed on `feat/campfire-mafia`, reply ≤ 10 lines
