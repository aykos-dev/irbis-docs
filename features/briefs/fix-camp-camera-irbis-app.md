# Fix brief fix-camp-camera-irbis-app — QR scan camera black in release + permission flow

- Owner report (2026-10-20): release APK (devRelease from `npm run android:apk`), CampJoin "Scan QR to join":
  (1) camera preview is a black box even after camera permission granted manually in app info; (2) tapping to grant
  camera opens the app info / settings screen instead of the one-tap system dialog. No logcat available.
- Repo / branch: irbis-app · `fix/camp-camera` from `feat/campfire-mafia` (HEAD 1f521f6). Commit, never push.
- Find code with `graphify` if on PATH, else grep `useCameraPermission|requestPermission|openSettings|Camera` in
  `src/features/campfire-core/join/`.

## (2) Permission — reproduce with a failing test first
- Expected: status not granted → call the OS request (`requestPermission()` from react-native-vision-camera, or
  `PermissionsAndroid.request(CAMERA)` if that's what the code uses) → system dialog. Only when the request
  returns denied **and** the OS will not ask again (`never_ask_again` / VC returns 'denied' after a request) show
  the existing "open settings" path (`Linking.openSettings()`). Re-check status on app foreground (AppState) so
  returning from settings starts the camera without a restart.
- Note: on Android VC4 `getCameraPermissionStatus()` may return 'denied' before the first request — never treat
  that as "permanently denied".
- Test: in the existing CampJoin test file, a case "first tap asks the OS dialog, not settings" (mock returns
  not-granted → request called, openSettings not called) + "settings only after a denied request". Show it red, then fix.

## (1) Black preview in release — R8
- `android/app/build.gradle` has `enableProguardInReleaseBuilds = true`; `proguard-rules.pro` keeps only BuildConfig.
- Add keep rules for `com.mrousavy.camera.**`, ML Kit barcode (`com.google.mlkit.**`,
  `com.google.android.gms.internal.mlkit_vision_barcode**` and the bundled variant), CameraX (`androidx.camera.**`)
  as needed, with a comment. Check whether the code scanner needs a `VisionCamera_*` gradle property — read only
  those lines (`grep -n VisionCamera android/gradle.properties`); never print other lines of that file (signing keys).
- Also check the Camera is `isActive` only when focused + permission granted, and that the preview re-mounts once
  permission flips to granted (a Camera mounted while denied can stay black).
- Verify: `./gradlew assembleDevRelease -q | tail -30` ok; in `android/app/build/outputs/mapping/devRelease/mapping.txt`
  the `com.mrousavy.camera` and mlkit barcode classes map to themselves (not renamed/removed) — paste 2–3 grep lines.
  No unit test possible for R8 → owner checks on the phone.

## Done when
- [ ] failing test shown, then green; no other existing tests edited
- [ ] `npm run check` green (tail in summary), release build ok, mapping evidence, committed on `fix/camp-camera`
- [ ] reply ≤ 10 lines: root cause of each, test name(s), commit hash, check tail
