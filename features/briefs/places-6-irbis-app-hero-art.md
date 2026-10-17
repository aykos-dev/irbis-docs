# Brief places-6-irbis-app-hero-art — swap place hero art for the owner's images

- Spec: features/places.md · AC4 (card thumbnail), AC7 (hero) · Media: design/media/places/MEDIA.md
- Repo / branch: irbis-app · `feat/places-hero-art` (create from main)
- Source (owner, 2026-10-18): `../irbis-docs/design/images/hero/hero-{peak,lake,cave,camping,trail,waterfall,canyon}.png`
  (≈1586×992, 2.1 MB each — never copy the originals into the app)

## Files
- Touch: `src/assets/images/places/hero-<type>.jpg` (new, 7 files) · `src/features/places/placeTypes.ts` (type →
  image) · `PlaceHero` + `PlaceCard` components (render `Image` with `resizeMode="cover"` instead of the SVG string)
  · remove now-unused place-only SVG modules (`placeCave.ts`, `placeWaterfall.ts`, `placeCanyon.ts`) if nothing else
  imports them; keep `onb3Peak/onb3Lake/onb3Trail` (onboarding uses them) · tests in `src/app/__tests__/places/`
- Read: `src/assets/images.d.ts`, `src/assets/images/pins/` (existing PNG pattern), `PlaceScreen.tsx`, `ExploreScreen.tsx`

## Behaviour
- Convert each PNG with macOS `sips` (no new package): `sips -s format jpeg -s formatOptions 80 -Z 1170 <in> --out <out>`
  → 1170 px wide JPEG (3× of 390 pt), target ≤ 250 KB each; report the sizes.
- Every one of the 7 types shows its own image on the Place hero and on the Explore card thumbnail (camping no longer
  reuses trail). Hero keeps the current 390×240 frame (cover, centred crop); card thumbnail keeps its current size
  and corner radius. Same image in light and dark.
- Image has `accessible={false}` (decorative; the type pill carries the label).

## Tests
- One test: each PlaceType maps to a distinct image source (7 unique), and the hero renders an `Image` for a waterfall place.
  Don't edit existing tests; if one asserts the old SVG, report it instead of changing it.

## Approved packages
none

## Done when
- [ ] `npm run check` green, `cd android && ./gradlew assembleDebug -q | tail -30` compiles
- [ ] one commit `feat(places): owner hero art for all place types`; don't push, don't merge; reply ≤6 lines
