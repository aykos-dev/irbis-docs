# profile

- Status: Built on local `feat/profile-phase1` branches (not merged or pushed); owner device QA pending
- Surfaces: api | app
- Related ADRs: ADR-001 (auth), ADR-003 (api style), ADR-005 (object storage)
- Requirements: Product Overview § Accounts & profile · Screens: `design/canvas/Profile.dc.html`,
  `ProfileDark.dc.html`, `EditProfile.dc.html`, `Settings.dc.html`, `Notifs.dc.html`,
  `AccGuestProfile.dc.html`

## Goal
A signed-in explorer gets a real profile — photo, name, bio, home region, interests and privacy — can edit it,
change the login username safely, manage appearance/units/notification preferences, open an honest empty
notification inbox, share a public profile, and delete their account. Admin web is not touched.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| `GET` | `/v1/me` | user | — | `MeResponse` + `displayName`, `bio`, `avatarUrl`, `homeRegion`, `preferences` | 401, 403 |
| `PATCH` | `/v1/me` | user | partial profile / locale / `preferences` | `MeResponse` | 400 `VALIDATION_FAILED`, 401 `INVALID_PASSWORD`, 403, 409 `USERNAME_TAKEN`, 429 |
| `POST` | `/v1/me/avatar` | user | multipart `file` ≤ 2 MB JPEG/PNG/WebP | `MeResponse` | 400, 413 `IMAGE_TOO_LARGE`, 415 `IMAGE_TYPE`, 503 `STORAGE_UNAVAILABLE` |
| `DELETE` | `/v1/me/avatar` | user | — | `MeResponse` with `avatarUrl: null` | 401, 403 |
| `DELETE` | `/v1/me` | user | `{ currentPassword }` | 204 | 400, 401 `INVALID_PASSWORD`, 403, 429 |
| `GET` | `/v1/users/:username` | public | — | `PublicProfileResponse` | 404 `PROFILE_NOT_FOUND`, 429 |
| `GET` | `/v1/notifications` | user | `category?`, `cursor?`, `limit?` (default 20, max 50) | `{ items, nextCursor, unreadCount }` | 400, 401, 403 |
| `POST` | `/v1/notifications/read-all` | user | — | `{ updated }` | 401, 403 |

`PATCH /v1/me` fields: `displayName?`, `bio?`, `homeRegion?`, `interests?`, `locale?`, `username?`,
`currentPassword?`, and `preferences?: { showStats?, showHomeRegion?, units?, appearance?, notifications?: {
streakReminders?, dailyGame?, dailyGameTime?, groupsMessages?, social?, offers? }, privacy?: { publicProfile?,
findBuddies? } }`. `tripSafety` is always on and `shareLocation` is always `trips`; neither is writable.

`PublicProfileResponse`: `username`, `displayName`, `avatarUrl`, `bio`, `homeRegion` (only when
`showHomeRegion`), `level`, `createdAt`, `showStats`. No phone, role, XP, preferences or email.

## Data model changes
New migration `profile_init`.

- `User`: `displayName String? @db.VarChar(40)`, `bio String? @db.VarChar(150)`, `homeRegion HomeRegion?`,
  `avatarKey String? @db.VarChar(255)`, `showStats Boolean @default(true)`, `showHomeRegion Boolean @default(false)`,
  `units Units @default(metric)`, `appearance Appearance @default(auto)`, `notifyStreak Boolean @default(true)`,
  `notifyDailyGame Boolean @default(true)`, `dailyGameTime String @default("19:00") @db.VarChar(5)`,
  `notifyGroups Boolean @default(true)`, `notifySocial Boolean @default(true)`,
  `notifyOffers Boolean @default(false)`, `publicProfile Boolean @default(true)`,
  `findBuddies Boolean @default(true)`, `deletedAt DateTime? @db.Timestamptz(3)`.
- New enums: `HomeRegion` (14 Uzbekistan regions + `other`), `Units` (`metric | imperial`),
  `Appearance` (`light | dark | auto`), `NotificationCategory` (`trips | social | rewards`).
- New `Notification`: `id`, `userId`, `category`, `kind`, `title Json`, `body Json?`, `data Json?`,
  `readAt DateTime?`, `createdAt`; indexes `(userId, createdAt, id)` and `(userId, readAt)`.
- Avatar bytes stay in object storage (ADR-005); the DB stores only `avatarKey`. `avatarUrl` is derived.

