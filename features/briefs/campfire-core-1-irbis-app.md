# Brief campfire-core-1-irbis-app — Community segments, CampHub, player sheet

- Spec: features/campfire-core.md · ACs in this slice: AC1, AC2, AC3
- Repo / branch: irbis-app · `feat/campfire-core` (exists, from main 2fb47df)
- Depends on: none. No API, no `gen:api`.

## Files
- Touch: `src/app/navigation/TabNavigator.tsx` (Community tab → `CommunityScreen`) · `src/features/campfire-core/`
  (new): `screens/CommunityScreen.tsx` (segmented control + content), `screens/CampHubScreen.tsx` (rendered as the
  Campfire segment), `components/PlayerSheet.tsx`, `components/GameTile.tsx`, `components/ComingSoonTag.tsx`,
  `campTheme.ts` (dark palette from design.md dark tokens, used regardless of system scheme), `playerProfile.ts`
  (pure validation + MMKV read/write via `src/shared/storage`), `__tests__/` · `src/shared/storage/index.ts` (typed
  key `camp.profile`) · `src/shared/i18n/{en,ru,uz}/camp.json` (new) + register namespace
- Read for patterns: `src/shared/components/{ComingSoon,Sheet,TextField,AppButton,Toast,Screen}.tsx`,
  `src/features/levels/screens/LevelScreen.tsx` (screen structure), `src/shared/components/levels/CompanionArt.tsx`
  (animal art), `src/features/auth` session hook (signed-in username), `design/design.md` dark tokens via
  `src/shared/constants`.
- Art: hero `src/assets/images/places/hero-camping.jpg` + `src/assets/svg/pandaCheering.ts` + `companionFox.ts`
  (placeholder for fox cheering, comment-free; tracked in STATUS). Game icons: draw from the CampHub canvas values
  below with react-native-svg (simple glyphs: Imposter = mask, Mafia = hat, Who am I = question, Rather = split
  arrows). Colours: Imposter #7B61FF, Mafia #D93636, Who am I #1CB0A8, Rather #FF9F1C.

## Behaviour
- AC1 — Community: segmented control (3 equal pills, selected = white pill on surface, canvas Groups board), order
  Feed · Groups · Campfire games, default **Campfire games**. Feed and Groups render the shared `ComingSoon`.
  Campfire screens use `campTheme` (dark) in both system schemes; status bar light.
- AC2 — CampHub (scroll): header title + "Works offline" chip; hero card (camp image, panda + fox, title, body);
  two buttons Host (orange primary, `AppButton`) and Join (secondary); section "Games": 2×2 tiles (icon 50 px r16,
  name, "3–15 · 5–10 min" etc.) each with `ComingSoonTag`; card "Play with your trip group" + tag; card "Campfire
  badges" + tag (no count). Tapping any tagged item → toast `camp.comingSoonToast`. No network calls; works as guest.
- AC3 — Host or Join opens `PlayerSheet`: nickname field (trim, 2–16 chars, else inline error), prefill = saved
  nickname → signed-in username → empty; 6 animal chips (fox, ibex, bear, marmot, eagle, panda; CompanionArt, 52 px
  circles with tint) default saved → fox; Continue (disabled while invalid) saves `camp.profile` and calls
  `onContinue(role)`. In this slice `onContinue` navigates to routes `CampLobby` / `CampJoin` that you register as
  stubs rendering `ComingSoon` (replaced in slices 2–3).

## Copy (`camp.json`)
| key | en | ru | uz |
|---|---|---|---|
| segments.feed | Feed | Лента | Lenta |
| segments.groups | Groups | Группы | Guruhlar |
| segments.campfire | Campfire games | Игры у костра | Gulxan o'yinlari |
| hub.title | Campfire games | Игры у костра | Gulxan o'yinlari |
| hub.offline | Works offline | Работает без интернета | Internetsiz ishlaydi |
| hub.heroTitle | No internet. No problem. | Нет интернета? Не беда. | Internet yo'qmi? Muammo emas. |
| hub.heroBody | Just connect to one hotspot and play together. | Подключитесь к одной точке доступа и играйте вместе. | Bitta hotspotga ulaning va birga o'ynang. |
| hub.host / hub.join | Host / Join | Создать / Войти | Ochish / Qo'shilish |
| hub.games | Games | Игры | O'yinlar |
| games.imposter / mafia / whoami / rather | Imposter / Mafia / Who am I? / Would you rather | Самозванец / Мафия / Кто я? / Что бы ты выбрал | Sotqin / Mafiya / Men kimman? / Nimani tanlaysan |
| games.imposterMeta / mafiaMeta / whoamiMeta / ratherMeta | 3–15 · 5–10 min / 6–15 · 20–40 min / 3–12 · 10–20 min / 2–15 · endless | 3–15 · 5–10 мин / 6–15 · 20–40 мин / 3–12 · 10–20 мин / 2–15 · без конца | 3–15 · 5–10 daq / 6–15 · 20–40 daq / 3–12 · 10–20 daq / 2–15 · cheksiz |
| hub.tripGroup | Play with your trip group | Играть с группой похода | Sayohat guruhingiz bilan o'ynang |
| hub.badges | Campfire badges | Значки у костра | Gulxan nishonlari |
| comingSoon | Coming soon | Скоро | Tez orada |
| comingSoonToast | Coming in the next update | Появится в следующем обновлении | Keyingi yangilanishda chiqadi |
| player.title | Who's playing? | Кто играет? | Kim o'ynayapti? |
| player.nickname | Nickname | Имя в игре | O'yindagi ism |
| player.nicknameError | 2–16 characters | 2–16 символов | 2–16 ta belgi |
| player.avatar | Pick your animal | Выберите зверя | Hayvoningizni tanlang |
| player.continue | Continue | Продолжить | Davom etish |
| animals.fox…panda | Fox, Ibex, Bear, Marmot, Eagle, Panda (a11y labels) | Лиса, Козерог, Медведь, Сурок, Орёл, Панда | Tulki, Tog' echkisi, Ayiq, Sug'ur, Burgut, Panda |

## testIDs · QA events
`community.segment.feed|groups|campfire` · `camp.hub.screen` · `camp.hub.host` · `camp.hub.join` ·
`camp.hub.game.<imposter|mafia|whoami|rather>` · `camp.hub.trip-group` · `camp.hub.badges` · `camp.player.nickname`
· `camp.player.avatar.<animal>` · `camp.player.continue` · no QA events in this slice.

## Approved packages
none in this slice.

## Done when
- [ ] tests: AC1 default segment + Feed coming soon; AC2 tile tap → toast, renders offline/guest; AC3 validation
  (1, 2, 16, 17 chars, trim) + prefill order + saved profile
- [ ] `npm run check` green (output in summary), committed on `feat/campfire-core`, `graphify update .`
