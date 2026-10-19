# campfire-mafia

- Status: Approved
- Surfaces: app only (no api, no web: the game runs on the host phone over the campfire-core room; no XP, no badges)
- Related ADRs: ADR-001 (guest-first: offline games need no account)
- Requirements: Product Overview § Campfire games (offline) · Screens: `design/canvas/MafSetup.dc.html` (setup),
  `MafRole.dc.html` (role card), `MafEnd.dc.html` (game over), `CampSpec.dc.html` (Secrets stay secret).
  `MafNight` and `MafDay` are **not** built (voting and night actions happen in person, owner brief).
- Builds on: `campfire-core` + `campfire-party` (irbis-app `feat/campfire-party`, not merged). Branch: irbis-app
  `feat/campfire-mafia` from `feat/campfire-party`.

## Goal
The host picks how many of each Mafia role to use; the app deals them at random, one secret role per phone
(hold to reveal). The host is the narrator: no role, sees every role, marks who is killed or exiled and steps
night/day. The app spots a win and shows everyone's role at game over. Talking and voting stay around the fire.
Also: `npm run android:apk` builds a release APK and serves it to phones on the same Wi-Fi via a QR code, and the
app gets its real launcher icon.

## Local protocol changes (no API)
- `PROTOCOL_VERSION` 2 → **3** (a v2 phone gets "Update Irbis to join this room").
- Host → one seat only: `deal { game: 'mafia', round, secret: { roleId } }`. Host gets no deal.
- Host → all: `game { game: 'mafia', round, phase, public }` — `phase` `{ kind: night|day, n }`, `readyCount`,
  `playerCount`, `out: [{ seatId, reason: killed|exiled, phase, roleId? }]` (`roleId` only when "Reveal role when
  out" is on), `ended?: { winner: town|mafia|maniac|none, roles: [{ seatId, roleId }] }`.
- Client → host: `mafReady { round }`.
- State in the pure `gameReducer` (new `mafia` branch) on the host; saved with the host room (resume 12 h).

## Data model changes
None on the server. App MMKV: `camp.maf.setup` (last role counts + reveal toggle, host phone).

## Acceptance criteria
- **AC1** — **Setup (MafSetup):** Mafia tile in CampHub and the lobby picker drops "Coming soon". Host setup:
  header "Choose roles" · "<n> players" (n = connected seats **excluding the host**), 11 role rows (icon, name,
  team chip, one-line description, − / + stepper 0–n): Mafia Boss (mafia), Mafia (mafia), Detective, Doctor,
  Maniac (solo), Lover, Bodyguard, Sniper, Journalist, Immortal (town), Civilian (town, **no stepper**: Civilian =
  n − specials, live). Summary "<total> / <n> roles · <balance>" and "● Town x ● Mafia y ● Solo z". Balance (hint
  only, never blocks): mafia team (Boss + Mafia) `m`, `lo = max(1, floor(n/4))`, `hi = max(1, floor(n/3))`:
  m < lo "town heavy", m > hi "mafia heavy", else "balanced". Toggle "Reveal role when out" (default on). "Deal
  roles" disabled with reason: n < 5 "Needs 5+ players besides the host"; specials > n "Too many roles"; m = 0
  "Add at least 1 mafia". Defaults: Boss 1, Mafia max(0, floor(n/3) − 1), Detective 1, Doctor 1, rest 0; the last
  setup is remembered on the host phone. No narrator or discussion-timer settings.
- **AC2** — **Deal + seats:** "Deal roles" shuffles the role list over the non-host seats (uniform random), each
  phone gets only its own `deal`. Reconnect → same role. New seat during a game → "Game in progress — you're in the
  next one". Removed player leaves the game (counts as out, reason exiled). Host "End game" → confirm → all phones
  to the lobby. Protocol v3.
- **AC3** — **Role card (MafRole, players):** header "MAFIA · <n> PLAYERS", "Seat <k> · <nickname>", "Your role is
  ready", "Hold the card to look. Make sure nobody can see your screen." Hold-to-reveal `SecretCard` (+ screen
  protection from campfire-party AC3): "YOU ARE THE", role name, "TEAM <TOWN|MAFIA|SOLO>", 3 lines (night, day,
  how you win) per role. Button "I'm ready · r / n" → once tapped shows "Ready" (r counts players who tapped).
  The card stays available for the whole game.
- **AC4** — **Host control (narrator):** host sees no card; list of all players: avatar, nickname, role chip
  (colour + name), status "alive" / "killed · Night n" / "exiled · Day n", "Ready" tick until the first phase step.
  Line "Alive a / n · Mafia x · Town y · Solo z" (alive counts). Phase starts at "Night 1"; button "Start Day <n>"
  / "Start Night <n+1>". Tap a player → sheet: "Killed at night" (in a night phase) or "Exiled by day" (in a day
  phase), "Back in game" for an out player (undo). End game button.
- **AC5** — **Players during the game:** header shows the phase ("Night 2" / "Day 2") and "<alive> / <n> alive";
  list "Out" with nickname + "killed · Night n" / "exiled · Day n" + role chip when reveal is on. When this phone
  is marked out: banner "You're out — <fate>. Stay quiet, no hints!" + heavy haptic; "Back in game" removes it.
