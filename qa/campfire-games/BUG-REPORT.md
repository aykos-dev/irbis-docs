# Campfire games: bug report (Android emulator pass, 2026-10-20)

**Summary:** I tested build 1, Mafia + Crocodile + art (`feat/campfire-crocodile` `d3a398e` + `fix/campfire-art`
`e1b1346`, protocol v5), and build 2, X and O (`feat/campfire-xo` `76654d4`, protocol v4). Devices were 2 × pixel-8a
emulators (Android 15): A as host and B as a real joiner, plus up to 17 Python bot players. I ran **67 cases: 61
pass, 3 fail, 1 blocked, 2 not run**, and found **6 bugs: 0 blocker, 4 major, 2 minor**. The details are in
`runs/2026-10-20_2305/run.md`. Evidence paths below are relative to that run folder. Screenshots (`proof/`,
`shots/`) are on the QA Mac only (`qa/.gitignore`). The logs are committed.

The core bugs (CORE-*) belong to the shared Campfire join/room layer, so they affect every game.

**Fix status (2026-10-21): all 6 fixed.** The shared fixes (CORE-1..3, MAF-1..2 and the shared XO-1 lobby/Back
guard) are in irbis-app `fix/campfire-bugs` (from `feat/campfire-crocodile`) `e4ab3a3`, cherry-picked to
`fix/campfire-bugs-xo` (from `feat/campfire-xo`) `07396bd`; the XO regression test is `9213400` on the same branch.
`npm run check` is green on both branches (72 suites, 354 tests on `fix/campfire-bugs-xo`). Nothing is pushed.

---

## CORE-1: Joining by code fails with "Room not found" right after the room was found
- **Severity:** major
- **Game + AC:** all games; campfire-core AC5 (Join by code)
- **Preconditions:** A is hosting a room. Bonjour/NSD does not find the room, so B falls back to the /24 subnet scan.
  On the emulators NSD never crosses devices, so this was always the case. On real phones it happens whenever NSD is
  blocked or slow.
- **Reproduce:**
  1. Host a room on phone A and note the code.
  2. On phone B: Community → Campfire games → Join → Continue → type the code.
  3. Wait for the card "Connected to "<network>" · Room found · N players waiting".
  4. Tap "Join as <nickname>" within about 10 s of the card appearing.
- **Actual:** after about 2–4 s B shows "Room not found. Join the host's Wi-Fi first, then try again."
  (`camp_join_failed {reason: not_found}`). The host never receives the `hello`: the relay log shows only the probe
  connection, with no join connection. After "Room found", B's logcat shows probe sockets 23–30 still failing with
  `NoRouteToHostException`, each taking about 1 s on two native threads.
- **Expected:** core AC5: "Found → card … + button "Join as <nickname>"", and tapping it seats the player.
- **Evidence:** `proof/core_join_error_B.jpg`, `logs/core_join_B_logcat.txt`, `logs/relay.log` (23:12:35 attempt:
  probe only).
- **Reproducibility:** 4/4 when tapped within 12 s. 4/4 succeeded when Join was tapped 30 s after the card appeared.
- **Status:** fixed in `fix/campfire-bugs` `e4ab3a3` / `fix/campfire-bugs-xo` `07396bd` (native `connectTimeout`
  on probes, first join attempt waits 15 s, reconnects 4 s).
- **Possible area:** `join/discovery.ts` `scanSubnet` stops starting new probes but leaves up to `SCAN_PARALLEL` (32)
  native connects queued. `join/playerClient.ts` `connect()` gives up after `RETRY_INTERVAL_MS` (2 s), before its own
  connect reaches a free native thread. The tcp-socket native executor looks like it has 2 threads (from logcat).

## CORE-2: Joiner app crashes with `IllegalArgumentException: No socket with id N`
- **Severity:** major (app crash)
- **Game + AC:** all games; campfire-core AC5 / AC7
- **Preconditions:** a join attempt failed as in CORE-1.
- **Reproduce:**
  1. Do CORE-1 steps 1–4 so B shows "Room not found".
  2. Either wait about 10 s, or tap "Try again" on B.
- **Actual:** the Irbis app on B closes to the home screen. Crash buffer:
  `FATAL EXCEPTION: pool-5-thread-1 … java.lang.IllegalArgumentException: No socket with id 32 at
  com.asterinet.react.tcpsocket.TcpSocketModule.getTcpClient`. It was also seen once with id 75, on a re-join right
  after the host removed B.
- **Expected:** core AC5: the failure states show an error "with retry where it makes sense". The app must not crash.
- **Evidence:** `logs/core_crash_B_1.txt`, `logs/core_crash_B_2.txt`, `logs/core_crash_B_3.txt`,
  `proof/core_join_found_B.jpg` (home screen after the crash).
