# ADR-005: Object storage for uploaded media

- Status: Accepted (owner, 2026-10-20)
- Date: 2026-10-20
- Feature: `lessons-admin` (first user: question images)

## Decision
- **Storage:** one S3-compatible bucket. Local dev runs **MinIO** in irbis-api `docker-compose.yml`; staging /
  production point the same code at any S3-compatible endpoint (MinIO, Cloudflare R2, AWS S3) through env only:
  `S3_ENDPOINT`, `S3_REGION`, `S3_BUCKET`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`, `S3_FORCE_PATH_STYLE`,
  `S3_PUBLIC_BASE_URL`. Values are filled in by a human (`.env`, secrets manager), never in code or chat.
- **Client:** `@aws-sdk/client-s3` inside irbis-api only, behind one `StorageService` in `src/lib/storage/`.
  Web and app never hold storage credentials.
- **Uploads go through the api** (multipart, admin-only for now): the api checks type (JPEG/PNG/WebP) and size
  (≤ 2 MB), re-encodes with `sharp` (strips EXIF/GPS, longest side ≤ 1600 px) and puts the object under
  `<feature>/<uuid>.<ext>`. The DB stores the object **key**; responses carry `url = S3_PUBLIC_BASE_URL + "/" + key`.
- Public objects are read-only by URL (bucket policy public-read on the public prefix). No presigned PUTs yet.

## Why
The owner chose MinIO (S3 compatible). Going through the api keeps one place for validation and metadata stripping
(product rule: photo location data is stripped), needs no bucket CORS, and is fine at admin upload volume.

## Consequences
- New packages in irbis-api: `@aws-sdk/client-s3`, `sharp` (approved with the `lessons-admin` spec).
- User photo uploads (spots, feed) will need presigned or streamed uploads at higher volume — revisit in a new ADR.
- Orphaned objects (uploaded, never saved) are not cleaned up yet.
