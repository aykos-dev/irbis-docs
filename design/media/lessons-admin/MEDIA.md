# Media — lessons-admin

Admin web has no canvas design (built from `design/design.md` tokens). The app screens (LessonsHub, Quiz*) belong to
`lessons`. Question images are content uploaded by the admin, not design media.

| File | What | Used on | Format / size | Status (exists · needed · placeholder OK) |
|---|---|---|---|---|
| Lesson icon glyphs ×10 (compass, leaf, padlock, cloud, paw, first-aid cross, mountain, waves, avalanche, bolt) | Icon picker in the lesson editor; same keys drawn by the app hub | Web lesson editor (and app LessonsHub in `lessons`) | inline SVG paths copied from canvas `LessonsHub` | exists on canvas · final |
| Tier colours ×6 | Tier chip colour in admin lists | Web tiers / lessons pages | tokens from canvas LessonsHub circles | exists on canvas · final |
| Question images | Optional picture per question | Web editor preview, app Quiz (in `lessons`) | JPEG / PNG / WebP ≤ 2 MB, re-encoded without metadata, longest side ≤ 1600 px | uploaded by the admin (none needed now) |