- **Reproducibility:** 4 crashes in 6 failed-join sequences.
- **Status:** fixed in `fix/campfire-bugs` `e4ab3a3` / `fix/campfire-bugs-xo` `07396bd` (new `connectCamp` helper
  destroys only after the native connect attempt has settled).
- **Possible area:** a JS `destroy()` / `write()` on a socket the native side already dropped (the join socket that
  timed out in CORE-1). The native module throws on its executor thread, which kills the process.

## CORE-3: The last message before the host hangs up is often lost (`removed`, `rejected`), so a removed player silently rejoins
- **Severity:** major
- **Game + AC:** all games; campfire-core AC6 (remove → "The host removed you from the room"), AC5 (`version` / `full`
  messages)
- **Preconditions:** A is hosting with B (or a bot) in the lobby.
- **Reproduce:**
  1. On A, long-press B's avatar in the lobby → "Remove guest_1?" → Remove.
  2. Watch B for 15 s.
- **Actual:** in 1 of 2 tries, B never showed "The host removed you from the room". About 2 s later B appeared in the
  host lobby again as a **new seat** (p2 → p9, `camp_player_joined {rejoin: false}`), because its auto-retry ran
  with the freed seat token. A bot that was removed received no `removed` line at all; the socket just closed. A
  plain TCP check showed the same for `rejected version`: the host closed without sending it in 3/10 tries straight
  through `adb forward` and 6/10 through the relay. A phone that hits this would show "Room not found" instead of
  "Update Irbis to join this room". `closed` (Close room) reached all 3 bots.
- **Expected:** core AC6: "removed player sees "The host removed you from the room" and returns to CampHub". Core
  AC5: `version` → "Update Irbis to join this room".
- **Evidence:** `proof/core_removed_B_2s.jpg` (B back in the lobby as a new seat after removal),
  `bots/s1/bot_4.jsonl` (no `removed` before `closed`), `logs/relay.log` (removal at t=1792521344: the host
  connection closes with no data), `proof/core_removed_B_try2.jpg` (try 2: B went to CampHub).
- **Reproducibility:** `removed` lost 2/3 (B 1/2, bot 1/1). `rejected` lost 3/10 direct, 6/10 via relay. **Please
  confirm on two real phones:** part of this could come from the emulator `adb forward` path.
- **Status:** fixed in `fix/campfire-bugs` `e4ab3a3` / `fix/campfire-bugs-xo` `07396bd` (last messages flush
  before hang-up; freed seat tokens are tombstoned so a retry gets `removed`, never a new seat).
- **Possible area:** `room/hostServer.ts`: `freed()` / the `rejected` path call `send(conn, …)` and then `hangUp(conn)`
  right away. A `destroy()` straight after `write()` can drop unflushed data. Ending the socket after the write
  flushes (`end()`), or a short delay, would keep it. Also, the client keeps retrying with a token the host has freed.

## MAF-1: A player who leaves or is removed at night shows "exiled · Day n"
- **Severity:** minor
- **Game + AC:** Mafia AC2 ("Removed player leaves the game (counts as out, reason exiled)"), AC4/AC5 fate labels
- **Preconditions:** a Mafia game in a Night phase (for example Night 1 right after Deal).
- **Reproduce:**
  1. Deal roles with 6+ players. The game is at "Night 1".
  2. A player leaves the room (Leave, or the host removes them).
  3. Look at the host's player list, the players' "Out" list and the game-over list.
- **Actual:** the row reads "exiled · **Day 1**" while the game is at Night 1. The protocol says
  `{reason: exiled, phase: {kind: night, n: 1}}`.
- **Expected:** a fate that matches the phase it happened in. AC4 formats are "killed · Night n" / "exiled · Day n".
  For an exit at night either "· Night 1" or a distinct "left · Night 1".
- **Evidence:** `proof/maf22_exiled_night_label_A.jpg`, `proof/maf22_left_row_A_r2.jpg`,
  `proof/maf22_left_out_B_r2.jpg`, `bots/s1/bot_1.jsonl` (`out` entry with `kind: night`).
- **Reproducibility:** 2/2
- **Status:** fixed in `fix/campfire-bugs` `e4ab3a3` / `fix/campfire-bugs-xo` `07396bd` (a night exit renders
  `left · Night n`; day exits stay `exiled · Day n`).
- **Possible area:** `games/mafia/OutList.tsx` `fateLabel()` picks the copy from `reason` only, so "exiled" always
  renders as "Day {n}".

## MAF-2: A player who left has no nickname or avatar on the host list, the Out list and game over
- **Severity:** minor
- **Game + AC:** Mafia AC5 ("list "Out" with nickname"), AC6 ("Everyone's role" list: avatar, nickname, fate, role chip)
- **Preconditions:** as MAF-1.
- **Reproduce:**
  1. Deal roles with 6+ players.
  2. One player leaves (or is removed).
  3. Look at the host narrator list, B's "Out" list, then End game and look at "Everyone's role".
