# Campfire games QA run, 2026-10-20 23:05 to 2026-10-21 00:10

- **Build 1 (Mafia + Crocodile + art):** throwaway local branch `qa/campfire-games` = `feat/campfire-crocodile`
  `d3a398e` + merge of `fix/campfire-art` `e1b1346` (clean merge, commit `8b8c930`, branch deleted after the run).
  Protocol v5. `assembleDevRelease -PreactNativeArchitectures=arm64-v8a` (arm64 only so it fits the emulator; no source change).
- **Build 2 (X and O):** `feat/campfire-xo` `76654d4`, protocol v4, same build command.
- **Devices:** A = `emulator-5554` host, B = `emulator-5556` real joiner. Both are pixel-8a (Android 15) started with
  `-read-only`. The `Medium_Phone_API_35` AVD was below Android's low-storage threshold (411 MB free) and refused the install.
  App language English (Profile → Language). Bots: `scripts/qa/campbot.py` on the Mac through
  `adb forward tcp:47821`, with a logging relay (`logs/relay.log`) between the Mac port and the forward.
- **Hosting worked on the emulator:** local-only hotspot "Hotspot on" (`AndroidShare_xxxx`). B found the room through its
  subnet scan (10.0.2.2 → Mac → forward → A).
- Evidence: `proof/*.jpg` (downscaled, 2 MB) and full-size `shots/*.png` (16 MB) stay on this Mac only, because
  `qa/.gitignore` keeps media out of git. Bot logs are in
  `bots/s1` (Mafia/Crocodile) and `bots/xo`, and `bots/privacy_s1.txt` holds the privacy check
  (`scripts/qa/campleak.py`). Logcat is in `logs/`. Seat tokens are redacted.

## Results

| Game | Cases | Pass | Fail | Blocked | Not run |
|---|---|---|---|---|---|
| Mafia | 26 | 24 | 1 | 0 | 1 |
| Crocodile | 22 | 19 | 1 | 1 | 1 |
| X and O | 19 | 18 | 1 | 0 | 0 |
| **Total** | **67** | **61** | **3** | **1** | **2** |

Bugs: CORE-1, CORE-2, CORE-3, MAF-1, MAF-2, XO-1 (see `../../BUG-REPORT.md`).

### Mafia
| id | verdict | note / evidence |
|---|---|---|
| MAF-01 | Pass | Hub tile "Mafia, 6–15 · 20–40 min" with no Coming soon; picker selectable (`core_hub_A`) |
| MAF-02 | Pass | 6 seats → "5 players" (`maf_setup_5`) |
| MAF-03 | Pass | 11 rows; Civilian has no stepper and = n − specials, live |
| MAF-04 | Pass (n=5) | n=4/5: Boss 1, Mafia 0, Det 1, Doc 1. n=9 not run: the remembered setup overrides the defaults |
| MAF-05 | Pass | n=5: m=1 balanced, m=2 mafia heavy, m=0 town heavy; n=6: m=1,2 balanced, m=3 mafia heavy |
| MAF-06 | Pass | 4 players: Deal disabled "Needs 5+ players besides the host" (`maf06_setup_4players`) |
| MAF-07 | Pass | "Add at least 1 mafia" (`maf07_no_mafia`) |
| MAF-08 | Pass | "6 / 5 roles", "Too many roles" (`maf08_too_many`) |
| MAF-09 | Pass | Counts remembered after game, lobby and host restart |
| MAF-10 | Pass | 6 deals, one per bot, counts match setup; host has no card; `privacy_s1.txt` no leaks |
| MAF-11 | Pass | All card texts present; hold reveals role + 3 lines; window flag `SECURE` (`maf11_card_B`) |
| MAF-12 | Pass | 1/6 → duplicate mafReady still 1 → stale round 99 ignored → B double tap → 2/6 "Ready" disabled |
| MAF-13 | Pass | "Alive 6 / 6 · Mafia 2 · Town 4 · Solo 0", Night 1, role chips (`maf13_host`) |
| MAF-14 | Pass | Night sheet only "Killed at night"; day only "Exiled by day"; out player only "Back in game"; B banner + removal |
| MAF-15 | Pass | Night 1 → Day 1 → Night 2 → Day 2 on host button and B header |
| MAF-16 | Pass | Reveal on: `roleId` in `out` + chip; off: no `roleId` in any bot log (`maf16_out_noreveal_B`) |
| MAF-17 | Pass | Alive = Maniac + Boss → "Maniac wins?" (not Mafia). Mafia 2 vs Town 2 → `maf_win_suggested mafia` |
| MAF-18 | Pass | "Town wins?" → Keep playing closes; End with no match → "End without a winner?" → "Game over" |
| MAF-19 | Pass | "GAME OVER · Night 2", "Town wins!", "4 players survived", all roles; B "Waiting for the host"; Play again → round 2, new deal |
| MAF-20 | Pass | Mid-game bot gets `game` and no `deal`; UI "Game in progress — you're in the next one" seen on B (XO build, `xo13_in_progress_B`) |
| MAF-21 | Pass | Silent drop 13 s, then reconnect with token → same seat p4, same role re-sent |
| MAF-22 | **Fail** | Leave counts as out "exiled" (OK), but row shows "exiled · Day 1" during Night 1 and has no nickname → MAF-1, MAF-2. Host remove mid-game: no path from the game screen |
| MAF-23 | Pass | Game over → Lobby → all bots got `lobby`; B back in player lobby |
| MAF-24 | Pass | force-stop host → "Resume room 6841" → game restored (phase, out list); bots and B rejoin same seats/roles |
| MAF-25 | Pass | hello v3 / v4 → `rejected version` (on this host; see CORE-3 for a lost rejection) |
| MAF-26 | Not run here | Covered on the same core by CROC-05 (16th seat → `rejected full`) |

