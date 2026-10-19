# Brief campfire-mafia-1-irbis-app — setup, deal, protocol v3

- Spec: features/campfire-mafia.md · ACs in this slice: AC1, AC2
- Repo / branch: irbis-app · `feat/campfire-mafia` (create from `feat/campfire-party`; slices stack on it)
- Depends on: campfire-party (gameReducer, deal/game messages, SecretCard, lobby picker)
- Also read: features/briefs/campfire-mafia-roles-copy.md (role table + all role copy — add it all in this slice)

## Files
- New: `src/features/campfire-core/games/mafia/roles.ts` (role table: id, team, colour, glyph; `defaultCounts(n)`,
  `civilians(counts,n)`, `balance(counts,n)`, `dealRoles(counts, seatIds, rng)`), `mafia/RoleGlyph.tsx` (11 glyphs),
  `mafia/MafiaSetup.tsx`, `mafia/__tests__/`.
- Edit: `games/gameReducer.ts` (new `mafia` game branch), protocol constants + message types (`PROTOCOL_VERSION`
  2 → 3, `mafReady`), lobby game picker + CampHub tile (Mafia selectable), host room persistence, `camp.json` ×3.
- Read for patterns: campfire-party code in `games/` (how Imposter deals + settings are stored), `campTheme.ts`,
  existing campfire-core tests that assert protocol version (follow the v2 bump precedent — editing their expected
  version 2 → 3 is part of this spec; list each edited test in the summary).
- Find things with `graphify explain/query` in irbis-app first.

## Behaviour
- AC1 — Setup screen (host, after picking Mafia in the lobby): header "Mafia · host setup" / "Choose roles" /
  "<n> players" where n = connected seats **excluding the host**. 11 rows in table order: glyph tile (role colour),
  name, team chip, desc, − / + stepper (0..n) with count; Civilian has no stepper, shows n − specials (min 0).
  Summary `maf.summary` with balance word and `maf.teamCounts`. Balance: m = boss + mafia; lo = max(1, floor(n/4)),
  hi = max(1, floor(n/3)); m < lo → townHeavy, m > hi → mafiaHeavy, else balanced (hint only). Toggle
  `maf.revealOut` + sub (default on). "Deal roles" disabled with first matching reason: n < 5 needPlayers;
  specials > n tooMany; m = 0 needMafia. Defaults for a fresh host: boss 1, mafia max(0, floor(n/3) − 1),
  detective 1, doctor 1, others 0. Last counts + toggle saved in MMKV `camp.maf.setup` and reused (clamped to n).
  Mafia tile/picker loses "Coming soon"; the room range for Mafia is 6–15 connected seats incl. host.
- AC2 — Deal: build the role list (specials + civilians), Fisher–Yates over non-host seats with an injectable rng;
  each seat gets `deal { game:'mafia', round, secret:{ roleId } }` only to itself; host gets none. `game.public`:
  `{ phase:{kind:'night',n:1}, readyCount:0, playerCount:n, out:[], revealOut }`. Reconnect → same deal. A new seat
  mid-game gets `maf.inProgress` and plays next game. Removed seat → added to `out` with reason exiled in the
  current phase. End game (existing confirm) → lobby. v2 phone → existing "Update Irbis to join this room".
  Until slice 2, players/host land on the existing `GameWaiting` after the deal.

## Copy (`camp.json`, add) — plus every key in campfire-mafia-roles-copy.md
| key | en | ru | uz |
|---|---|---|---|
| maf.setupTitle | Mafia · host setup | Мафия · настройка ведущего | Mafiya · boshlovchi sozlamasi |
| maf.chooseRoles | Choose roles | Выберите роли | Rollarni tanlang |
| maf.players | {{n}} players | Игроков: {{n}} | {{n}} o'yinchi |
| maf.summary | {{total}} / {{n}} roles · {{balance}} | Ролей {{total}} / {{n}} · {{balance}} | {{total}} / {{n}} rol · {{balance}} |
| maf.balanced | balanced | баланс | muvozanatli |
| maf.townHeavy | town heavy | перевес города | shahar ustun |
| maf.mafiaHeavy | mafia heavy | перевес мафии | mafiya ustun |
| maf.teamCounts | Town {{town}} · Mafia {{mafia}} · Solo {{solo}} | Город {{town}} · Мафия {{mafia}} · Одиночка {{solo}} | Shahar {{town}} · Mafiya {{mafia}} · Yakka {{solo}} |
| maf.revealOut | Reveal role when out | Показывать роль выбывших | Chiqqanning rolini ko'rsatish |
| maf.revealOutSub | Off makes the game harder | Если выключить, играть сложнее | O'chirilsa, o'yin qiyinroq |
| maf.deal | Deal roles | Раздать роли | Rollarni tarqatish |
| maf.needPlayers | Needs 5+ players besides the host | Нужно 5+ игроков кроме ведущего | Boshlovchidan tashqari 5+ o'yinchi kerak |
| maf.tooMany | Too many roles | Слишком много ролей | Rollar juda ko'p |
| maf.needMafia | Add at least 1 mafia | Добавьте хотя бы 1 мафию | Kamida 1 ta mafiya qo'shing |
| maf.inProgress | Game in progress — you're in the next one | Идёт игра — вы в следующей | O'yin ketmoqda — keyingisida qatnashasiz |

## Glyphs (24×24 viewBox, fill)
crown `M3 18h18l-1.5-10-4.5 4-3-6-3 6-4.5-4zM3 20h18v2H3z` · hat `M7 4h10v9H7zM2 13h20v3H2z` · glass
`M10 3a7 7 0 1 1 0 14 7 7 0 0 1 0-14zm0 3a4 4 0 1 0 0 8 4 4 0 0 0 0-8zM15 15l2-2 5 5-2 2z` · cross
`M9 3h6v6h6v6h-6v6H9v-6H3V9h6z` · moon `M14 3a9 9 0 1 0 7 13A7 7 0 0 1 14 3z` · heart `M12 21s-8-5.2-8-11a4.5 4.5 0
0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 5.8-8 11-8 11z` · shield `M12 2l8 3v6.2c0 5-3.4 9-8 10.8-4.6-1.8-8-5.8-8-10.8V5z` ·
person `M12 3a4.5 4.5 0 1 1 0 9 4.5 4.5 0 0 1 0-9zM4 21c.6-4.4 3.8-6.5 8-6.5s7.4 2.1 8 6.5z` · crosshair, notepad,
infinity: draw simple shapes in the same style (placeholders).

## testIDs · QA events
`camp.lobby.game.mafia` · `maf.setup` · `maf.role.<id>.minus|plus|count` · `maf.balance` · `maf.reveal-out` ·
`maf.deal` · `camp_game_started { game:'mafia', players }` · `maf_dealt { players, mafia, town, solo }`

## Approved packages
none

## Done when
- [ ] tests: civilians/balance/defaults/disabled reasons; deal gives each role exactly once, host no deal, only own
      seat receives it; reconnect same role; mid-game join waits; protocol 3 rejects v2; setup persisted
- [ ] `npm run check` green (output in summary), committed on `feat/campfire-mafia`, reply ≤ 10 lines
