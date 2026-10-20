# campfire-crocodile

- Status: Approved
- Surfaces: app only (no api, no web: the game runs on the host phone over the campfire-core room; no XP, no badges)
- Related ADRs: ADR-001 (guest-first: offline games need no account)
- Requirements: ROADMAP 29b (owner 2026-10-20): Crocodile, the describer sees a word (animals, movie heroes, famous
  people), others guess. No canvas board and no Product Overview section — this spec is the source.
  Look and feel: campfire boards (`CampLobby`, `ImpReveal`, `MafEnd`) and `campTheme`.
- Builds on: `campfire-core` + `campfire-party` + `campfire-mafia` (irbis-app `main` at f7290a3, protocol v3).
  Branch: irbis-app `feat/campfire-crocodile` from `main` (Q8). Independent of `feat/campfire-xo`.

## Goal
3–15 phones in a Campfire room play Crocodile: the host picks who shows next, that player secretly sees a word
and mimes it (no words, no sounds) while a timer runs on every phone; the turn ends on "Guessed!" or time-up and
the word is shown to all. No points; when the host ends, every phone sees a group summary.

## Local protocol changes (no API)
- `PROTOCOL_VERSION` 3 → **5** (v4 is taken by `feat/campfire-xo`; a skip keeps the two builds from claiming the
  same version. Whichever merges second bumps again). Older phones get the existing "Update Irbis to join this room".
- Host → all: `game { game: 'croc', round, public }` — `public` `{ phase: pick|ready|running|result|ended,
  describerSeatId?, turnNo, durationSec: 30|60|90, remainingMs?, result?: { kind: guessed|timeUp|cancelled,
  word: Localized }, totals: { guessed, skipped, turns } }`. The current word goes **only** to the describer
  (per-seat `secret { word: Localized, pack }`, like Imposter) and only appears in `public.result` after the turn.
- Client → host: `crocStart { round, turnNo }`, `crocSkip { round, turnNo }`, `crocGuessed { round, turnNo }`.
- State in the pure `gameReducer` (new `croc` branch) on the host; the host phone owns the timer and decides
  time-up. Saved with the host room (resume 12 h).

## Data model changes
None on the server. App: 3 new packs (`game: 'croc'`) in `games/packs/`; used-word memory reuses `usedStore`.

## Acceptance criteria
- **AC1** — **Tile + settings + start:** "Crocodile" tile (code-drawn glyph, own `campTheme` colour) in the CampHub
  games grid and the lobby game picker. Lobby settings: turn timer 30 / 60 / 90 s (default 60) and pack ticks
  Animals · Movie & cartoon heroes · Famous people (default all, at least 1). Range 3–15 players **including the
  host**; with fewer, Start is disabled with "Crocodile needs 3+ players". Protocol v5.
- **AC2** — **Pick the describer:** at game start and after every turn the host sees "Who shows next?" with every
  connected seat (host included) and taps one; other phones see "The host is choosing who shows". The host can also
  pick their own seat.
- **AC3** — **Secret word:** the describer gets a hold-to-reveal card (existing `SecretCard`, screen capture blocked
  as in Imposter) with the word, its pack name and the rule "Show it, don't say it — no words, no sounds", plus
  "Skip" (new word, `skipped`+1) and "Start". Others see "<nickname> is showing" with the avatar. The word is
  random from the ticked packs, never repeated per pack on the host phone until that pack runs out (then it resets).
- **AC4** — **Timer:** "Start" runs the countdown on every phone (ring + seconds; last 10 s in the warning colour,
  light haptic each of the last 5 s). Skip still works while running. The host phone decides time-up.
- **AC5** — **Turn end:** describer taps "Guessed!" → every phone shows "Guessed!" + the word, `guessed`+1, success
  haptic; time runs out → "Time's up!" + the word, heavy haptic. `turns`+1 either way. Then back to AC2.
