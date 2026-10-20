# Brief lessons-admin-2-irbis-api — images (MinIO) + level tier gates

- Spec: features/lessons-admin.md · ACs in this slice: AC4, AC5
- Repo / branch: irbis-api · `feat/lessons-admin`
- Depends on: brief lessons-admin-1-irbis-api (on the branch)
- ADR: `../irbis-docs/decisions/ADR-005-object-storage.md` (binding)

## Files
- Touch: `src/lib/storage/` (new `StorageService`: put, exists, publicUrl; S3 client from env) ·
  config/env validation (where existing env is validated) · `.env.example` (placeholders only, e.g.
  `S3_ACCESS_KEY_ID=S3_ACCESS_KEY_ID`) · `docker-compose.yml` (add `minio` + one-shot `minio-init` creating the bucket
  with public-read on `lessons/`; credentials from env vars like the db service) ·
  `src/features/lessons-admin/` (image upload endpoint, key check on PUT) · `src/features/levels/` (gate numbers) ·
  `openapi.json`
- Read for patterns: `src/features/levels/level-engine.ts`, `levels.service.ts`, `game-config.service.ts`,
  `src/lib/field-cipher.ts` (lib style). Never read `.env*` other than `.env.example`.

## Behaviour
- AC4 — `POST /v1/admin/lesson-images` multipart field `file`: mime by content sniff (sharp metadata), JPEG/PNG/WebP
  only → else 415 IMAGE_TYPE; > 2 MB → 413 IMAGE_TOO_LARGE. Re-encode with sharp: `.rotate()` (apply orientation)
  then resize `fit: inside` 1600×1600 without enlargement, output same format, no metadata. Put at
  `lessons/<uuid>.<jpg|png|webp>`. Return `{ key, url, width, height }`, `url = S3_PUBLIC_BASE_URL + "/" + key`.
  Lesson `PUT` with `image: { key }` → key must match `^lessons/[0-9a-f-]{36}\.(jpg|png|webp)$` and exist (HEAD)
  else VALIDATION_FAILED at `questions.N.image`; responses return `image: { key, url }`. Any S3 error →
  503 STORAGE_UNAVAILABLE, logged with requestId, never logging credentials.
- AC5 — level gates: when building the effective levels table (used by engine, `GET /v1/levels`, `GET /v1/me/level`),
  for rows with `lessons.kind = tier` set `required` = count of published lessons in the tier with that key; kind
  `all` = count of all published lessons; kind `count` unchanged. If the computed `required` is 0 the gate is NOT met
  (engine treats it as unmet) and `required: 0` is shown. Cache with the existing ≤60 s config cache; publish /
  unpublish invalidates it. Levels never go down (existing rule). Existing levels tests: if one asserts the old
  config tier sizes, STOP and report it (do not edit).

## Tests (1–3 per AC)
- upload: PNG with EXIF GPS → stored object has no EXIF and ≤1600 px (StorageService faked in unit test; an e2e may
  use MinIO only if it is up — otherwise unit-level with a fake) · 415 + 413 · bad key on PUT.
- gates: published count drives `required`; 0 published → gate unmet; `all` sums tiers.

## Approved packages
`@aws-sdk/client-s3` (latest 3.x) · `sharp` (latest) · `@types/multer` (dev). Nothing else.

## Done when
- [ ] tests above, `npm run check` green (paste output), openapi exported, committed
- [ ] reply ≤10 lines incl. the env var names the owner must fill and `docker compose up` note
