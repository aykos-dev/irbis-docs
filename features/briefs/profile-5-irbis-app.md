# Brief profile-5-irbis-app — Notifs inbox

- Spec: features/profile.md · ACs in this slice: AC7
- Repo / branch: irbis-app · `feat/profile`
- Depends on: profile-3-irbis-app (Settings notification row + placeholder) + profile-4-irbis-api
  (notifications endpoints)

## Files
- Touch: `src/features/profile/screens/NotificationsScreen.tsx` (replace placeholder),
  `components/NotifRow.tsx`, `components/NotifTabs.tsx`, `SettingsScreen.tsx` (row already points here),
  `src/app/navigation/types.ts` / `RootNavigator.tsx` (replace placeholder screen), `linking.ts`
  (`Notifications: 'notifications'` already added), `src/shared/i18n/{en,ru,uz}/notifs.json` + `index.ts`, tests.
- Read for patterns: `src/features/places/screens/ExploreScreen.tsx` (tabs/filter chips),
  `src/features/lessons/screens/LessonsHubScreen.tsx` (empty/error/loading), `EmptyState` (mascot `sleepy`),
  `ErrorState`, `Screen`, `ListCard`, `Pressable`, `useNotificationsList` / `notificationsList`,
  `useNotificationsReadAll`, `tashkentDay`/`tashkentMonth` helpers, `qaLog`.

## Behaviour
- AC7 — Screen header “Notifications” + back, tabs All / Trips / Social / Rewards. All calls
  `useNotificationsList` with no category; the others pass `category`. Fetch newest-first with `limit=20`; when
  `nextCursor` exists show a “Load more” footer or load on scroll end (use the generated `notificationsList`
  function with `useInfiniteQuery` if the generated query hook only gives one page). Keep pages per tab.
- Render rows in two sections, **Today** and **Earlier**, by `createdAt` in Asia/Tashkent (reuse `tashkentDay`).
  Each row: category icon, localized `title`, optional `body`, localized time, and an unread dot when `readAt` is
  null. Tap is a no-op in this slice (no deep-link handlers yet); the row must still be accessible.
- “Mark all as read” calls `useNotificationsReadAll`, updates/refetches the current list and the header count,
  and is disabled when `unreadCount === 0`. QA `notifications_mark_all_read { count }`. Switching tabs logs
  `notifications_tab { tab }`.
- Empty: `EmptyState` with `mascot="sleepy"`, title “No notifications yet” and the body below; the tabs stay
  visible. A category tab with no rows uses its category-specific empty title. Error uses `ErrorState` with retry;
  loading shows skeleton rows; offline shows the network copy with retry. There are no producers yet, so a fresh
  account is empty by design — do not seed or construct demo rows in the app.
- Refresh on focus and pull-to-refresh. Preserve the selected tab across a refetch. Light/dark via tokens; long
  ru/uz titles wrap; rows have 44 px targets; unread dot is announced.

## API (generated hooks)
`useNotificationsList` / `notificationsList` (cursor pages) · `useNotificationsReadAll` (no body).

## Copy (`notifs.json`; en / ru / uz)
| key | en | ru | uz |
|---|---|---|---|
| `title` / `back` | `Notifications` / `Back` | `Уведомления` / `Назад` | `Bildirishnomalar` / `Orqaga` |
| `tabs.all` / `tabs.trips` / `tabs.social` / `tabs.rewards` | `All` / `Trips` / `Social` / `Rewards` | `Все` / `Поездки` / `Общение` / `Награды` | `Barchasi` / `Sayohatlar` / `Muloqot` / `Mukofotlar` |
| `today` / `earlier` | `Today` / `Earlier` | `Сегодня` / `Ранее` | `Bugun` / `Avvalroq` |
| `empty.title` / `empty.body` | `No notifications yet` / `Notifications from trips, groups and rewards will appear here.` | `Пока нет уведомлений` / `Уведомления о поездках, группах и наградах появятся здесь.` | `Hozircha bildirishnomalar yo‘q` / `Sayohatlar, guruhlar va mukofotlar haqidagi bildirishnomalar shu yerda ko‘rinadi.` |
| `empty.trips` / `empty.social` / `empty.rewards` | `No trip notifications yet.` / `No social notifications yet.` / `No reward notifications yet.` | `Пока нет уведомлений о поездках.` / `Пока нет уведомлений об общении.` / `Пока нет уведомлений о наградах.` | `Hozircha sayohat bildirishnomalari yo‘q.` / `Hozircha muloqot bildirishnomalari yo‘q.` / `Hozircha mukofot bildirishnomalari yo‘q.` |
| `markAll` / `unread` | `Mark all as read` / `Unread` | `Прочитать все` / `Непрочитано` | `Hammasini o‘qilgan qilish` / `O‘qilmagan` |
| `error` / `loading` / `loadMore` | `Couldn’t load notifications.` / `Loading notifications` / `Load more` | `Не удалось загрузить уведомления.` / `Загрузка уведомлений` / `Показать ещё` | `Bildirishnomalarni yuklab bo‘lmadi.` / `Bildirishnomalar yuklanmoqda` / `Yana ko‘rsatish` |

Category glyphs come from the canvas (conditions, duels, Top Shots, groups, spots, feed, streaks) and are drawn in
`Icon`; no new image files.

## testIDs · QA events
`notifs.tab-{all|trips|social|rewards}`, `notifs.list`, `notifs.empty`, `notifs.mark-all-read`,
`notifs.item-{id}`, `notifs.loading`, `notifs.error`, `notifs.retry`, `notifs.load-more` ·
`notifications_tab { tab }`, `notifications_mark_all_read { count }`.

## Approved packages
none.

## Done when
- [ ] tests: empty state per tab; fixture rows group Today/Earlier and show unread dots; category filter; mark-all
  updates unread to 0 and disables; error/retry; deep link `irbis://notifications`; Settings row reaches it
- [ ] `npm run check` green (output in summary) · committed on `feat/profile`
