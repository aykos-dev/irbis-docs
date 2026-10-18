# Brief campfire-core-2-irbis-app — host: Android hotspot, room server, lobby, resume

- Spec: features/campfire-core.md (read § Local protocol) · ACs in this slice: AC4 (Android + Wi-Fi fallback), AC6
  (host side), AC7 (host side: save, resume, close)
- Repo / branch: irbis-app · `feat/campfire-core`
- Depends on: campfire-core-1 (CampHub, PlayerSheet, `CampLobby` stub route, `camp.json`)

## Files
- Touch (new unless noted) in `src/features/campfire-core/`: `protocol/codec.ts` (NDJSON encode/decode + zod
  schemas for every message, `v: 1`), `protocol/qr.ts` (build/parse `irbis-camp://join?...`), `room/roomReducer.ts`
  (pure: seats, join/rejoin by seatToken, duplicate-name suffix, cap 15 incl. host, disconnect → reconnecting,
  remove, close), `room/hostServer.ts` (tcp-socket server :47821 ↔ reducer, ping/timeout, broadcast roster),
  `room/hostRoomStore.ts` (MMKV `camp.hostRoom` save on every change, load if savedAt < 12 h), `native/campNet.ts`
  (typed JS wrapper of the native module), `screens/CampLobbyScreen.tsx` (replace stub), `components/PlayerAvatar.tsx`,
  `components/RoomQr.tsx`, `__tests__/` · CampHubScreen (edit: "Resume room <code>" button) · Android:
  `android/app/src/main/java/.../campnet/CampNetModule.kt` + `CampNetPackage.kt` (register in MainApplication),
  manifest permissions `CHANGE_WIFI_STATE`, `ACCESS_WIFI_STATE`, `NEARBY_WIFI_DEVICES` (`neverForLocation`, 33+),
  `ACCESS_FINE_LOCATION` (maxSdk 32) · `src/shared/storage` (key `camp.hostRoom`) · `camp.json` (add keys below)
- Read for patterns: `src/shared/utils/{qaLog,uuid,haptics}.ts`, `src/shared/hooks/useAppState.ts`, existing native
  module registration in `android/app/src/main/java/` (MainApplication), slice-1 components.

## Behaviour
- AC4 — Host tapped (after PlayerSheet): request the Android permission; `CampNet.startHotspot()` uses
  `WifiManager.startLocalOnlyHotspot` and resolves `{ ssid, password, ip }` (ip = IPv4 of the hotspot interface via
  `NetworkInterface`; SoftApConfiguration on API 30+, WifiConfiguration below). Denied/failed → if
  `CampNet.getWifiIp()` returns an address → host on Wi-Fi (chip `lobby.wifiChip` with the network name from NetInfo)
  else error state `lobby.hotspotError` + Try again. Then: random 4-digit code (1000–9999), start server, publish
  zeroconf `_irbiscamp._tcp` name `irbis-<code>` TXT `code`, open lobby. Lobby top: "You're the host" ·
  "Campfire room" · chip; QR card (white card, `react-native-qrcode-svg`, 200 px) "Scan to join Wi-Fi and room",
  code in 40 px 900 weight, hotspot name + "Wi-Fi password in the QR". `camp_room_hosted { mode }`.
