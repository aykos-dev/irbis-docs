# Brief profile-4-irbis-app — units app-wide, Help and account deletion

- Spec: features/profile.md · ACs in this slice: AC6 (units formatting), AC8
- Repo / branch: irbis-app · `feat/profile`
- Depends on: profile-3-irbis-app (Settings) + profile-3-irbis-api (avatar + `DELETE /v1/me`)

## Files
- Touch: `src/shared/utils/units.ts` (new), `src/shared/hooks/useUnits.ts` (new),
  `src/features/places/formatDistance.ts`, `PlaceCard.tsx`, `PlaceScreen.tsx`, `FilterChips.tsx`,
  `FilterSheet.tsx`, `src/features/weekly-path/components/SwapCard.tsx`,
  `src/features/profile/screens/HelpScreen.tsx` (replace placeholder), `DeleteAccountSheet.tsx` (new),
  `SettingsScreen.tsx` (wire Help), `src/shared/i18n/{en,ru,uz}/{places,path,profile,settings}.json`,
  tests.
- Read for patterns: `places/formatDistance.ts`, `PlaceCard`, `PlaceScreen`, `FilterSheet`, `SwapCard`,
  `useAuth`, `useAuthOptional`, `storage`, `Sheet`, `TextField`, `AppButton`, `toast`, `qaLog`,
  `useMeDelete`, `src/shared/api/errors`.
- Reuse `profile.stats.km` / `.m`, `places.distanceKm` / `elevationValue`, and `path.swap.body` where possible;
  add only the imperial keys below.

## Behaviour
- AC6 units — Add `useUnits()` returning `'metric' | 'imperial'` from `user.preferences.units`, then
  `storage.getString('prefs.units')`, then `'metric'`; mirror the user value to `prefs.units`. Add pure helpers:
  `formatDistance(m, units, locale)` (km/mi: one decimal below 10, whole above), `formatElevation(m, units, locale)`
  (m/ft whole), `formatSignedElevation(m, units, locale)` and `formatMaxDistance(km, units, locale)` (whole).
  Use `Intl.NumberFormat(locale, { maximumFractionDigits })`.
- Replace every read-only distance/elevation label: profile stats (`Walked` / `Climbed`), Place card + detail,
  place filter chip labels, weekly-path swap body. Metric is the default and must match today's output exactly.
  Imperial uses `%{d} mi`, `%{n} ft`, `≤ %{km} mi`, `path.swap.bodyImperial`, `profile.stats.mi` / `.ft`.
  Do not change the API values stored in metres/kilometres; only display.
- AC8 — Settings → Help & feedback opens `HelpScreen` with the intro copy and a destructive “Delete account” row.
  Tapping it opens `DeleteAccountSheet`: warning body, current-password field, Cancel and destructive “Delete
  account”. Missing password is inline `delete.required`; wrong password is `delete.wrong`; other errors use
  `delete.error`. On confirm call `useMeDelete({ data: { currentPassword } })`; disable the button while pending.
  On 204: `qaLog('account_deleted')`, `toast.show({ variant: 'success', message: t('delete.done') })`, then
  `await signOut()` (it clears tokens/query cache; its server call may 401 and is already swallowed) and land on the
  guest Profile. Do not navigate to Settings after deletion.
- Help screen has a back button, scroll, safe-area and light/dark tokens. The account row is the only action in
  this slice; “Community guidelines” stays disabled from Settings. No support ticket integration.
- Long ru/uz labels wrap; the password field is `secureTextEntry`, `textContentType="password"`, never logged.

## API (generated hooks)
`useMeDelete` (body `{ currentPassword }`) · `useAuth().signOut` · `useUnits` for the profile/place/path labels.

## Copy (en / ru / uz)
| key | en | ru | uz |
|---|---|---|---|
| `help.title` | `Help & feedback` | `Помощь и отзывы` | `Yordam va fikr` |
| `help.body` | `Need a hand? Delete your account here or write to support.` | `Нужна помощь? Удалите аккаунт здесь или напишите в поддержку.` | `Yordam kerakmi? Akkauntni shu yerda o‘chiring yoki qo‘llab-quvvatlashga yozing.` |
| `help.deleteAccount` / `help.deleteAccountNote` | `Delete account` / `Permanently close your profile and sign out everywhere.` | `Удалить аккаунт` / `Навсегда закрыть профиль и выйти на всех устройствах.` | `Akkauntni o‘chirish` / `Profilni butunlay yopish va hamma qurilmalardan chiqish.` |
| `delete.title` / `delete.body` | `Delete account?` / `This closes your profile, clears your personal details and signs you out everywhere. This can’t be undone.` | `Удалить аккаунт?` / `Профиль закроется, личные данные очистятся, вы выйдете на всех устройствах. Отменить нельзя.` | `Akkauntni o‘chirasizmi?` / `Profilingiz yopiladi, shaxsiy ma’lumotlar tozalanadi va hamma qurilmalardan chiqasiz. Buni bekor qilib bo‘lmaydi.` |
| `delete.password` / `delete.confirm` / `delete.cancel` | `Current password` / `Delete account` / `Cancel` | `Текущий пароль` / `Удалить аккаунт` / `Отмена` | `Joriy parol` / `Akkauntni o‘chirish` / `Bekor qilish` |
| `delete.required` / `delete.wrong` / `delete.error` / `delete.done` | `Enter your password.` / `Wrong password.` / `Couldn’t delete the account. Try again.` / `Account deleted.` | `Введите пароль.` / `Неверный пароль.` / `Не удалось удалить аккаунт. Попробуйте ещё раз.` / `Аккаунт удалён.` | `Parolni kiriting.` / `Parol noto‘g‘ri.` / `Akkauntni o‘chirib bo‘lmadi. Qayta urinib ko‘ring.` / `Akkaunt o‘chirildi.` |
| `places.distanceMi` / `places.elevationFt` / `places.filter.maxMi` | `%{d} mi` / `%{n} ft` / `≤ %{km} mi` | `%{d} миль` / `%{n} футов` / `≤ %{km} миль` | `%{d} mi` / `%{n} ft` / `≤ %{km} mi` |
| `path.swap.bodyImperial` | `%{elev} ft, %{km} mi from %{original}, clear skies on %{day}.` | `%{elev} футов, %{km} миль от %{original}, ясно в %{day}.` | `%{elev} ft, %{original}dan %{km} mi, %{day} kuni ochiq.` |
| `profile.stats.mi` / `profile.stats.ft` | `%{value} mi` / `%{value} ft` | `%{value} миль` / `%{value} футов` | `%{value} mi` / `%{value} ft` |

## testIDs · QA events
`help.delete-account`, `delete-account.password`, `delete-account.confirm`, `delete-account.cancel`,
`delete-account.error` · `account_deleted`.

## Approved packages
none.

## Done when
- [ ] tests: metric output unchanged; imperial profile/place/path/filter labels; setting units re-renders all
  labels; delete requires/wrong password; success signs out and shows guest profile; public profile 404 after
  delete
- [ ] `npm run check` green (output in summary) · committed on `feat/profile`
