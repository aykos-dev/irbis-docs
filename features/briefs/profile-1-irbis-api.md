# Brief profile-1-irbis-api — profile schema, me fields, public profile

- Spec: features/profile.md · ACs in this slice: AC1
- Repo / branch: irbis-api · `feat/profile` (create from main if missing; slices stack on it)
- Depends on: none

## Files
- Touch: `prisma/schema.prisma` (all profile enums/columns + `Notification`; one migration `profile_init`) ·
  `src/features/profile/` (new `profile.module.ts`, `profile.controller.ts`, `profile.service.ts`,
  `profile.repository.ts`, `dto/profile.request.dto.ts`, `dto/profile.response.dto.ts`,
  `dto/public-profile.response.dto.ts`, `profile.errors.ts`, tests) ·
  `src/features/auth/dto/me.response.dto.ts`, `src/features/auth/me.service.ts`,
  `src/features/auth/auth.module.ts` (import `StorageModule`) · `src/features/auth/auth.repository.ts`
  (`userSelect` new fields incl. `deletedAt`) · `src/app.module.ts` (import `ProfileModule`) ·
  `openapi.json` (export)
- Read for patterns: `src/features/levels/levels.module.ts`, `levels.controller.ts`, `levels.repository.ts`,
  `src/features/places/places.repository.ts`, `src/features/auth/me.controller.ts`,
  `src/features/auth/dto/me.response.dto.ts`, `src/lib/storage/storage.service.ts`,
  `src/common/decorators/public.decorator.ts`, `src/common/decorators/throttle.decorator.ts`,
  `test/levels-api.e2e-spec.ts`.

## Data model (fold into `profile_init`)
- Enums: `HomeRegion` = `tashkent_city | tashkent_region | andijan | bukhara | fergana | jizzakh |
  karakalpakstan | khorezm | namangan | navoiy | kashkadarya | samarkand | syrdarya | surkhandarya | other`;
  `Units` = `metric | imperial`; `Appearance` = `light | dark | auto`; `NotificationCategory` =
  `trips | social | rewards`.
- `User` add `displayName String? @db.VarChar(40)`, `bio String? @db.VarChar(150)`, `homeRegion HomeRegion?`,
  `avatarKey String? @db.VarChar(255)`, `showStats Boolean @default(true)`, `showHomeRegion Boolean
  @default(false)`, `units Units @default(metric)`, `appearance Appearance @default(auto)`, `notifyStreak
  Boolean @default(true)`, `notifyDailyGame Boolean @default(true)`, `dailyGameTime String @default("19:00")
  @db.VarChar(5)`, `notifyGroups Boolean @default(true)`, `notifySocial Boolean @default(true)`, `notifyOffers
  Boolean @default(false)`, `publicProfile Boolean @default(true)`, `findBuddies Boolean @default(true)`,
  `deletedAt DateTime? @db.Timestamptz(3)`.
- Add `Notification` model now (used by profile-4): `id`, `userId`, `category`, `kind`, `title Json`, `body
  Json?`, `data Json?`, `readAt DateTime?`, `createdAt`; relations + indexes from the spec.
- Existing rows keep defaults; no data backfill.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| GET | /v1/me | user | — | `MeResponse` + new fields + `preferences` | 401, 403 |
| PATCH | /v1/me | user | `displayName?`, `bio?`, `homeRegion?`, `interests?`, `locale?` | `MeResponse` | 400 VALIDATION_FAILED, 401, 403, 429 |
| GET | /v1/users/:username | public (`@Public()`, `@Throttled('lookup')`) | path | `PublicProfileResponse` | 404 PROFILE_NOT_FOUND, 429 |

`preferences` = `{ showStats, showHomeRegion, units, appearance, notifications: { tripSafety: true,
streakReminders, dailyGame, dailyGameTime, groupsMessages, social, offers }, privacy: { publicProfile,
findBuddies, shareLocation: 'trips' } }`. `tripSafety` and `shareLocation` are read-only for now.

`PublicProfileResponse` = `{ username, displayName, avatarUrl, bio, homeRegion|null, level, createdAt,
showStats }`. `homeRegion` is null unless `showHomeRegion`; never return phone, role, XP or preferences.

## Behaviour
- AC1 — `GET /v1/me` returns the new fields and preferences with the defaults above. `avatarUrl` is
  `storage.publicUrl(avatarKey)` or null when `avatarKey` is null; catch `StorageUnavailableError` and return
  null so a storage outage never fails `/v1/me`.
- `PATCH /v1/me` is partial. Trim strings; empty `displayName`/`bio` clears to null; `homeRegion` accepts an
  enum or null; `interests` is an array of 0–5 unique `Interest` values; `locale` is `uz|ru|en`. `displayName`
  non-empty must be 2–40 chars; `bio` max 150. Unknown keys are rejected by the global validation pipe.
  Return the updated `MeResponse`.
- `GET /v1/users/:username` lowercases the param and returns 404 `PROFILE_NOT_FOUND` for missing, `deletedAt
  != null`, `blockedAt != null`, or `publicProfile=false` (same response, no leak). `createdAt` is ISO UTC.
- Do not add username, preferences updates, avatar routes or notifications routes in this slice; DTOs may
  include `preferences` on the response only.
- Swagger: all DTOs decorated so orval generates `useMeGet` (updated), `useMeUpdate` (later extended), and
  `useUsersGetProfile`. Operation ids: `Me_update`, `Users_getProfile`.

## Copy
none (API).

## testIDs · QA events
none · none.

## Approved packages
none (uses existing `sharp` / storage deps; do not add).

## Done when
- [ ] unit: defaults; display-name/bio trims and limits; interests dedupe/limit; locale enum; avatarUrl null
  when storage unconfigured; private/deleted/blocked public profile → 404
- [ ] e2e: `GET /v1/me` shape/defaults; `PATCH` name/bio/region/interests; public profile 200 for public user,
  404 after `publicProfile=false`, 404 for blocked, case-insensitive username
- [ ] `npm run check` green (output in summary) · `npm run openapi:export` committed · `graphify update .`
