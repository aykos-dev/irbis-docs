# campfire-party

- Status: Approved
- Surfaces: app only (no api, no web: games run on the host phone over the campfire-core room; no XP, no badges — Q4, Q8)
- Related ADRs: ADR-001 (guest-first: offline games need no account)
- Requirements: Product Overview § Campfire games (offline) · Screens: `design/canvas/CampLobby.dc.html` (game picker +
  settings), `ImpReveal.dc.html` (C4), `ImpImposter.dc.html` (C5), `WhoAmI.dc.html` (C7), `WYR.dc.html` (C8),
  `CampSpec.dc.html` (Secrets stay secret); notes `n_c_reveal`, `n_c_wyr`. `ImpVote` (C6) is **not** built (Q5).
- Builds on: `campfire-core` (irbis-app `feat/campfire-core`, not merged). Branch: irbis-app `feat/campfire-party`
  from `feat/campfire-core`.

## Goal
In a campfire room the host picks Imposter, Who am I? or Would you rather, and every phone gets its own screen:
a secret word or character dealt only to that phone, or a question everyone votes on at once. The talking happens
around the fire; the host's phone runs rounds (reveal, new round, next question). Words never repeat until a pack
is used up.

## Local protocol changes (no API)
- `PROTOCOL_VERSION` 1 → **2** (a v1 phone gets `rejected version` → "Update Irbis to join this room").
- Host → one client only (never broadcast): `deal { game, round, secret }` — Imposter `{ role: word|imposter,
  wordId?, categoryId? }`, Who am I `{ others: [{ seatId, characterId }] }` (own character is not sent until
  `showMine`). Host → all: `game { game, round, phase, public }` (players in round, WYR question id, vote count,
  reveal data), `lobby` (game ended). Client → host: `wyrVote { round, qIndex, pick: a|b }`, `showMine { round }`.
- Messages carry ids only; each phone renders the text from its own bundled pack in its own app language.
- Game state lives in a pure `gameReducer` on the host next to `roomReducer`; saved with the host room (resume 12 h
  restores the current round and deals).

## Data model changes
None on the server. App MMKV: `camp.used.<game>.<packId>` (ids already dealt, host phone), `camp.hostRoom` gains
`game` (current game, settings, round, deals). Packs: bundled JSON in `src/features/campfire-core/games/packs/`, copied
from `design/media/campfire-party/packs/` (Q3).

## Acceptance criteria
- **AC1** — **Game picker (host lobby):** Imposter, Who am I and Rather are selectable; Mafia keeps "Coming soon".
  Settings: Imposter — word pack, imposters 1 (2 selectable only at 8+ players in the room), "Imposter sees the
  category" (on); Who am I — pack; Rather — pack. Start button "Start <game>" is enabled only within the player
  range (Imposter 3–15, Who am I 3–12, Rather 2–15, counting connected seats incl. host); otherwise disabled with
  "Needs 3+ players" / "Max 12 players". CampHub tiles for the 3 games drop "Coming soon" and open Host with that
  game preselected. Players in the lobby see "Waiting for the host to start".
