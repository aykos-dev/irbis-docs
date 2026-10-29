# Brief owner-fixes-1022-1-irbis-app — APK API URL, player Back in games, inputs in sheets

- Source: owner device test 2026-10-22 (Android APK). Bugfix slice, no spec change.
- Repo / branch: irbis-app · `fix/owner-1022` (create from the current `feat/active-trip` HEAD)
- The working tree has uncommitted owner edits to `src/features/campfire-core/games/packs/*.json`:
  leave them alone, never stage or commit them.

## 1. `npm run android:apk` must call `https://devhotupdateapi.wayout.uz`
- Today `scripts/serve-apk.js` builds `assembleDevRelease`, which reads the git-ignored `.env.dev` (local API).
  `npm run android` (devDebug) must keep using `.env.dev` unchanged.
- Fix: add a committed, public-values-only env file for the APK (not named `.env.*`, e.g. `env/apk.env`) with
  `API_URL=https://devhotupdateapi.wayout.uz` (+ `/v1` or not: match how `src/shared/api/client.ts` and generated
  paths build URLs), `APP_ENV=dev`; MAP_STYLE_URL falls back to its default. In `serve-apk.js` spawn gradle with
  `ENVFILE=<that file>` (react-native-config: ENVFILE beats `envConfigFiles`; path relative to the repo root —
  confirm against `android/app/build.gradle`). Print the API URL used in the script's console output.
- Never read `.env*` files. No secrets in the new file.

## 2. Player Back during a game (camp.game)
- `src/features/campfire-core/games/GameWaiting.tsx`: `usePreventRemove(isPlayer && active, () => undefined)`
  makes hardware/gesture Back do nothing for players (the XO-1 fix), so players are stuck in a game.
- New behaviour: player Back while a game is active opens a confirm sheet "Leave the game?" (body: you leave the
  room; the others keep playing) with Leave (danger) and Stay. Leave → `client.leave()` path via
  `navigation.popToTop()` exactly as the lobby's `camp.lobby.leave` does (the lobby's unmount gives up the seat);
  Stay closes the sheet. Host behaviour unchanged. Reuse the host's existing end-confirm sheet pattern in this file.
- Copy (uz/ru/en, add to i18n): `camp.game.leaveTitle` "Leave the game?" · `camp.game.leaveBody` "You'll leave
  the room. The others keep playing." · `camp.game.leave` "Leave" · `camp.game.stay` "Stay". Write natural ru/uz.
- testIDs: `camp.game.leave-sheet`, `camp.game.leave-confirm`, `camp.game.leave-stay`.
- Tests (1–2): player Back with an active game shows the sheet; Leave pops to top.

## 3. Inputs inside a `Sheet` are hidden by the keyboard (Android) — fix once, in shared code
- Cause: `shared/components/Sheet.tsx` is `@gorhom/bottom-sheet` 5.2.14 `BottomSheetModal`. Its keyboard
  handling only reacts to inputs that register their focus target (`BottomSheetTextInput`); `TextField` renders a
  plain `TextInput`, so the sheet never lifts. The inner `KeyboardAvoidingView` in `PlayerSheet` / `ContactSheet`
  can't fix it (the sheet is portaled and absolutely positioned). App is edge-to-edge, manifest `adjustResize`.
- Fix in shared code: `TextField` renders `BottomSheetTextInput` when it is inside a sheet (detect with gorhom's
  `useBottomSheetInternal(true)` → null outside a sheet, or a small context set by `Sheet`), plain `TextInput`
  elsewhere; same props/ref. `Sheet`: set `keyboardBehavior="interactive"`, `keyboardBlurBehavior="restore"`,
  `android_keyboardInputMode="adjustResize"` and verify the right value for edge-to-edge in the gorhom v5 docs
  (Context7). Remove the now-redundant `KeyboardAvoidingView` wrappers in `PlayerSheet.tsx` and
  `trip-plan/components/ContactSheet.tsx`. Grep for any other `Sheet` containing an input and cover it the same way.
- Result: focused field AND the sheet's primary button sit above the keyboard on Android and iOS.
- Test (1): `TextField` inside `Sheet` renders the bottom-sheet input (mock gorhom as the repo's jest setup does).

## 4. Document the keyboard rule (binding for every future input)
- `docs/engineering-standards.md` keyboard section + Quick gate line, and `RULES.md` "Every screen" line:
  inputs on screens go through `Screen` (KeyboardAwareScrollView); inputs in sheets use shared `TextField` inside
  shared `Sheet` (never raw `TextInput`, never `KeyboardAvoidingView` inside a sheet); never a raw `TextInput`
  in a feature. Mention the gorhom focus-target cause in one line so nobody "fixes" it back. Keep it short.

## Approved packages
none

## Done when
- [ ] tests above, `npm run check` green, one commit per item (1–4) on `fix/owner-1022`, no push
- [ ] reply: what changed, deviations, the API URL the APK now uses, last line of `npm run check`
