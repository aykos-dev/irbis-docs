# Brief profile-4-irbis-api — notifications inbox API

- Spec: features/profile.md · ACs in this slice: AC7
- Repo / branch: irbis-api · `feat/profile`
- Depends on: profile-1-irbis-api (the `Notification` table + enums are already in `profile_init`)

## Files
- Touch: `src/features/profile/notifications.controller.ts` (new), `notifications.service.ts` (new),
  `notifications.repository.ts` (new), `dto/notifications.request.dto.ts`, `dto/notifications.response.dto.ts`,
  `profile.module.ts` (providers/controllers) · `openapi.json`
- Read for patterns: `src/features/places/places.controller.ts`, `places.service.ts` (`decodeCursor` / `encodeCursor`),
  `src/lib/cursor.ts`, `src/lib/dates.ts` (Asia/Tashkent if grouping is server-side; this API returns ISO only),
  `src/common/decorators/current-user.decorator.ts`, `test/levels-api.e2e-spec.ts`.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | /v1/notifications | user | `category?` (`trips|social|rewards`), `cursor?`, `limit?` default 20 / max 50 | `{ items, nextCursor, unreadCount }` | 400 VALIDATION_FAILED, 401, 403 |
| POST | /v1/notifications/read-all | user | — | `{ updated }` | 401, 403 |

`NotificationItem` = `{ id, category, kind, title, body, data, readAt, createdAt }`. `title`/`body` are strings
already localized to the account's `locale` (fallback `en`); `data` is the stored JSON or null; `createdAt` is
ISO-8601 UTC. `unreadCount` is the total unread for the user across all categories, not just the filtered page.

## Behaviour
- AC7 — List the current user's notifications newest-first (`createdAt desc, id desc`). Apply `category` when
  given. Use the shared opaque cursor encoding `{ createdAt, id }`; a malformed cursor is 400
  `fieldErrors.cursor=['invalid']`. Fetch `limit + 1` to set `nextCursor` only when another page exists.
  `readAt` is null for unread. `POST /v1/notifications/read-all` sets `readAt=now` on every unread row for the
  user and returns the updated count (0 is valid). It marks all categories; there is no per-item read route.
- Resolve the localized `title`/`body` from the JSON columns with the current user's `locale`; fall back to
  `en`, then the first available language. A missing `body` stays null. Never expose another user's rows.
- This slice adds **no producers, no push tokens and no seed rows**. New accounts are honestly empty. Tests may
  insert `Notification` rows through Prisma fixtures.
- `@ApiBearerAuth()`; operation ids `Notifications_list` and `Notifications_readAll`; orval should generate
  `useNotificationsList` and `useNotificationsReadAll`.

## Copy
none (API).

## testIDs · QA events
none · none.

## Approved packages
none.

## Done when
- [ ] unit: order + category filter; cursor round-trip and invalid cursor; limit clamp; `unreadCount` total;
  mark-all returns updated count and only touches the current user
- [ ] e2e: empty list for a fresh account; insert 3 rows (2 trips, 1 social) → list and filter; mark-all →
  `unreadCount=0`; another user's rows never appear
- [ ] `npm run check` green (output in summary) · `npm run openapi:export` committed · `graphify update .`
