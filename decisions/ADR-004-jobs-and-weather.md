# ADR-004: Scheduled jobs and weather provider

- Status: Accepted (owner, 2026-10-18)
- Date: 2026-10-18
- Feature: `conditions`

## Decision
- **Job runner:** `@nestjs/schedule` (cron decorators) inside irbis-api. Every job's cron runs in `Asia/Tashkent`.
  A job guards against overlapping runs in-process (one instance in Phase 1). Moving to a queue (e.g. BullMQ) when the
  API runs on more than one instance needs a new ADR.
- **Weather:** Open-Meteo forecast API (`/v1/forecast`, daily variables, `timezone=Asia/Tashkent`), called only by the
  API, batched by coordinates. Base URL in server config (`OPEN_METEO_BASE_URL`); no key on the free tier. An optional
  `OPEN_METEO_API_KEY` env var is read if set (paid customer endpoint). Clients never call the weather provider.
- Attribution "Weather data by Open-Meteo.com" is shown wherever forecast data is shown (CC BY 4.0).

## Why
`@nestjs/schedule` is the Nest-native option with no extra infrastructure (no Redis). Open-Meteo needs no key, covers
Central Asia, and returns everything the condition rules need (weather code, wind, gusts, precipitation, snowfall,
temperature) in one call for many coordinates.

## Consequences
- The free Open-Meteo tier is non-commercial: a paid plan is needed before production launch (open question on the
  `conditions` spec).
- With more than one API instance, jobs would run twice — revisit before scaling out.
