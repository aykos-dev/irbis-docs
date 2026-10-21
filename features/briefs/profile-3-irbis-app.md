# Brief profile-3-irbis-app — Settings, appearance, recovery/sign-out move

- Spec: features/profile.md · ACs in this slice: AC6 (Settings + appearance; units formatting follows in slice 4)
- Repo / branch: irbis-app · `feat/profile`
- Depends on: profile-1-irbis-app (Profile header) + profile-2-irbis-app (EditProfile) + profile-2-irbis-api
  (preferences/locale PATCH)

## Files
- Touch: `src/features/profile/screens/SettingsScreen.tsx` (replace the placeholder), `HelpScreen.tsx`
  (placeholder for slice 4), `NotificationsScreen.tsx` (placeholder for slice 5),
  `components/SettingsToggleRow.tsx`, `components/Segmented.tsx`, `components/TimeSheet.tsx`,
  `src/features/profile/screens/ProfileScreen.tsx` (remove the temporary language/recovery/sign-out rows from
  AccountProfile; keep them on GuestProfile), `src/shared/contexts/theme.tsx`, `src/shared/contexts/auth.tsx`
  (`useAuthOptional`; clear cached prefs on sign-out), `src/shared/storage/index.ts` (`prefs.units`; use existing
  `prefs.colorScheme`), `src/app/navigation/types.ts` (`Settings`, `Help`, `Notifications`),
  `RootNavigator.tsx`, `linking.ts` (`Notifications: 'notifications'`), `src/shared/i18n/{en,ru,uz}/settings.json`
  + `index.ts`, existing auth tests that used `profile.recovery-phone` / `profile.sign-out` / signed-in
  `profile.language-*`.
- Read for patterns: current `ProfileScreen` rows, `RecoveryPhoneScreen`, `ListCard`/`ListRow`, `Sheet`,
  `Switch`, `createThemedStyles`, `theme.tsx`, `storage`, `getMeGetQueryKey`, `useMeUpdate`, `setLocale`,
  `languageNames`, `qaLog`.

## Behaviour
- AC6 — Settings sections exactly: **Irbis Plus** disabled row “Preview” with a note; **Account** (Edit profile →
  EditProfile; Recovery phone → existing RecoveryPhoneScreen with Add/Verify/Verified values; Language UZ/RU/EN;
  Units km·m / mi·ft; Appearance Light/Dark/Auto); **Notifications** (a “Notifications” row with chevron → the
  placeholder Notifs screen; Trip & safety locked on; Streak reminders; Bu qayer? daily with `19:00` and a
  18/19/20/21 sheet; Groups & messages; Likes, comments, Top Shots; Tours & offers); **Privacy** (Public profile;
  Show me in Find buddies; Share location read-only “Trips only”; Blocked people 0 disabled “Coming with
  Community”); **More** (Safety center & offline maps → Safety; Community guidelines disabled “Coming soon”;
  Help & feedback → Help placeholder); Log out; “Irbis 1.0”.
- Every toggle/segment saves immediately with `useMeUpdate` (`preferences.showStats` is not here; profile edit owns
  it). Optimistically update `setUser`, then PATCH; on failure revert the previous value and toast
  `settings.error`. `qaLog('settings_changed', { key, value })`. Disable a control while its request is in flight.
- Language: PATCH `locale`, `setLocale(next)` and `setUser`; if offline, revert. Units: PATCH
  `preferences.units` only; formatting is slice 4. Appearance: PATCH `preferences.appearance`; `ThemeProvider`
  reads it through `useAuthOptional` (or `prefs.colorScheme` before the user loads) and applies Light/Dark/Auto
  immediately. Sign-out removes `prefs.colorScheme` and `prefs.units` so the next account starts clean.
- Move the signed-in language/recovery/sign-out rows and testIDs to `settings.language-*`,
  `settings.recovery-phone`, `settings.logout`; update the auth/onboarding tests to navigate Settings. Guest
  Profile keeps `profile.language` / `profile.safety` / `profile.debug`.
- Loading: if `user` is null show the auth error/retry or a skeleton; Settings needs no separate fetch.
- Light/dark tokens; grouped cards with captions; 44 px targets; switches expose role/value. Plus/guidelines/
  blocked rows are visibly disabled (muted, no chevron action).

## API (generated hooks)
`useMeUpdate` · `useAuth().setUser` · `useAuth().signOut` · `getMeGetQueryKey`.