- **AC2** — **Dealing + seats:** Start sends each seat its own `deal` (host phone included, hidden like everyone
  else's). A player who reconnects gets the same deal for the current round. A player who joins (new seat) during
  a round sees "Round in progress — you're in the next one" and is dealt in on the next round. Host "End game" →
  confirm "End the game for everyone?" → all phones back to the lobby. A removed player leaves the game too.
- **AC3** — **Hold to reveal + screen protection:** every secret card is covered ("Hold to see") and shows only
  while a finger is on it ("Release to hide"), with a light haptic tick on show. While a secret screen is open,
  Android blocks screenshots/recording (`FLAG_SECURE`), iOS blurs the card while the screen is being captured.
- **AC4** — **Imposter deal:** random imposter(s) among players in the round; everyone else gets the same word from
  the chosen pack. Word card: "YOUR SECRET WORD", word, category, header "Imposter" · "Round <n> · <m> players" ·
  "Offline · host <name>", "Clue order · one word each" = players in a random order, hint line. Imposter card:
  "SHH…", "You are the imposter", "You don't know the word. The category is:" + category (when the setting is off:
  "You don't know the word." only), "How to win" + 2 lines, "Got it" (closes the card). No clue entry, no vote,
  no timer in the app (Q5).
- **AC5** — **Imposter host controls:** host sees "Reveal imposter" and "New round". Reveal → every phone shows
  "The imposter was <name(s)>" and "The word was <word>". New round (enabled before or after reveal) → new word,
  new imposter(s), round +1, same players + anyone waiting.
- **AC6** — **Who am I?:** each player gets a different character from the pack. Screen: header "Who am I?" ·
  "Pack: <pack> · <n> players", own card "?" "YOU · <nickname>" "Your character is hidden on your phone", list
  "Everyone else's character" · "Only they can't see it" with avatar, nickname, character. "I know who I am!" →
  confirm "Show your character?" → own card shows the character for that player only. Host: "New round" (new
  characters for everyone). No question counter, no Pass turn, no hints (Q6).
- **AC7** — **Would you rather:** round = 20 questions from the chosen pack. Each phone shows "Would you rather…",
  option A, "OR", option B, "<n> / <m> voted" (m = connected players incl. host); a tap selects, can be changed
  until reveal. Reveal happens when all connected players voted or the host taps "Reveal": both bars fill to their
  % at once, voter avatars drop under their pick, "Your pick" marks yours, a haptic burst plays (no sound, Q7); the
  smaller side (if not a tie) gets "<names> — defend your choice!". Host "Next question"; after question 20:
  "Pack round done" + "New round" / "End game". Header "Would you rather" · "<pack> · question <i> of 20".
- **AC8** — **Packs + no repeats:** bundled packs in uz / ru / en — Imposter: Places in Uzbekistan, Food, Animals,
  Camping (60 words each); Who am I: Famous in Central Asia, Animals & things (40 each); Rather: Camping, Travel (40
  questions each). The host phone stores dealt ids per pack (`camp.used.*`) across rooms and days; an id is dealt
  again only after the whole pack was used, then the pack reshuffles. Lobby shows "<pack> · <count> words /
  characters / questions".

### QA events (app, dev/staging builds)
`camp_game_started { game, players }` · `camp_round_started { game, round }` · `camp_imposter_revealed { imposters }`
· `camp_whoami_show_mine` · `camp_wyr_revealed { votes, forced }` · `camp_game_ended { game, rounds }` ·
`camp_pack_reshuffled { game, pack }` — counts and ids only, no nicknames, no words.

### testIDs (app)
`camp.lobby.game.<imposter|whoami|rather>` · `camp.lobby.pack` · `camp.lobby.imposters` ·
`camp.lobby.sees-category` · `camp.lobby.start` · `camp.game.waiting` · `camp.game.end` · `camp.secret.card` ·
`imp.screen` · `imp.word` · `imp.imposter` · `imp.got-it` · `imp.reveal` · `imp.new-round` · `imp.result` ·
`whoami.screen` · `whoami.player.<seatId>` · `whoami.show-mine` · `whoami.new-round` · `wyr.screen` ·
`wyr.option.a|b` · `wyr.voted` · `wyr.reveal` · `wyr.next` · `wyr.new-round`

### Required UI states
- [ ] Loading (dealing / waiting for the host's first `game` message)
- [ ] Empty (no players in range → Start disabled with reason; waiting for next round)
- [ ] Error (host lost → existing reconnecting state; game ended / room closed → lobby / CampHub)
- [ ] Offline: works with no internet; no OfflineBanner on campfire screens
- [ ] Keyboard: none needed; safe areas; haptics on reveal / vote / WYR reveal; press states
- [ ] Dark campfire theme (`campTheme`) + design tokens + shared components only

## Media
From `design/media/campfire-party/MEDIA.md`: everything exists (companions, `irbisDefault`, `hero-lake`, canvas
vectors). Drumroll sound → haptic only (Q7, not a placeholder: no sound in this feature). Packs: drafted by Claude,
**owner review pending** (Q3) — tracked in STATUS known issues.

## Waivers
- Phone-to-phone play is not unit-testable end to end: tests cover `gameReducer` (deal, reconnect, reveal, new
  round, WYR votes/reveal), the no-repeat store, pack validation (every id has uz/ru/en) and the screens with the
  room mocked; the owner tests on real phones.
- iOS capture blur: code only, iOS never built (same as campfire-core).

## Out of scope
- Pass-and-play (one phone), campfire XP, campfire badges → `campfire-party-2` (Q1, next feature).
- In-app clues, vote and discussion timer for Imposter (ImpVote board) (Q5).
- Who am I question counter / Pass turn / hints (Q6); WYR sound and spicy pack; Mafia.

## Assumptions
- Q1 (owner, 2026-10-19): split — this feature = the 3 games over the room; `campfire-party-2` = pass-and-play +
  badges (+ XP), built right after.
- Q2 (owner, 2026-10-19): XP rule "5 play · +5 win · +5 host" chosen, then superseded by Q4/Q8 (no XP here).
- Q3 (owner, 2026-10-19): Claude drafts packs, owner reviews: Imposter 4 × 60, Who am I 2 × 40, Rather 2 × 40; no
  spicy pack.
- Q4 (owner, 2026-10-19): badges card stays "Coming soon"; Imposter and Who am I give no XP and no badge.
- Q5 (owner, 2026-10-19): Imposter = host starts, each phone shows its card, the rest is conversation; host has
  Reveal imposter + New round; lobby settings kept (pack, imposters 1 / 2 at 8+, sees category on); no clues,
  vote or timer in the app.
- Q6 (owner, 2026-10-19): Who am I = list of others' characters + "Show mine"; guessing is talk; host New round;
  no counter, Pass turn or hints.
- Q7 (owner, 2026-10-19): WYR = host taps Next, reveal on all votes or host Reveal, haptic only, 20 per round.
- Q8 (owner, 2026-10-19): no campfire XP in this feature (app only, no API).
- Q9 (owner, 2026-10-19): words / characters / questions don't repeat — host phone remembers per pack across rooms
  until the pack is used up, then reshuffles.
- Each phone shows pack text in its own app language (ids over the wire) (main session).
- Code lives in `irbis-app/src/features/campfire-core/games/` (not `campfire-party/`): eslint-boundaries forbids
  feature → feature imports and the games need the room engine; moving the room to `shared/` would be a refactor
  outside scope (main session).
- Protocol bumped to v2 so campfire-core-only builds get "Update Irbis to join this room" (main session).

## Open questions
- none