- **AC6** — **Disconnect:** describer drops or is removed mid-turn → turn cancelled ("<nickname> left — the word
  is not counted"), back to AC2; reconnects to the same seat and is pickable again. Host drops → existing
  "reconnecting…" state; host app restart resumes the game (timer restarts the current turn at "ready"). A phone
  joining mid-game becomes a guesser and is pickable in AC2. If connected players fall below 3 the game goes on
  (the host decides when to end).
- **AC7** — **End + summary:** host "End" (any phase) → confirm "End the game?" → every phone: "Game over",
  "Words guessed <g> · Skipped <s> · Turns <t>", small confetti (Mafia game-over confetti). Host: "Play again"
  (totals 0, same settings, back to AC2) and "Lobby"; others: "Waiting for the host".
- **AC8** — **Packs + feedback:** 3 packs × 60 words, uz/ru/en (Claude drafts, owner review): animals, movie &
  cartoon heroes, famous people (Central Asia + world); validated by the existing pack schema (unique ids, all 3
  locales). Haptics only — **no sounds** (the sound player lives in `lessons` on `main`; it moves to
  `src/shared/sounds` with `campfire-xo`, sounds can follow after that merge).

### QA events (app, dev/staging builds)
`camp_game_started { game: 'croc', players }` · `croc_pick { turnNo }` · `croc_start { turnNo, durationSec }` ·
`croc_skip { turnNo, pack }` · `croc_turn_end { turnNo, kind }` · `camp_game_ended { game: 'croc', guessed,
skipped, turns }` — no nicknames, no words.

### testIDs (app)
`camp.hub.game.croc` · `camp.lobby.game.croc` · `croc.settings.timer.<30|60|90>` · `croc.settings.pack.<id>` ·
`croc.pick` · `croc.pick.<seatId>` · `croc.waiting` · `croc.card` · `croc.skip` · `croc.start` · `croc.timer` ·
`croc.guessed` · `croc.result` · `croc.end` · `croc.summary` · `croc.play-again` · `croc.lobby`

### Required UI states
- [ ] Loading (waiting for the first `game` message → existing GameWaiting)
- [ ] Empty (Start disabled with reason when < 3 players or no pack ticked)
- [ ] Error (host lost → existing reconnecting state; room closed → CampHub; describer lost → AC6 message)
- [ ] Offline: works with no internet; no OfflineBanner on campfire screens
- [ ] Keyboard: none; safe areas; haptics; press states; buttons ≥ 44 pt, RU/UZ copy wraps
- [ ] Dark campfire theme (`campTheme`) + design tokens + shared components only

## Media
`design/media/campfire-crocodile/MEDIA.md`: tile glyph drawn in code (placeholder → STATUS known issue), timer ring
drawn in code, `SecretCard`, avatars and confetti reused; 3 word packs drafted by Claude in
`design/media/campfire-crocodile/packs/` (owner review → STATUS known issue). No sounds (AC8).

## Waivers
- Phone-to-phone play is not unit-testable end to end: tests cover the `croc` reducer (pick, secret only to the
  describer, skip, start, guessed, time-up, cancel on drop, totals, end, play again, no repeats) and the screens with
  the room mocked; the owner tests on 3+ phones.

## Out of scope
- Points, teams, words-allowed (Alias) mode, custom words, pass-and-play, sounds, XP / badges, guess input on phones.

## Assumptions
- Q1 (owner, 2026-10-20): mime only — gestures, no words, no sounds.
- Q2 (owner, 2026-10-20): no score; group totals only.
- Q3 (owner, 2026-10-20): timer is a host setting 30 / 60 / 90 s, default 60; one word per turn, free skips.
- Q4 (owner, 2026-10-20): game goes on until the host ends it.
- Q5 (owner, 2026-10-20): end shows a group summary (guessed, skipped, turns) + Play again / Lobby.
- Q6 (owner, 2026-10-20): the host picks the next describer after every turn (and the first).
- Q7 (owner, 2026-10-20): 3 packs × 60 words, host ticks packs (default all), no repeats per pack on the host phone.
- Q8 (owner, 2026-10-20): 3–15 players with the host playing; branch from `main`; tile glyph placeholder drawn in code.
- Protocol v5 (not v4), haptics instead of sounds, mid-game joiners as guessers, host restart resumes at "ready" —
  main-session picks (main session, 2026-10-20).
- Code in `irbis-app/src/features/campfire-core/games/croc/` (same as party/mafia).

## Open questions
- none