- AC6 (host) — "Players · n / 15" + "All connected" | "<k> reconnecting"; grid of 64 px seats (host first, name + " ★",
  ring #FF9F1C; others ring #2B3B42; status line "waiting" / "reconnecting…" dimmed 50 %). Only host: empty →
  "Waiting for players…". 16th hello → `rejected full`; dup name → " 2", " 3". Long-press a non-host seat → confirm
  sheet "Remove <name>?" → send `removed`, close socket, free seat, haptic, `camp_player_removed`. Section "Game":
  4 pills (canvas `.gt`, selected Imposter border #7B61FF) each with "Coming soon" tag, tap → toast; Start button
  disabled + caption `lobby.startSoon`.
- AC7 (host) — reducer state saved after every change. CampHub shows `camp.hub.resume` when a saved room < 12 h:
  restores seats as reconnecting, same code, new hotspot/QR; player hellos with a known seatToken take their seat.
  Back or `camp.lobby.close` → confirm "Close the room for everyone?" → broadcast `closed`, stop server + hotspot +
  zeroconf, clear saved room, `camp_room_closed { seats }`, `camp_room_resumed { seats }` on resume.
- Keep the screen awake is NOT in scope. Stop everything on unmount/close; app background keeps the server.

## Copy (`camp.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| lobby.youHost | You're the host | Вы ведущий | Siz boshlovchisiz |
| lobby.room | Campfire room | Комната у костра | Gulxan xonasi |
| lobby.hotspotOn | Hotspot on | Точка доступа вкл. | Hotspot yoqilgan |
| lobby.wifiChip | Hosting on {{name}} | Через Wi-Fi {{name}} | {{name}} orqali |
| lobby.scan | Scan to join Wi-Fi and room | Сканируйте, чтобы войти в Wi-Fi и комнату | Wi-Fi va xonaga kirish uchun skanerlang |
| lobby.pwInQr | Wi-Fi password in the QR | Пароль Wi-Fi в QR-коде | Wi-Fi paroli QR kodda |
| lobby.players | Players · {{n}} / 15 | Игроки · {{n}} / 15 | O'yinchilar · {{n}} / 15 |
| lobby.allConnected | All connected | Все на связи | Hamma ulangan |
| lobby.reconnectingCount | {{k}} reconnecting | Переподключаются: {{k}} | {{k}} kishi qayta ulanmoqda |
| lobby.waiting / lobby.reconnecting | waiting / reconnecting… | ждёт / переподключается… | kutmoqda / qayta ulanmoqda… |
| lobby.empty | Waiting for players… | Ждём игроков… | O'yinchilar kutilmoqda… |
| lobby.game | Game | Игра | O'yin |
| lobby.gameRather | Rather | Выбор | Tanlov |
| lobby.start | Start | Начать | Boshlash |
| lobby.startSoon | Games arrive in the next update | Игры появятся в следующем обновлении | O'yinlar keyingi yangilanishda chiqadi |
| lobby.removeConfirm | Remove {{name}}? | Убрать {{name}}? | {{name}}ni chiqarasizmi? |
| lobby.remove / common.cancel | Remove / Cancel | Убрать / Отмена | Chiqarish / Bekor qilish |
| lobby.close | Close room | Закрыть комнату | Xonani yopish |
| lobby.closeConfirm | Close the room for everyone? | Закрыть комнату для всех? | Xona hamma uchun yopilsinmi? |
| lobby.hotspotError | Couldn't start the hotspot | Не удалось включить точку доступа | Hotspotni yoqib bo'lmadi |
| lobby.tryAgain | Try again | Повторить | Qayta urinish |
| hub.resume | Resume room {{code}} | Вернуться в комнату {{code}} | {{code}} xonasiga qaytish |
| lobby.permission | Allow nearby Wi-Fi devices to start the hotspot | Разрешите доступ к устройствам Wi-Fi поблизости | Yaqin Wi-Fi qurilmalariga ruxsat bering |

## testIDs · QA events
`camp.lobby.screen` · `camp.lobby.qr` · `camp.lobby.code` · `camp.lobby.count` · `camp.lobby.player.<seatId>` ·
`camp.lobby.start` · `camp.lobby.close` · `camp.hub.resume` · `camp_room_hosted` · `camp_room_resumed` ·
`camp_room_closed` · `camp_player_joined { seats, rejoin }` · `camp_player_removed` (counts only, no names)

## Approved packages
`react-native-tcp-socket`, `react-native-qrcode-svg`, `react-native-zeroconf` — latest that builds on RN 0.88 New
Arch (interop OK). If zeroconf doesn't build, drop it, say so in the summary (subnet scan in slice 3 covers it).

## Done when
- [ ] tests: reducer (cap 15, dup suffix, rejoin by token keeps seatId, disconnect → reconnecting, remove, close),
  codec (bad JSON / wrong `v` rejected), qr build/parse round trip, store (12 h expiry), lobby screen with mocked
  `campNet` + server (host card, remove confirm, close confirm, Start disabled), hub resume button
- [ ] `npm run check` green (output in summary), Android debug build compiles (`assembleDebug | tail -30`),
  committed, `graphify update .`
