# Brief campfire-core-3-irbis-app — join: QR scan, Wi-Fi join, code discovery, player lobby, reconnect

- Spec: features/campfire-core.md (read § Local protocol) · ACs in this slice: AC5, AC6 (player side), AC7 (player
  side: auto-retry, same seat, removed / closed)
- Repo / branch: irbis-app · `feat/campfire-core`
- Depends on: campfire-core-2 (codec, qr, reducer messages, `CampLobbyScreen`, `campNet`, zeroconf decision)

## Files
- Touch (new unless noted) in `src/features/campfire-core/`: `screens/CampJoinScreen.tsx` (replace stub),
  `join/discovery.ts` (zeroconf scan 3 s → subnet scan /24 :47821, 32 parallel, 400 ms timeout, ask `hello`-less
  `probe { code }` → host answers `probeOk { players, network }`; add `probe/probeOk` to codec), `join/playerClient.ts`
  (tcp client: hello with stored seatToken, ping 3 s, retry every 2 s while active + on app foreground, events),
  `join/seatStore.ts` (MMKV `camp.seats.<code>` = seatToken), `CampLobbyScreen.tsx` (edit: player mode), `__tests__/`
  · `room/hostServer.ts` (edit: answer probe) · iOS `Info.plist`: `NSCameraUsageDescription`,
  `NSLocalNetworkUsageDescription`, `NSBonjourServices` (`_irbiscamp._tcp`), Hotspot Configuration entitlement for
  wifi-reborn · Android: CAMERA permission · `camp.json` (add keys below)
- Read for patterns: slice-2 files, `src/shared/hooks/useAppState.ts`, `src/shared/components/TextField.tsx`,
  `CampJoin` canvas values below. Player IP for the subnet: `@react-native-community/netinfo` `details.ipAddress`
  (installed), or `campNet.getWifiIp()` on Android.

## Behaviour
- AC5 — CampJoin (dark): header "Join a game" + back; camera area 342×300 r20 with 4 orange corners (#FF9F1C, 44 px),
  caption `join.point`; Vision Camera `useCodeScanner(['qr'])`. Valid `irbis-camp://` QR → if `ssid` present and not
  already on it: `WifiManager.connectToProtectedSSID(ssid, pw, false, false)` (failure → `join.wifiFailed`,
  `camp_join_failed { reason: wifi }`), then connect to `ip:port`. Below: "or enter the room code" + 4 digit boxes
  (60 px, one hidden numeric TextField, auto-run discovery on 4th digit). Found → card (green check) `join.connected`
  + `join.roomFound` and primary button `join.as` (nickname from PlayerSheet). Errors in `camp.join.error`:
  not found after 8 s total, full, version, removed/closed; each with Try again. Camera denied → camera area shows
  `join.cameraDenied` + "Allow camera" (Linking.openSettings), code entry works. Footer hint `join.hint` always.
- AC6 (player) — after `welcome` open CampLobby in player mode: same roster grid live from `roster`; no QR, no
  game picker, no Start; text `lobby.waitHost`; Leave button → `leave` → CampHub.
- AC7 (player) — socket drop → banner `lobby.reconnectingSelf`, retry every 2 s + on foreground; reconnect uses the
  seatToken → same seatId (`camp_player_joined { rejoin: true }` on host). Rejoin also after app restart via QR/code
  (token read from `camp.seats.<code>`). `removed` → toast `join.removed` → CampHub, token deleted. `closed` →
  toast `join.closed` → CampHub, token deleted.

## Copy (`camp.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| join.title | Join a game | Войти в игру | O'yinga qo'shilish |
| join.point | Point at the QR code on the host's phone | Наведите на QR-код на телефоне ведущего | Boshlovchi telefonidagi QR kodga qarating |
| join.orCode | or enter the room code | или введите код комнаты | yoki xona kodini kiriting |
| join.searching | Looking for the room… | Ищем комнату… | Xona qidirilmoqda… |
| join.connected | Connected to "{{network}}" | Подключено к «{{network}}» | "{{network}}" ga ulandi |
| join.roomFound | Room found · {{n}} players waiting | Комната найдена · ждут игроков: {{n}} | Xona topildi · {{n}} o'yinchi kutmoqda |
| join.as | Join as {{name}} | Войти как {{name}} | {{name}} sifatida kirish |
| join.hint | Not seeing it? Open Wi-Fi settings and join the host's hotspot first. | Не находится? Откройте настройки Wi-Fi и подключитесь к точке доступа ведущего. | Topilmayaptimi? Wi-Fi sozlamalarini oching va avval boshlovchining hotspotiga ulaning. |
| join.notFound | Room not found. Join the host's Wi-Fi first, then try again. | Комната не найдена. Подключитесь к Wi-Fi ведущего и попробуйте снова. | Xona topilmadi. Avval boshlovchining Wi-Fi tarmog'iga ulaning va qayta urining. |
| join.full | This room is full (15 / 15) | Комната заполнена (15 / 15) | Xona to'la (15 / 15) |
| join.version | Update Irbis to join this room | Обновите Irbis, чтобы войти | Kirish uchun Irbisni yangilang |
| join.wifiFailed | Couldn't join the host's Wi-Fi. Join it in Settings. | Не удалось подключиться к Wi-Fi ведущего. Подключитесь в настройках. | Boshlovchi Wi-Fi tarmog'iga ulanib bo'lmadi. Sozlamalardan ulaning. |
| join.cameraDenied | Camera is off. You can still type the code. | Камера выключена. Можно ввести код. | Kamera o'chiq. Kodni kiritishingiz mumkin. |
| join.allowCamera | Allow camera | Разрешить камеру | Kameraga ruxsat berish |
| join.removed | The host removed you from the room | Ведущий убрал вас из комнаты | Boshlovchi sizni xonadan chiqardi |
| join.closed | The host closed the room | Ведущий закрыл комнату | Boshlovchi xonani yopdi |
| lobby.waitHost | Waiting for the host to start | Ждём, когда ведущий начнёт | Boshlovchi boshlashini kutyapmiz |
| lobby.reconnectingSelf | Reconnecting to the host… | Переподключаемся к ведущему… | Boshlovchiga qayta ulanmoqda… |
| lobby.leave | Leave | Выйти | Chiqish |

## testIDs · QA events
`camp.join.screen` · `camp.join.code` · `camp.join.found` · `camp.join.submit` · `camp.join.error` ·
`camp_join_failed { reason: not_found|full|version|wifi|camera_denied }`

## Approved packages
`react-native-vision-camera` (code scanner), `react-native-wifi-reborn` — latest that builds on RN 0.88 New Arch.
No Expo plugins; configure natively.

## Done when
- [ ] tests: discovery order (zeroconf hit skips scan; miss → subnet; 8 s → not_found), QR → wifi then connect,
  client rejoin sends stored token + retry on drop, removed/closed → hub + token cleared, join screen states
  (found card, each error, camera denied) with mocked native modules
- [ ] `npm run check` green (output in summary), `assembleDebug` compiles, committed, `graphify update .`
