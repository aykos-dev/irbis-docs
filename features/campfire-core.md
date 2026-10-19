# campfire-core

- Status: Done
- Surfaces: app (no api, no web: play is phone-to-phone over a local network; XP and badges come with `campfire-party`)
- Related ADRs: ADR-001 (guest-first: offline games need no account)
- Requirements: Product Overview § Campfire games (offline) · Screens: `design/canvas/CampSpec.dc.html`,
  `CampHub.dc.html` (C1), `CampLobby.dc.html` (C2), `CampJoin.dc.html` (C3); entry: `FeedSpec` point 4 + `Groups`
  (Community = Feed · Groups · Campfire games); canvas notes `n_c_join`
- Branch: irbis-app `feat/campfire-core` from `main` (conditions + levels fast-forwarded into main 2026-10-19, Q9)

## Goal
From the Community tab a group can open Campfire games, one phone hosts a room (its own hotspot on Android, Personal
Hotspot or any shared Wi-Fi on iPhone), everyone else joins by scanning one QR or typing a 4-digit room code, and the
lobby shows every player live, survives drops and a host restart. The games themselves come in `campfire-party` /
`campfire-mafia`; here they are visible but "Coming soon".

## Local protocol (no API)
- Transport: host runs a TCP server on port **47821** (`react-native-tcp-socket`); messages are newline-delimited
  JSON `{ v: 1, type, ... }`. Client → host: `hello { code, nickname, avatar, seatToken? }`, `ping`, `leave`.
  Host → client: `welcome { seatId, seatToken, room }`, `roster { players[] }`, `rejected { reason: full |
  wrong_code | version }`, `removed`, `closed`, `pong`. Other `v` → `rejected version`.
- Liveness: ping every 3 s; no traffic for 10 s = disconnected (seat kept, status `reconnecting`).
- QR payload: `irbis-camp://join?v=1&code=4821&ip=<host ip>&port=47821[&ssid=..&pw=..]` (Wi-Fi fields only when
  the app created the hotspot, i.e. Android).
- Discovery by code: Bonjour/NSD service `_irbiscamp._tcp` with TXT `code=4821` (`react-native-zeroconf`) for 3 s;
  if not found, scan the phone's /24 subnet on port 47821 (parallel connects, 400 ms timeout) asking for the code.
- Room engine is a pure reducer (`roomReducer`) on the host; the socket layer only feeds it events.

## Data model changes
None on the server. App MMKV keys: `camp.profile` (nickname, avatar), `camp.hostRoom` (code, seats, savedAt),
`camp.seats.<code>` (seatToken per joined room).

## Acceptance criteria
- **AC1** — Community tab shows a segmented control **Feed · Groups · Campfire games**; Feed and Groups show the
  shared Coming soon state; Campfire games is the default segment while the other two are coming soon. CampHub is
  dark in light and dark mode (night-friendly, CampSpec).
- **AC2** — CampHub shows header "Campfire games" + "Works offline" chip, hero "No internet. No problem." / "Just
  connect to one hotspot and play together.", **Host** and **Join** buttons, the 4 game tiles (Imposter 3–15 · 5–10
  min, Mafia 6–15 · 20–40 min, Who am I? 3–12 · 10–20 min, Would you rather 2–15 · endless), "Play with your trip
  group" card and "Campfire badges" card. Game tiles, trip-group card and badges card carry a "Coming soon" tag;
  tapping one shows the toast "Coming in the next update". Works offline and as a guest.