- **Actual:** the row has no avatar and no nickname, only "exiled · Day 1" and the role chip. On game over it reads
  "exiled · Day 1 · Mafia" with no name.
- **Expected:** AC5 / AC6 rows show the player's nickname (and avatar).
- **Evidence:** `proof/maf22_exiled_night_label_A.jpg`, `proof/maf22_left_out_B_r2.jpg`, `proof/maf18_over_none_A.jpg`.
- **Reproducibility:** 2/2 (fresh round and after host resume)
- **Status:** fixed in `fix/campfire-bugs` `e4ab3a3` / `fix/campfire-bugs-xo` `07396bd` (Mafia out entries keep an
  optional `player: { nickname, avatar }` snapshot; host list, Out list and game over fall back to it).
- **Possible area:** the rows look up nickname/avatar from the live roster, and a seat that leaves is removed from it.
  The game state could keep a name snapshot per dealt seat.

## XO-1: Joiner pressing Back during a series is stranded in the lobby and never sees the board or final score again
- **Severity:** major
- **Game + AC:** X and O AC2 ("3×3 board on both phones, same state"), AC7 ("both phones: Final score")
- **Preconditions:** A hosts, B has joined, "Start X and O" tapped. Both phones show the board.
- **Reproduce:**
  1. On A, tap any cell (or not; it doesn't matter).
  2. On B, press the Android Back button or gesture once.
  3. On A, keep playing or tap End → "End the series?" → End.
- **Actual:** B lands on the player lobby "Waiting for the host to start" and stays there. Its seat is still
  connected, so A keeps waiting for B's move. B can't get back to the board, and after A ends the series B still
  shows the lobby, not "Final score". Pressing Back again on B leaves the room.
- **Expected:** the board stays on both phones until the host ends it, then both phones show Final score (AC2, AC7).
  Back on the joiner should either be blocked, or ask to leave, or the lobby should return to the running game.
- **Evidence:** `proof/xo_back_B_lobby.jpg`, `proof/xo_back_B_retry.jpg`, `proof/xo_back_B_after_end.jpg`,
  `proof/xo_back_A_after_playagain.jpg`.
- **Reproducibility:** 2/2 (XO build). Not checked on Mafia or Crocodile, which share the player lobby. Likely the same.
- **Status:** fixed in `fix/campfire-bugs` `e4ab3a3` / `fix/campfire-bugs-xo` `07396bd` (player Back is blocked
  while a game runs; the player lobby re-enters a running game when refocused). XO regression test
  `xoJoin.test.tsx` on `fix/campfire-bugs-xo` `9213400`.
- **Possible area:** `screens/CampLobbyScreen.tsx` `PlayerLobby` navigates to `CampGame` in an effect only when
  `inGame` changes, so a lobby reached by Back while a game runs never navigates again. The game route has no
  Back guard for players (the host has one: the End sheet).

---

## Not tested / blocked
- **QR scan join and joining the hotspot Wi-Fi from the QR** (`react-native-wifi-reborn`): the emulator camera
  can't scan the host's QR. Only join by code was tested.
- **Bonjour/NSD discovery:** it doesn't work between two emulators, so only the subnet-scan path ran (see CORE-1).
- **iPhone host/guide and iOS joiners:** Android only.
- **Host removes a player mid-game** (Mafia AC2, Crocodile AC6, XO AC6): no UI path. Removal exists only in the lobby,
  so it was tested as a player leaving (CROC-17 blocked).
- **Crocodile: players fall below 3 mid-game** (CROC-16): not run.
- **Core AC8 battery banner:** blocked. The emulated low battery fired `camp_battery_low {pct:15}` but crashed the
  emulator's SystemUI and the host left the lobby (rig issue), so the banner was not captured.
- **Toast copy** "The host closed the room" / "The host removed you…": transient, not captured. The bots received
  `closed` (3/3).
- **Timers 60 / 90 s:** only 30 s was run.
- **Manual / sensory:** haptics, XO sounds (AC8 playback), confetti, timer last-10 s colour, placed-mark animation,
  tile glyphs and role art (screenshots in `proof/` for a visual check).
- **Mafia defaults for n = 9** (MAF-04): the remembered setup overrides the defaults, and resetting it needs an
  app-data wipe.
- **Mafia AC7 (APK server) and AC8 (launcher icon):** build tooling, not exercised.
- **XO "host drops → joiner reconnecting…"** was not run on XO. On Crocodile, B 3 s after a host force-stop still
  showed the running turn. A longer window was not observed.