## Copy (`settings.json`; en / ru / uz)
| key | en | ru | uz |
|---|---|---|---|
| `title` | `Settings` | `Настройки` | `Sozlamalar` |
| `plus` / `preview` / `plusNote` | `Irbis Plus` / `Preview` / `Offline maps, more companions` | `Irbis Plus` / `Превью` / `Офлайн-карты, больше компаньонов` | `Irbis Plus` / `Ko‘rish` / `Oflayn xaritalar, ko‘proq hamrohlar` |
| `account` / `editProfile` / `recoveryPhone` | `Account` / `Edit profile` / `Recovery phone` | `Аккаунт` / `Редактировать профиль` / `Телефон для восстановления` | `Akkaunt` / `Profilni tahrirlash` / `Tiklash telefoni` |
| `language` / `units` / `unitsMetric` / `unitsImperial` | `Language` / `Units` / `km · m` / `mi · ft` | `Язык` / `Единицы` / `км · м` / `мили · футы` | `Til` / `Birliklar` / `km · m` / `mi · ft` |
| `appearance` / `light` / `dark` / `auto` | `Appearance` / `Light` / `Dark` / `Auto` | `Оформление` / `Светлая` / `Тёмная` / `Авто` | `Ko‘rinish` / `Yorug‘` / `Qorong‘i` / `Avto` |
| `notifications` / `inbox` | `Notifications` / `Notifications` | `Уведомления` / `Уведомления` | `Bildirishnomalar` / `Bildirishnomalar` |
| `tripSafety` / `tripSafetyNote` | `Trip & safety alerts` / `Condition changes, check-out reminders. Always on.` | `Оповещения о поездках и безопасности` / `Изменения условий, напоминания о возврате. Всегда включено.` | `Sayohat va xavfsizlik ogohlantirishlari` / `Sharoit o‘zgarishi, qaytish eslatmalari. Doim yoniq.` |
| `streak` / `streakNote` | `Streak reminders` / `Only when your streak is at risk` | `Напоминания о серии` / `Только когда серия под угрозой` | `Seriya eslatmalari` / `Faqat seriya xavf ostida bo‘lganda` |
| `daily` / `dailyNote` / `timeTitle` | `Bu qayer? daily` / `Daily at %{time}` / `Daily reminder time` | `Bu qayer? каждый день` / `Каждый день в %{time}` / `Время ежедневного напоминания` | `Bu qayer? har kuni` / `Har kuni %{time}da` / `Kunlik eslatma vaqti` |
| `groups` / `groupsNote` | `Groups & messages` / `Likes, comments, Top Shots` | `Группы и сообщения` / `Лайки, комментарии, Top Shots` | `Guruhlar va xabarlar` / `Layklar, izohlar, Top Shots` |
| `offers` / `offersNote` | `Tours & offers` / `Partner trips and discounts` | `Туры и предложения` / `Партнёрские поездки и скидки` | `Turlar va takliflar` / `Hamkor sayohatlari va chegirmalar` |
| `privacy` / `publicProfile` / `publicProfileNote` | `Privacy` / `Public profile` / `Others can see your stats and posts` | `Приватность` / `Открытый профиль` / `Другие видят вашу статистику и посты` | `Maxfiylik` / `Ochiq profil` / `Boshqalar statistikangiz va postlaringizni ko‘radi` |
| `findBuddies` / `findBuddiesNote` | `Show me in Find buddies` / `Let explorers find you nearby` | `Показывать в поиске попутчиков` / `Пусть исследователи находят вас рядом` | `Sayohatdosh topishda ko‘rsatish` / `Kashfiyotchilar sizni yaqin atrofda topsin` |
| `shareLocation` / `tripsOnly` / `blocked` / `blockedSoon` | `Share location` / `Trips only` / `Blocked people` / `Coming with Community` | `Делиться геолокацией` / `Только в поездках` / `Заблокированные` / `Появится с сообществом` | `Joylashuvni ulashish` / `Faqat sayohatlarda` / `Bloklanganlar` / `Hamjamiyat bilan keladi` |
| `more` / `safety` / `guidelines` / `comingSoon` / `help` | `More` / `Safety center & offline maps` / `Community guidelines` / `Coming soon` / `Help & feedback` | `Ещё` / `Центр безопасности и офлайн-карты` / `Правила сообщества` / `Скоро` / `Помощь и отзывы` | `Boshqa` / `Xavfsizlik markazi va oflayn xaritalar` / `Hamjamiyat qoidalari` / `Tez orada` / `Yordam va fikr` |
| `logout` / `version` / `error` | `Log out` / `Irbis 1.0` / `Couldn’t save that setting. Try again.` | `Выйти` / `Irbis 1.0` / `Не удалось сохранить настройку. Попробуйте ещё раз.` | `Chiqish` / `Irbis 1.0` / `Sozlamani saqlab bo‘lmadi. Qayta urinib ko‘ring.` |

## testIDs · QA events
`settings.plus`, `settings.edit-profile`, `settings.recovery-phone`, `settings.language-{uz|ru|en}`,
`settings.units-{metric|imperial}`, `settings.appearance-{light|dark|auto}`, `settings.notifications-inbox`,
`settings.notify-{streak|daily|groups|social|offers}`, `settings.daily-time-{18|19|20|21}`,
`settings.privacy-public`, `settings.privacy-find-buddies`, `settings.blocked`, `settings.safety`,
`settings.guidelines`, `settings.help`, `settings.logout`, `settings.version` ·
`settings_changed { key, value }`.

## Approved packages
none.

## Done when
- [ ] tests: defaults render; each toggle/segment PATCHes and reverts on failure; language updates i18n; appearance
  switches theme; recovery/sign-out move from Profile and auth tests updated; disabled rows; Help/Notifs navigation
- [ ] `npm run check` green (output in summary) · committed on `feat/profile`