- **AC6** — **Win + game over (MafEnd):** after every out change the host phone checks, in order: maniac alive and
  alive ≤ 2 → Maniac; no mafia and no maniac alive → Town; alive mafia ≥ alive non-mafia → Mafia. On a match the
  host gets "<Team> wins?" with "End game" / "Keep playing". Host "End game" without a match → "End without a
  winner?" (winner none). Every phone shows: "GAME OVER · <phase>", "Town wins!" / "Mafia wins!" / "Maniac wins!"
  / "Game over", sub-line "<s> players survived", "Everyone's role" list (avatar, nickname, fate, role chip; out
  rows at 60 %), small confetti on a win. No XP or badge rows. Host: "Lobby" and "Play again" (same setup, new
  random deal, round + 1); players see "Waiting for the host".
- **AC7** — **APK over Wi-Fi:** `npm run android:apk` = `node scripts/serve-apk.js release` → `./gradlew
  assembleDevRelease` (`debug` arg → `assembleDevDebug`; `--no-build` serves the last APK), then an HTTP server on
  0.0.0.0:8787 (next free port if taken) serves `/` (a tiny page with a download button, app name, version, size,
  build time) and `/irbis.apk` (`application/vnd.android.package-archive`). Prints the LAN IPv4 URL (first
  non-internal interface, `--host <ip>` override) + a terminal QR code; Ctrl+C stops it. Fails clearly when the
  build fails or no LAN address is found.
- **AC8** — **App icon:** launcher icon from `irbis-icon.svg` (canvas `68fc129c…`): Android `mipmap-*`
  `ic_launcher.png` + `ic_launcher_round.png` (48/72/96/144/192 px), adaptive icon (`mipmap-anydpi-v26`,
  foreground = Irbis + ridge on the teal tile colour as background); iOS `AppIcon.appiconset` (all sizes, 1024
  marketing). Flavour names stay "Irbis Dev" / "Irbis Staging" / "Irbis".

### QA events (app, dev/staging builds)
`camp_game_started { game: 'mafia', players }` · `maf_dealt { players, mafia, town, solo }` · `maf_ready { ready,
players }` · `maf_phase { kind, n }` · `maf_out { reason, phase }` · `maf_back { }` · `maf_win_suggested { winner }`
· `camp_game_ended { game: 'mafia', rounds, winner }` — counts only, no nicknames or roles per seat.

### testIDs (app)
`camp.lobby.game.mafia` · `maf.setup` · `maf.role.<roleId>.minus|plus|count` · `maf.balance` · `maf.reveal-out` ·
`maf.deal` · `maf.card` · `maf.ready` · `maf.host` · `maf.player.<seatId>` · `maf.sheet.killed|exiled|back` ·
`maf.phase-next` · `maf.end` · `maf.out-banner` · `maf.win-sheet` · `maf.over` · `maf.play-again` · `maf.lobby`

### Required UI states
- [ ] Loading (waiting for the deal / first `game` message)
- [ ] Empty (Deal disabled with reason; joined mid-game → next game)
- [ ] Error (host lost → existing reconnecting state; room closed → CampHub)
- [ ] Offline: works with no internet; no OfflineBanner on campfire screens
- [ ] Keyboard: none; safe areas; haptics (reveal, out, win); press states
- [ ] Dark campfire theme (`campTheme`) + design tokens + shared components only

## Media
`design/media/campfire-mafia/MEDIA.md`: 8 canvas role glyphs + colours final; Sniper / Journalist / Immortal glyphs
and colours are placeholders (Q8, STATUS known issue); app icon final.

## Waivers
- Phone-to-phone play is not unit-testable end to end: tests cover the `mafia` reducer (deal, reconnect, out/back,
  phases, win checks), setup counting/balance, and the screens with the room mocked; the owner tests on phones.
- `scripts/serve-apk.js` is a dev tool: tested by hand (owner); a unit test covers LAN-address pick + port fallback
  only if it stays small.
- iOS icon set generated but iOS never built (same as campfire-core).

## Out of scope
- Night actions in the app, night task for everyone, day vote, timers, narrator voice (MafNight, MafDay boards).
- Mafia members seeing each other on the card (they meet on Night 1 in person).
- XP, badges (Life Saver etc.), pass-and-play; custom roles; play store signing / prod APK.

## Assumptions
- Q1 (owner, 2026-10-19): host is the narrator — no role, sees all roles; players = seats except the host (5–14).
- Q2 (owner, 2026-10-19): roles = canvas 8 + Sniper, Journalist, Immortal.
- Q3 (owner, 2026-10-19): Civilians auto-fill; Deal blocked only by too many roles / no mafia / < 5 players; balance is a hint.
- Q4 (owner, 2026-10-19): host marks killed/exiled (undo), steps Night/Day, app suggests a win, host confirms;
  "Reveal role when out" shows the role to all; Play again re-deals.
- Q5 (owner, 2026-10-19): APK = devRelease (.env.dev, debug key, "Irbis Dev").
- Q6 (owner, 2026-10-19): `qrcode-terminal` approved as a devDependency.
- Q7 (owner, 2026-10-19): app icon from canvas asset `68fc129c…` (Android + iOS), generated with macOS tools.
- Q8 (owner, 2026-10-19): Sniper / Journalist / Immortal glyphs drawn in canvas style as placeholders.
- No XP / badges (owner brief). Voting and talking in person (owner brief).
- Code in `irbis-app/src/features/campfire-core/games/mafia/` (same reason as campfire-party) (main session).
- Balance thresholds lo/hi and default counts are main-session guesses — change in one constant (main session).

## Open questions
- none
