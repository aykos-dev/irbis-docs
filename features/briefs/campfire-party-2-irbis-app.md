# Brief campfire-party-2-irbis-app — hold to reveal, screen protection, Imposter

- Spec: features/campfire-party.md · ACs in this slice: AC3, AC4, AC5
- Repo / branch: irbis-app · `feat/campfire-party`
- Depends on: campfire-party-1 (gameReducer, protocol v2, game route, packs)

## Files
- New: `src/features/campfire-core/games/components/SecretCard.tsx` (hold to reveal), `games/useSecureScreen.ts`,
  `games/imposter/ImposterScreen.tsx` (+ word / imposter / result parts), `__tests__/`.
- Edit native (in-repo, no package): Android `CampNet` module — `setSecure(on: boolean)` adds/clears
  `WindowManager.LayoutParams.FLAG_SECURE` on the current activity (UI thread). iOS `CampNet.swift` — `isCaptured()`
  + event `campCaptureChanged` from `UIScreen.capturedDidChangeNotification`. `native/campNet.ts` (JS wrappers).
- Edit: the slice-1 game route (Imposter body replaces `GameWaiting`), `camp.json` ×3.
- Read for patterns: canvas copy below (do not open canvas HTML), `campTheme.ts`, `components/PlayerAvatar.tsx`,
  existing native module + its jest mock.

## Behaviour
- AC3 — `SecretCard`: covered state shows `secret.hold` ("Hold to see"); while pressed shows content + `secret.release`;
  on release hides again. Light haptic on show (existing haptics helper). `useSecureScreen()` on every secret screen
  (Imposter, Who am I): Android `setSecure(true)` on focus, false on blur/unmount; iOS: when captured, the card is
  replaced by a blur/solid cover + `secret.recording`. testID `camp.secret.card`.
- AC4 — Word card (ImpReveal): header "Imposter", sub `imp.roundLine` ("Round {{n}} · {{m}} players"), chip
  `imp.hostLine` ("Offline · host {{name}}"); card label "YOUR SECRET WORD", word, category (= pack name), lake
  illustration backdrop (`hero-lake.jpg`). "Clue order · one word each": players of the round in a random order
  fixed per round (host sends the order in `game.public`), "You" for self. Hint (Irbis mascot `irbisDefault`):
  `imp.hint`. Imposter card (ImpImposter): "SHH…", "You are the imposter", `imp.noWord` + category when
  `showCategory`, else `imp.noWordOnly`; "How to win" + `imp.win1`, `imp.win2`; "Got it" closes the explainer and
  leaves the covered card. No clue input, no vote, no timer.
- AC5 — Host bottom bar: "Reveal imposter" (`imp.reveal`) and "New round" (`imp.new-round`). Reveal → `game.public`
  gets `{ imposterSeatIds, wordId }` → every phone shows result block (`imp.result`): `imp.wasImposter` with names
  (joined with ", ") and `imp.wasWord`. New round (before or after reveal) → new word (unused), new imposter(s),
  round +1, waiting players dealt in. Players see `imp.waitHost` under their card. `camp_imposter_revealed { imposters }`.

## Copy (`camp.json`, add)
| key | en | ru | uz |
|---|---|---|---|
| secret.hold | Hold to see | Удерживайте, чтобы увидеть | Ko'rish uchun bosib turing |
| secret.release | Release to hide | Отпустите, чтобы скрыть | Yashirish uchun qo'yib yuboring |
| secret.recording | Hidden while the screen is recorded | Скрыто во время записи экрана | Ekran yozilayotganda yashirin |
| imp.roundLine | Round {{n}} · {{m}} players | Раунд {{n}} · игроков: {{m}} | {{n}}-raund · {{m}} o'yinchi |
| imp.hostLine | Offline · host {{name}} | Офлайн · ведущий {{name}} | Oflayn · boshlovchi {{name}} |
| imp.yourWord | YOUR SECRET WORD | ВАШЕ СЕКРЕТНОЕ СЛОВО | SIZNING MAXFIY SO'ZINGIZ |
| imp.clueOrder | Clue order · one word each | Порядок подсказок · по одному слову | Ishora navbati · har kim bitta so'z |
| imp.you | You | Вы | Siz |
| imp.hint | Give a clue that proves you know the word — but don't hand it to the imposter. | Дайте подсказку, которая докажет, что вы знаете слово, — но не выдавайте его самозванцу. | So'zni bilishingizni ko'rsatadigan ishora bering — lekin uni sotqinga oshkor qilmang. |
| imp.shh | SHH… | ТСС… | JIM… |
| imp.youAre | You are the imposter | Вы самозванец | Siz sotqinsiz |
| imp.noWord | You don't know the word. The category is: | Вы не знаете слова. Категория: | Siz so'zni bilmaysiz. Toifa: |
| imp.noWordOnly | You don't know the word. | Вы не знаете слова. | Siz so'zni bilmaysiz. |
| imp.howToWin | How to win | Как победить | Qanday yutish mumkin |
| imp.win1 | Listen to the clues before yours and blend in with something vague. | Слушайте подсказки до вас и сливайтесь с толпой чем-то расплывчатым. | O'zingizdan oldingi ishoralarni tinglang va noaniq so'z bilan aralashib keting. |
| imp.win2 | Not voted out? You win. Caught? Guess the word to steal the win. | Вас не вычислили? Вы победили. Поймали? Угадайте слово и заберите победу. | Sizni topishmadimi? Yutdingiz. Qo'lga tushdingizmi? So'zni topib, g'alabani tortib oling. |
| imp.gotIt | Got it | Понятно | Tushunarli |
| imp.reveal | Reveal imposter | Показать самозванца | Sotqinni ko'rsatish |
| imp.newRound | New round | Новый раунд | Yangi raund |
| imp.wasImposter | The imposter was {{names}} | Самозванцем был(а): {{names}} | Sotqin: {{names}} |
| imp.wasWord | The word was {{word}} | Слово было: {{word}} | So'z: {{word}} edi |
| imp.waitHost | The host starts the next round | Следующий раунд начнёт ведущий | Keyingi raundni boshlovchi boshlaydi |

## testIDs · QA events
`camp.secret.card` · `imp.screen` · `imp.word` · `imp.imposter` · `imp.got-it` · `imp.reveal` · `imp.new-round` ·
`imp.result` · `camp_imposter_revealed { imposters }`

## Approved packages
none (native code in-repo only)

## Done when
- [ ] tests: SecretCard hold/release, useSecureScreen calls setSecure on focus/blur (mocked native), word vs imposter
      card, showCategory off, host-only buttons, reveal shows names + word, new round changes word
- [ ] `npm run check` green (output in summary), Android debug build compiles (`./gradlew assembleDebug -q | tail`),
      committed on `feat/campfire-party`, reply ≤ 10 lines
