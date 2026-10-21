# Brief profile-3-irbis-api — avatar upload/remove, delete account

- Spec: features/profile.md · ACs in this slice: AC3, AC8
- Repo / branch: irbis-api · `feat/profile`
- Depends on: profile-1-irbis-api (schema + profile module on the branch)

## Files
- Touch: `src/features/profile/profile.controller.ts`, `profile.service.ts`, `profile.repository.ts`,
  `profile-avatar.service.ts` (new), `dto/profile.request.dto.ts`, `dto/delete-account.dto.ts`, tests ·
  `src/features/auth/auth.service.ts` (`checkSession` rejects `deletedAt`) ·
  `src/features/auth/auth.repository.ts` (`userSelect` already includes `deletedAt`; add transaction helpers if
  needed) · `openapi.json`
- Read for patterns: `src/features/lessons-admin/lesson-images.service.ts` (byte sniff + sharp + `StorageService`),
  `src/features/lessons-admin/admin-lesson-images.controller.ts` (multipart + 2 MB limit + 413 mapping),
  `src/features/lessons-admin/image-too-large.interceptor.ts`, `src/lib/storage/storage.service.ts`,
  `src/features/auth/auth.repository.ts` (`revokeAllForUser`), `src/features/auth/password.service.ts`,
  `src/common/errors/validation.error.ts`, `test/levels-api.e2e-spec.ts`.

## API
| Method | Path | Auth | Request | Response | Errors |
|---|---|---|---|---|---|
| POST | /v1/me/avatar | user | multipart `file` | `MeResponse` | 400 VALIDATION_FAILED, 401, 403, 413 IMAGE_TOO_LARGE, 415 IMAGE_TYPE, 503 STORAGE_UNAVAILABLE |
| DELETE | /v1/me/avatar | user | — | `MeResponse` with `avatarUrl: null` | 401, 403 |
| DELETE | /v1/me | user | `{ currentPassword }` | 204 | 400, 401 INVALID_PASSWORD, 403, 429 |

## Behaviour
- AC3 — Use `FileInterceptor('file', { storage: memoryStorage(), limits: { fileSize: 2 MB, files: 1 } })`
  and map `PayloadTooLargeException` to `IMAGE_TOO_LARGE` (copy the tiny interceptor into the profile feature or
  move it to `src/common/interceptors/`; do not edit lessons-admin if avoidable). Sniff the format from bytes
  with `sharp.metadata()`; accept only JPEG/PNG/WebP; otherwise `IMAGE_TYPE` 415. Re-encode with
  `sharp(file).rotate().resize(512, 512, { fit: 'cover', position: 'centre' }).jpeg({ quality: 82 })`; metadata
  is stripped by default. Store under `avatars/<uuid>.jpg` with `image/jpeg`, set `avatarKey`, return the updated
  `MeResponse`. Missing file → 400 `fieldErrors.file=['required']`. `DELETE /v1/me/avatar` clears `avatarKey`
  and returns `MeResponse`; do not delete the stored object (ADR-005 orphan rule).
- AC8 — `DELETE /v1/me` requires the current password: missing → 400 `fieldErrors.currentPassword=['required']`;
  wrong → 401 `INVALID_PASSWORD`; use `PasswordService.verify`. In one transaction: set `deletedAt=now`; set
  `username` to `deleted_` + 12 lowercase hex (20 chars, collision-safe); clear `displayName`, `bio`, `avatarKey`,
  `homeRegion`, `interests` to `[]`, `experience`, `recoveryPhone`, `recoveryPhoneVerifiedAt`; set `passwordHash`
  to `passwords.hash(randomUUID()+randomUUID())`; revoke every refresh token. Return 204.
- Reject deleted accounts on authenticated routes: `AuthService.checkSession` must load `deletedAt` and throw
  `UnauthorizedException` when it is non-null, so an old access token stops working immediately. The public
  profile already filters `deletedAt` (slice 1). Do not hard-delete the user row or the avatar object.
- Password/currentPassword never appears in logs or responses. Keep `@ApiBearerAuth()` and `@ApiErrorResponses`.
- Swagger operation ids: `Me_uploadAvatar`, `Me_deleteAvatar`, `Me_delete`. Orval should generate
  `useMeUploadAvatar`, `useMeDeleteAvatar`, `useMeDelete`.

## Copy
none (API).

## testIDs · QA events
none · none.

## Approved packages
none (existing `sharp`, multer/storage deps; do not add).

## Done when
- [ ] unit: JPEG/PNG/WebP accepted and square 512; wrong bytes → 415; >2 MB → 413; missing file → 400; remove
  clears key; delete requires/wrong password; anonymized username shape and cleared fields; refresh tokens revoked
- [ ] e2e: upload then `GET /v1/me` returns `avatarUrl`; remove returns null; delete returns 204, old access
  token now 401, old username/password login fails, public profile 404
- [ ] `npm run check` green (output in summary) · `npm run openapi:export` committed · `graphify update .`
