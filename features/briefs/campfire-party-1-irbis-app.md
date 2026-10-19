# Brief campfire-party-1-irbis-app — game engine, protocol v2, lobby picker, packs

- Spec: features/campfire-party.md · ACs in this slice: AC1, AC2, AC8
- Repo / branch: irbis-app · `feat/campfire-party` (create from `feat/campfire-core`; slices stack on it)
- Depends on: campfire-core (all 4 slices, on `feat/campfire-core`)

## Files
- New: `src/features/campfire-core/games/` — `gameReducer.ts` (pure, host side), `packs/` (copy the 8 JSON files from
  `irbis-docs/design/media/campfire-party/packs/` as-is) + `packs/index.ts` (typed loader, zod-validated),
  `usedStore.ts` (MMKV no-repeat), `GameWaiting.tsx` (placeholder screen per game until slices 2–3: header + "Round
  in progress" / dealt state; slices 2–3 replace the body), `__tests__/`. Never put game code in a new feature folder:
  eslint-boundaries forbids feature → feature imports.
- Edit: `protocol/codec.ts` (v2 + messages), `room/roomReducer.ts` / `hostServer.ts` / `useHostRoom.ts` /
  `hostRoomStore.ts` (route game actions, per-seat send, save game state), `join/playerClient.ts` (handle `deal`,
  `game`, `lobby`), `screens/CampLobbyScreen.tsx` (picker + settings + Start), `screens/CampHubScreen.tsx` +
  `components/GameTile.tsx` (3 tiles live), navigation for the game route, `camp.json` ×3.
- Read for patterns: existing `roomReducer` tests, `hostRoomStore.ts` (MMKV), `components/ComingSoonTag.tsx`.

## Behaviour
- Protocol: `PROTOCOL_VERSION = 2`. Host → one seat: `deal { game, round, secret }` (Imposter `{ role: 'word'|'imposter',
  wordId?, packId, showCategory }`; Who am I `{ others: [{ seatId, characterId }] }`; Rather: no deal). Host → all:
  `game { game, round, phase, public }`, `lobby {}`. Client → host: `wyrVote { round, qIndex, pick }`,
  `showMine { round }` (shape only; handling comes in slice 3). zod schemas like the existing ones. Secrets are never
  in a broadcast message; test that `game.public` never contains a word/character id for Imposter/Who am I deals.
- `gameReducer(state, action)`: `start { game, settings, seats, rng }`, `newRound`, `end`, `seatJoined`,
  `seatRemoved`, `reveal` (Imposter), `wyrVote` / `wyrReveal` / `wyrNext` (WYR — state only, UI in slice 3). Inject
  rng for tests. Players in a round = connected seats at start/newRound (incl. host); seats joining mid-round go to
  `waiting` and are included on the next `newRound`; reconnecting seats keep their deal.
- AC1 — Lobby picker: Imposter / Who am I / Rather selectable (`camp.lobby.game.<id>`), Mafia keeps Coming soon.
  Settings rows (canvas CampLobby): Imposter — Word pack (`<name> · <n> words`), Imposters 1 (2 only when ≥ 8 seats),
  "Imposter sees the category" switch default on + sub "Makes bluffing easier"; Who am I — Pack; Rather — Pack. Pack
  picker = simple sheet list. Start "Start <game>" enabled only if connected seats (incl. host) in range: Imposter
  3–15, Who am I 3–12, Rather 2–15; else disabled + `game.needsMin` / `game.max`. Footer "You play too — your word
  stays hidden on this phone." Players see the existing "Waiting for the host to start". CampHub tiles for the 3
  games: no Coming soon; tap → same Host flow with that game preselected (Mafia tile unchanged).
- AC2 — Start → every phone (host too) opens the game route; late joiners see `game.inProgress`. Host header has
  "End game" (`camp.game.end`) → confirm `game.endConfirm` → `lobby` to all → lobby. Removed seat → existing removed
  flow. Host room save (`camp.hostRoom`) includes game state so resume restores the round and deals.
- AC8 — `packs/index.ts` loads and validates (ids unique, uz/ru/en present); text rendered in the phone's app
  language. `usedStore`: `camp.used.<game>.<packId>` = dealt ids; dealing picks only unused ids; when not enough left,
  clear and reshuffle (`camp_pack_reshuffled`). Who am I needs one unused id per player; Rather takes 20 per round.

## Copy (`camp.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| game.start | Start {{game}} | Начать: {{game}} | {{game}}ni boshlash |
| game.needsMin | Needs {{n}}+ players | Нужно от {{n}} игроков | Kamida {{n}} o'yinchi kerak |
| game.max | Max {{n}} players | Максимум {{n}} игроков | Ko'pi bilan {{n}} o'yinchi |
| game.youPlayToo | You play too — your word stays hidden on this phone. | Вы тоже играете — ваше слово скрыто на этом телефоне. | Siz ham o'ynaysiz — so'zingiz bu telefonda yashirin qoladi. |
| game.pack | Word pack | Набор слов | So'zlar to'plami |
| game.packWhoami | Pack | Набор | To'plam |
| game.words / characters / questions | {{n}} words / {{n}} characters / {{n}} questions | {{n}} слов / {{n}} персонажей / {{n}} вопросов | {{n}} ta so'z / {{n}} ta qahramon / {{n}} ta savol |
| game.imposters | Imposters | Самозванцы | Sotqinlar |
| game.seesCategory | Imposter sees the category | Самозванец видит категорию | Sotqin toifani ko'radi |
| game.seesCategorySub | Makes bluffing easier | Так легче блефовать | Aldash osonroq bo'ladi |
| game.inProgress | Round in progress — you're in the next one | Идёт раунд — вы сыграете в следующем | Raund ketmoqda — keyingisida qatnashasiz |
| game.end | End game | Завершить игру | O'yinni tugatish |
| game.endConfirm | End the game for everyone? | Завершить игру для всех? | O'yin hamma uchun tugatilsinmi? |
| game.name.imposter / whoami / rather | Imposter / Who am I? / Would you rather | Самозванец / Кто я? / Что бы ты выбрал | Sotqin / Men kimman? / Qaysi birini tanlarding |

(Use plural forms the existing i18n setup supports for ru counts.)

## testIDs · QA events
`camp.lobby.game.<imposter|whoami|rather>` · `camp.lobby.pack` · `camp.lobby.imposters` · `camp.lobby.sees-category`
· `camp.lobby.start` · `camp.game.waiting` · `camp.game.end` · `camp_game_started { game, players }` ·
`camp_round_started { game, round }` · `camp_game_ended { game, rounds }` · `camp_pack_reshuffled { game, pack }`

## Approved packages
none

## Done when
- [ ] tests: gameReducer (deal secrecy, reconnect same deal, late joiner waits, end), usedStore reshuffle, pack
      validation, lobby Start range/disabled reason; existing campfire-core tests still green
- [ ] `npm run check` green (output in summary), committed on `feat/campfire-party`, reply ≤ 10 lines
