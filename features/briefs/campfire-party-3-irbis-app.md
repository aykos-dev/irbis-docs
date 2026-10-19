# Brief campfire-party-3-irbis-app — Who am I? and Would you rather

- Spec: features/campfire-party.md · ACs in this slice: AC6, AC7
- Repo / branch: irbis-app · `feat/campfire-party`
- Depends on: campfire-party-1 (engine, protocol), campfire-party-2 (`SecretCard`, `useSecureScreen`)

## Files
- New: `src/features/campfire-core/games/whoami/WhoAmIScreen.tsx`, `games/rather/RatherScreen.tsx` (+ parts),
  `__tests__/`.
- Edit: `games/gameReducer.ts` (handle `showMine`, WYR votes/reveal/next if slice 1 left them stubbed), host server
  routing for `showMine` / `wyrVote`, the game route (replace `GameWaiting` for these games), `camp.json` ×3.
- Read for patterns: slice-2 `ImposterScreen.tsx` (header, host bar, result block), `PlayerAvatar.tsx`, `campTheme.ts`.

## Behaviour
- AC6 — Who am I (WhoAmI board, minus counter / Pass turn / "What I know"): header "Who am I?", sub `who.packLine`.
  Own card: "?" + `who.you` ("YOU · {{name}}") + `who.hidden`; it is a covered card (no secret yet). List
  `who.othersTitle` + `who.othersSub`: every other player of the round — avatar, nickname, character (from own deal
  `others`). Secure screen on (`useSecureScreen`). Button "I know who I am!" (`whoami.show-mine`) → confirm
  `who.showConfirm` → client sends `showMine` → host replies with a `deal` that adds `mine: characterId` → own card
  becomes a `SecretCard` with the character (hold to see). `camp_whoami_show_mine`. Host bar: "New round" → new
  unused characters for everyone, `mine` cleared. Players see `imp.waitHost`-style line `who.waitHost`.
- AC7 — Rather (WYR board): header "Would you rather", sub `wyr.subLine` ("{{pack}} · question {{i}} of 20"), chip
  `wyr.voted` ("{{n}} / {{m}} voted", m = connected players in the round incl. host). "Would you rather…", option A
  card, "OR", option B card (`wyr.option.a|b`); tap selects (highlight), tap the other to change, until reveal.
  Votes are hidden (only the count) until reveal. Reveal when every connected player in the round voted, or host taps
  "Reveal" (`wyr.reveal`) → both bars animate from 0 to their % together (Reanimated, ~0.6 s), voter avatars drop in
  under their option, "Your pick" tag on yours, heavy haptic burst. If one side has fewer votes (not a tie, > 0):
  `wyr.defend` with those names joined by ", ". Host "Next question" (`wyr.next`); after question 20: `wyr.done` +
  "New round" (20 new unused questions) / "End game". `camp_wyr_revealed { votes, forced }`.

## Copy (`camp.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| who.title | Who am I? | Кто я? | Men kimman? |
| who.packLine | Pack: {{pack}} · {{n}} players | Набор: {{pack}} · игроков: {{n}} | To'plam: {{pack}} · {{n}} o'yinchi |
| who.you | YOU · {{name}} | ВЫ · {{name}} | SIZ · {{name}} |
| who.hidden | Your character is hidden on your phone | Ваш персонаж скрыт на вашем телефоне | Qahramoningiz telefoningizda yashirin |
| who.othersTitle | Everyone else's character | Персонажи остальных | Boshqalarning qahramoni |
| who.othersSub | Only they can't see it | Только они его не видят | Faqat ular o'zinikini ko'rmaydi |
| who.knowIt | I know who I am! | Я знаю, кто я! | Men kimligimni bilaman! |
| who.showConfirm | Show your character? | Показать вашего персонажа? | Qahramoningiz ko'rsatilsinmi? |
| who.show | Show | Показать | Ko'rsatish |
| who.waitHost | The host starts the next round | Следующий раунд начнёт ведущий | Keyingi raundni boshlovchi boshlaydi |
| wyr.title | Would you rather | Что бы ты выбрал | Qaysi birini tanlarding |
| wyr.subLine | {{pack}} · question {{i}} of 20 | {{pack}} · вопрос {{i}} из 20 | {{pack}} · 20 tadan {{i}}-savol |
| wyr.voted | {{n}} / {{m}} voted | Проголосовали: {{n}} / {{m}} | {{n}} / {{m}} ovoz berdi |
| wyr.ask | Would you rather… | Что бы ты выбрал… | Qaysi birini tanlarding… |
| wyr.or | OR | ИЛИ | YOKI |
| wyr.yourPick | Your pick | Ваш выбор | Sizning tanlovingiz |
| wyr.defend | {{names}} — defend your choice! | {{names}} — защитите свой выбор! | {{names}} — tanlovingizni himoya qiling! |
| wyr.reveal | Reveal | Показать | Ko'rsatish |
| wyr.next | Next question | Следующий вопрос | Keyingi savol |
| wyr.done | Pack round done | Раунд набора пройден | To'plam raundi tugadi |
| wyr.newRound | New round | Новый раунд | Yangi raund |

## testIDs · QA events
`whoami.screen` · `whoami.player.<seatId>` · `whoami.show-mine` · `whoami.new-round` · `wyr.screen` · `wyr.option.a` ·
`wyr.option.b` · `wyr.voted` · `wyr.reveal` · `wyr.next` · `wyr.new-round` · `camp_whoami_show_mine` ·
`camp_wyr_revealed { votes, forced }`

## Approved packages
none

## Done when
- [ ] tests: Who am I — own character absent before showMine, others listed, showMine reveals only for that seat, new
      round clears; WYR — count only before reveal, auto-reveal on all connected votes, host force reveal, change vote,
      defend line (minority, none on tie), question 20 → done; secrecy of votes before reveal
- [ ] `npm run check` green (output in summary), committed on `feat/campfire-party`, reply ≤ 10 lines
