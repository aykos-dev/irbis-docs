# Brief campfire-mafia-4-irbis-app — APK over Wi-Fi + app icon

- Spec: features/campfire-mafia.md · ACs in this slice: AC7, AC8
- Repo / branch: irbis-app · `feat/campfire-mafia`
- Depends on: none (tooling; run after slice 3 on the same branch)

## Files
- New: `scripts/serve-apk.js` (Node 22, CommonJS or ESM to match other scripts; plain `http`, `os`, `fs`,
  `child_process`), `package.json` script `"android:apk": "node scripts/serve-apk.js release"`.
- New/replace: `android/app/src/main/res/mipmap-{mdpi,hdpi,xhdpi,xxhdpi,xxxhdpi}/ic_launcher.png` +
  `ic_launcher_round.png`, `mipmap-anydpi-v26/ic_launcher.xml` + `ic_launcher_round.xml` (adaptive: background
  colour + foreground PNG `ic_launcher_foreground.png` per density), `values/ic_launcher_background.xml`;
  `ios/<App>/Images.xcassets/AppIcon.appiconset/*` + `Contents.json`.
- Source art: `../irbis-web/public/irbis-icon.svg` (read only; copy into `design`-free location is not needed —
  generate PNGs into a scratch dir, commit only the PNG outputs). Check that `lint` / `check` ignore or pass
  `scripts/`.

## Behaviour
- AC7 — `node scripts/serve-apk.js <release|debug> [--no-build] [--host <ip>] [--port <n>]`:
  release → `./gradlew assembleDevRelease` in `android/` (debug → `assembleDevDebug`), streaming gradle output;
  non-zero exit → print "Build failed" + exit 1. APK path from `android/app/build/outputs/apk/dev/<type>/` (pick the
  newest `.apk`). `--no-build` serves the existing one (error if none). Server on 0.0.0.0, port 8787 or next free
  (try +1 up to 10). Routes: `/` → small HTML page (app name "Irbis Dev", versionName from `build.gradle`, size MB,
  build time, big "Download APK" button, line "Allow installs from this source if Android asks"); `/irbis.apk` →
  stream with `Content-Type: application/vnd.android.package-archive`, `Content-Disposition: attachment;
  filename="irbis-dev-<type>.apk"`, `Content-Length`. Each download logs "↓ <client ip>". LAN IP = first non-internal
  IPv4 (prefer en0/wlan; `--host` overrides); none → "No Wi-Fi/LAN address found" exit 1. Print URL + QR via
  `qrcode-terminal` (`small: true`) + "Scan on the same Wi-Fi · Ctrl+C to stop". No secrets read or printed.
- AC8 — App icon from `irbis-icon.svg`: render to 1024 px PNG with macOS tools (`qlmanage -t -s 1024 -o …` then
  `sips -z` for each size; verify the PNG is not blank/cropped by checking dimensions and that it isn't a single
  colour). Legacy mipmaps 48/72/96/144/192 (square tile) and round variants (circle-masked if feasible with
  available tools, else the same tile). Adaptive: background = the tile's teal (read it from the SVG), foreground =
  the art without the tile at 108 dp canvas sizes (162/…/432 px) with the 66 dp safe zone; if separating the art is
  not feasible from the SVG, use the full tile scaled to the safe zone. iOS AppIcon: all sizes Xcode needs, opaque,
  no alpha, 1024 marketing. Flavour names unchanged.

## Copy
none (dev tool page in English)

## testIDs · QA events
none

## Approved packages
`qrcode-terminal` (devDependency, latest)

## Done when
- [ ] `node scripts/serve-apk.js release --no-build` errors clearly with no APK; `./gradlew assembleDevRelease -q`
      succeeds (tail in summary); start the script with `--no-build` after that, `curl -sI` on `/` and
      `/irbis.apk` shows 200 + right content type, then stop it
- [ ] icons present at every density + adaptive XML; `assembleDevDebug` still builds
- [ ] `npm run check` green (output in summary), committed on `feat/campfire-mafia`, reply ≤ 10 lines