- **AC3** — Host or Join first opens the **player sheet**: nickname 2–16 characters after trim (error "2–16
  characters"), prefilled with the last nickname, else the signed-in username, else empty; pick one of 6 animals
  (fox, ibex, bear, marmot, eagle, panda; default the last pick, else fox). Saved to MMKV on Continue.
- **AC4** — **Host, Android:** the app starts a local-only hotspot (in-repo native module; asks Nearby Wi-Fi devices
  on Android 13+, location below 13), starts the server and opens the lobby: "You're the host" · "Campfire room" ·
  "Hotspot on" chip, QR, room code (4 random digits), hotspot name and "Wi-Fi password in the QR". Permission denied
  or hotspot failure → if the phone is on Wi-Fi, host on that network ("Hosting on <Wi-Fi name>"), else error
  "Couldn't start the hotspot" + Try again. **Host, iPhone:** a guide sheet "Turn on Personal Hotspot" with 3
  numbered steps and "It's on"; the server then starts on the hotspot / current Wi-Fi address and the QR carries
  room + address only, with the line "Players join your Wi-Fi in Settings first". iOS asks Local Network once.
- **AC5** — **Join** (CampJoin): camera QR scanner ("Point at the QR code on the host's phone"), or 4-digit code
  entry. Scan → join the Wi-Fi in the QR if present (`react-native-wifi-reborn`), then connect. Code → discovery
  (protocol above). Found → card "Connected to "<network>"" · "Room found · N players waiting" + button "Join as
  <nickname>". Failures: not found in 8 s → "Room not found. Join the host's Wi-Fi first, then try again."; `full`
  → "This room is full (15 / 15)"; `version` → "Update Irbis to join this room"; camera denied → code entry stays
  usable + "Allow camera" (opens settings). Always shown: "Not seeing it? Open Wi-Fi settings and join the host's
  hotspot first."
- **AC6** — **Lobby roster** (host and players see the same list, updates within 1 s): max **15 including the
  host** ("8 / 15"); host first with ★ and orange ring; each player shows animal + nickname + "waiting" or
  "reconnecting…"; header "All connected" or "<n> reconnecting". Duplicate nickname gets " 2", " 3". Host can
  long-press a player → "Remove <name>?" → removed player sees "The host removed you from the room" and returns to
  CampHub. Host sees the game picker (Imposter, Mafia, Who am I, Rather) with "Coming soon" and a disabled Start
  button + "Games arrive in the next update"; players see "Waiting for the host to start".
- **AC7** — **Reconnect + resume:** a dropped player's seat stays (`reconnecting…`) until the host removes it or
  the room ends. The player app retries every 2 s while on the lobby and on app foreground, and rejoins the same
  seat via its stored `seatToken` (also after an app restart, by scanning or typing the same code). The host room
  (code, seats) is saved on every change; reopening Campfire within **12 h** shows "Resume room <code>" on CampHub,
  which restores the lobby with the same code and all players `reconnecting…` (Android: a new hotspot and QR).
  Host back / "Close room" → confirm "Close the room for everyone?" → players see "The host closed the room" →
  CampHub; saved room cleared.
- **AC8** — **Host battery:** while the host phone is at ≤ 20% and not charging, the lobby shows the banner
  "Battery <n>% — plug in so the room doesn't stop" (`react-native-device-info`); it hides when charging or above
  20%.

### QA events (app, dev/staging builds)
`camp_room_hosted { mode: hotspot|wifi }` · `camp_room_resumed { seats }` · `camp_room_closed { seats }` ·
`camp_player_joined { seats, rejoin }` · `camp_player_removed` · `camp_join_failed { reason: not_found|full|version|wifi|camera_denied }`
· `camp_battery_low { pct }` — counts only, no nicknames.

### testIDs (app)
`community.segment.feed|groups|campfire` · `camp.hub.screen` · `camp.hub.host` · `camp.hub.join` ·
`camp.hub.resume` · `camp.hub.game.<imposter|mafia|whoami|rather>` · `camp.hub.trip-group` · `camp.hub.badges` ·
`camp.player.nickname` · `camp.player.avatar.<animal>` · `camp.player.continue` · `camp.lobby.screen` ·
`camp.lobby.qr` · `camp.lobby.code` · `camp.lobby.count` · `camp.lobby.player.<seatId>` · `camp.lobby.start` ·
`camp.lobby.close` · `camp.lobby.battery` · `camp.ios-guide.done` · `camp.join.screen` · `camp.join.code` ·
`camp.join.found` · `camp.join.submit` · `camp.join.error`

### Required UI states
- [ ] Loading (starting hotspot, searching for room, connecting)
- [ ] Empty (lobby with only the host: "Waiting for players…")
- [ ] Error (hotspot failed, room not found, full, version, removed, closed) with retry where it makes sense
- [ ] Offline: everything works with no internet (it is the point); no OfflineBanner on campfire screens
- [ ] Permissions denied: camera, nearby Wi-Fi/location (Android), Local Network (iOS) — each has a path forward
- [ ] Keyboard (nickname, code), safe areas, haptics on join/remove, press states
- [ ] Design tokens + shared components only

## Media
From `design/media/campfire-core/MEDIA.md`. Placeholders (Q10): fox cheering → neutral `companionFox`; iOS hotspot
guide picture → numbered text steps. Everything else exists.

## Waivers
- Real two-device networking is not unit-testable: tests cover `roomReducer`, the message codec, QR parse/build,
  discovery fallback order and the screens with mocked native modules; the owner tests on real phones.

## Out of scope
- Any game (Imposter, Who am I?, Would you rather → `campfire-party`; Mafia → `campfire-mafia`), pass-and-play,
  hold-to-reveal, screenshot blocking, campfire XP and badges, "Play with your trip group" (needs `trip-events`).
- Feed and Groups segments (their own features).

## Assumptions
- Q1 (owner, 2026-10-19): coming soon = Feed + Groups segments, the 4 game tiles, trip-group card, badges card, game
  picker / Start in the lobby. Host / Join / lobby / reconnect fully work.
- Q2 (owner, 2026-10-19): packages approved: react-native-tcp-socket, react-native-vision-camera,
  react-native-qrcode-svg, react-native-wifi-reborn.
- Q3 (owner, 2026-10-19): every player types a nickname (prefilled), no login needed.
- Q4 (owner, 2026-10-19): in core: reconnect keeps seat, host battery warn 20%, Android hotspot by the app, host
  restart resumes.
- Q5 (owner, 2026-10-19): react-native-device-info approved for battery.
- Q6 (owner, 2026-10-19): code discovery "best and easiest, a package is fine" → Bonjour/NSD via
  react-native-zeroconf (no Apple multicast entitlement needed, unlike UDP broadcast) + /24 subnet scan fallback
  (Android local-only hotspots often drop mDNS). If zeroconf does not build on New Arch, the agent reports it and
  ships subnet scan only.
- Q7 (owner, 2026-10-19): nickname 2–16 chars, pick one of 6 animals, duplicate gets " 2".
- Q8 (owner, 2026-10-19): 15 including host; dropped seat kept until removed or room ends; host can remove; resume
  within 12 h; Close room ends it for everyone.
- Q9 (owner, 2026-10-19): merge conditions + levels into main first, branch from main.
- Q10 (owner, 2026-10-19): ship placeholders for the fox cheering pose and the iOS hotspot guide picture.
- Campfire is the default Community segment while Feed and Groups are coming soon (main session; canvas order kept).
- iOS cannot read its own Personal Hotspot password, so iPhone hosts' QR carries the room only (main session).

## Open questions
- none
