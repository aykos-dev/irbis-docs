# search

- Status: Built on local `feat/search` branches (not merged or pushed)
- Surfaces: api | app
- Requirements: Roadmap #15 · `design/canvas/Search.dc.html`

## Goal
Search places and discover public explorers from Explore, while showing the complete planned five-tab shape.

## Contract
`GET /v1/search?q=&scope=&lat=&lng=` is public and lookup-throttled. It returns place list items, people and empty
groups/tours arrays. Queries are trimmed and require two characters. Without coordinates, place distance uses the
configured Tashkent fallback.

People appear only when `publicProfile=true` and `findBuddies=true`; deleted and blocked accounts are excluded.
Avatar keys become public URLs, with a null fallback when storage is unavailable. Selecting a person opens the
existing public profile and intentionally has no Follow action.

## App
The Search screen always exposes All, Places, People, Groups and Tours. Groups and Tours show explicit “coming
soon” empty states. Place results open Place; people open PublicProfile. Search is debounced and has loading,
empty, error/retry and initials fallbacks.

## Verification
API e2e covers scopes, privacy filters and empty future categories; the full API check is green. App lint,
typecheck, source hygiene and all tests unrelated to the owner's uncommitted word-pack edits pass; iOS has not
been built.
