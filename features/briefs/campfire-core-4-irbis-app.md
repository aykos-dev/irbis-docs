# Brief campfire-core-4-irbis-app — iPhone host guide + host battery warning

- Spec: features/campfire-core.md · ACs in this slice: AC4 (iPhone host), AC8
- Repo / branch: irbis-app · `feat/campfire-core`
- Depends on: campfire-core-2 and -3 (host flow, `campNet`, lobby)

## Files
- Touch: iOS native `ios/<app>/CampNet/CampNet.swift` + `.m` bridge (same JS name as Android `CampNet`):
  `getWifiIp()` / `getHotspotIp()` via `getifaddrs` (`bridge100` = Personal Hotspot, `en0` = Wi-Fi), returns
  `{ ip, iface }` or null; `startHotspot()` rejects `unsupported` on iOS · `src/features/campfire-core/native/campNet.ts`
  (edit: platform branch) · `components/IosHotspotGuide.tsx` (new sheet) · `hooks/useHostBattery.ts` (new) ·
  `CampLobbyScreen.tsx` (edit: battery banner; iOS host line) · CampHub host flow (edit: iOS → guide first) ·
  `__tests__/` · `camp.json` (add keys below)
- Read for patterns: slice-2 host flow + `campNet.ts`, `src/shared/components/{Sheet,OfflineBanner}.tsx` (banner look).

## Behaviour
- AC4 (iPhone) — Host on iOS opens `IosHotspotGuide` (placeholder: no picture, 3 numbered steps in tokens; tracked in
  STATUS): `guide.title`, steps 1–3, primary `guide.done`. Done → `getHotspotIp()` ?? `getWifiIp()`; none → sheet
  stays with `guide.notOn`. Then same server/zeroconf/lobby as Android; chip "Hotspot on" when iface is bridge100,
  else `lobby.wifiChip`. QR has `code, ip, port` only (no ssid/pw); under the code show `lobby.iosJoinFirst` instead
  of `lobby.pwInQr`. First server start triggers iOS Local Network prompt (no extra code; Info.plist key from slice 3).
- AC8 — `useHostBattery()` (host lobby only): `DeviceInfo.getPowerState()` on mount + `useBatteryLevel` /
  power-state listener; banner `camp.lobby.battery` visible while level ≤ 0.20 and state ≠ charging/full; text
  `lobby.battery` with rounded percent; hides when charging or > 20 %. `camp_battery_low { pct }` once per room when
  it first shows. Banner: warning colour from design.md, top of lobby under header, not dismissible.

## Copy (`camp.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| guide.title | Turn on Personal Hotspot | Включите режим модема | Shaxsiy hotspotni yoqing |
| guide.step1 | Open Settings → Personal Hotspot | Откройте Настройки → Режим модема | Sozlamalar → Shaxsiy hotspotni oching |
| guide.step2 | Switch on "Allow Others to Join" | Включите «Разрешать другим» | "Boshqalarga ruxsat berish"ni yoqing |
| guide.step3 | Come back to Irbis and tap "It's on" | Вернитесь в Irbis и нажмите «Включено» | Irbisga qayting va "Yoqildi"ni bosing |
| guide.done | It's on | Включено | Yoqildi |
| guide.notOn | We can't see the hotspot or Wi-Fi yet. Check it's on and try again. | Пока не видим модем или Wi-Fi. Проверьте и попробуйте снова. | Hotspot yoki Wi-Fi hali ko'rinmayapti. Tekshirib, qayta urining. |
| lobby.iosJoinFirst | Players join your Wi-Fi in Settings first | Игроки сначала подключаются к вашему Wi-Fi в настройках | O'yinchilar avval sozlamalarda Wi-Fi tarmog'ingizga ulanadi |
| lobby.battery | Battery {{pct}}% — plug in so the room doesn't stop | Заряд {{pct}}% — подключите зарядку, чтобы комната не закрылась | Batareya {{pct}}% — xona to'xtamasligi uchun quvvatlang |

## testIDs · QA events
`camp.ios-guide.done` · `camp.lobby.battery` · `camp_battery_low { pct }`

## Approved packages
`react-native-device-info` (latest, New Arch).

## Done when
- [ ] tests: battery banner at 20 % unplugged shown, 21 % hidden, 15 % charging hidden, event once; iOS guide → no
  ip keeps sheet, ip → lobby with room-only QR (Platform.OS mocked)
- [ ] `npm run check` green (output in summary), `assembleDebug` compiles; iOS build only if pods already work
  (pods never installed — report, don't fix), committed, `graphify update .`
