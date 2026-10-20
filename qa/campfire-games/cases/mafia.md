# Mafia — test cases (campfire-mafia AC1–AC6 + campfire-core multi-player)

Players: **A** = emulator-5554 host (app UI driven by testID), **B** = emulator-5556 real joiner, **bots** =
`scripts/qa/campbot.py` (synthetic names bot_1…). Bots log every received message to JSONL, which is how privacy
is checked. AC7 (APK server) and AC8 (launcher icon) are build/tooling ACs, covered by MAF-20/21 only lightly.
"manual" = purely visual, judged on the screenshot.

| id | title | AC | players | steps | expected |
|---|---|---|---|---|---|
| MAF-01 | Mafia tile live in hub and picker | AC1 | A | Open CampHub; tap Host → Continue; in lobby look at game picker | `camp.hub.game.mafia` has no "Coming soon"; `camp.lobby.game.mafia` selectable |
| MAF-02 | Setup header counts players excluding host | AC1 | A + B + 4 bots | Select Mafia in lobby | "Choose roles" · "5 players" (A not counted) |
| MAF-03 | 11 role rows, civilian auto-fills | AC1 | A + 5 bots | Inspect rows; + Detective / − Doctor; read Civilian count | 11 rows (Boss, Mafia, Detective, Doctor, Maniac, Lover, Bodyguard, Sniper, Journalist, Immortal, Civilian); Civilian has no stepper and = n − specials, live |
| MAF-04 | Defaults for n=5 and n=9 | AC1 | A + 5 bots, then 9 | Fresh setup (no remembered setup) read counts | Boss 1, Mafia max(0, floor(n/3)−1) (n=5→0, n=9→2), Detective 1, Doctor 1, others 0 |
| MAF-05 | Balance hint | AC1 | A + 6 bots | Vary mafia team m; read `maf.balance` | n=6: lo=1, hi=2: m=0..→"town heavy" only below 1, m=1–2 "balanced", m=3 "mafia heavy"; never blocks Deal (when m≥1) |
| MAF-06 | Deal blocked: fewer than 5 | AC1 | A + 4 bots | Select Mafia | Deal disabled, reason "Needs 5+ players besides the host" |
| MAF-07 | Deal blocked: no mafia | AC1 | A + 5 bots | Set Boss 0, Mafia 0 | Deal disabled, "Add at least 1 mafia" |
| MAF-08 | Deal blocked: too many roles | AC1 | A + 5 bots | Raise specials to 6 (if steppers allow) | Deal disabled "Too many roles" or + capped at n; never more specials than n |
| MAF-09 | Last setup remembered | AC1 | A + 5 bots | Change counts + toggle reveal off, deal, end, back to setup | Same counts and toggle restored |
| MAF-10 | Deal: one role per seat, private | AC2 | A + B + 5 bots | Deal; read every bot's `deal` | Each bot gets exactly one `deal` with its own roleId; no bot log contains another seat's role before `ended`; host gets no card; role counts match setup |
| MAF-11 | Role card + hold to reveal | AC3 | A + B + 5 bots | On B: read card texts, hold `maf.card` (screenshot during hold) | "MAFIA · n PLAYERS", "Seat k · <nick>", "Your role is ready", hold → "YOU ARE THE", role, "TEAM …", 3 lines; screenshot blocked (FLAG_SECURE) — manual |
| MAF-12 | I'm ready count | AC3 | A + B + 5 bots | Bots send `mafReady` one by one; B taps `maf.ready`; double-tap; stale round | "I'm ready · r / n" increments per seat; double tap/duplicate counts once; stale round ignored; host shows Ready tick |
| MAF-13 | Host narrator list + alive line | AC4 | A + 5 bots | After deal, read `maf.host` | Each player row: avatar, nickname, role chip, "alive"; "Alive a / n · Mafia x · Town y · Solo z"; phase "Night 1" |
| MAF-14 | Killed at night / exiled by day / back | AC4, AC5 | A + B + 5 bots | Tap B row → Killed; next phase → Day 1; tap bot → Exiled; tap B → Back in game | Sheet shows only the phase-right action; status "killed · Night 1" / "exiled · Day 1"; B sees out banner "You're out — …"; Back removes it; bots' `game.out` updates |
| MAF-15 | Night/Day stepping | AC4, AC5 | A + B + 5 bots | Tap `maf.phase-next` 3× | Night 1 → Day 1 → Night 2 → Day 2 on host and B header; "<alive> / <n> alive" |
| MAF-16 | Reveal role when out on/off | AC1, AC5 | A + B + 5 bots | Deal with reveal on, kill a bot; repeat with reveal off | On: `out[].roleId` present + role chip on B Out list; off: no roleId in any bot log |
| MAF-17 | Win suggestion order | AC6 | A + 5 bots (Boss, Maniac, Det, Doc, Civ) | Kill so maniac alive and alive ≤ 2 (with mafia also ≥ non-mafia) | Host gets "Maniac wins?" (maniac first), not Mafia |
| MAF-18 | Town win + Keep playing / End without winner | AC6 | A + 5 bots | Kill all mafia → "Town wins?" → Keep playing; End game with no match | Keep playing closes sheet; End without match → "End without a winner?" → "Game over" |
| MAF-19 | Game over lists all roles + Play again | AC6 | A + B + 5 bots | End with a winner | Every phone "GAME OVER · <phase>", "<Team> wins!", "<s> players survived", all roles; players "Waiting for the host"; Play again → new deal, round+1 |
| MAF-20 | Join mid-game | AC2, core AC6 | A + 5 bots + bot_new / B | Deal, then new bot hello / B joins by code | New seat gets "Game in progress — you're in the next one" (`camp.game.in-progress`), no `deal` |
| MAF-21 | Drop + reconnect keeps role | AC2, core AC7 | A + 5 bots | bot_1 mute (no ping) 12 s → host shows reconnecting; reconnect with seatToken | Same seatId, same roleId re-sent; no new seat |
| MAF-22 | Host removes a player mid-game | AC2, core AC6 | A + 5 bots | Long-press bot in lobby/host list → Remove | Bot gets `removed`; counts as out, reason exiled |
| MAF-23 | Host End game → everyone to lobby | AC2 | A + B + 5 bots | `camp.game.end` → confirm | All receive `lobby`; B back in player lobby |
| MAF-24 | Host app killed and resumed | AC2, core AC7 | A + 5 bots | Deal, `am force-stop`, reopen → Resume room | Same code, game state restored, bots reconnect with tokens and get same role |
| MAF-25 | Old protocol rejected | AC2 (protocol), core AC5 | bot | Send hello with v 4 / v 3 | `rejected { reason: version }` |
| MAF-26 | Too many players (16th seat) | core AC6 | A + 14 bots + bot_15 | Fill to 15 incl host, add one more | 16th gets `rejected full` |