### Crocodile
| id | verdict | note / evidence |
|---|---|---|
| CROC-01 | Pass | Hub "Crocodile, 3–15 · mime", picker pill (`croc01_hub_B`); glyph visual: manual |
| CROC-02 | Pass | 60 s selected, 3 packs ticked (`croc02_settings`) |
| CROC-03 | Pass | The last ticked pack can't be unticked |
| CROC-04 | Pass | 2 players: "Crocodile needs 3+ players" (`croc04_two_players`) |
| CROC-05 | Pass | 15/15 seated; 16th → `rejected full` |
| CROC-06 | Pass | Host "Who shows next?" lists all 5 incl. host; B "The host is choosing who shows" |
| CROC-07 | Pass | Only the describer receives `deal croc`; others see "bot_1 is showing"; no word in public before result |
| CROC-08 | Pass | B card: word "Snow leopard", "Animals", rule, Skip, Start (`croc08_card_B`) |
| CROC-09 | Pass | Skip in ready and while running → new word, skipped +1; the clock keeps running |
| CROC-10 | Pass | 30 s: `running` remainingMs 29998 → `result timeUp` at +30.1 s, turns +1, back to pick at +33 s |
| CROC-11 | Pass | B "Guessed!" → all phones "Guessed! · The word: Amir Timur", guessed +1, turns +1 |
| CROC-12 | Pass | Skip/Start/Guessed from a non-describer, stale turnNo, wrong round, double Guessed: all ignored |
| CROC-13 | Pass | Host picks itself → card + Start/Guessed on host |
| CROC-14 | Pass | Leave mid-turn → "bot_3 left — the word is not counted"; silent drop → cancelled; reconnect → pickable |
| CROC-15 | Pass | Mid-game bot joins and appears in the pick list |
| CROC-16 | Not run | Never dropped below 3 connected during a game |
| CROC-17 | Blocked | Host removal is only in the lobby; no path from the game screen |
| CROC-18 | Pass | "End the game?" → "Game over · Words guessed 2 · Skipped 203 · Turns 3" on A and B; Play again → totals 0, pick |
| CROC-19 | Pass | 200 skips: no word repeats until each pack's remaining words ran out (57/58/57 left after earlier turns) |
| CROC-20 | Pass | force-stop during running → Resume → phase `ready`, same describer; B recovers on its own |
| CROC-21 | Pass | hello v4 → `rejected version` |
| CROC-22 | **Fail** | B by code: "Room found" → Join → "Room not found" (4/4) and crash (4×) → CORE-1, CORE-2. Works when Join is tapped 30 s after found |

### X and O
| id | verdict | note / evidence |
|---|---|---|
| XO-01 | Pass | Hub "X and O, 2 · 1–5 min", picker pill |
| XO-02 | Pass | 1 and 3 seats: Start disabled "X and O is for 2 players"; 2 seats enabled |
| XO-03 | Pass | Game 1 host X, X first, "Your turn" / "host_1's turn" (`xo03_start_A`) |
| XO-04 | Pass | Out-of-turn move (bot) and out-of-turn tap (host and B) ignored |
| XO-05 | Pass | Taken cell ignored |
| XO-06 | Pass | Move after result and move with an old gameNo ignored |
| XO-07 | Pass | All 8 lines detected with the right `line`; "You win!" / "guest_1 wins!" + line drawn (`xo17_*`) |
| XO-08 | Pass | Draw board xoxxoooxx → "Draw", Draws 1 |
| XO-09 | Pass | X/O swap every game incl. after the draw; X first; "Game n"; Next from host UI, bot and B |
| XO-10 | Pass | Second xoNext ignored |
| XO-11 | Pass | Score bar avatar, nickname, mark, wins, "Draws d" |
| XO-12 | Pass | Joiner silent → "Waiting for bot_1…", cells disabled; reconnect → same board, turn, score |
| XO-13 | Pass | B as third phone → "Game in progress — you're in the next one" |
| XO-14 | Pass (via leave) | Joiner leaving ends the series → host Final score. Host remove: no path from the game screen |
| XO-15 | Pass | "End the series?" → both phones "Final score", "It's a tie 0–0 / You win the series 5–4", "Draws d · Games n"; joiner "Waiting for the host", no End |
| XO-16 | Pass | force-stop → Resume → Game 11, score 5–4, Draws 1, board kept |
| XO-17 | **Fail** | Two-phone play works, but joiner Back strands B in the lobby → XO-1 |
| XO-18 | Pass | Mute label toggles "Mute sounds" / "Turn sounds on" (sound itself: manual) |
| XO-19 | Pass | hello v5 / v3 on the v4 host → `rejected version` (sometimes lost, CORE-3) |

### Other observations (not filed as bugs)
- XO "Play again" with 3 seats in the room goes back to the lobby instead of starting (spec silent).
- In every game the host can reach seat removal only from the lobby; the game screens have only End. So "host
  removes a player mid-game" (Mafia AC2, Crocodile AC6, XO AC6) can only happen as a player leaving.
- The host narrator list in Mafia shows no "reconnecting" state for a dropped seat (not required by AC4).
- Core AC8 battery banner: emulated 15 %/unplugged fired `camp_battery_low {pct:15}`, but the emulator's SystemUI
  crashed (`com.google.android.flipendo`) and the host app left the lobby, so the banner was not captured (rig issue).