## Acceptance criteria
- **AC1 — Profile data and public visibility.** `GET /v1/me` returns the fields above with these defaults:
  `showStats=true`, `showHomeRegion=false`, `units=metric`, `appearance=auto`, streak/daily/groups/social
  notifications on, offers off, daily time `19:00`, `publicProfile=true`, `findBuddies=true`. `PATCH /v1/me`
  trims strings; an empty name/bio/home region clears it; name is 2–40 characters, bio ≤150, interests are 0–5
  unique values from the existing enum, locale is `uz|ru|en`; invalid input is 400 with field errors. Public
  `GET /v1/users/:username` is case-insensitive and returns the public fields only; it returns 404
  `PROFILE_NOT_FOUND` when the user is missing, deleted, blocked or `publicProfile=false`. `avatarUrl` is `null`
  when storage is not configured. The app does not display the canvas demo values (6 peaks, 184 km, 4.9, #7).
- **AC2 — Username change.** Changing the username requires `currentPassword`: missing → 400 `currentPassword:
  required`, wrong → 401 `INVALID_PASSWORD`; invalid/reserved → 400 `USERNAME_INVALID`/`USERNAME_RESERVED`;
  taken → 409 `USERNAME_TAKEN`; the same normalized username is a no-op. On success the username is stored
  lowercase and the current session stays signed in while every other refresh-token family is revoked. Access
  tokens carry a `sid` claim (the refresh family id) so the API can tell the current session apart. The app asks
  for the password in a sheet only when the username changed.
- **AC3 — Avatar.** `POST /v1/me/avatar` accepts one JPEG/PNG/WebP by bytes, ≤2 MB, center-crops and re-encodes
  to 512×512 JPEG (quality 82), strips EXIF/GPS, stores `avatars/<uuid>.jpg`, sets `avatarKey` and returns the
  new `MeResponse`. `DELETE /v1/me/avatar` clears it. App: “Change photo” opens the gallery only via
  `react-native-image-picker` (no camera, no crop UI); the photo previews in EditProfile and uploads when Save
  is tapped; Cancel discards; remove returns to initials; permission denied, wrong type, >2 MB and upload/network
  errors are shown inline. Add only `NSPhotoLibraryUsageDescription`.
- **AC4 — Profile and public profile.** Signed-in Profile shows: photo or initials; the current-level companion;
  display name (fallback `@username`); `@username · home region (only if showHomeRegion) · since MMM yyyy`;
  level chip `Level N · title`; share and settings icons. Until their features ship, stats show Peaks/Lakes/Caves
  0, Walked 0 km, Climbed 0 m, Spots 0 with “Stats start with your first check-in.”; badges show 4 locked tiles
  with “Badges unlock with check-ins.”; ratings show “No buddy ratings yet.”; league shows “Unranked”. Safety
  center opens the existing Safety screen; Marketplace is a disabled “Preview” row. `irbis://profile/:username`
  opens a public Profile with the same identity/level/bio, home region only when public, stats only when
  `showStats`, the same empty badge/rating/league states, and no edit/settings actions; private/missing shows a
  back-capable “This profile is private or doesn’t exist.” state. Share uses the native sheet with the display
  name, `@username` and `irbis://profile/<username>`. The guest Profile stays as today.
- **AC5 — EditProfile.** Reachable from Settings (and the own Profile edit action). Fields: Name, Username, Bio
  with a live `n / 150` counter, Home region sheet (14 regions + Other), five interest chips (0–5 selected), “Show
  stats on my profile” (default on) and “Show my home region” (default off; disabled until a region is set; clears
  when the region is cleared). “Backpack colour” is a disabled row with “Coming with companion styles”. Save
  validates locally, uploads/deletes the staged photo, then PATCHes the fields; a username change opens the AC2
  password sheet. Success updates the auth user, shows “Profile saved” and returns to Settings/Profile; errors are
  inline; Cancel discards every staged change. The five interests are peaks, caves, lakes, camping, trails —
  Photography is omitted because it is not a place type and onboarding is unchanged.
- **AC6 — Settings and app-wide preferences.** Settings shows: Irbis Plus (disabled “Preview”); Account (Edit
  profile; Recovery phone — the existing Add/Verify/Verified screen; Language UZ/RU/EN; Units km·m / mi·ft;
  Appearance Light/Dark/Auto); Notifications (Trip & safety locked on; Streak reminders; Bu qayer? daily at 19:00
  with a 18:00/19:00/20:00/21:00 sheet; Groups & messages; Likes, comments, Top Shots; Tours & offers); Privacy
  (Public profile; Show me in Find buddies; Share location read-only “Trips only”; Blocked people 0 disabled
  “Coming with Community”); More (Safety center & offline maps; Community guidelines disabled “Coming soon”;
  Help & feedback); Log out; version. The Notifications section header has a “Notifications” row with a chevron
  that opens the Notifs screen (`irbis://notifications` also works). Each toggle saves immediately with
  `PATCH /v1/me`; on failure it reverts and
  shows a retry toast. Appearance applies app-wide immediately (Light/Dark/Auto), Units applies app-wide to every
  distance/elevation label (km/mi: one decimal under 10, whole above; m/ft: whole), and both are mirrored to MMKV
  so the last choice shows before the user loads. Language switches immediately and persists. Metric is the
  default. Trip & safety cannot be turned off. Sign-out clears the cached appearance/units so the next account does
  not inherit them.
- **AC7 — Notifications.** New accounts have no notification rows, so Notifs is honestly empty. `GET
  /v1/notifications` returns the user’s rows newest-first, filtered by category when asked, with an opaque cursor,
  `nextCursor` and total `unreadCount`; `POST /v1/notifications/read-all` sets `readAt` on all unread rows and
  returns the updated count. Notifs opens from Settings → Notifications → Notifications and from
  `irbis://notifications`; it shows All/Trips/Social/Rewards, Today/Earlier in Asia/Tashkent, unread dots,
  “Mark all as read” (disabled at 0 unread) and an empty state; loading, error+retry and offline states work. No
  push/device tokens and no producers ship in this feature; fixtures prove rows and mark-all-read.
- **AC8 — Delete account.** Settings → Help & feedback → Delete account opens a destructive confirmation with the
  current password. `DELETE /v1/me` requires it (400 if missing, 401 `INVALID_PASSWORD` if wrong), then soft-deletes
  in one transaction: `deletedAt=now`, username becomes `deleted_<12 hex>` (≤20 chars), display name, bio,
  avatarKey, home region, interests, experience and recovery phone are cleared, the password hash is replaced with
  a random un-matchable value, and every refresh token is revoked. The app clears its session/cache, signs out and
  lands on the guest Profile. The old username/password cannot log in, old access tokens are rejected, and the
  public profile returns 404. The avatar object is left orphaned (ADR-005); hard purge is later.

### QA events (app, dev/staging builds)
`profile_edit_saved { fields }` · `username_changed` · `avatar_uploaded { sizeBucket }` · `avatar_removed` ·
`settings_changed { key, value }` · `profile_shared` · `public_profile_viewed` · `notifications_tab { tab }` ·
`notifications_mark_all_read { count }` · `account_deleted` — no names, usernames, phone numbers or image data.

### testIDs (app)
`profile.avatar`, `profile.name`, `profile.username`, `profile.meta`, `profile.level`, `profile.share`,
`profile.settings`, `profile.stats`, `profile.stats-{peaks|lakes|caves|walked|climbed|spots}`, `profile.badges`,
`profile.ratings`, `profile.league`, `profile.safety`, `profile.marketplace`,
`public-profile.avatar`, `public-profile.name`, `public-profile.username`, `public-profile.meta`,
`public-profile.bio`, `public-profile.stats`, `public-profile.badges`, `public-profile.ratings`,
`public-profile.league`, `public-profile.private`, `public-profile.retry`,
`edit-profile.name`, `edit-profile.username`, `edit-profile.bio`, `edit-profile.bio-count`,
`edit-profile.home-region`, `edit-profile.interest-{peaks|caves|lakes|camping|trails}`,
`edit-profile.show-stats`, `edit-profile.show-home-region`, `edit-profile.change-photo`,
`edit-profile.remove-photo`, `edit-profile.backpack-colour`, `edit-profile.save`, `edit-profile.cancel`,
`edit-profile.error`, `edit-profile.password`, `edit-profile.password-confirm`,
`settings.plus`, `settings.edit-profile`, `settings.recovery-phone`, `settings.language-{uz|ru|en}`,
`settings.units-{metric|imperial}`, `settings.appearance-{light|dark|auto}`,
`settings.notify-{streak|daily|groups|social|offers}`, `settings.daily-time-{18|19|20|21}`,
`settings.privacy-public`, `settings.privacy-find-buddies`, `settings.blocked`, `settings.safety`,
`settings.guidelines`, `settings.help`, `settings.logout`, `settings.version`,
`settings.notifications-inbox`, `help.delete-account`, `delete-account.password`, `delete-account.confirm`,
`delete-account.cancel`, `delete-account.error`,
`notifs.tab-{all|trips|social|rewards}`, `notifs.list`, `notifs.empty`, `notifs.mark-all-read`,
`notifs.item-{id}`.

### Required UI states (every touched client)
- [x] Loading — Profile/PublicProfile/Notifs skeleton; Settings uses the auth user
- [x] Empty — stats, badges, ratings, league, Notifs, public stats hidden by privacy
- [x] Error (message + retry) — profile load, public profile, notifications, avatar/upload, save
- [x] Offline — cached profile/preferences; edits and uploads fail with retry; Notifs error
- [x] Permission denied — photo library denied (gallery only)
- [x] Not configured — storage missing → `avatarUrl: null`; upload shows retryable error
- [x] Private/not found — public profile 404 state with back
- [ ] App: light + dark via design tokens; safe areas; dynamic type and long ru/uz strings wrap; press states;
      haptics on destructive confirm and save
- [ ] Accessibility: avatar/photo labels, switch roles and values, 44 px targets, destructive action announced

## Media
`design/media/profile/MEDIA.md`: avatar photos are runtime uploads with an initials fallback; companion and
Irbis SVGs exist and are final; badge and league art are code placeholders until `badges`/`leagues`; all row
icons are drawn in code from the canvas. No sound/video/animation.

## Waivers
- Badge showcase and Granite league chip are labelled empty states, not the canvas demo art; real art arrives with
  `badges` and `leagues`.
- Stats, buddy ratings and league rank show honest empty states until `check-in`, `trips` and `leagues` ship.
- “Backpack colour” is disabled until companion colour variants exist.
- Irbis Plus, Marketplace, Community guidelines and blocked-people management are previews/disabled; no purchase,
  marketplace, guidelines content or block list.
- No camera capture, crop UI or avatar moderation.
- Delete account is a soft delete; hard purge/retention is later.
- Avatar object is orphaned on replace/delete (ADR-005).

## Out of scope
- Admin web.
- Check-in, trips, badges, leagues, streak and rating data (only their Profile empty states).
- Push/device tokens, notification producers, notification email/SMS.
- Blocked-people management, Find buddies, public posts, followers.
- Public profile posts/badges, profile search/listing.
- Hard account deletion, data export, support ticketing.
- Camera capture, image crop, companion backpack colour.
- Onboarding changes (Photography stays out).
- Email/social login.

## Assumptions
- Q1 (owner, 2026-10-21): stats/badges/ratings/league stay visible as honest empty states; no canvas demo numbers.
- Q2 (owner, 2026-10-21): username change is included.
- Q3 (owner, 2026-10-21): avatar flow is gallery only, no crop UI; initials fallback.
- Q4 (owner, 2026-10-21): full Settings plus an empty Notifs screen.
- Q5 (owner, 2026-10-21): keep the five existing interests; omit Photography.
- Q6 (owner, 2026-10-21): `showHomeRegion` defaults off; Profile shows the region only after opt-in.
- Q7 (owner, 2026-10-21): add a minimal notifications table/API; no producers yet.
- Q8 (owner, 2026-10-21): username change requires the current password and revokes other sessions.
- Q9 (owner, 2026-10-21): account deletion is included in this feature.
- Q10 (owner, 2026-10-21): display name optional 2–40; bio ≤150; home region from the fixed Uzbekistan list
  (14 regions + Other); `showHomeRegion` off by default.
- Q11 (owner, 2026-10-21): backpack colour is deferred with a disabled row.
- Q12 (owner, 2026-10-21): share builds a public profile (`GET /v1/users/:username`, deep link).
- Q13 (owner, 2026-10-21): public profile defaults to on; the public endpoint returns 404 when it is off.
- Existing auth tests/QA that used `profile.recovery-phone`, `profile.sign-out` or the signed-in
  `profile.language` row move to the Settings equivalents (`settings.recovery-phone`, `settings.logout`,
  `settings.language-*`); auth acceptance criteria do not change. The guest Profile keeps its language/safety
  rows.
- The Product Overview artifact was inaccessible in this session; requirements were taken from `PROJECT.md`,
  `ROADMAP.md`, the canvas boards and the existing specs. The canvas is English-only; ru/uz copy is written in the
  briefs for owner review.

## Open questions
- none
